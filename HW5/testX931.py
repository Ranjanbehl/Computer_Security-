import x931
import time
from BitVector import *
from datetime import timedelta

if __name__ == "__main__":
    v0 = BitVector(textstring="computersecurity") #v0 will be  128 bits
    #As mentioned before, for testing purposes dt is set to a predetermined value
    dt = BitVector(intVal = 501, size=128)
    start = time.time()
    listX931 = x931.x931(v0,dt,3,"keyX931.txt")
    elapsed = (time.time() - start)
    print(str(timedelta(seconds=elapsed)))
    #Check if list is correct
    print("{}\n{}\n{}".format(int(listX931[0]),int(listX931[1]),int(listX931[2])))
