def rec_sum(n):
    if n == 1:
        return 1
    return rec_sum(n - 1) + n