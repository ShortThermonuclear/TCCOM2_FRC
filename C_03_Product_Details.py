# FUnction goes here

def num_check(question, num_type = "float"):
    """Checks if the input is an integer or not"""

    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:
        try:

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


# Main routine goes here

# Loop fo testing purposes
while True:
    product_name = not_blank("Product Name: ")
    quantity_made = num_check("Quantity being made: ", "integer")
    print(f"You are making {quantity_made} {product_name}")
    print()

