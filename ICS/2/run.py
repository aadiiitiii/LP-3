import numpy as np
import keygen
import argparse
import encrypt
import mixing

def input_from_file(filename=None, decrypt=False):
    a = np.fromfile(filename, dtype=np.uint8)
    if decrypt:
        # Read data. Will always be of length 4x + 1
        # Last byte indicates number of padding zeros added
        a, num_padding_zeros = a[:-1], a[-1]
        length = a.shape[0] * 2
        b = np.empty((length), dtype=np.uint8)
        b[0::2], b[1::2] = a // 16, a % 16
        return a, num_padding_zeros
    # Read data. Length cannot be predetermined.
    # Divide into nibbles, and add padding zeros
    length = a.shape[0] * 2
    b = np.empty((length), dtype=np.uint8)
    b[0::2], b[1::2] = a // 16, a % 16
    num_padding_zeros = (4 - (length % 4)) % 4
    b = np.pad(b, ((0, num_padding_zeros)), mode='constant')
    return b, length

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action",
        help="Encryption or Decryption to be performed",
        choices=["encrypt", "decrypt"]
    )
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")

    args = parser.parse_args()

    # Prompt for keys and generate key schedule
    keys = keygen.keygen()
    # Table holding remainder values for polynomial
    # division mod 0b10011
    mixing.initialise_rem_lookup()

    if args.action == 'encrypt':
        # Generate ciphertext, and store it in a file
        # along with number of padding zeros added
        arr, l = input_from_file(filename=args.input_filename)
        ciphertext = encrypt.encrypt(arr, keys)
        ciphertext.tofile(args.output_filename)
        print(ciphertext.shape, l)
        with open(args.output_filename, 'ab') as f:
            print(f.write(bytes([ciphertext.shape[0] - l])))
    else:
        # Decrypt ciphertext and store plaintext,
        # ignoring padding elements added
        arr, pad_len = input_from_file(filename=args.input_filename, decrypt=True)
        plaintext = encrypt.decrypt(arr, keys)
        plaintext = plaintext[:pad_len * -1]
        plaintext = plaintext[0::2] * 16 + plaintext[1::2]
        plaintext.tofile(args.output_filename)

if __name__ == '__main__':
    main()
