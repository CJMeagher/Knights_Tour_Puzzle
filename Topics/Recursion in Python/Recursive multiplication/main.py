def multiply(a, b):
    if b == 0:
        return 0
    if b == 1:
        return a
    return multiply(a, b - 1) + a
