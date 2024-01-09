import os
import re
import ast
import sys
import gdb

sys.path.append(os.getcwd())
from config import *

# def getmemorymaxsize(vname):
#     length = 10
#     while (True):
#         try:
#             gdb.execute("x/{}wx &{}".format(length, vname), to_string = True)
#             length *= 10
#         except:
#             break
#     return length

# def getmemorysize(vname, lowsize, uppsize):
#     if (lowsize == uppsize):
#         return lowsize
#     if (uppsize - lowsize == 1):
#         try:
#             gdb.execute("x/{}wx &{}".format(uppsize, vname), to_string = True)
#             return uppsize
#         except gdb.MemoryError:
#             return lowsize
#     length = (uppsize + lowsize) // 2
#     try:
#         gdb.execute("x/{}wx &{}".format(length, vname), to_string = True)
#         return getmemorysize(vname, length, uppsize)
#     except gdb.MemoryError:
#         return getmemorysize(vname, lowsize, length)

def getmemory(vname):
    size = gdb.execute("call sizeof({})".format(vname), to_string = True)
    size = int(size.split("=")[-1].strip("\n "))

    result = gdb.execute("x/{}bx &{}".format(size, vname), to_string = True)

    memorylist = []
    resultline = result.strip("\n").split("\n")

    for line in resultline:
        memorylist.extend(line.split(":")[-1].strip("\t").split("\t"))

    return memorylist

def memorychange(memorylist1, memorylist2):
    if (len(memorylist1) != len(memorylist2)):
        return True

    for i in range(len(memorylist1)):
        if (memorylist1[i] != memorylist2[i]):
            if (memorylist2[i] != "0x00"):
                return True
                
    return False

def watchgdb():
    valuechange = False

    paramfile = os.path.join(MONITOR_LOG, "paramfile.txt")

    f = open(paramfile)
    content = f.read()
    f.close()

    valgrindlog = os.path.join(MONITOR_LOG, "valgrindlog.txt")
    logfile = os.path.join(MONITOR_LOG, "gdblog.txt")

    vardict = ast.literal_eval(content)
    vname = vardict["vname"]
    vpath = vardict["vpath"]
    vline = vardict["vline"]

    f = open(valgrindlog)
    content = f.readlines()
    f.close()
    pid = re.search(r'==(.*?)==', content[0]).group(1)
    
    gdb.execute("set logging file " + logfile)
    gdb.execute("set logging overwrite on")
    gdb.execute("set pagination off")
    gdb.execute("set logging off")
    gdb.execute("set logging on")

    command = ["target", "remote", "|", VALGRIND_PATH, "--pid=" + str(pid)]
    gdb.execute(" ".join(command))

    gdb.execute("set $_exitcode = -1")
    gdb.execute("set pagination off")

    spec = os.path.join(LIBRARY_PATH, vpath) + ":" + str(vline)
    gdb.Breakpoint(spec)

    gdb.execute("continue")

    gdb.execute("watch " + vname)
    memoryold = getmemory(vname)

    gdb.execute("continue")

    while True:
        if (int(gdb.parse_and_eval("$_exitcode")) == 0):
            break
        
        f = open(logfile)
        content = f.read()
        f.close()

        if ("the program has left the block in" in content):
            gdb.execute("kill")
            break
        else:
            callstack = gdb.execute("where", to_string = True)
            callstack = callstack.strip("\n").split("\n")
            
            for i in range(len(callstack), -1, -1):
                try:
                    gdb.execute("frame {}".format(i))
                    gdb.parse_and_eval(vname)
                    
                    memorynew = getmemory(vname)
                    
                    if (memorychange(memoryold, memorynew)):
                        valuechange = True

                    gdb.execute("frame 0")
                    break
                except gdb.error:
                    continue
        
        gdb.execute("continue")

    sys.stdout.write("\n" + str(valuechange))
    gdb.execute("quit")

if __name__ == "__main__":
    watchgdb()