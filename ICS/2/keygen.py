import numpy as np
from __init__ import sub_table

# Round constants: Arbitrary, unique for each round, lower nibble always 0
RC = np.array([[0x8, 0x0], [0x3, 0x0]], dtype=np.uint8)

# Returns int corresp to 16 bit input
def key_input():
    k_str = input("Enter a 16 bit key: ")
    if len(k_str) != 16:
        raise ValueError("Incorrect key length")
    k = int(k_str, 2)
    return k

# 16 bit key accepted from user. Used to generate 6 8bit keys/words
# First 2 w0, w1 are simply the two halves of the input
# Returns 6x2 np array of uint8
def keygen():
    k = key_input()
    w0, w1 = k // 0x100, k % 0x100
    keys = np.empty([6, 2], dtype=np.uint8)
    keys[0, 0], keys[0, 1] = w0 // 16, w0 % 16
    keys[1, 0], keys[1, 1] = w1 // 16, w1 % 16
    for i in range(2, 6):
        if i % 2 == 0:
            t = subnibbles(rotate_word(keys[i-1])) ^ RC[i // 2 - 1]
            keys[i] = t ^ keys[i-2]
        else:
            keys[i] = keys[i-1] ^ keys[i-2]
    return keys

def rotate_word(word):
    return word[[1, 0]]

def subnibbles(word):
    return sub_table[word]
