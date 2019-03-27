import numpy as np
from __init__ import sub_table, sub_inv_table
import mixing

index_of_every_2nd_ele = None
index_of_every_3rd_ele = None

# Convert array of nibbles to array of 2x2blocks,
# Returns nx2x2 np array of uint8
def arrto2x2blocks(np_arr):
    global index_of_every_2nd_ele, index_of_every_3rd_ele
    l = np_arr.shape[0]
    # By convention, Fortran order used.
    # So simply swap every 2nd and third element
    index_of_every_2nd_ele = [x for x in range(1, l, 4)]
    index_of_every_3rd_ele = [x for x in range(2, l, 4)]
    temp = np_arr.copy()
    temp[index_of_every_2nd_ele], temp[index_of_every_3rd_ele] = \
        np_arr[index_of_every_3rd_ele], np_arr[index_of_every_2nd_ele]
    return np.reshape(temp, [-1, 2, 2])

# Convert array of blocks back to a 1d array
# Returns 1d np array of uint8
def blocks2x2toarr(blocks):
    global index_of_every_2nd_ele, index_of_every_3rd_ele
    np_arr = np.reshape(blocks, [-1])
    np_arr[index_of_every_2nd_ele], np_arr[index_of_every_3rd_ele] = \
        np_arr[index_of_every_3rd_ele], np_arr[index_of_every_2nd_ele]
    return np_arr

# Actually shift row operation, But for a 2x2 block,
# all it does is rotate the second row
def row1rotate(blocks):
    temp = blocks.copy()
    temp[:, 1, [0, 1]] = blocks[:, 1, [1, 0]]
    return temp

def subnibbles(blocks):
    # print(blocks)
    temp = sub_table[blocks]
    return temp

def invsubnibbles(blocks):
    temp = sub_inv_table[blocks]
    return temp

def add_round_key(blocks, key):
    return blocks ^ key


def encrypt(plaintext, keys):
    blocks = arrto2x2blocks(plaintext)
    # Separate keys and transpose
    k0, k1, k2 = keys[:2].T, keys[2:4].T, keys[4:].T
    blocks = add_round_key(blocks, k0)

    # Round 1
    t = subnibbles(blocks)
    t = row1rotate(t)
    blocks = mixing.mixcols(t)
    # blocks = mixing.mixcols(row1rotate(subnibbles(blocks)))
    blocks = add_round_key(blocks, k1)

    # Round 2
    t = subnibbles(blocks)
    t = row1rotate(t)
    blocks = add_round_key(t, k2)
    # blocks = add_round_key(row1rotate(subnibbles(blocks)), k2)
    # print(k2)
    return blocks2x2toarr(blocks)

def decrypt(ciphertext, keys):
    blocks = arrto2x2blocks(ciphertext)
    k0, k1, k2 = keys[:2].T, keys[2:4].T, keys[4:].T
    blocks = add_round_key(blocks, k2)
    # Round 1
    blocks = add_round_key(invsubnibbles(row1rotate(blocks)), k1)
    blocks = mixing.invmixcols(blocks)

    # Round 2
    blocks = add_round_key(invsubnibbles(row1rotate(blocks)), k0)
    return blocks2x2toarr(blocks)
