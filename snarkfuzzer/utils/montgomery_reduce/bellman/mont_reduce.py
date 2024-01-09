#!/usr/bin/env python3
#cython: language_level=3

import os
import sys
import subprocess
import re

ABSPATH = os.path.dirname(os.path.abspath(__file__))
GDBFILE = os.path.join(ABSPATH, "script.gdb")
LOGFILE = os.path.join(ABSPATH, "log.txt")
MONT_REDUCE = os.path.join(ABSPATH, "mont_reduce")

def gdbscript():
    mont_repr = []
    for num in sys.argv[1:]:
        mont_repr.append(int(num))

    f = open(GDBFILE, "w")

    f.write("set pagination off\n")
    f.write("break 15\n")

    command = "run {} {} {} {}"
    f.write("run {} > {}\n".format(" ".join([str(n) for n in mont_repr]), LOGFILE))

    if (len(sys.argv) == 5):
        f.write("call tmp1.__0.__0 = {}\n".format(mont_repr))
    elif (len(sys.argv) == 7):
        f.write("call tmp2.__0.__0 = {}\n".format(mont_repr))

    f.write("continue\n")
    
    f.write("quit\n")
    f.close()

def mont_trans():
    if (os.path.exists(GDBFILE)):
        os.remove(GDBFILE)
    if (os.path.exists(LOGFILE)):
        os.remove(LOGFILE)
    
    gdbscript()

    subprocess.run(["gdb", "-q", "-x", GDBFILE, MONT_REDUCE], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
    f = open(LOGFILE)
    content = f.read()
    f.close()
    num = int(re.findall('\((.*?)\)', content)[0], 16)

    os.remove(GDBFILE)
    os.remove(LOGFILE)

    return num

def main():
    num = mont_trans()
    print(num, end = "")

if __name__ == "__main__":
    main()
