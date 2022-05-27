#Homework Number: HW6   
#Name: Ranjan Behl
#ECN Login: rbehl
#Due Date: 03/09/21

#!/usr/bin/env python3
import sys
import os
import copy
import warnings
import BitVector
from BitVector import *
from PrimeGenerator import *

#define e
e = 65537

def main():
    #three input cases
    if(sys.argv[1] == '-g'):
        #key gen
        keyGen(sys.argv[2],sys.argv[3])
    elif(sys.argv[1] == '-e'):
        #encrypt
        encrypt(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    elif(sys.argv[1] == '-d'):
        #decrypt
        decrypt(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    else:
        print("Error invalid format given!")


def gcd(a,b):
    while b:                                                                 
        a, b = b, a%b                                                        
    return a  

def keyGen(pFile,qFile):
    #open files for writing
    pFH = open(pFile,'w')
    qFH = open(qFile,'w')
    #pick p and q
    pGen = PrimeGenerator(bits=128,debug = 0)
    p = pGen.findPrime()
    q = pGen.findPrime()
    while(1):
        if(p == q or gcd(p-1,e) != 1 or gcd(q-1,e) != 1):
            #pick new values
            p = pGen.findPrime()
            q = pGen.findPrime()
        else:
            break
    #write keys to file
    pFH.write(str(p))
    qFH.write(str(q))
    #close file
    pFH.close()
    qFH.close()
    
def encrypt(msg,pFile,qFile,ct):
    cipherText = open(ct,'w')
    bvMsg = BitVector(filename=msg)
    pFH = open(pFile,'r')
    p = pFH.read()
    bvPkey = BitVector(intVal = int(p))
    pFH.close()
    qFH = open(qFile,'r')
    q = qFH.read()
    bvQkey = BitVector(intVal = int(q))
    qFH.close()
    n = bvPkey.int_val() * bvQkey.int_val()
    while(bvMsg.more_to_read):
        bvRead = bvMsg.read_bits_from_file(128)
        #pad zeros fron the right till 128
        if(len(bvRead) != 128):
            bvRead.pad_from_right(128-len(bvRead))
        #now pad zeros from the left to make it 256
        bvRead.pad_from_left(256-len(bvRead))
        #encryption process
        c = pow(bvRead.int_val(),e,n)
        bvCT = BitVector(intVal = c,size = 256)
        #write to the file
        cipherText.write(bvCT.get_bitvector_in_hex())

def CRT(c,d,p,q):
   vP = pow(c.int_val(),d,p.int_val())
   vQ = pow(c.int_val(),d,q.int_val())
   qI = q.multiplicative_inverse(p) 
   xP = q.int_val() * qI.int_val()
   pI = p.multiplicative_inverse(q)
   xQ = p.int_val() * pI.int_val() 
   pt = (vP*xP + vQ*xQ) % (p.int_val() * q.int_val())
   return pt

def decrypt(ct,pFile,qFile,msg):
    plainText = open(msg,'w')
    cipherText = open(ct.strip(),'r')
    data = cipherText.read()
    cipherText.close()
    bvCt = BitVector(hexstring = data)
    #Creating d, the private key
    pFH = open(pFile,'r')
    p = pFH.read()
    bvPkey = BitVector(intVal = int(p))
    pFH.close()
    qFH = open(qFile,'r')
    q = qFH.read()
    bvQkey = BitVector(intVal = int(q))
    qFH.close()
    bvE = BitVector(intVal = e)
    n = (bvPkey.int_val() - 1) * (bvQkey.int_val() - 1)
    bvEI = bvE.multiplicative_inverse(BitVector(intVal = n)) # e^-1 mod n, n is (p-1)*(q-1) !!!
    d = bvEI.int_val() % ((bvPkey.int_val() - 1) * (bvQkey.int_val() - 1)) 
    g = 0
    h = 256
    while(h <= bvCt.length()):
        bvRead = bvCt[g:h]
        g += 256
        h += 256
        #decryption process
        ptCTR = CRT(bvRead,d,bvPkey,bvQkey)
        bvPt = BitVector(intVal = ptCTR,size = 256)
        #unpad the plainText, remove 128 bits of zeros from the left
        unPadded = bvPt[128:]
        #write to file
        plainText.write(unPadded.get_bitvector_in_ascii())

if __name__ == "__main__":
    main()