__author__ = 'patrick'

import data_encryption_standard as DES
from bitstring import BitArray

def triple_DES_encrypt(input, key_one, key_two):
    result = DES.des_block_encrypt(input, key_one)
    result = DES.des_block_decrypt(result, key_two)
    result = DES.des_block_encrypt(result, key_one)
    return result

def triple_DES_decrypt(input, key_one, key_two):
    result = DES.des_block_decrypt(input, key_one)
    result = DES.des_block_encrypt(result, key_two)
    result = DES.des_block_decrypt(result, key_one)
    return result

if __name__ == "__main__":
    input = BitArray(uint=42, length=64)
    key_one = BitArray(uint=9379, length=64)
    key_two = BitArray(uint=1234, length=64)

    EC = triple_DES_encrypt(input, key_one, key_two)
    print(EC.uint)
    DC = triple_DES_decrypt(input,key_one, key_two)
    print(DC.uint)