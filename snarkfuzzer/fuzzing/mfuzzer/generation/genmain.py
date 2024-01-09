import random

import fuzzing.mfuzzer.generation.genValid as gbf
import fuzzing.utils.fuzzMatrix as mt
import fuzzing.utils.random.randnormal as rn
import fuzzing.utils.random.randtriangular as rt

from config import *

class GenValidMatrix(object):
    def __init__(self):
        """Generation based fuzzer to output valid matrix
        
        GenValidMatrix -> None"""
        self.num = 0
        
    def get(self):
        """Return a matrix from fuzzer
        
        GenValidMatrix -> Matrix, str"""
        while (True):
            #num_input = random.randint(NUM_INPUT_MIN, NUM_INPUT_MAX)
            #num_constraint = random.randint(NUM_CONSTRAINT_MIN, NUM_CONSTRAINT_MAX)
            num_input, num_constraint = rt.randomSize(NUM_INPUT_MIN, NUM_INPUT_MAX, NUM_CONSTRAINT_MIN, NUM_CONSTRAINT_MAX)
            num_pubinput = rn.randomInvNormal(0, num_input - 1)

            # Generate random matrix
            randmatrix = gbf.ValidMatrix(num_input, num_constraint, num_pubinput)
            randmatrix.randomWitness()
            randmatrix.matrixVariables()
            randmatrix.solveMatrix()
            
            matrix = randmatrix.returnMatrix()
            correctness = matrix.verify()
            
            if (correctness):
                break
        
        filename = "generation_valid_" + str(self.num)
        #output_dst = os.path.join(FUZZING_OUTPUT, filename + ".txt")
        
        self.num += 1
        
        return matrix, filename

class GenInvalidMatrix(object):
    def __init__(self):
        """Generation based fuzzer to output invalid matrix
        
        GenInvalidMatrix -> None"""
        self.num = 0
        
    def get(self):
        """Return a matrix from fuzzer
        
        GenInvalidMatrix -> Matrix, str"""
        # num_input = random.randint(NUM_INPUT_MIN, NUM_INPUT_MAX)
        # num_constraint = random.randint(NUM_CONSTRAINT_MIN, NUM_CONSTRAINT_MAX)
        num_input, num_constraint = rt.randomSize(NUM_INPUT_MIN, NUM_INPUT_MAX, NUM_CONSTRAINT_MIN, NUM_CONSTRAINT_MAX)
        num_pubinput = rn.randomInvNormal(0, num_input - 1)
        
        while (True):
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
                
            matrix = mt.Matrix(num_input, num_constraint, num_pubinput, witness, A, B, C)
            correctness = matrix.verify()
            
            if (not correctness):
                break
        
        filename = "generation_invalid_" + str(self.num)
        #output_dst = os.path.join(FUZZING_OUTPUT, filename + ".txt")
        
        self.num += 1
        
        return matrix, filename
