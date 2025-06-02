

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
            print(f"Please choose {valid_ans_list.__getitem__(0)} / {valid_ans_list.__getitem__(1)}.")
        # Prints an error message in the case of invalid input

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


# Main routine goes

# loop for testing purposes
while True:
    total_expenses = 200
    target = profit_goal(total_expenses)
    sales_target = total_expenses + target
    print(f"Profit Goal: ${target:.2f}")
    print(f"Sales Target: ${sales_target:.2f}")


