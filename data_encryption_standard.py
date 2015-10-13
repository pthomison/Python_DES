__author__ = 'patrick'

from bitstring import BitArray
from permutations import *

def permutate(input, permutation):
    result = BitArray(int=0, length=len(permutation))
    for i in range(len(permutation)):
        result[i] = input[permutation[i]-1]
    return result

def key_schedule(key):
    subkeys = [BitArray(int=0, length=56)] * 16
    perm_1 = permutate(key,PC_1)

    C = perm_1[:28]
    D = perm_1[28:]

    for i in range(16):
        iter = i+1
        one_shift = [1,2,9,16]
        if iter in one_shift:
            C.rol(1)
            D.rol(1)
        else:
            C.rol(2)
            D.rol(2)
        subkeys[i] = permutate(C+D, PC_2)

    return subkeys


def des_block_encrypt(input, key):
    if len(input) != 64:
        raise ValueError("Give inputs of size 64 bits")
    if len(key) != 64:
        raise ValueError("Give keys of size 64 bits")
    subkeys = key_schedule(key)

    intial_perm = permutate(input, IP)
    L = intial_perm[:32]
    R = intial_perm[32:]

    for i in range(16):
        iter = i+1
        E_R = permutate(R, E)


    return



if __name__ == "__main__":
    input = BitArray(int=7000, length=64)
    #key = BitArray(int=9379, length=64)
    key = BitArray(bin="00010011 00110100 01010111 01111001 10011011 10111100 11011111 11110001")
    result = des_block_encrypt(input, key)