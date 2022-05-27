#Homework Number: HW6   
#Name: Ranjan Behl
#ECN Login: rbehl
#Due Date: 03/09/21

#!/usr/bin/env python3
import sys
import os
import copy
import warnings
import solve_pRoot_BST
import BitVector
from BitVector import *
from PrimeGenerator import *

#define e
e = 3

def main():
    if(sys.argv[1] == '-e'):
        #encrypt
        encrypt(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
    elif(sys.argv[1] == '-c'):
        #crack the RSA
        crack(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
    else:
        print("Error invalid format given!")


def gcd(a,b):
    while b:                                                                 
        a, b = b, a%b                                                        
    return a 

def keyGen():
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
    return [p,q]

def encrypt(msg,enc1,enc2,enc3,nFile):
    # Generates three sets of public and private keys with e = 3
    # e is our public key for all three sets
    puKeylist = [[3,0],[3,0],[3,0]] #[e,n]
    # d is private key
    pKeylist = [[0,0],[0,0],[0,0]]  #[d,n]
    bvE = BitVector(intVal = e)
    bvMsg = BitVector(filename=msg)
    #enc list
    ct1 = open(enc1,'w')
    ct2 = open(enc2,'w')
    ct3 = open(enc3,'w') 
    cipherText = [ct1,ct2,ct3]
    for i in range(3):
        pqList = keyGen()
        bvPkey = BitVector(intVal = pqList[0])
        bvQkey = BitVector(intVal = pqList[1])
        n = bvPkey.int_val() * bvQkey.int_val()
        pKeylist[i][1] = n
        puKeylist[i][1] = n
        n = (bvPkey.int_val() -1) * (bvQkey.int_val() -1)
        bvN = BitVector(intVal = n)
        bvEI = bvE.multiplicative_inverse(bvN) # e^-1 mod n, n is (p - 1) * (q - 1) aka the totient 
        d = bvEI.int_val() % ((bvPkey.int_val() - 1) * (bvQkey.int_val() - 1)) 
        pKeylist[i][0] = d
    
    #encrypt the pt with each of the three public keys and write to the files
    for i in range(3):
        while(bvMsg.more_to_read):
            bvRead = bvMsg.read_bits_from_file(128)
            #pad zeros fron the right till 128
            if(len(bvRead) != 128):
                bvRead.pad_from_right(128-len(bvRead))
            #now pad zeros from the left to make it 256
            bvRead.pad_from_left(256-len(bvRead))
            #encryption process
            c = pow(bvRead.int_val(),e,puKeylist[i][1])
            bvCT = BitVector(intVal = c,size = 256)
            #write to the file
            cipherText[i].write(bvCT.get_bitvector_in_hex())
        #reset the file pointer
        bvMsg = BitVector(filename=msg) 
   #close the files
    ct1.close()
    ct2.close()
    ct3.close()
    print(pKeylist)
   #write the public keys to the file
    keyFile = open(nFile,'w')
    bvNl = BitVector(textstring = "\n")
    for i in range(3):
        bv = BitVector(intVal = puKeylist[i][1])
        keyFile.write(str(bv.int_val()))
        keyFile.write("\n")
    #close the files
    keyFile.close()

def CRT(ct1,ct2,ct3,N,nList):
    n1 = N // nList[0]
    n2 = N // nList[1]
    n3 = N // nList[2]

    bvN1 = BitVector(intVal = n1) 
    bvN2 = BitVector(intVal = n2)
    bvN3 = BitVector(intVal = n3)
    n1MI = bvN1.multiplicative_inverse(BitVector(intVal = nList[0]))
    n2MI = bvN2.multiplicative_inverse(BitVector(intVal = nList[1]))
    n3MI = bvN3.multiplicative_inverse(BitVector(intVal = nList[2]))

    result = ((ct1.int_val() * n1 * n1MI.int_val()) + (ct2.int_val() * n2 * n2MI.int_val()) + (ct3.int_val() * n3 * n3MI.int_val())) % N
    return result

def crack(enc1,enc2,enc3,nFile,crackedFile):
    #create the public key product N
    N = 1
    nList = []
    nFH = open(nFile,'r')
    for i in range(3):
        nList.append(int(nFH.readline()))
    for i in range(3):
        N *= nList[i]
    #close the file
    nFH.close()
    enc1Ct = open(enc1.strip(),'r')
    data0 = enc1Ct.read()
    bv0 = BitVector(hexstring = data0)
    enc2Ct = open(enc2.strip(),'r')
    data1 = enc2Ct.read()
    bv1 = BitVector(hexstring = data1)
    enc3Ct = open(enc3.strip(),'r')
    data2 = enc3Ct.read() 
    bv2 = BitVector(hexstring = data2)
    g = 0
    h = 256
    #open the output file
    crk = open(crackedFile,'w')
    while(h <= bv0.length()):
        bvRead0 = bv0[g:h]
        bvRead1 = bv1[g:h]
        bvRead2 = bv2[g:h]
        g += 256
        h += 256
        ptCTR = CRT(bvRead0,bvRead1,bvRead2,N,nList)
        ptPRT = solve_pRoot_BST.solve_pRoot(3,ptCTR)
        bvPT = BitVector(intVal = ptPRT,size = 256)
        unPadded = bvPT[128:]
        crk.write(unPadded.get_bitvector_in_ascii())

if __name__ == "__main__":
    main()