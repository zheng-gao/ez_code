from random import randint


def knuth_shuffle(array: list):
    # https://en.wikipedia.org/wiki/Fisher-Yates_shuffle
    for i in range(len(array) - 1, 0, -1):
        j = randint(0, i)  # 0 <= j <=i
        if j != i:
            array[i], array[j] = array[j], array[i]
