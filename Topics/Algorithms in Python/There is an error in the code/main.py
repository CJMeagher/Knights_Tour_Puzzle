sentence = input()

def aver(sent):

    for sym in ['!', '?', ';', '.', '"', "'"]:
        sent = sent.replace(sym, '')

    words = sent.split()

    total = 0
    for word in words:
        total = total + len(word)

    if len(words) != 0:
        result = total / len(words)
    else:
        result = 0

    return result

print(aver(sentence))