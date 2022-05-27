#!/usr/bin/env python
# FOR HW 3 replace // and * with bitwise operations
#Homework Number: HW3
#Name: Ranjan Behl
#ECN Login: rbehl
#Due Date: 02/11/21

import sys
from operator import xor

def main():
    if len(sys.argv) != 3:  
        sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0]) 
        sys.exit(1) 

    NUM =  int(sys.argv[1])
    MOD =  int(sys.argv[2])
    MI(NUM,MOD)

def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = divide(num,mod)
        num, mod = mod, num % mod
        x, x_old = x_old - multiply(q,x), x
        y, y_old = y_old - multiply(q,y), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))

#MI(NUM, MOD)

def multiply(x, y):
     #check for the sign 
    if(xor((x < 0),(y < 0))):
        sign = -1
    else:
        sign = 1 

    # since we have the sign, we can remove the negatives
    x = abs(x)
    y = abs(y)

    result = 0
    while(y != 0):
        if(y & 1):
            #result = add(result,x) #if y is odd add x to result
            if(sign == -1):
                result = result - x
            else:
                result = result + x
        #print("This is x\n",x)
        #if(x < 0):
         #   print("error")
        x  = x << 1 
        y  = y >> 1
    return result


def divide(x,y):
     #check for the sign 
    if(xor((x < 0),(y < 0))):
        sign = -1
    else:
        sign = 1 

    # since we can the sign we can remove the negatives
    x = abs(x)
    y = abs(y)

    #edge case
    if(y == 1):
        return multiply(sign,x)
    #normal case
    result = 0
    while(x >= y):
        x = x - y
        result = result + 1
    
    return multiply(sign,result)
    

if __name__ == "__main__":
    main()




