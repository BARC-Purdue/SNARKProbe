import subprocess
import os
import shutil
import random
import copy

import fuzzing.utils.fuzzMatrix as mt

from config import *
    
class MutValidMatrix(object):
    def __init__(self):
        """Mutation based fuzzer to output valid matrix
        
        MutValidMatrix -> None"""
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.seeddir = os.path.join(self.abspath, "seed_valid")
        
        self.seedlist = []
        self.seedmatrix = {}
        self.mutlist = []
        self.mutnum = {}
        
        self.setup()
        
    def setup(self):
        """Create seed folder and copy seed files
        
        MutValidMatrix -> None"""
        # Remove and create seed file folder
        if os.path.exists(self.seeddir):
            shutil.rmtree(self.seeddir)
        os.mkdir(self.seeddir)
        
        # Copy source seed file
        for file in os.listdir(SEED_INPUT):
            if file.endswith(".txt"):
                seedname = file.split(".")[0]
                seedpath = os.path.join(SEED_INPUT, file)
                
                shutil.copy(seedpath, self.seeddir)
                self.seedlist.append(seedname)
                self.mutnum[seedname] = 0
                
                self.seedmatrix[seedname] = mt.Matrix(os.path.join(self.seeddir, file))
        
    def get(self):
        """Return a matrix from fuzzer
        
        MutValidMatrix -> Matrix, str"""
        seed = self.seedlist.pop(0)
        self.seedlist.append(seed)
        
        seedmatrix = self.seedmatrix[seed]
        matrix = copy.deepcopy(seedmatrix)
        
        while True:
            # Multiply matrix
            multi1 = random.randint(MULTIPLY_MIN, MULTIPLY_MAX)
            multi2 = random.randint(MULTIPLY_MIN, MULTIPLY_MAX)
            multi3 = multi1 * multi2
            multiply = [multi1, multi2, multi3]
            
            for i in range(len(matrix.r1csmatrix)):
                for j in range(len(matrix.r1csmatrix[0])):
                    for k in range(len(matrix.r1csmatrix[0][0])):
                        matrix.r1csmatrix[i][j][k] *= multiply[i]
            
            if (matrix not in self.mutlist):
                self.mutlist.append(matrix)
                break
        
        fname = "mutation_" + seed + "_valid_" + str(self.mutnum[seed])
        self.mutnum[seed] += 1
        
        return matrix, fname
    
class Mutname(object):
    def __init__(self, seed, num):
        """Use single variable to represent file name
        
        Mutname, str, int -> None"""
        self.seed = seed
        self.num = num
        
    def __str__(self):
        """String representation of Mutname class
        
        Mutname -> str"""
        return "mutation_" + self.seed + "_invalid_" + str(self.num)
    
    def __repr__(self):
        """String representation of Mutname class
        
        Mutname -> str"""
        return str(self)
    
    def filename(self, mutnum):
        """Return file name with correct id count
        
        Mutname, dict -> str"""
        for seedname in mutnum.keys():
            if (seedname == self.seed):
                num = mutnum[seedname]
                mutnum[seedname] += 1
                return "mutation_" + self.seed + "_invalid_" + str(num)
        
        raise KeyError("Seed name " + self.seed + " does not exist in dictionary")

class MutInvalidMatrix(object):
    def __init__(self):
        """Mutation based fuzzer to output invalid matrix
        
        MutInvalidMatrix -> None"""
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.fuzzout = os.path.join(self.abspath, "mutfile")
        self.seeddir = os.path.join(self.abspath, "seed_invalid")
        
        self.seedlist = []
        self.mutlist = []
        
        self.seedcopy = 0
        self.mutnum = {}
        self.total = 10 #HARDCODE
        
        self.setup()
        
    def setup(self):
        """Create seed folder, tmp out folder, and copy seed files
        
        MutInvalidMatrix -> None"""
        # Remove and create fuzzing output file folder
        if os.path.exists(self.fuzzout):
            shutil.rmtree(self.fuzzout)
        os.mkdir(self.fuzzout)
        
        # Remove and create seed file folder
        if os.path.exists(self.seeddir):
            shutil.rmtree(self.seeddir)
        os.mkdir(self.seeddir)
        
        # Copy source seed file
        for file in os.listdir(SEED_INPUT):
            if file.endswith(".txt"):
                seedname = file.split(".")[0]
                seedpath = os.path.join(SEED_INPUT, file)
                
                shutil.copy(seedpath, self.seeddir)
                self.seedlist.append(seedname)
                self.mutnum[seedname] = 0
                
    def mutationFuzz(self, seed_src, total):
        """Run atheris fuzzing to get mutation matrix files
        
        MutInvalidMatrix, str, int -> None"""
        abspath = os.path.dirname(os.path.abspath(__file__))
        argspath = os.path.join(abspath, "args.txt")
        
        f = open(argspath, "w")
        f.write(str(seed_src) + "\n")
        f.write(str(total))
        f.close()
        
        python_version = "python3"
        atherispath = os.path.join(abspath, "atherisMutation.py")
        
        subprocess.call([python_version, atherispath], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        os.system("rm crash-*")
        
    def mutationInvalidMatrix(self):
        """Mutation based fuzzing tool to generate invalid R1CS matrix
        
        MutInvalidMatrix -> None"""
        # Run atheris fuzzing for each seed file
        for seed in self.seedlist:
            seedpath = os.path.join(self.seeddir, seed + ".txt")
        
            self.mutationFuzz(seedpath, self.total)
            
        # Add mutation seed to the list
        for i in range(self.total):
            for seed in self.seedlist:
                mutname = Mutname(seed, i)
                self.mutlist.append(mutname)
                
        # Update seed file as last mutation file
        for seed in self.seedlist:
            src = os.path.join(self.seeddir, seed + ".txt")
            dst = os.path.join(self.seeddir, seed + "_" + str(self.seedcopy) + ".txt")
            
            shutil.copy(src, dst)
            
        self.seedcopy += 1
    
    def get(self):
        """Return a matrix from fuzzer
        
        MutInvalidMatrix -> Matrix, str"""
        if (len(self.mutlist) == 0):
            self.mutationInvalidMatrix()
        
        mutname = self.mutlist.pop(0)
        mutpath = os.path.join(self.fuzzout, str(mutname) + ".txt")
        
        mutmatrix = mt.Matrix(mutpath)
        
        mutnametotal = str(mutname.filename(self.mutnum))
        return mutmatrix, mutnametotal