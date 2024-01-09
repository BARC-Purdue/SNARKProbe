
import os
import math
import shutil

import fuzzing.mfuzzer.generation.genmain as gbf
import fuzzing.mfuzzer.mutation.mutmain as mbf

from config import *

# |--------------------------|----------------|-----------------------------------|------------|
# |       Fuzzing Type       |  Matrix Type   |          Fuzzing Method           | Proportion |
# |--------------------------|----------------|-----------------------------------|------------|
# |                          | Invalid Matrix | Random witness with random matrix |     5%     |
# | Generation-based Fuzzing |----------------|-----------------------------------|------------|
# |                          |  Valid Matrix  | Random witness with solver matrix |    40%     |
# |--------------------------|----------------|-----------------------------------|------------|
# |                          | Invalid Matrix |       Flip value in matrix        |    40%     |
# |  Mutation-based Fuzzing  |----------------|-----------------------------------|------------|
# |                          |  Valid Matrix  |    Multiply matrix and witness    |    15%     |
# |--------------------------|----------------|-----------------------------------|------------|

class Queue(object):
    def __init__(self):
        """Queue list to store available output matrix type
        
        Queue -> None"""
        proportion = [GEN_INVALID, GEN_VALID, MUT_INVALID, MUT_VALID]
        
        proportion[:] = [int(n / math.gcd(*proportion)) for n in proportion]
        
        self.fuzzqueue = []
        self.typename = ["GEN_INVALID", "GEN_VALID", "MUT_INVALID", "MUT_VALID"]
        
        while (sum(proportion) != 0):
            for i in range(len(self.typename)):
                if (proportion[i] > 0):
                    self.fuzzqueue.append(self.typename[i])
                    proportion[i] -= 1
        
    def gettype(self):
        """Pop the first item in queue and add to the end of queue
        
        Queue -> str"""
        ftype = self.fuzzqueue[0]
        self.fuzzqueue.append(self.fuzzqueue.pop(0))
        
        return ftype
    
    def __str__(self):
        """Convert Queue as string
        
        Queue -> str"""
        return str(self.fuzzqueue)
    
    def __repr__(self):
        """Convert Queue as string
        
        Queue -> str"""
        return str(self)
        
class MatrixFuzz(object):
    def __init__(self):
        """Matrix fuzzer to output matrix based on the proportion
        
        MatrixFuzz -> None"""
        self.queue = Queue()
        
        self.geninvalid = gbf.GenInvalidMatrix()
        self.genvalid = gbf.GenValidMatrix()
        self.mutinvalid = mbf.MutInvalidMatrix()
        self.mutvalid = mbf.MutValidMatrix()
        
        self.setup()
    
    def setup(self):
        """Clean and create required directory
        
        MatrixFuzz -> None"""
        if (os.path.exists(FUZZING_OUTPUT)):
            shutil.rmtree(FUZZING_OUTPUT)
        os.makedirs(FUZZING_OUTPUT)
        
    def get(self):
        """Output matrix with fuzzer in the queue
        
        MatrixFuzz -> Matrix, str, str"""
        ftype = self.queue.gettype()
        #print('###', ftype)
        
        if (ftype == self.queue.typename[0]):
            # GEN_INVALID
            matrix, fname = self.geninvalid.get()
            ftype = "GEN_INVALID"
            groundtruth = False
        
        elif (ftype == self.queue.typename[1]):
            # GEN_VALID
            matrix, fname = self.genvalid.get()
            ftype = "GEN_VALID"
            groundtruth = True
        
        elif (ftype == self.queue.typename[2]):
            # MUT_INVALID
            matrix, fname = self.mutinvalid.get()
            ftype = "MUT_INVALID"
            groundtruth = False
        
        elif (ftype == self.queue.typename[3]):
            # MUT_VALID
            matrix, fname = self.mutvalid.get()
            ftype = "MUT_VALID"
            groundtruth = True
        
        writepath = os.path.join(FUZZING_OUTPUT, fname + ".txt")
        matrix.writeToFile(writepath)
        
        #return matrix, fname, ftype, groundtruth
        return fname, groundtruth
