import random

import mfuzz.generation.genValid as gbf
import utils.fuzzMatrix as mt

from config import *

def genOneValidMatrix(i):
    """Generation based fuzzing tool to generate valid R1CS matrix
    
    int -> None"""
    while (True):
        num_input = random.randint(NUM_INPUT_MIN, NUM_INPUT_MAX)
        num_constraint = random.randint(NUM_CONSTRAINT_MIN, NUM_CONSTRAINT_MAX)

        # Generate random matrix
        randmatrix = gbf.ValidMatrix(num_input, num_constraint)
        randmatrix.randomWitness()
        randmatrix.matrixVariables()
        randmatrix.solveMatrix()
        correctness = randmatrix.verify()
        
        if (correctness):
            break

    matrix = randmatrix.returnMatrix()
    
    output_dst = os.path.join(FUZZING_OUTPUT, "generation_valid_" + str(i) + ".txt")
    matrix.writeToFile(output_dst)

def genOneInvalidMatrix(i):
    """Generation based fuzzing tool to generate invalid R1CS matrix
    
    int -> None"""
    num_input = random.randint(NUM_INPUT_MIN, NUM_INPUT_MAX)
    num_constraint = random.randint(NUM_CONSTRAINT_MIN, NUM_CONSTRAINT_MAX)
    
    A = []
    B = []
    C = []

    for _ in range(num_constraint):
        row = []
        for _ in range(num_input):
            num = random.randint(RANDOM_WITNESS_MIN, RANDOM_WITNESS_MAX)
            row.append(num)
        
        A.append(row)
        
    for _ in range(num_constraint):
        row = []
        for _ in range(num_input):
            num = random.randint(RANDOM_WITNESS_MIN, RANDOM_WITNESS_MAX)
            row.append(num)
        
        B.append(row)
        
    for _ in range(num_constraint):
        row = []
        for _ in range(num_input):
            num = random.randint(RANDOM_WITNESS_MIN, RANDOM_WITNESS_MAX)
            row.append(num)
        
        C.append(row)
        
    witness = []
    for _ in range(num_input):
        num = random.randint(RANDOM_WITNESS_MIN, RANDOM_WITNESS_MAX)
        witness.append(num)
        
    matrix = mt.Matrix(num_input, num_constraint, witness, A, B, C)
    
    output_dst = os.path.join(FUZZING_OUTPUT, "generation_invalid_" + str(i) + ".txt")
    matrix.writeToFile(output_dst)

def generationValidMatrix(count):
    """Generation based fuzzing tool to generate multiple valid R1CS matrix
    
    int -> None"""
    for i in range(count):
        genOneValidMatrix(i)

def generationInvalidMatrix(count):
    """Generation based fuzzing tool to generate multiple invalid R1CS matrix
    
    int -> None"""
    for i in range(count):
        genOneInvalidMatrix(i)