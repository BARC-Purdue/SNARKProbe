
import os
import ast
import subprocess

import model.value.checker.convertecc as convert

from config import *

if (PROTOCOL.upper() == "PGHR13"):
    import model.value.checker.pghr13.generator as ge
    import model.value.checker.pghr13.prover as pr
    import model.value.checker.pghr13.verifier as ve
elif (PROTOCOL.upper() == "GROTH16"):
    import model.value.checker.groth16.generator as ge
    import model.value.checker.groth16.prover as pr
    import model.value.checker.groth16.verifier as ve

class Variables(object):
    def __init__(self):
        self.variables = {}
        self.vartype = {}

class Checker(object):
    def __init__(self, source):
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.source = source
        
        self.variableset = {"generator": Variables(), "prover": Variables(), "verifier": Variables()}
        
    def readScheme(self):
        f = open(SCHEME_VALUE_PATH)
        content = f.readlines()
        f.close()
        
        while ("\n" in content):
            content.remove("\n")
            
        for info in content:
            if (info[0] == "#"):
                continue
            
            info = info.split("#")[0].strip("\n ")
            
            if (info.startswith("Generator Variables")):
                part = "generator"
                continue
            elif (info.startswith("Prover Variables")):
                part = "prover"
                continue
            elif (info.startswith("Verifier Variables")):
                part = "verifier"
                continue
            
            pvar, vtype, _, _, _ = info.split(",")
            
            self.variableset[part].variables[pvar] = None
            self.variableset[part].vartype[pvar] = vtype
    
    def readVariables(self):
        for part in self.variableset:
            for var in self.variableset[part].variables:
                path = os.path.join(VALUE_DATA_PATH, self.source.progname, part)
                
                file = os.path.join(path, var + ".txt")
                f = open(file)
                content = f.readlines()
                f.close()
                
                prevalue = ast.literal_eval(content[2].strip("\n"))
                
                if (self.variableset[part].vartype[var] == "Int"):
                    value = prevalue
                else:
                    value = convert.varConvert(prevalue)
                
                #self.variableset[part][var] = value
                self.variableset[part].variables[var] = value
        
    def protocol(self):
        # # generator
        # generator = ge.Generator(self.source, self.variableset)
        # generator.protocol()
        
        # prover
        prover = pr.Prover(self.source, self.variableset)
        prover.protocol()
        
        # # verifier
        verifier = ve.Verifier(self.source, self.variableset)
        verifier.protocol()
