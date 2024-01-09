import subprocess
import os

ABSPATH = os.path.dirname(os.path.abspath(__file__))
FILE1 = os.path.join(ABSPATH, "input1.txt")
FILE2 = os.path.join(ABSPATH, "input2.txt")
CIRCL = os.path.join(ABSPATH, "circl")

def int2bytes(num):
    bnum = num.to_bytes((num.bit_length() + 7) // 8, byteorder = "big")
    blist = []

    for i in range(len(bnum)):
        blist.append(bnum[i])
    
    return blist

def gen_ff(filename, num):
    f = open(filename, "w")
    f.write(str(num))
    f.close()
    
def gen_g1(filename, x, y):
    xb = int2bytes(x)
    yb = int2bytes(y)

    bytearray = " ".join(str(n) for n in xb + yb)

    f = open(filename, "w")
    f.write(bytearray)
    f.close()
    
def gen_g2(filename, x, y):
    x1, x2 = x
    y1, y2 = y
    
    x1b = int2bytes(x1)
    x2b = int2bytes(x2)
    y1b = int2bytes(y1)
    y2b = int2bytes(y2)
    
    bytex = x2b + x1b
    bytey = y2b + y1b

    bytearray = " ".join(str(n) for n in bytex + bytey)

    f = open(filename, "w")
    f.write(bytearray)
    f.close()

def del_file():
    os.remove(FILE1)
    os.remove(FILE2)

def add_g1(g11, g12):
    gen_g1(FILE1, *g11)
    gen_g1(FILE2, *g12)
    
    exit = subprocess.run([CIRCL, "1", FILE1, FILE2], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    del_file()
    
    result = exit.stdout.decode("utf-8")
    
    prex, prey, _ = result.split("\n")
    x = int(prex.split(": ")[-1], 16)
    y = int(prey.split(": ")[-1], 16)
    
    return (x, y)

def mul_g1(g1, ff):
    gen_g1(FILE1, *g1)
    gen_ff(FILE2, ff)
    
    exit = subprocess.run([CIRCL, "2", FILE1, FILE2], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    del_file()
    
    result = exit.stdout.decode("utf-8")
    
    prex, prey, _ = result.split("\n")
    x = int(prex.split(": ")[-1], 16)
    y = int(prey.split(": ")[-1], 16)
    
    return (x, y)

def add_g2(g21, g22):
    gen_g2(FILE1, *g21)
    gen_g2(FILE2, *g22)
    
    exit = subprocess.run([CIRCL, "3", FILE1, FILE2], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    del_file()
    
    result = exit.stdout.decode("utf-8")
    
    prex1, prex2, prey1, prey2, _, _ = result.split("\n")
    x1 = int(prex1.split(": ")[-1], 16)
    x2 = int(prex2.split(": ")[-1], 16)
    y1 = int(prey1.split(": ")[-1], 16)
    y2 = int(prey2.split(": ")[-1], 16)
    
    return ((x1, x2), (y1, y2))

def mul_g2(g2, ff):
    gen_g2(FILE1, *g2)
    gen_ff(FILE2, ff)
    
    exit = subprocess.run([CIRCL, "4", FILE1, FILE2], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    del_file()
    
    result = exit.stdout.decode("utf-8")
    
    prex1, prex2, prey1, prey2, _, _ = result.split("\n")
    x1 = int(prex1.split(": ")[-1], 16)
    x2 = int(prex2.split(": ")[-1], 16)
    y1 = int(prey1.split(": ")[-1], 16)
    y2 = int(prey2.split(": ")[-1], 16)
    
    return ((x1, x2), (y1, y2))

def add_ff(ff1, ff2):
    gen_ff(FILE1, ff1)
    gen_ff(FILE2, ff2)
    
    exit = subprocess.run([CIRCL, "5", FILE1, FILE2], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    del_file()
    
    result = int(exit.stdout.decode("utf-8"), 16)
    
    return result
        
def mul_ff(ff1, ff2):
    gen_ff(FILE1, ff1)
    gen_ff(FILE2, ff2)
    
    exit = subprocess.run([CIRCL, "6", FILE1, FILE2], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

    del_file()
    
    result = int(exit.stdout.decode("utf-8"), 16)
    
    return result

def pow_ff(ff1, ff2):
    def quickMul(n):
        ans = 1

        x_contribute = ff1

        while (n > 0):
            if (n % 2 == 1):
                ans = mul_ff(ans, x_contribute)

            x_contribute = mul_ff(x_contribute, x_contribute)

            n //= 2
        
        return ans
    
    return quickMul(ff2)