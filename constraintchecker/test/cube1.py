import os
import sys
import inspect
import z3

# import FunctionComparison model from main.py file
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from config import *
from main import *

def main():
    x = z3.Int("x")
    out = z3.Int("out")

    statement = [(z3.ToInt(x**3) + x + 5) % MOD == out]
    
    allocate = ["out", "sym_1", "y", "sym_2", "x"]
    variables = [out, x, None, None, None]
    
    path = os.path.join(currentdir, "cube1")
    
    fcmp = FunctionComparison(path)
    
    fcmp.allocate(allocate)
    fcmp.set_input_sizes(1)
    
    fcmp.addVariables(variables)
    fcmp.addStatement(statement)
    
    fcmp.runComparisonTests()
    
if __name__ == "__main__":
    main()
