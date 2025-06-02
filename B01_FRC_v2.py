import pandas
from tabulate import tabulate
from datetime import date
import math


# Functions goes here
def make_statement(statement, decoration):
    """Makes the heading stand out more by adding decorations."""
    return f"{decoration * 3} {statement} {decoration * 3}"


def string_check(question, valid_ans_list=('yes', 'no'), num_letters=1):
    """Checks if the user enters the first letter or a full word from a list of words """

    while True:
        response = input(question).lower()

        for item in valid_ans_list:
            if response == item:
                return item
            elif response == item[:num_letters]:
                return item
            # checks if user enters valid item and responds correctly.
        else:
            print(f"Please choose {valid_ans_list[0]} / {valid_ans_list[1]}.")
        # Prints an error message in the case of invalid input


def instructions():
    # Function for printing out instructions.
    print(make_statement("Instructions", "ℹ️"))

    print('''
    
    This program will ask you for...
    - The name of the product you are selling
    - How many items you plan on selling
    - The costs for each component of the product
    (variable expenses)
    - Whether or not you have fixed expenses (if you have
    fixed expenses, it will ask you what they are)/
    - How much money you want to make (ie: your profit goal)
    
It will also ask you how much the recommended sales prices should
be rounded to.

The program outputs an itemised list of the variables and fixed 
expenses (which includes the subtotals for these expenses)/

Finally it will tell you how much you should sell each item for 
to reach your profit goal.

The data will also be written to a test file which has the same
name as your product and today's date.


program continues...

    ''')


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

            elif num_type == "float":
                response = float(response)

            else:
                response = int(response)

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


def get_expenses(exp_type, how_many=1):
    """Gets variable / fixed expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_items = []
    all_amounts = []
    all_dollar_per_item = []

    # Expenses dictionary
    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$/ Item": all_dollar_per_item
    }

    # defaults for fixed expenses
    amount = how_many
    how_much_question = "How much? $"

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
        if exp_type == "variable":
            amount = num_check(f"How many <enter for {how_many}>: ",
                               "Integer","")

            if amount == "":
                amount = how_many

            how_much_question = "Price for one? $"

        #Get price for one (depending on exp_type)

        price_for_one = num_check(how_much_question, "float")

        all_items.append(item_name)
        all_amounts.append(amount)
        all_dollar_per_item.append(price_for_one)

    # make panda
    expense_frame = pandas.DataFrame(expenses_dict)

    # Calculate row cost
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$/ Item']

    # calculate subtotal
    subtotal = expense_frame['Cost'].sum()

    # Apply currency formatting to currency columns
    add_dollars = ['Amount', '$/ Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns
    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers = 'keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item','Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)

    # return all items for now so we can check loop
    return expense_string , subtotal


def currency(x):
    return "${:.2f}".format(x)


def profit_goal(total_costs):
    """Calculates profit goal  work out profit goal and total sales required"""
    # Initialize variables and error message
    error =  "Please enter a valid profit goal \n"

    valid = False
    while not valid:

        # ask for profit goal...
        response = input("What is your profit goal (eg $500 or 50%): ")

        # check if first character is $
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if last character is %
        elif response[-1] == "%":
            profit_type = "%"
            # Get amount (Everything before the %)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = string_check(f"Do you mean ${amount:.2f}. ie {amount:.2f} dollars? :")

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = string_check(f"Do you mean {amount}%? :")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type == "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount

        else:
            goal = (amount / 100) * total_costs
            return goal


def round_up(amount , round_val):
    """Rounds amount to desired whole number"""
    return int(math.ceil(amount / round_val)) * round_val


# Main routine goes here

# Initialize variables

# assume no fixed expenses for now
fixed_subtotal = 0
fixed_panda_string = ""

print(make_statement("Fund Raising Calculator", "🍿"))

print()
want_instructions = string_check("Do you want to see the instructions? ")
print()

if want_instructions == "yes":
    instructions()

print()

# Get product details.

product_name = not_blank("Product Name: ")
quantity_made = num_check("Quantity being made: ", "integer")

# Get variable expenses
print("Let's get the variable expenses....")
variable_expenses = get_expenses("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

# ask user if they have fixed expenses and retrieve them
print()
has_fixed = string_check("Do you have fixed expenses? ")

if has_fixed == "yes":
    fixed_expenses = get_expenses("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    # If the user has not entered any fixed expenses,
    # Set empty panda to "" so that it does not display!
    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"

# Get profit goal here.
target = profit_goal(total_expenses)
sales_target = total_expenses + target

# Calculate minimum selling price and round
# it to nearest desired dollar amount
selling_price = (total_expenses + target) / quantity_made
round_to = num_check("Round To: ",'integer' )
suggested_price = round_up(selling_price, round_to)


# Strings / Output area

# Get current date for heading and filename
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
mont = today.strftime("%m")
year = today.strftime("%Y")

# Headings /Strings...
main_heading_string = make_statement(f"Fund Raising Calculator "
                                     f"{product_name}, {day}/{mont}/{year}", "=")
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement("Variable Expenses", "-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"

# set u[p strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement("Fixed Expenses", "-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal: ${fixed_subtotal:.2f}"

# set fixed cost strings to blank wif we don't have fixed costs
else:
    fixed_heading_string = make_statement("You have no Fixed Expenses", "-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal = $0.00"

selling_price_heading = make_statement("Selling Price Calculations", "*")
profit_goal_string = f"Profit Goal ${target:.2f}"
sales_target_string = f"\nTotal Sales Needed: ${sales_target:.2f}"

minimum_price_string = f"Minimum Selling Price: ${selling_price:.2f}"
suggested_price_string = make_statement(f"Suggested Selling Price: "
                                        f"${suggested_price:.2f}", "*")

# List of strings to be outputted / written to file
to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, total_expenses_string,
            profit_goal_string, sales_target_string,
            minimum_price_string, "\n", suggested_price_string]

# Print area
print()
for item in to_write:
    print(item)

# create file to hold data(add .txt extension )
file_name = f"{product_name}_{year}_{mont}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write the item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")