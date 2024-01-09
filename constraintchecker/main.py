import sys
import z3

import extractor.libsnark.r1csGenerator as g
import solver.snarkSolver as smt

from gadget.gadget import *
from config import *

def extractR1CS(source):
    """Run the extraction model to get the R1CS constraint variable
    
    None -> None"""
    if (LIBRARY_CHOICE.lower() == "libsnark"):
        cprint.info("Extract R1CS matrix with " + LIBRARY_CHOICE.upper() + " library from " + source)
        
        r1cse = g.R1CSGenerator(source)
        r1cse.gdbScript()
        r1cse.translate()
    else:
        cprint.error("Does not support zk-SNARKs library: " + LIBRARY_CHOICE)
        raise KeyError("Does not support zk-SNARKs library: " + LIBRARY_CHOICE)


class FunctionComparison(object):
    def __init__(self, source = None):
        """Main function and class to compare two functions with SMT solver
        
        FunctionComparison -> None"""
        # Check python version
        if (sys.version_info.major != 3):
            cprint.error("This tool only supports Python 3.x version")
            raise SystemError("This tool only supports Python 3.x version")
        
        if (sys.version_info.minor < 8):
            cprint.warning("Python versions earlier than 3.8.x have not been tested; bugs may exist")
        
        if (EXTRACTION):
            if (source == None):
                cprint.warning("Did not provide the path of binary file to extract R1CS constraint")
                raise ValueError("Did not provide the path of binary file to extract R1CS constraint")
            extractR1CS(source)
        else:
            cprint.warning("Did not execute extraction model; user should provde R1CS matrix")
        
        self.s = smt.SNARKSolver()
        
    def allocate(self, allocatelst):
        """Add allocate list to the solver
        
        FunctionComparison, list -> None"""
        self.s.addAllocate(allocatelst)
        
    def set_input_sizes(self, size):
        """Set input size in the solver
        
        FunctionComparison, int -> None"""
        self.s.set_input_sizes(size)
        
    def addVariables(self, variables):
        """Add public and private variables to the solver
        
        FunctionComparison, list, list -> None"""
        self.s.addVariables(variables)
        
    def addStatement(self, statement):
        """Add statement to the solver
        
        FunctionComparison, list -> None"""
        self.s.addStatement(statement)
        
    def addGadget(self, gadget):
        """Add gadget rule to the solver
        
        FunctionComparison, str -> None"""
        self.s.addGadget(gadget)

    def addRange(self, var, range):
        """Add range for statement variables
        
        FunctionComparison, z3.z3.ArithRef, z3.z3.BoolRef -> None"""
        self.s.addRange(var, range)
        
    def runComparisonTests(self):
        """Use SMT solver to compare two functions
        
        FunctionComparison -> None"""    
        # Run the function comparison check
        match = self.s.matchComparison()
        
        # Run the doamin comparison check
        domain = self.s.domainComparison()
        
        # Run the extra doamin comparison check
        if (DOMAIN_FUZZING):
            domain2 = self.s.domainFuzzing()
        
        # Test 1 Result - Function Comparison with Public Variables
        if (match[0] == None):
            cprint.testskip("Function Comparison with Public Variables", 1)
        elif (match[0] == z3.unsat):
            cprint.testpass("Function Comparison with Public Variables", 1)
        else:
            cprint.testfail("Function Comparison with Public Variables", 1)
        
        # Test 2 Result - Function Comparison with Boolean Variables
        if (match[1] == z3.unsat):
            cprint.testpass("Function Comparison with Boolean Variables", 2)
        else:
            cprint.testfail("Function Comparison with Boolean Variables", 2)
        
        # Test 3 - Domain Comparison
        if (domain == z3.unsat):
            cprint.testpass("Domain Comparison", 3)
        else:
            cprint.testfail("Domain Comparison", 3)
        
        # Test 4 - Fuzzing Domain Comparison
        if (DOMAIN_FUZZING):
            if (domain2 == z3.sat):
                cprint.testpass("Fuzzing Domain Comparison", 4)
            else:
                cprint.testfail("Fuzzing Domain Comparison", 4)
        else:
            cprint.testskip("Fuzzing Domain Comparison", 4)
 