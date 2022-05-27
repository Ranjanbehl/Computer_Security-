#Homework 5
#Ranjan Behl
#rbehl
#03/01/21

#!/usr/bin/env python3
import sys
import os
import copy
import warnings
import AES
import BitVector
from BitVector import *

def ctr_aes_image(iv,image_file='image.ppm',out_file='enc_image.ppm',key_file='key.txt'):
    bv = BitVector(filename=image_file)
    image_enc = open(out_file,'wb')
    #copy the header over to image_enc from imagefile
    idx = 0
    #print("value of idx", idx)
    while(idx < 3):
        bvRead = bv.read_bits_from_file(8)
        #print(bvRead.get_bitvector_in_ascii())
        if(bvRead.get_bitvector_in_ascii() == '\n'):
            idx = idx + 1
        bvRead.write_to_file(image_enc)
    
    AES.genTables() # caused index out of bounds expection, fixed required global variables
    AES.genRoundKeys(key_file) #create the round keys
    while(bv.more_to_read):
        ivCt = AES.encrypt(iv,key_file)
        bvRead = bv.read_bits_from_file(128)
        if(bvRead.length() != 128):
        #pad with zeros, needs to be done here instead of AES...
            bvRead.pad_from_right(128 - bvRead.length())
        bvRead ^= ivCt
        #print(bvRead.get_bitvector_in_hex())
        bvRead.write_to_file(image_enc)
        val = iv.int_val()
        val += 1
        #print("\nVal is: " + str(val))
        iv = BitVector(intVal = val, size = 128)
        

