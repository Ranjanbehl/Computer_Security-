#!/usr/bin/env python3
import sys
import os
import hashlib

def main():
    if (len(sys.argv) != 3):
        print("Usage: %s Filename HashfileName\n" % sys.argv[0])
        sys.exit(1)
    
    with open(sys.argv[1],'r') as fileToHash:
        msg = fileToHash.read()
    fileToHash.close()
    outFileFH = open(sys.argv[2],'w')
    outFileFH.write(hashlib.sha512(msg.encode()).hexdigest())
    outFileFH.close()

if __name__ == "__main__":
    main()