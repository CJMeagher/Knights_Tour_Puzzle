def check_name(name):
    if len(name) == 1 and name in "lOI":
        print(
            "Never use the characters 'l', 'O', or 'I' as single-character variable names"
        )
    elif name.islower():
        print("It is a common variable")
    elif name.isupper():
        print("It is a constant")
    else:
        print("You shouldn't use mixedCase")
