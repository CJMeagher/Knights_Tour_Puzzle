def check():
    try:
        number = int(input())
        if 25 <= number <= 37:
            print(number)
        else:
            raise ValueError
    except ValueError:
        print("Correct the error!")
