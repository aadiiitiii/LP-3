import numpy as np

# Results of multiplication by 9 in GF(2^4)
# Simpler to make a lookup table
mult_by9_lookup_table = np.array(
    [0, 9, 18, 27, 36, 45, 54, 63, 72, 65, 90, 83, 108, 101, 126, 119],
    dtype=np.uint8
)

# Lookup table for results of remainder mod 0b10011
rem_lookup_table = np.empty([128], dtype=np.uint8)

# Perform matmult(C, block) mod 0b10011, for each block in input
# C = [1  4]
#     [4  1]
# VVIMP: Operations in GF(2^4)
# Returns np array of same shape as input
def mixcols(blocks):
    global rem_lookup_table
    temp1, temp2 = blocks, blocks * 4
    op = temp1[:, [0, 1]] ^ temp2[:, [1, 0]]
    op = rem_lookup_table[op]
    del temp1, temp2
    return op

# Perform matmult(Cinv, block) od 0b10011, for each block in input
# Cinv = [9  2]
#        [2  9]
# VVIMP: Operations in GF(2^4)
# Returns np array of same shape as input
def invmixcols(blocks):
    temp1 = mult_by9_lookup_table[blocks]
    temp2 = blocks * 2
    op = temp1[:, [0, 1]] ^ temp2[:, [1, 0]]
    del temp1, temp2
    op = rem_lookup_table[op]
    return op

# Store remainder esults for all 128 possible numbers mod 0b10011
def initialise_rem_lookup():
    global rem_lookup_table
    for i in range(128):
        n = i
        s, mask = 0b10011000, 0b10000000
        for j in range(3):
            s = s >> 1
            mask = mask >> 1
            if n >= mask:
                n = n ^ s
        rem_lookup_table[i] = n

# Just for debugging.
def rem(n):
    i = n
    s = 0b10011000
    mask = 0b10000000
    for j in range(3):
        s = s >> 1
        mask = mask >> 1
        if n >= mask:
            n = n ^ s
    print(i, n)
