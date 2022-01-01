def last_indexof_max(numbers):
    if not numbers:
        return -1
    index_of_max = 0
    for i in range(len(numbers)):
        if numbers[i] >= numbers[index_of_max]:
            index_of_max = i
    return index_of_max
