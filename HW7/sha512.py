#Homework Number: HW7   
#Name: Ranjan Behl
#ECN Login: rbehl
#Due Date: 03/19/21

#!/usr/bin/env python3
import sys
import os
import copy
import warnings
import hashlib
import BitVector
from BitVector import *

K = ["428a2f98d728ae22",  "7137449123ef65cd", "b5c0fbcfec4d3b2f",
     "e9b5dba58189dbbc",  "3956c25bf348b538", "59f111f1b605d019",
     "923f82a4af194f9b",  "ab1c5ed5da6d8118", "d807aa98a3030242",
     "12835b0145706fbe",  "243185be4ee4b28c", "550c7dc3d5ffb4e2",
     "72be5d74f27b896f",  "80deb1fe3b1696b1", "9bdc06a725c71235",
     "c19bf174cf692694",  "e49b69c19ef14ad2", "efbe4786384f25e3",
     "0fc19dc68b8cd5b5",  "240ca1cc77ac9c65", "2de92c6f592b0275",
     "4a7484aa6ea6e483",  "5cb0a9dcbd41fbd4", "76f988da831153b5",
     "983e5152ee66dfab",  "a831c66d2db43210", "b00327c898fb213f",
     "bf597fc7beef0ee4",  "c6e00bf33da88fc2", "d5a79147930aa725",
     "06ca6351e003826f",  "142929670a0e6e70", "27b70a8546d22ffc",
     "2e1b21385c26c926",  "4d2c6dfc5ac42aed", "53380d139d95b3df",
     "650a73548baf63de",  "766a0abb3c77b2a8", "81c2c92e47edaee6",
     "92722c851482353b",  "a2bfe8a14cf10364", "a81a664bbc423001",
     "c24b8b70d0f89791",  "c76c51a30654be30", "d192e819d6ef5218",
     "d69906245565a910",  "f40e35855771202a", "106aa07032bbd1b8",
     "19a4c116b8d2d0c8",  "1e376c085141ab53", "2748774cdf8eeb99",
     "34b0bcb5e19b48a8",  "391c0cb3c5c95a63", "4ed8aa4ae3418acb",
     "5b9cca4f7763e373",  "682e6ff3d6b2b8a3", "748f82ee5defb2fc",
     "78a5636f43172f60",  "84c87814a1f0ab72", "8cc702081a6439ec",
     "90befffa23631e28",  "a4506cebde82bde9", "bef9a3f7b2c67915",
     "c67178f2e372532b",  "ca273eceea26619c", "d186b8c721c0c207",
     "eada7dd6cde0eb1e",  "f57d4f7fee6ed178", "06f067aa72176fba",
     "0a637dc5a2c898a6",  "113f9804bef90dae", "1b710b35131c471b",
     "28db77f523047d84",  "32caab7b40c72493", "3c9ebe0a15c9bebc",
     "431d67c49c100d4c",  "4cc5d4becb3e42b6", "597f299cfc657e2a",
     "5fcb6fab3ad6faec",  "6c44198c4a475817"]

K_bv = [BitVector(hexstring = kConst) for kConst in K]

def main():
    if (len(sys.argv) != 3):
        print("Usage: %s Filename HashfileName\n" % sys.argv[0])
        sys.exit(1)
    hash(sys.argv[1],sys.argv[2])

def hash(inFile,outputFile):
    with open(inFile,'r') as fileToHash:
        msg = fileToHash.read()
    fileToHash.close()
    # Initialize Hash Buffer
    h0 = BitVector(hexstring = '6a09e667f3bcc908')
    h1 = BitVector(hexstring = 'bb67ae8584caa73b')
    h2 = BitVector(hexstring = '3c6ef372fe94f82b')
    h3 = BitVector(hexstring = 'a54ff53a5f1d36f1')
    h4 = BitVector(hexstring = '510e527fade682d1')
    h5 = BitVector(hexstring = '9b05688c2b3e6c1f')
    h6 = BitVector(hexstring = '1f83d9abfb41bd6b')
    h7 = BitVector(hexstring = '5be0cd19137e2179')


#step 1 : Pad the message so that its length is an integral multiple of 1024 bits, the block size.
#The only complication here is that the last  128 bits of the last block must contain a
#value that is the length of the message. 

    bv = BitVector(textstring  = msg)
    bv1 = bv + BitVector(bitstring = "1") #padding consists of a single 1 followed by 0s
    numZeros = (896 - bv1.length()) % 1024
    zeroList = [0] * numZeros
    bv2 = bv1 + BitVector(bitlist = zeroList)
    bv3 = BitVector(intVal = bv.length(), size = 128)
    bv4 = bv2 + bv3


