import numpy as np
import mixing

# Substitution table for nibbles
# Used in encryption and key generation
sub_table = np.array([
     9,  4, 10, 11,
    13,  1,  8,  5,
     6,  2,  0,  3,
    12, 14, 15,  7],
    dtype=np.uint8
)

sub_inv_table = np.array([
    10,  5,  9, 11,
     1,  7,  8, 15,
     6,  0,  2,  3,
    12,  4, 13, 14],
    dtype = np.uint8
)
