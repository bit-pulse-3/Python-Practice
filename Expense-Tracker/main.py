import datetime
import json
import argparse


class Expense:
    def __init__(self, expense_id: int, description: str, amount: float):
        self.expense_id = expense_id
        self.description = description
        self.amount = amount
        self.expense_created = str(datetime.datetime.now())
        self.expense_updated = ""


class ExpenseHandler:

    def create_expense(self, description: str, amount: float):
        retrieved_expense_id = self.expense_id_tracker()
        expense = Expense(retrieved_expense_id, description, amount)
        expense_dict = {
            "expense_id": expense.expense_id,
            "expense_description": expense.description,
            "expense_amount": expense.amount,
            "expense_created_at": expense.expense_created,
            "expense_updated_at": expense.expense_updated,
        }
        try:
            with open("expense-info.json", "r") as file:
                expense_data = json.load(file)
        except FileNotFoundError:
            expense_data = []
        expense_data.append(expense_dict)
        with open("expense-info.json", "w") as file:
            json.dump(expense_data, file, indent=5)

    def delete_expense(self, expense_id: int):
        try:
            with open("expense-info.json", "r") as file:
                expense_data = json.load(file)
                if expense_data == {}:
                    print("No expenses were found.")
                else:
                    original_data = expense_data
                    expense_data = [
                        data
                        for data in expense_data
                        if data["expense_id"] != expense_id
                    ]
                    if len(original_data) > len(expense_data):
                        print(f"expense deleted successfully with {expense_id }\n")
                        with open("expense-info.json", "w") as file:
                            json.dump(expense_data, file, indent=5)

                    elif len(original_data) == len(expense_data):
                        print(
                            f"No expense was found to delete with expense id:{expense_id}\n"
                        )
                    else:
                        return 1
        except FileNotFoundError:
            return "No File found!."

    def update_expense(self, expense_id: int, description: str):
        try:
            with open("expense-info.json", "r") as file:
                expenses = json.load(file)
                update_status = False
                for e in expenses:
                    if expense_id == e["expense_id"]:
                        e["expense_description"] = description
                        e["expense_updated_at"] = str(datetime.datetime.now())
                        update_status = True
                        break
                    else:
                        continue
                if update_status == 1:
                    with open("expense-info.json", "w") as file:
                        json.dump(expenses, file, indent=5)
                    return "Expense Updated SuccessFully.\n"
                else:
                    return "No expense was found to update.\n"
        except FileNotFoundError:
            return "File not Found!.\n"

    def expense_id_tracker(self):
        try:
            with open("expense-info.json", "r") as file:
                expenses = json.load(file)
                if not expenses:
                    return 1
                existing_ids = [item["expense_id"] for item in expenses]
                return max(existing_ids) + 1
        except FileNotFoundError:
            return 1

    def view_all_expense(self):
        try:
            with open("expense-info.json", "r") as file:
                expenses = json.load(file)
                if not expenses:
                    return "Not Expense to Display.\n"
                for e in expenses:
                    print(
                        f"Expense Id:{e["expense_id"]}\nExpense Description:{e["expense_description"]}\nExpense Amount:${e["expense_amount"]}\nExpense Creation Date:{e["expense_created_at"]}\nExpense Updated Date:{e["expense_updated_at"]}"
                    )
        except FileNotFoundError:
            return "File not found.\n"

    def expenses_summary(self):
        try:
            with open("expense-info.json", "r") as file:
                expenses = json.load(file)
                if not expenses:
                    return "Not Expense to Display.\n"
                for e in expenses:
                    t_amount = sum([e["expense_amount"] for e in expenses])

                print(f"Expense Amount:${t_amount}\n")
        except FileNotFoundError:
            return "File not found.\n"


handler = ExpenseHandler()
parser = argparse.ArgumentParser(description="Efficient Expense Tracker")
subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add", help="Add data for the expense")
add_parser.add_argument("description", type=str, help="Enter description of expense")
add_parser.add_argument("amount", type=float, help="enter amount of expense")


add_parser = subparsers.add_parser("delete", help="Enter expense id to delete.")
add_parser.add_argument("id", type=int)

add_parser = subparsers.add_parser(
    "update", help="Enter expense id to update and description to update."
)
add_parser.add_argument("id", type=int)
add_parser.add_argument("description", type=str)

add_parser = subparsers.add_parser("view", help="To View all expenses.")

add_parser = subparsers.add_parser("summary", help="Total amount of all expenses.")


args = parser.parse_args()

if args.command == "add":
    handler.create_expense(args.description, args.amount)
elif args.command == "delete":
    handler.delete_expense(args.id)
elif args.command == "update":
    handler.update_expense(args.id, args.description)
elif args.command == "view":
    handler.view_all_expense()
elif args.command == "summary":
    handler.expenses_summary()
