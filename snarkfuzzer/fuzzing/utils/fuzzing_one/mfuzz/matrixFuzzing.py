
import os

import mfuzz.generation.genmain as gbf
import mfuzz.mutation.mutmain as mbf

from config import *

# |--------------------------|------------------|-----------------------------------|
# |       Fuzzing Type       |   Matrix Type    |          Fuzzing Method           |
# |--------------------------|------------------|-----------------------------------|
# |                          | Non-valid Matrix | Random witness with random matrix |
# | Generation-based Fuzzing |------------------|-----------------------------------|
# |                          |   Valid Matrix   | Random witness with solver matrix |
# |--------------------------|------------------|-----------------------------------|
# |                          |                  |       Flip value in witness       |
# |                          | Non-valid Matrix |-----------------------------------|
# |                          |                  |       Flip value in matrix        |
# |  Mutation-based Fuzzing  |------------------|-----------------------------------|
# |                          |                  |  Flip witness with solver matrix  |
# |                          |   Valid Matrix   |-----------------------------------|
# |                          |                  |  Flip matrix with solver witness  |
# |--------------------------|------------------|-----------------------------------|

def generationValidMatrix():
    count = 20
    
    gbf.generationValidMatrix(count)

def generationInvalidMatrix():
    count = 5
    
    gbf.generationInvalidMatrix(count)

def mutationValidMatrix():
    count = 5
    
    mbf.mutationValidMatrix(count)
    
def mutationInvalidMatrix():
    count = 5
    
    mbf.mutationInvalidMatrix(count)
    

