import numpy as np
import sys
import argparse
from keygen import keygen
from encrypt import encrypt, decrypt

IP = np.array([1, 5, 2, 0, 3, 7, 4, 6])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action",
        help="Encryption or Decryption to be performed",
        choices=["encrypt", "decrypt"])
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    
    args = parser.parse_args()
    with open(args.input_filename, 'rb') as f:
        inp = np.fromfile(f, dtype=np.uint8)
    k1, k2 = keygen()
    if args.action == 'encrypt':
        op = encrypt(inp, k1, k2)
    else:
        op = decrypt(inp, k1, k2)
    with open(args.output_filename, 'wb') as f:
        op.tofile(f)        

if __name__ == '__main__':
    main()
