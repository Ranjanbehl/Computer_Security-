#Homework Number: 2
#Name: Ranjan Behl
#ECN Login: rbehl
#Due Date: 01/28/21

#!/usr/bin/env python3
import sys
import os
from BitVector import *

expansionPermutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

keyPermutation1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,
                      9,1,58,50,42,34,26,18,10,2,59,51,43,35,
                     62,54,46,38,30,22,14,6,61,53,45,37,29,21,
                     13,5,60,52,44,36,28,20,12,4,27,19,11,3]


keyPermutation2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,
                      3,25,7,15,6,26,19,12,1,40,51,30,36,46,
                     54,29,39,50,44,32,47,43,48,38,55,33,52,
                     45,41,49,35,28,31]

shiftsForRoundKeyGen = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

sBoxes = {i:None for i in range(8)}

sBoxes[0] = [ [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
               [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
               [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
               [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13] ]

sBoxes[1] = [ [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
               [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
               [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
               [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9] ]

sBoxes[2] = [ [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
               [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
               [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
               [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12] ]

sBoxes[3] = [ [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
               [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
               [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
               [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14] ]

sBoxes[4] = [ [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
               [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
               [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
               [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3] ]  

sBoxes[5] = [ [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
               [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
               [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
               [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13] ]

sBoxes[6] = [ [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
               [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
               [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
               [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12] ]

sBoxes[7] = [ [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
               [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
               [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
               [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11] ]

pBoxPermutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

def main():
    '''
    If sys.argv[1] is e then call the encrypt function, 
    If sys.argv[1] is d then decrypt function, and anything else is a errror
    '''
    if(len(sys.argv) != 5):
        'error'
        print("Usage: python3 DES_text.py -e message.txt key.txt encrypted.txt\n Or python3 DES_text.py -d encrypted.txt key.txt decrypted.txt")
        sys.exit(1)
    if(sys.argv[1] == '-e'):
        
        plainText = sys.argv[2]
        keyStr = sys.argv[3]
        cipherText = sys.argv[4]
        encrypt(plainText,keyStr,cipherText)

    elif(sys.argv[1] == '-d'):
        
        cipherText = sys.argv[2]
        keyStr = sys.argv[3]
        plainText = sys.argv[4]
        decrypt(cipherText,keyStr,plainText)


def encrypt(plainText,keyStr,cipherText):
    #break the plainText in 64 bit blocks
    bv = BitVector(filename=plainText)
    keyfp = open(keyStr,'r')
    cipherText = open(cipherText,'w')
    key = getEncryptionKey(keyfp)
    keyfp.close()
    roundKeys = extractRoundKeys( key )
    while (bv.more_to_read):
        bvRead = bv.read_bits_from_file( 64 )
        if(bvRead.length() != 64):
            #pad with zeros
            bvRead.pad_from_left(64 - bvRead.length())
        #break 64 bit vector into two 32 bit vectors and perform expansion permutation on rightside vector
        if bvRead.length() > 0: #bv.getsize() throws error for some reason
            #16 rounds
            bvHex = bvRead.get_bitvector_in_hex()
            #print("First 64 bit block before round 1:",bvHex)
            [leftHalf, rightHalf] = bvRead.divide_into_two()
            for i in range(16):
                originalRH = rightHalf # needed for the next left half 
                #expand rightHalf to 48 bit
                newRH = rightHalf.permute(expansionPermutation)
                #XOR newRH with the roundkey to get new 48 bit
                outXor = newRH ^ roundKeys[i]
                #substitution with 8 s-boxes to get new 32 bit
                sBoxesOutput = substitute(outXor)
                #permutation with pBox
                rightHalf = sBoxesOutput.permute(pBoxPermutation)
                newRH = rightHalf ^ leftHalf
                newLH = originalRH # need og RH
                #swap to create the bitvector for the next round
                #reset bv to all zeros just to be safe
                bvRead.reset(0)
                leftHalf = newLH
                rightHalf = newRH
                #bvRead = newLH + newRH
                bvHex = bvRead.get_bitvector_in_hex()
                #print("First 64 bit block after round 1:",bvHex)
        #write the 64 encrypted block to the cipherText file
        bvRead = rightHalf + leftHalf
        print("64 Bit Block: ",bvRead.get_bitvector_in_hex())
        cipherText.write(bvRead.get_bitvector_in_hex())
    bv.close_file_object()
    cipherText.close()

def getEncryptionKey(keyfp):
    key = BitVector(textstring = keyfp.read())
    key = key.permute(keyPermutation1)
    return key

def extractRoundKeys(encryptionKey):
    roundKeys = []
    key = encryptionKey.deep_copy()
    for round_count in range(16):
        [LKey, RKey] = key.divide_into_two()    
        shift = shiftsForRoundKeyGen[round_count]
        LKey << shift
        RKey << shift
        key = LKey + RKey
        round_key = key.permute(keyPermutation2)
        roundKeys.append(round_key)
    return roundKeys

def substitute(expandedHalfBlock):
    '''
    This method implements the step "Substitution with 8 S-boxes" step you see inside
    Feistel Function dotted box in Figure 4 of Lecture 3 notes.
    '''
    output = BitVector (size = 32)
    segments = [expandedHalfBlock[x*6:x*6+6] for x in range(8)]
    for sindex in range(len(segments)):
        row = 2*segments[sindex][0] + segments[sindex][-1]
        column = int(segments[sindex][1:-1])
        output[sindex*4:sindex*4+4] = BitVector(intVal = sBoxes[sindex][row][column], size = 4)
    return output        


def decrypt(cipherText,keyStr,plainText):
    #break the plainText in 64 bit blocks
    cipherText = open(cipherText.strip(),'r')
    data = cipherText.read()
    bv = BitVector(hexstring = data) 
    cipherText.close()
    keyfp = open(keyStr,'r')
    plainText = open(plainText,'wb')
    key = getEncryptionKey(keyfp)
    roundKeys = extractRoundKeys( key )
    keyfp.close()
    j = 0
    k = 64
    #round key reverse
    roundKeys.reverse()
    while(k <= bv.length()):
        bvRead = bv[j:k]
        j = j + 64
        k = k + 64
        #print(bv_read)
        if(bvRead.length() != 64):
            #pad with zeros
            bvRead.pad_from_left(64 - bvRead.length())
        #break 64 bit vector into two 32 bit vectors and perform expansion permutation on rightside vector
        if bvRead.length() > 0:
            #16 rounds
            [leftHalf, rightHalf] = bvRead.divide_into_two()
            for i in range(16):
                originalRH = rightHalf # needed for the next left half 
                #expand rightHalf to 48 bit
                newRH = rightHalf.permute(expansionPermutation)
                #XOR newRH with the roundkey to get new 48 bit
                outXor = newRH ^ roundKeys[i]
                #substitution with 8 s-boxes to get new 32 bit
                sBoxesOutput = substitute(outXor)
                #permutation with pBox
                rightHalf = sBoxesOutput.permute(pBoxPermutation)
                newRH = rightHalf ^ leftHalf
                newLH = originalRH # need og RH
                #swap to create the bitvector for the next round
                #reset bv to all zeros just to be safe
                bvRead.reset(0)
                leftHalf = newLH
                rightHalf = newRH
        #write the decrypted text to the decrypted file
        bvRead = rightHalf + leftHalf
        bvRead.write_to_file(plainText)

#The following is needed
if __name__ == "__main__":
    main()