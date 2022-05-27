#Homework 5
#Ranjan Behl
#rbehl
#03/01/21

#/usr/bin/env python3
import sys
import os
import copy
import warnings
import AES
import BitVector
from BitVector import *

def x931(v0,dt,totalNum,key_file):
    #random number list
    randList = []
    #create s -box
    AES.genTables()
    #create round keys
    AES.genRoundKeys(key_file)
    #get dt key
    dtCT = AES.encrypt(dt,key_file)
    #encrypt dt vector
    for i in range(totalNum):
        v0 ^= dtCT
        randNum = AES.encrypt(v0,key_file)
        randList.append(AES.encrypt(v0,key_file)) # add random number to list
        randNum ^= dtCT
        #update v
        v0 = AES.encrypt(randNum,key_file)
    return randList