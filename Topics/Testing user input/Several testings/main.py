def check(number):
    try:
        if int(number) < 202:
            print("There are less than 202 apples! You cheated me!")
        else:
            print(number)
    except ValueError:
        print("It is not a number!")
