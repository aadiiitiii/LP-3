import numpy as np

# Returns 10 element np array of uint8
def accept_key():
    temp = input("Enter 10 bit key: ")
    if len(temp) != 10:
        raise ValueError("Invalid key length")
    bitlist = [ int(bit_char, 2) for bit_char in temp ]
    key = np.array(bitlist, dtype=np.uint8)
    return key

# Returns an 8bit permutation of 10bit key. 2 bits dropped
def p8(key10bit):
    p8_indices = [0, 1, 5, 2, 6, 3, 7, 4, 9, 8]
    key = key10bit[p8_indices]
    return key[2:]

# Returns a 10bit permutation of 10bit key
def p10(key10bit):
    p10_indices = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    key = key10bit[p10_indices]
    return key

# Returns np array corresponding to individual
# nibbles left rotated by 1
def ls1(key10bit):
    ls1_indices = [1, 2, 3, 4, 0, 6, 7, 8, 9, 5]
    key = key10bit[ls1_indices]
    return key

# Returns np array corresponding to individual
# nibbles left rotated by 2
def ls2(key10bit):
    ls2_indices = [2, 3, 4, 0, 1, 7, 8, 9, 5, 6]
    key = key10bit[ls2_indices]
    return key

# Returns 2 8bit keys, ie 2 8 element np arrays
def keygen():
    key10bit = accept_key()
    key10bit = p10(key10bit)
    ls1_10bit_op = ls1(key10bit)
    k1 = p8(ls1_10bit_op)
    ls2_10bit_op = ls2(ls1_10bit_op)
    k2 = p8(ls2_10bit_op)
    return k1, k2
