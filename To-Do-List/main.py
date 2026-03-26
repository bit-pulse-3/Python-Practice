import json
import datetime
import sys


def new_task_id(tasks):
    if not tasks:
        return 1
    return max(task["task_id"] for task in tasks) + 1


def add_task(task_description: str):
    try:
        with open("task-info.json", "r") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    new_id = new_task_id(tasks)

    Task = {
        "task_id": new_id,
        "task-description": task_description,
        "status": "todo",
        "created_at": str(datetime.datetime.now()),
        "updated_at": "",
    }

    tasks.append(Task)

    with open("task-info.json", "w") as file:
        json.dump(tasks, file, indent=5)

    print(f"Task {new_id} added successfully")


def delete_task(task_id: int):
    try:
        with open("task-info.json", "w") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        print("No task found.")
        return

    original_count = len(tasks)

    tasks = [t for t in tasks if t["task_id"] != task_id]

    if len(tasks) == original_count:
        print(f"task Id {task_id} not found.")
        return

    with open("task-info.json", "w") as file:
        json.dump(tasks, file, indent=5)

    print(f"Task {task_id} deleted")


def list_tasks(status: str):
    try:
        with open("task-info.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        print("No File Found")

    match status:
        case "todo":
            todo_tasks = [t for t in tasks if t["status"] == "todo"]
            print(todo_tasks)
        case "in-progress":
            in_progress_tasks = [t for t in tasks if t["status"] == "in-progress"]
            print(in_progress_tasks)
        case "done":
            completed_tasks = [t for t in tasks if t["status"] == "done"]
            print(completed_tasks)
        case "all":
            print(tasks)
        case _:
            print(f"{status} not accepted")


def update_task_status(task_id: int, status: str):
    try:
        with open("task-info.json", "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        print("No File Found")

    task_to_update = [t for t in tasks if t["task_id"] == task_id]

    if task_to_update is []:
        print(f"task Id {task_id} not found.")
        return
    else:
        task_to_update["status"] = status

    print(f"Status of {task_id} updated successfully. ")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: task-cli [command] [arguments]")
        sys.exit(1)

    command = sys.argv[1]

    match command:
        case "add":
            if len(sys.argv) < 3:
                print("Error: Please provide a task description.")
            else:
                add_task(sys.argv[2])

        case "delete":
            if len(sys.argv) < 3:
                print("Error: Please provide a task ID.")
            else:
                delete_task(int(sys.argv[2]))

        case "list":

            status = sys.argv[2] if len(sys.argv) > 2 else "all"
            list_tasks(status)

        case "mark-in-progress":
            # You would need a function 'update_status(id, "in-progress")'
            update_status(int(sys.argv[2]), "in-progress")

        case "mark-done":
            update_status(int(sys.argv[2]), "done")

        case _:
            print(f"Unknown command: {command}")
