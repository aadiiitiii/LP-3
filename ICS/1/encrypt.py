import numpy as np

# Substitution boxes
s0 = np.array([
    [[0,1], [0,0], [1,1], [1,0]],
    [[1,1], [1,0], [0,1], [0,0]],
    [[0,0], [1,0], [0,1], [1,1]],
    [[1,1], [0,1], [1,1], [1,0]]
], dtype=np.uint8)

s1 = np.array([
    [[0,0], [0,1], [1,0], [1,1]],
    [[1,0], [0,0], [0,1], [1,1]],
    [[1,1], [0,0], [0,1], [0,0]],
    [[1,0], [0,1], [0,0], [1,1]]
], dtype=np.uint8)

# Initial permutation of data
def apply_IP(plaintext):
    ip_indices = [1, 5, 2, 0, 3, 7, 4, 6]
    temp = np.unpackbits(plaintext, axis=1)
    op = temp[:, ip_indices]
    del temp
    return op

# Reverse initial permutation.
def apply_IPinv(code):
    ipinv_indices = [3, 0, 2, 4, 6, 1, 7, 5]
    temp = code[:, ipinv_indices]
    op = np.packbits(temp, axis=1)
    del temp
    return op

# Input received here is an 8bit mixture generated from the upper nibble
# Output is a nibble used to mangle the lower nibble
# Nibble generated from Substitution boxes
# rx obtained by first and last bits of corresp nibble
# cx obtained by 2nd and 3rd bits of the corresp nibble
def sbox_lookup(code):
    p4_indices = [1, 3, 2, 0]
    row1, col1 = code[:, 0] * 2 + code[:, 3], code[:, 1] * 2 + code[:, 2]
    row2, col2 = code[:, 4] * 2 + code[:, 7], code[:, 5] * 2 + code[:, 6]
    # Concatenate to give 4 bits
    op = np.c_[s0[row1, col1], s1[row2, col2]]
    op = op[:, p4_indices]           # Apply 4 bit permutation
    return op

def mangle_left4(code, key):
    ep_indices = [3, 0, 1, 2, 1, 2, 3, 0]
    temp = code[:, 4:]                    # Right nibble
    ep_r4 = temp[:, ep_indices]           # 4bits to an 8bit permutation
    del temp
    k1_xor_op = ep_r4 ^ key               # xor with key
    return sbox_lookup(k1_xor_op)

def encrypt(plaintext, k1, k2):
    ip = apply_IP(np.reshape(plaintext, [-1, 1]))      # Initial Permutation
    new_u4 = mangle_left4(ip, k1)
    ip[:, :4] = ip[:, :4] ^ new_u4                     # Mangle upper nibble
    ip = ip[:,[4, 5, 6, 7, 0, 1, 2, 3]]
    new_l4 = mangle_left4(ip, k2)
    ip[:, :4] = ip[:, :4] ^ new_l4                     # Mangle upper nibble
    ciphertext = np.reshape(apply_IPinv(ip), [-1])     # IP inverse
    return ciphertext

def decrypt(ciphertext, k1, k2):
    ip = apply_IP(np.reshape(ciphertext, [-1, 1]))     # Initial Permutation
    new_u4 = mangle_left4(ip, k2)
    ip[:, :4] = ip[:, :4] ^ new_u4                     # Mangle upper nibble
    ip = ip[:,[4, 5, 6, 7, 0, 1, 2, 3]]                # Swap nibbles
    new_l4 = mangle_left4(ip, k1)
    ip[:, :4] = ip[:, :4] ^ new_l4                     # Mangle upper nibble
    plaintext = np.reshape(apply_IPinv(ip), [-1])
    return plaintext
