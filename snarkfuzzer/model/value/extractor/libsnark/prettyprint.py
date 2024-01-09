import os
import subprocess
import gdb
import ast
import sys

sys.path.append(os.getcwd())

import utils.ec_coordinate.transform as coord
from config import *

def Int(name):
    var = gdb.parse_and_eval(name)
    
    return int(var)
    
def Fr(name):
    var = gdb.parse_and_eval(name)
    mont = var["mont_repr"]["data"]

    if (MONTGOMERY_OUTPUT):
        v1 = int(mont[0])
        v2 = int(mont[1])
        v3 = int(mont[2])
        v4 = int(mont[3])
        
        # Convert montgomery form into integer form
        prog = os.path.join(MONTGOMERY_REDUCE, "mont_reduce")
        exit = subprocess.run([prog, str(v1), str(v2), str(v3), str(v4)], stdout = subprocess.PIPE)
        data = int(exit.stdout)
    else:
        data = int(mont)

    return data

def G1(name):
    c1 = gdb.execute("call " + name + ".coord[0].toString(10)", to_string = True)
    c2 = gdb.execute("call " + name + ".coord[1].toString(10)", to_string = True)
    c3 = gdb.execute("call " + name + ".coord[2].toString(10)", to_string = True)
    
    c1 = int(c1.split("=")[1].strip('\n" '))
    c2 = int(c2.split("=")[1].strip('\n" '))
    c3 = int(c3.split("=")[1].strip('\n" '))
    
    if (c3 == 0):
        return 0
    if (c3 == 1):
        return c1, c2
    else:
        c1, c2 = coord.to_affine((c1, c2, c3))
        return c1, c2

def G2(name):
    c1 = gdb.execute("call " + name + ".coord[0].toString(10)", to_string = True)
    c2 = gdb.execute("call " + name + ".coord[1].toString(10)", to_string = True)
    c3 = gdb.execute("call " + name + ".coord[2].toString(10)", to_string = True)
    
    c1 = c1.split("=")[1].strip('\n"[] ').split(",")
    c2 = c2.split("=")[1].strip('\n"[] ').split(",")
    c3 = c3.split("=")[1].strip('\n"[] ').split(",")
    
    c11 = int(c1[0])
    c12 = int(c1[1])
    c21 = int(c2[0])
    c22 = int(c2[1])
    c31 = int(c3[0])
    c32 = int(c3[1])
    
    if (c31 == 0 and c32 == 0):
         return 0
    elif (c31 == 1 and c32 == 0):
         return ((c11, c12), (c21, c22))
    else:
        c1, c2 = coord.to_affine(([c11, c12], [c21, c22], [c31, c32]))
        return (c1, c2)

def GT(name):
    aa = gdb.execute("call " + name + ".elem.a_.a_.toString(10)", to_string = True)
    ab = gdb.execute("call " + name + ".elem.a_.b_.toString(10)", to_string = True)
    ac = gdb.execute("call " + name + ".elem.a_.c_.toString(10)", to_string = True)

    ba = gdb.execute("call " + name + ".elem.b_.a_.toString(10)", to_string = True)
    bb = gdb.execute("call " + name + ".elem.b_.b_.toString(10)", to_string = True)
    bc = gdb.execute("call " + name + ".elem.b_.c_.toString(10)", to_string = True)

    aa = ast.literal_eval(aa.split("=")[-1].strip('\n "'))
    ab = ast.literal_eval(ab.split("=")[-1].strip('\n "'))
    ac = ast.literal_eval(ac.split("=")[-1].strip('\n "'))

    ba = ast.literal_eval(ba.split("=")[-1].strip('\n "'))
    bb = ast.literal_eval(bb.split("=")[-1].strip('\n "'))
    bc = ast.literal_eval(bc.split("=")[-1].strip('\n "'))
    
    return tuple(aa + ab + ac + ba + bb + bc)

def ArrayFr(name):
    size = gdb.execute("call " + name + ".size()", to_string = True)
    size = int(size.split("=")[-1].strip("\n "))
    
    array = []
    for i in range(size):
        var = "{}[{}]".format(name, i)
        array.append(Fr(var))
    
    return array

def ArrayG(name):
    size = gdb.execute("call " + name + ".size()", to_string = True)
    size = int(size.split("=")[-1].strip("\n "))
    
    array = []
    for i in range(size):
        command = "whatis {}[{}]".format(name, i)
        gtype = gdb.execute(command, to_string = True)
        gtype = gtype.split("=")[-1].strip("\n ")
        
        if (gtype == "libff::bn128_G1"):
            var = "{}[{}]".format(name, i)
            array.append(G1(var))
        elif (gtype == "libff::bn128_G2"):
            var = "{}[{}]".format(name, i)
            array.append(G2(var))
        
    return array

def Query_IC(name):
    curve = []
    
    first = G1(name + ".first")
    curve.append(first)
    
    size = gdb.execute("call " + name + ".rest.values.size()", to_string = True)
    size = int(size.split("=")[-1].strip("\n "))
    
    for i in range(size):
        rest = G1("{}.rest.values[{}]".format(name, i))
        curve.append(rest)
    
    return curve

def Query(name, p = "g"):
    indices_size = gdb.execute("call " + name + ".indices.size()", to_string = True)
    indices_size = int(indices_size.split("=")[-1].strip("\n "))
    
    indices = []
    for i in range(indices_size):
        indices_num = gdb.execute("call {}.indices[{}]".format(name, i), to_string = True)
        indices_num = int(indices_num.split("=")[-1].strip("\n "))
        indices.append(indices_num)
    
    m = gdb.execute("call " + name + ".domain_size_", to_string = True)
    m = int(m.split("=")[-1].strip("\n "))

    curve = [0] * m

    # for i in indices:
    #     var = "{}[{}].{}".format(name, i, p)
        
    #     gtype = gdb.execute("whatis " + var, to_string = True)
    #     gtype = gtype.split("=")[-1].strip("\n ")
        
    #     if (gtype == "libff::bn128_G1"):
    #         curve[i] = G1(var)
    #     elif (gtype == "libff::bn128_G2"):
    #         curve[i] = G2(var)

    for i in range(indices_size):
        var = "{}.values[{}].{}".format(name, i, p)

        gtype = gdb.execute("whatis " + var, to_string = True)
        gtype = gtype.split("=")[-1].strip("\n ")
        
        if (gtype == "libff::bn128_G1"):
            curve[indices[i]] = G1(var)
        elif (gtype == "libff::bn128_G2"):
            curve[indices[i]] = G2(var)

    return curve

def QueryP(name):
    return Query(name, "h")
