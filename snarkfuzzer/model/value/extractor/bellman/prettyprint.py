import gdb
import os
import subprocess
import re
import sys

sys.path.append(os.getcwd())
from config import *

def Fr(name):
    # print("Fr name: " + name)
    var = gdb.parse_and_eval(name)
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
    # print("\n*************G1*************\n")
    try:
        gdb.parse_and_eval(name + ".z")
        raise ValueError("Curve point does not in Affine Format")
    except gdb.error:
        pass
    
    x = Fr(name + ".x")
    y = Fr(name + ".y")

    data = (x, y)

    return data

def G2(name):
    try:
        gdb.parse_and_eval(name + ".z")
        raise ValueError("Curve in not in Affine Format")
    except gdb.error:
        pass
    
    x = Fq2(name + ".x")
    y = Fq2(name + ".y")

    data = (x, y)

    return data

def IC_Query(name):
    # print("\n*************IC*************\n")
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
    vec_size = getVecSize(vec)

    result = []
    for i in range(vec_size):
        fr_result = Fr(name + ".buf.ptr.pointer[" + str(i) + "].__0")
        result.append(fr_result)
    
    return result

def ArrayArrayFr(name):
    #NOTE: accessing vec<vec<>>
    vec = gdb.parse_and_eval(name)
    vec_size = getVecSize(vec)

    result = []
    for i in range(vec_size):
        vec_name = name + ".buf.ptr.pointer[" + str(i) + "]"
        result.append(ArrayFr(vec_name))
    
    return result

def ArrayG(name):
    #NOTE: accessing ARC value type
    vec_var_name = name + ".ptr.pointer[0].data"
    vec_var = gdb.parse_and_eval(vec_var_name)
    vec_size = getVecSize(vec_var)
    
    result = []
    for i in range(vec_size):
        #TODO: edge case? 
        if "G1" in str(vec_var): 
            G_tuple = G1(vec_var_name + ".buf.ptr.pointer[" + str(i) + "]")
        else: 
            G_tuple = G2(vec_var_name + ".buf.ptr.pointer[" + str(i) + "]")
        result.append(G_tuple)

    return result

def ArrayFq2(name):
    #NOTE: accessing vec<>
    vec = gdb.parse_and_eval(name)
    vec_size = getVecSize(vec)

    result = []
    for i in range(vec_size):
        fq2_result = Fq2(name + ".buf.ptr.pointer[" + str(i) + "].__0")
        result.append(fq2_result)
    
    return result

def getVecSize(var):
    size = re.search(r'Vec\(size=(\d+)\)', str(var)).group(1)
    return int(size)

