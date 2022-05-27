#Homework 4
#Ranjan Behl
#rbehl
#02/23/21

#!/usr/bin/env python3
import sys
import os
import copy
import warnings
import BitVector
from BitVector import *

#get rid of warnings
warnings.filterwarnings(action='ignore')

#256 bit AES-14 Rounds
#double check the key schedule generate 

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption


#Create two 256-element arrays for byte substitution, one for encryption and one for decryption
def genTables():
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))


#This is the g() function 
def gee(keyword, round_constant, byte_sub_table):
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

#Key Expansion
def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

#substitute bytes function for both encypt and decrypt
def subBytes(stateArray,mode):
    #subBytes
    if(mode == 'e'):
        for i in range(4):
            for j in range(4):
                idx = stateArray[j][i]
                idx = ord(idx.get_bitvector_in_ascii()) #char to int
                stateArray[j][i] = BitVector(textstring = chr(subBytesTable[idx])) # int to char bc one byte
    #invSubBytes
    elif(mode == 'd'):
        for i in range(4):
            for j in range(4):
                idx = stateArray[j][i]
                idx = ord(idx.get_bitvector_in_ascii()) #char to int
                stateArray[j][i] = BitVector(textstring = chr(invSubBytesTable[idx])) # int to char bc one byte
    return stateArray

#function for array shifting
def shift(array,sVal):
    sVal %= len(array)
    shiftedArray = array[sVal:] + array[:sVal]
    return shiftedArray

def shiftRow(stateArray,mode):
    #ShiftRows
    if(mode == 'e'):
        #first row - no shift
        #seond row - one byte circular shift to the left
        #third row - two byte circular shift to the left
        #fourth row - three byte circular shift to the left
        for i in range(1,4):
            stateArray[i] = shift(stateArray[i],i)
    #InvShiftRows
    elif(mode == 'd'):
         #first row - no shift
        #seond row - one byte circular shift to the right
        #third row - two byte circular shift to the right
        #fourth row - three byte circular shift to the right
        for i in range(1,4):
            stateArray[i] = shift(stateArray[i],-i)
    return stateArray