#step 2 : Generate the MESSAGE SCHEDULE required for processing a 1024-bit block of the input
#message.  The message schedule consists of 80 64-bit WORDS. The first 16 of these
#words are obtained directly from the 1024-bit block.  The rest of the words are
#obtained by applying permutation and mixing operations to the some of the
#reviously generated words. 

    words = [None] * 80 # 80 64 bit words
    for n in range(0,bv4.length(),1024):
        block = bv4[n:n+1024]
        words[0:16] = [block[i:i+64] for i in range(0,1024,64)] #first 16 words are directly from the msg block
        for i in range(16,80):
            iMinus2Word  = words[i-2]
            iMinus7Word = words[i-7]
            iMinus15Word = words[i-15]
            iMinus16Word   = words[i-16]
            sigma0 = (iMinus15Word.deep_copy() >> 1) ^ (iMinus15Word.deep_copy() >> 8) ^ (iMinus15Word.deep_copy().shift_right(7))
            sigma1 = (iMinus2Word.deep_copy() >> 19) ^ (iMinus2Word.deep_copy() >> 61) ^ (iMinus2Word.deep_copy().shift_right(6))
            words[i] = BitVector(intVal = (int(iMinus16Word) + int(sigma0) + int(iMinus7Word) + int(sigma1)) & 0xFFFFFFFFFFFFFFFF, size = 64)


#step 3 : Apply round-based processing to each 1024-bit input message block. There are 80 rounds to
#be carried out.  For this round-based processing, we first store the hash values calculated
#for the PREVIOUS MESSAGE BLOCK in temporary 64-bit variables denoted a,b,c,d,e,f,g,h. In the
#i-th round, we permute the values stored in these eight variables and, with two of the
#variables, we mix in the message schedule word words[i] and a round constant K[i]. 

        a,b,c,d,e,f,g,h = h0,h1,h2,h3,h4,h5,h6,h7
        for i in range(80):
            ch = (e & f) ^ (~e & g)
            maj = (a & b) ^ (a & c) ^ (b & c)
            sumA = (a.deep_copy() >> 28) ^ (a.deep_copy() >> 34) ^ (a.deep_copy() >> 39)
            sumE = (e.deep_copy() >> 14) ^ (e.deep_copy() >> 18) ^ (e.deep_copy() >> 41)
            t1 = BitVector(intVal = (int(h) + int(ch) + int(sumE) + int(words[i]) + int(K_bv[i])) & 0xFFFFFFFFFFFFFFFF, size = 64)
            t2 = BitVector(intVal = (int(sumA) + int(maj)) & 0xFFFFFFFFFFFFFFFF,size = 64)
            h = g
            g = f 
            f = e
            e = BitVector(intVal = (int(d) + int(t1)) & 0xFFFFFFFFFFFFFFFF, size = 64)
            d = c 
            c = b 
            b = a 
            a = BitVector(intVal = (int(t1) + int(t2)) & 0xFFFFFFFFFFFFFFFF, size = 64)

#Step 4 : We update the hash values calculated for the PREVIOUS message block by adding to it the
#values in the temporary variables a,b,c,d,e,f,g,h.

        h0 = BitVector(intVal = (int(h0) + int(a)) & 0xFFFFFFFFFFFFFFFF, size = 64)
        h1 = BitVector(intVal = (int(h1) + int(b)) & 0xFFFFFFFFFFFFFFFF, size = 64)
        h2 = BitVector(intVal = (int(h2) + int(c)) & 0xFFFFFFFFFFFFFFFF, size = 64)
        h3 = BitVector(intVal = (int(h3) + int(d)) & 0xFFFFFFFFFFFFFFFF, size = 64)
        h4 = BitVector(intVal = (int(h4) + int(e)) & 0xFFFFFFFFFFFFFFFF, size = 64)
        h5 = BitVector(intVal = (int(h5) + int(f)) & 0xFFFFFFFFFFFFFFFF, size = 64)
        h6 = BitVector(intVal = (int(h6) + int(g)) & 0xFFFFFFFFFFFFFFFF, size = 64)
        h7 = BitVector(intVal = (int(h7) + int(h)) & 0xFFFFFFFFFFFFFFFF, size = 64)
# concatenate h0-h7 to create the hash value
    msgHash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    outFileFH = open(outputFile,'w')
    outFileFH.write(msgHash.get_bitvector_in_hex())
    outFileFH.close()
# Testing my sha512 with hashlib
    print(msgHash.get_bitvector_in_hex())
    print(hashlib.sha512(msg.encode()).hexdigest())
   
if __name__ == "__main__":
    main()