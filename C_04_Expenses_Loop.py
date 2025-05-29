# FUnction goes here
import pandas

def num_check(question, num_type = "float", exit_code = None):
    """Checks if the input is an integer or not"""

    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:
        try:

            # chek for exit code
            response = input(question)

            if response == exit_code:
                return response

            if num_type == "float":
                response = float(input(question))

            else:
                response = int(input(question))

            if response > 0:
                return response

        except ValueError:
            print(error)
            # prints an error message if the user does not enter an integer.



def not_blank(question):
    """Makes sure that the user can not enter a blank name."""

    while True:
        response = input(question)

        if response != "":
            return response

        print("This cannot be blank.")
        # Prints error message in the case when the user does not enter a name.


def get_expenses(exp_type, how_many):
    """Gets variable / fixed expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_items = []
    all_amounts = []
    all_costs = []

    # Expenses dictionary
    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "Cost": all_costs
    }


    # default amount ot 1 for fixed expenses and
    # to avoid PEP 8 error for variable expenses.
    amount = 1

    # loop to get expenses
    while True:
        item_name = not_blank("Item Name: ")

        # checks user enter at least one variable expense
        if (exp_type == "variable" and
            item_name == "xxx") and len(all_items) == 0:
            print("Oops - you have not entered anything."
                  "You need at least one item")
            continue

        elif item_name == "xxx":
            break

        # Get item amount <enter> defaults to number of
        # products being made

        amount = num_check(f"How many <enter for {how_many}: ",
                           "Integer","")

        if amount == "":
            amount = how_many

        cost = num_check("Price for one? ", "float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_costs.append(cost)

        # make panda
        expense_frame = pandas.DataFrame(expenses_dict)

    # return all items for now so we can check loop
        return expense_frame

# Main routine goes here

quantity_made = num_check("Quantity being made: ", "integer")
print()

print("Getting variable costs...")
variable_expenses = get_expenses("variable", quantity_made )
num_variable = len(variable_expenses)
print(f'You entered {num_variable} items')
print()