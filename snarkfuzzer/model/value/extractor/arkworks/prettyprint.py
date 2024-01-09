import gdb
import os
import subprocess
import re
import sys

import utils.ec_coordinate.transform as coord

sys.path.append(os.getcwd())
from config import *

def Int(name):
    var = gdb.parse_and_eval(name)
    
    return int(var)

def Fr(name):
    print("***Fr name: " + name)
    var = gdb.parse_and_eval(name)
    # print("***var: \n" + var)
    mont = var["__0"]["__0"]

    size = int(gdb.parse_and_eval("sizeof({}.__0.__0)/sizeof(*{}.__0.__0)".format(name, name)))

    mont_repr = []
    for i in range(size):
        mont_repr.append(str(mont[i]))
    
    # Convert montgomery form into integer form
    prog = os.path.join(MONTGOMERY_REDUCE, "mont_reduce.py")
    exit = subprocess.run([prog] + mont_repr, stdout = subprocess.PIPE)
    data = int(exit.stdout)

    return data

def Fq2(name):
    c0 = Fr(name + ".c0")
    c1 = Fr(name + ".c1")

    result = (c0, c1)
    return result

def Fq6(name):
    c0 = Fq2(name + ".c0")
    c1 = Fq2(name + ".c1")
    c2 = Fq2(name + ".c2")

    result = (c0, c1, c2)
    return result

def Fq12(name):

    c0 = Fq6(name + ".c0")
    c1 = Fq6(name + ".c1")

    result = (c0, c1)
    return result

def G1(name):
    try:
        gdb.parse_and_eval(name + ".z")
        x = Fr(name + ".x")
        y = Fr(name + ".y")
        z = Fr(name + ".z")
        print("x: {}".format(x))
        print("y: {}".format(y))
        print("z: {}".format(z))
        
        data = coord.to_affine((x, y, z))
        return data
    except gdb.error:
        pass
    
    x = Fr(name + ".x")
    y = Fr(name + ".y")

    data = (x, y)

    return data

def G2(name):
    try:
        gdb.parse_and_eval(name + ".z")
        x = Fq2(name + ".x")
        y = Fq2(name + ".y")
        z = Fq2(name + ".z")
        
        data = coord.to_affine((x, y, z))
        return data
    except gdb.error:
        pass
    
    x = Fq2(name + ".x")
    y = Fq2(name + ".y")

    data = (x, y)

    return data

def IC_Query(name):
    try:
        gdb.parse_and_eval(name + ".buf.ptr.pointer[0].z")
        raise ValueError("Curve in not in Affine Format")
    except gdb.error:
        pass
    
    #TODO: edge case?
    ic_query_0 = G1(name + ".buf.ptr.pointer[0]") #UNSURE
    ic_query_1 = G1(name + ".buf.ptr.pointer[1]")

    data = [ic_query_0, ic_query_1]

    return data

def ArrayFr(name):
    #NOTE: accessing vec<>
    vec = gdb.parse_and_eval(name)
    size = getSize(vec)
    vec_size = getVecSize(vec)

    result = []
    if(vec_size != None):
        for i in range(vec_size):
            fr_result = Fr(name + ".buf.ptr.pointer.pointer[" + str(i) + "]")
            result.append(fr_result)
    elif(size != None):
        for i in range(size):
            fr_result = Fr(name + "[" + str(i) + "]")
            result.append(fr_result)
    else: 
        raise ValueError("No match ArrayFr size")
    
    return result

def ArrayG(name):
    #NOTE: accessing ARC value type
    vec_var = gdb.parse_and_eval(name)
    vec_size = getVecSize(vec_var)
    
    result = []
    for i in range(vec_size):
        if "g1" in str(vec_var): 
            G_tuple = G1(name + ".buf.ptr.pointer.pointer[" + str(i) + "]")
        else: 
            G_tuple = G2(name + ".buf.ptr.pointer.pointer[" + str(i) + "]")
        result.append(G_tuple)

    return result

def getVecSize(var):
    match = re.search(r'Vec\(size=(\d+)\)', str(var))
    if(match == None): return None
    size = int(match.group(1))
    return size

def getSize(var):
    match = re.search(r'\(size=(\d+)\)', str(var))
    if(match == None): return None
    size = int(match.group(1))
    return size

