def startswith_capital_counter(names):
    count = 0
    for name in names:
        count += 1 if name.istitle() else 0
    return count