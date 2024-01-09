import os
import sys
import inspect
import z3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import *
from main import *

def main():
    x = z3.Int("x")

    allocate = ["x", "max"]
    variables = [x, None]
    
    statement = [x % MOD < 60]
    
    path = os.path.join(currentdir, "range")
    
    fcmp = FunctionComparison(path)
    
    fcmp.allocate(allocate)
    fcmp.set_input_sizes(0)
    fcmp.addVariables(variables)
    fcmp.addStatement(statement)
    fcmp.addGadget(gadget1.comparison_gadget("max"))
    fcmp.addRange(x, z3.And(x < 60))

    fcmp.runComparisonTests()
    
if __name__ == "__main__":
    main()
    
    
