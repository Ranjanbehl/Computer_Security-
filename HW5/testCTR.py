#!/usr/bin/env python3
import sys
import os
import time
import copy
import warnings
import AES
import BitVector
from BitVector import *
from datetime import timedelta
from AES_image import ctr_aes_image

start = time.time()
iv = BitVector(textstring = 'computersecurity')
ctr_aes_image(iv,'image.ppm','enc_image.ppm','keyCTR.txt')
elapsed = (time.time() - start)
print(str(timedelta(seconds=elapsed)))
