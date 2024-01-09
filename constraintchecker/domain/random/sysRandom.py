#!/usr/bin/env python3.9

import random
import sys

def randomGenerator(nmin, nmax):
    """Generate a random number by random in [nmin, nmax]
    
    int, int -> int"""
    rng = random
    rnum = rng.randint(nmin, nmax)

    return rnum

def systemRandomGenerator(nmin, nmax):
    """Generate a random number by random.SystemRandom in [nmin, nmax]
    
    int, int -> int"""
    rng = random.SystemRandom()
    rnum = rng.randint(nmin, nmax)

    return rnum

def main():
    """Generate n random number in range by value provided in the input arguments
    
    None -> None"""
    size, *minmax = sys.argv[1:]
    if (int(size) * 2 != len(minmax)):
        raise ValueError("Reuqire " + size + " minimum values and + size + maximum values")

    minlst = minmax[::2]
    maxlst = minmax[1::2]

    for i in range(int(size)):
        rnum = systemRandomGenerator(int(minlst[i]), int(maxlst[i]))
        sys.stdout.write(str(rnum))

        if (i != int(size) - 1):
            sys.stdout.write(" ")

# WARNING: The pseudo-random generators of this module should not be used for security purposes. 
if __name__ == "__main__":
    main()