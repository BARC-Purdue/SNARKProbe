import subprocess
import os
import shutil

import fuzzing.mfuzzer.matrixFuzzing as fuzz
import fuzzing.utils.utils as ut
import fuzzing.genprog.genProg as prog
import utils.modelsource as ms

from config import *

class SnarkFuzz(object):
    def __init__(self):
        """Snark fuzzer to output zk-SNARKs library program
        
        SnarkFuzz -> None"""
        self.setup()
        
        self.fuzzer = fuzz.MatrixFuzz()
        
    def setup(self):
        """Create required directories and log file
        
        SnarkFuzz -> None"""
        if (os.path.exists(DIR_OUTPUT)):
            shutil.rmtree(DIR_OUTPUT)
            
        os.makedirs(PROG_OUTPUT)
        os.makedirs(BINARY_OUTPUT)

    def get(self):
        """Output zk-SNARKs program from snarkFuzzer
        
        SnarkFuzz -> str"""
        name, groundtruth = self.fuzzer.get()

        pg = prog.ProGenerator(name)
        pg.readMatrixFromFile()
        pg.setvariables()
        pg.getRelation()
        fileparams = pg.generateProg()

        source = ms.ModelSource(*fileparams, name, groundtruth)
        
        return source