def MixCol(stateArray,mode):
    #MixColumns
    if(mode == 'e'):
        #required bitvectors
        #a = BitVector(intVal = 1)
        b = BitVector(intVal = 2)
        c = BitVector(intVal = 3)
        n = 8
       # mix = [b,c,a,a] #starting 
        #get transpose stateArray?
        #stateArrayT = stateArray
        #values were getting overridden so create a copy
        tmp = copy.deepcopy(stateArray) #should i do bitvectory copy?
        #first row
        for i in range(4):
            stateArray[0][i] =  (b.gf_multiply_modular(tmp[0][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[1][i],AES_modulus,n)) ^ (tmp[2][i]) ^ (tmp[3][i])
         #right shift mix by one
        #mix = mix[-1:] + mix[:-1]
        #second row
            stateArray[1][i] =  (b.gf_multiply_modular(tmp[1][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[2][i],AES_modulus,n)) ^ (tmp[3][i]) ^ (tmp[0][i])
        #third row
            stateArray[2][i] =  (b.gf_multiply_modular(tmp[2][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[3][i],AES_modulus,n)) ^ (tmp[0][i]) ^ (tmp[1][i])
        #fourth row
            stateArray[3][i] =  (b.gf_multiply_modular(tmp[3][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[0][i],AES_modulus,n)) ^ (tmp[1][i]) ^ (tmp[2][i])
        #transpose back
        #stateArray = flip(stateArrayT)
        
    #InvMixColumns
    elif(mode == 'd'):
         #required bitvectors
        a = BitVector(hexstring = "0E")
        b = BitVector(hexstring = "0B")
        c = BitVector(hexstring = "0D")
        d = BitVector(hexstring = "09")
        n = 8
        tmp = copy.deepcopy(stateArray)
        #stateArrayT = stateArray
        #first row
        for i in range(4):
            stateArray[0][i] =  (a.gf_multiply_modular(tmp[0][i],AES_modulus,n)) ^ (b.gf_multiply_modular(tmp[1][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[2][i],AES_modulus,n)) ^ (d.gf_multiply_modular(tmp[3][i],AES_modulus,n))
         #right shift mix by one
        #mix = mix[-1:] + mix[:-1]
        #second row
            stateArray[1][i] =  (a.gf_multiply_modular(tmp[1][i],AES_modulus,n)) ^ (b.gf_multiply_modular(tmp[2][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[3][i],AES_modulus,n)) ^ (d.gf_multiply_modular(tmp[0][i],AES_modulus,n))
        #third row
            stateArray[2][i] =  (a.gf_multiply_modular(tmp[2][i],AES_modulus,n)) ^ (b.gf_multiply_modular(tmp[3][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[0][i],AES_modulus,n)) ^ (d.gf_multiply_modular(tmp[1][i],AES_modulus,n))
        #fourth row
            stateArray[3][i] =  (a.gf_multiply_modular(tmp[3][i],AES_modulus,n)) ^ (b.gf_multiply_modular(tmp[0][i],AES_modulus,n)) ^ (c.gf_multiply_modular(tmp[1][i],AES_modulus,n)) ^ (d.gf_multiply_modular(tmp[2][i],AES_modulus,n))
        #transpose back
        #stateArray = flip(stateArrayT)
    return stateArray 

#bitvector to stateArray
def bvToSa(bv):
    stateArray = [[0 for x in range(4)] for x in range(4)]
    for i in range(4):
            for j in range(4):
                #each element will be a bitvector
                stateArray[j][i] = bv[32*i + 8*j:32*i + 8*(j+1)] 
    return stateArray

#stateArray to bitvector
def saToBv(stateArray):
   bvTest = BitVector(size = 0)
   for i in range(4):
        for j in range(4):
            bvTest += stateArray[j][i] 
   return bvTest

def main():
    '''
    If sys.argv[1] is e then call the encrypt function, 
    If sys.argv[1] is d then decrypt function, and anything else is a errror
    '''
    if(len(sys.argv) != 5):
        'error'
        print("Usage: python3 AES.py -e message.txt key.txt encrypted.txt\n Or python3 AES.py -d encrypted.txt key.txt decrypted.txt")
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

#do key expansion and return list of round keys
def KeyExpansion(keyBv,numRounds):
   #create the key expansion array
    key_words = []
    key_words = gen_key_schedule_256(keyBv)
    key_schedule = []
    #Each 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers
    for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
        key_schedule.append(keyword_in_ints)
    #create the round keys
    num_rounds = numRounds #14 bc 256 bit key 
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])
    return round_keys

def encrypt(plainText,keyStr,cipherText):
    #open key file
    keyfp = open(keyStr,'r')
    keyText = keyfp.read()
    #open cp file
    cipherText = open(cipherText,'w')
    key = keyText.strip()
    key += '0' * (256//8 - len(key)) if len(key) < 256//8 else key[:256//8]  
    key_bv = BitVector( textstring = key )
    #close key file
    keyfp.close()
    round_keys = KeyExpansion(key_bv,14)
    #create s-box
    genTables()
    #get 128 bit pt block
    bv = BitVector(filename = plainText)
    while(bv.more_to_read):
        bvRead = bv.read_bits_from_file(128)
        if(bvRead.length() != 128):
            #pad with zeros
            bvRead.pad_from_right(128 - bvRead.length())
        #now xor the bv before creating the stateArray with the first four words of the key schedule(roundkey[0])
        bvRead = bvRead ^ BitVector(bitstring = round_keys[0])
        # test for step 0 - it works
    #convert pt block to input state array
        stateArray = bvToSa(bvRead)
        #now start the encryption process(14 rounds but last round is special)
        for i in range(14):
            #step 1 - substitute bytes
            stateArray = subBytes(stateArray,'e')
            #step 2 - shift rows
            stateArray = shiftRow(stateArray,'e')
            #step 3 - mix columns(for rounds 0 to 13 only)
            if(i<13):
                stateArray = MixCol(stateArray,'e')
            #step 4 - add round key(XOR)
            bvRead = BitVector(size = 0)
            for k in range(4):
                for j in range(4):
                    bvRead += stateArray[j][k]
            bvRead ^= round_keys[i + 1]
            stateArray = bvToSa(bvRead)
            #step 5 write result to file
        cipherText.write(bvRead.get_bitvector_in_hex())
    bv.close_file_object()
    cipherText.close()

def decrypt(cipherText,keyStr,plainText):
    cipherText = open(cipherText.strip(),'r')
    data = cipherText.read()
    cipherText.close()
     #open pt file
    plainText = open(plainText,'wb') 
    #open key file
    keyfp = open(keyStr,'r')
    keyText = keyfp.read()
    key = keyText.strip()
    key += '0' * (256//8 - len(key)) if len(key) < 256//8 else key[:256//8]  
    key_bv = BitVector( textstring = key )
    #close key file
    keyfp.close()
    round_keys = KeyExpansion(key_bv,14)
    #create s-box
    genTables()
    #get 128 bit pt block
    bv = BitVector(hexstring = data)
    g = 0
    h = 128
    while(h <= bv.length()):
        #bvRead = BitVector(size = 0)
        bvRead = bv[g:h]
        g += 128
        h += 128
        if(bvRead.length() != 128):
            #pad with zeros
            bvRead.pad_from_right(128 - bvRead.length())
        #now xor the bv before creating the stateArray with the last four words of the key schedule(roundkey[14])
        bvRead = bvRead ^ BitVector(bitstring = round_keys[14])
        # test for step 0 - it works
    #convert pt block to input state array
        stateArray = bvToSa(bvRead)
        #now start the encryption process(14 rounds but last round is special)
        for i in range(14):
            #step 1 - Inverse shift rows
            stateArray = shiftRow(stateArray,'d')
            #step 2 - Inverse substitute bytes
            stateArray = subBytes(stateArray,'d')
            #step 3 - add round key(XOR)
            bvTest = BitVector(size = 0)
            for k in range(4):
                for j in range(4):
                    bvTest += stateArray[j][k]
            bvTest ^= round_keys[13 - i]
            stateArray = bvToSa(bvTest)
            #step 4 - mix columns(for rounds 0 to 13 only)
            if(i<13):
                stateArray = MixCol(stateArray,'d')
            #step 5 write result to file - it works 
        bvReadDc = saToBv(stateArray)
        bvReadDc.write_to_file(plainText)
    plainText.close()

if __name__ == "__main__":
    main()