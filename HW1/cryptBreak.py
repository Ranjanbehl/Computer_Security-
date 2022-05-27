#Homework Number: 1
#Name: Ranjan Behl
#ECN Login:rbehl    
#Due Date:01/28/21

#!/usr/bin/env python3
# imports
from BitVector import *
# constants
BLOCKSIZE = 16
numbytes = BLOCKSIZE // 8
# main function


def main():
    for intKey in range(0, 65535):
        key_bv = BitVector(intVal= intKey, size=16)
        decryptedMsg = cryptBreak(sys.argv[1], key_bv)
        #print(decryptedMsg)
        if 'Yogi Berra' in decryptedMsg:
            print('Encrpytion Broken!')
            print('\n The key was was: ', intKey)
            print('\n The original quote was: ',decryptedMsg)
        else:
            #print('Not decrypted yet')
            pass


def cryptBreak(ciphertextFile, key_bv):
        encryptedFile = open(ciphertextFile.strip(),'r')
        encrypted_bv = BitVector(hexstring = encryptedFile.read())
        encryptedFile.close()  # close the file
        ### use the code from DecryptForFun ###
        PassPhrase = "Hopes and dreams of a million years"
        # Reduce the passphrase to a bit array of size BLOCKSIZE:
        bv_iv = BitVector(bitlist=[0]*BLOCKSIZE)
        for i in range(0, len(PassPhrase) // numbytes):
            textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
            bv_iv ^= BitVector(textstring = textstr)
        # Create a bitvector for storing the decrypted plaintext bit array:
        msg_decrypted_bv = BitVector(size = 0)
        # Carry out differential XORing of bit blocks and decryption:
        previous_decrypted_block = bv_iv
        for i in range(0, len(encrypted_bv) // BLOCKSIZE):
            bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
            temp = bv.deep_copy()
            bv ^= previous_decrypted_block
            previous_decrypted_block = temp
            bv ^= key_bv
            msg_decrypted_bv += bv
        # Extract plaintext from the decrypted bitvector:
        outputtext = msg_decrypted_bv.get_text_from_bitvector()
        # Return text back to caller
        return outputtext


if __name__ == "__main__":
    main()