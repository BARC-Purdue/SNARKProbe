import subprocess
import os
import shutil
import z3

import utils.fuzzMatrix as mt

from config import *

def mutationFuzz(seed_src, total):
    """Run atheris fuzzing to get mutation matrix files
    
    str, str -> None"""
    abspath = os.path.dirname(os.path.abspath(__file__))
    argspath = os.path.join(abspath, "args.txt")
    
    f = open(argspath, "w")
    f.write(str(seed_src) + "\n")
    f.write(str(total))
    f.close()
    
    python_version = "python3"
    atherispath = os.path.join(abspath, "atherisMutation.py")
    
    subprocess.call([python_version, atherispath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    os.system("rm crash-*")
    
def calwitness(matrix : mt.Matrix, notzero = False):
    """Calculate the valid witness for input matrix
    
    Matrix -> list"""
    s = z3.Solver()
    
    variables = []
    for i in range(matrix.num_variables):
        variables.append(z3.Int("sym_" + str(i)))
    
    for i in range(matrix.num_constraint):
        eqA = z3.IntVal("0")
        eqB = z3.IntVal("0")
        eqC = z3.IntVal("0")
        
        rowA = matrix.r1csmatrix[0][i]
        for j in range(matrix.num_variables):
            eqA += rowA[j] * variables[j]
        
        rowB = matrix.r1csmatrix[1][i]
        for j in range(matrix.num_variables):
            eqB += rowB[j] * variables[j]
            
        rowC = matrix.r1csmatrix[2][i]
        for j in range(matrix.num_variables):
            eqC += rowC[j] * variables[j]
        
        s.add(z3.simplify(eqA) * z3.simplify(eqB) == z3.simplify(eqC))
    
    if (notzero):
        noteq = z3.IntVal("0")
        for var in variables[1:]:
            noteq += var
        s.add(noteq != 0)
        
    #s.add(variables[0] == 1)
    
    check = s.check()
    if(check != z3.sat):
        return []
    
    witness = []
    model = s.model()
    for var in variables:
        num = model[var].as_long()
        witness.append(num)
        
    return witness
    

def mutationValidMatrix(count):
    """Mutation based fuzzing tool to generate valid R1CS matrix
    
    int -> None"""
    abspath = os.path.dirname(os.path.abspath(__file__))
    
    # Remove and create fuzzing output file folder
    tmpout = os.path.join(abspath, "mutfile")
    if os.path.exists(tmpout):
        shutil.rmtree(tmpout)
    os.mkdir(tmpout)
    
    # Run atheris fuzzing for each seed file
    seedfiles = []
    for file in os.listdir(SEED_INPUT):
        if file.endswith(".txt"):
            seedfiles.append(file)
    
    for seed in seedfiles:
        seedpath = os.path.join(SEED_INPUT, seed)
        mutationFuzz(seedpath, count)
    
    # Move invalid matrix file from fuzzing output file folder to fuzzprog
    mutfiles = []
    for file in os.listdir(tmpout):
        if file.endswith(".txt"):
            mutfiles.append(file)
            
    for mfile in mutfiles:
        mfilepath = os.path.join(tmpout, mfile)
        matrix = mt.Matrix(mfilepath)
        
        witness = calwitness(matrix)
        if (len(witness) == 0):
            continue
        matrix.witness = witness
        
        outfile = mfile.replace("_mutation_invalid_", "_mutation_valid_")
        outpath = os.path.join(FUZZING_OUTPUT, outfile)
        matrix.writeToFile(outpath)
    
def mutationInvalidMatrix(count):
    """Mutation based fuzzing tool to generate invalid R1CS matrix
    
    int -> None"""
    abspath = os.path.dirname(os.path.abspath(__file__))
    
    # Remove and create fuzzing output file folder
    tmpout = os.path.join(abspath, "mutfile")
    if os.path.exists(tmpout):
        shutil.rmtree(tmpout)
    os.mkdir(tmpout)
    
    # Run atheris fuzzing for each seed file
    seedfiles = []
    for file in os.listdir(SEED_INPUT):
        if file.endswith(".txt"):
            seedfiles.append(file)
    
    for seed in seedfiles:
        seedpath = os.path.join(SEED_INPUT, seed)
        mutationFuzz(seedpath, count)
    
    # Move invalid matrix file from fuzzing output file folder to fuzzprog
    mutfiles = []
    for file in os.listdir(tmpout):
        if file.endswith(".txt"):
            mutfiles.append(file)
            
    for mfile in mutfiles:
        mfilepath = os.path.join(tmpout, mfile)
        matrix = mt.Matrix(mfilepath)
        
        if (matrix.verify()):
            continue
        
        src = os.path.join(tmpout, mfile)
        dst = os.path.join(FUZZING_OUTPUT, mfile)
        shutil.copy(src, dst)