import subprocess
import os
import shutil

import mfuzz.matrixFuzzing as fuzz
import genprog.libsnarkProg as prog

from config import *


def runFuzzing():
    if os.path.exists(FUZZING_OUTPUT):
        shutil.rmtree(FUZZING_OUTPUT)
    os.mkdir(FUZZING_OUTPUT)

    fuzz.generationValidMatrix()
    #fuzz.generationInvalidMatrix()

    #fuzz.mutationValidMatrix()
    fuzz.mutationInvalidMatrix()


class CompileProg(object):
    def __init__(self):
        self.progfeatures = [prog.ProgFeature("PGHR13", "STRONG_IC"), \
                             prog.ProgFeature("PGHR13", "WEAK_IC"), \
                             prog.ProgFeature("GROTH16", "STRONG_IC"), \
                             prog.ProgFeature("GROTH16", "WEAK_IC")]
        self.filetxt = []
        self.filecpp = []
        self.filebinary = []
        
        for file in os.listdir(FUZZING_OUTPUT):
            if file.endswith(".txt"):
                self.filetxt.append(file)
        self.filetxt.sort()
        
        self.setup()
        
    def setup(self):
        srcpath = os.path.join(COMPILE_PATH, "src")
        shutil.rmtree(srcpath)
        os.mkdir(srcpath)
    
    def genSnarkProg(self):
        # Generate cpp file to src
        for file in self.filetxt:
            filepath = os.path.join(FUZZING_OUTPUT, file)
            
            for feature in self.progfeatures:
                name, _ = file.split(".")
                fname = name + "_" + str(feature)
                cpppath = os.path.join(COMPILE_PATH, "src", fname + ".cpp")
                
                pg = prog.ProGenerator(filepath, feature)
                pg.readMatrixFromFile()
                pg.setvariables()
                pg.getRelation()
                pg.generateProg(cpppath)
                
                self.filecpp.append(fname + ".cpp")
                self.filebinary.append(fname)
        
    def genCMakeLists(self):
        # Create CMakeLists
        make = prog.CMakeLists(self.filecpp, self.filebinary)
        make.buildmakefile()
        
    def compileAll(self):
        buildpath = os.path.join(COMPILE_PATH, "build")
        
        subprocess.run(["make", ".."], cwd = buildpath)

def main():
    runFuzzing()
    cp = CompileProg()
    cp.genSnarkProg()
    cp.genCMakeLists()
    cp.compileAll()
    
main()