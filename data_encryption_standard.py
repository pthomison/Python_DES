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

def feistel(half_block, subkey):
    E_R = permutate(half_block, E)
    XO_E_R = E_R ^ subkey
    B_tot = BitArray()
    for y in range(8):
        B = XO_E_R[y*6:(y+1)*6]
        row = BitArray([B[0]]+[B[5]]).uint
        col = BitArray(B[1:5]).uint
        s_res = BitArray(uint=S[y][row][col], length=4)
        B_tot.append(s_res)
    result = permutate(B_tot, P)
    return result

def des_block_encrypt(input, key):
    if len(input) != 64:
        raise ValueError("Give inputs of size 64 bits")
    if len(key) != 64:
        raise ValueError("Give keys of size 64 bits")
    subkeys = key_schedule(key)

    intial_perm = permutate(input, IP)
    L = [None] * 17
    R = [None] * 17
    L[0] = intial_perm[:32]
    R[0] = intial_perm[32:]

    for i in range(16):
        iter = i+1
        L[iter] = R[i]
        R[iter] = L[i] ^ feistel(R[i], subkeys[i])

    C = permutate(R[16] + L[16], FP)

    return C

def des_block_decrypt(input, key):
    if len(input) != 64:
        raise ValueError("Give inputs of size 64 bits")
    if len(key) != 64:
        raise ValueError("Give keys of size 64 bits")
    subkeys = key_schedule(key)
    intial_perm = permutate(input, IP)
    L = [None] * 17
    R = [None] * 17
    L[16] = intial_perm[32:]
    R[16] = intial_perm[:32]

    for i in range(16).__reversed__():
        iter = i+1
        R[iter-1]=L[iter]
        L[iter-1]=R[iter] ^ feistel(L[iter], subkeys[i])

    PB = permutate(L[0]+R[0], FP)

    return PB




if __name__ == "__main__":
    input = BitArray(int=12, length=64)
    key = BitArray(uint=9397, length=64)
    result = des_block_encrypt(input, key)
    print(des_block_decrypt(result, key).uint)