import z3
import multiprocessing
import time

import solver.z3Solver as z3p
from config import *

def get_vars(f):
    r = set()

    def collect(f):
      if z3.is_const(f): 
          if f.decl().kind() == z3.Z3_OP_UNINTERPRETED and not f in r:
              r.add(f)
      else:
          for c in f.children():
              collect(c)
    collect(f)

    return list(r)

def timeSolver(s):
    def checkfunc():
        check = s.check()
        if (check == z3.sat):
            ret_value.value = 1
        elif (check == z3.unsat):
            ret_value.value = 0
        elif (check == z3.unknown):
            ret_value.value = -1
     
    ret_value = multiprocessing.Value("i", -1, lock = False)
    p = multiprocessing.Process(target = checkfunc, name = "checkfunc", args = ())
    p.start()

    time.sleep(OPT_TIME)
    p.terminate()

    return ret_value.value 
    
def opteq1(equation):
    OPT_VAR_1 = z3.Int("OPT_VAR_1")
    EQ1 = (OPT_VAR_1 * (1 + (MOD - 1) * OPT_VAR_1)) % MOD == 0

    variables = get_vars(equation)

    if (len(variables) != 1):
        return False, None, None
    
    var = variables[0]

    s = z3p.Solver()
    
    b1 = z3.Bool("b1")
    b2 = z3.Bool("b2")

    s.add(b1 == EQ1)
    s.add(b2 == equation)
    s.add(var == OPT_VAR_1)
    s.add(b1 != b2)

    check = timeSolver(s)

    if (check == 0):
        return True, var, z3.And(var >= 0, var <= 1)
    else:
        return False, None, None
   
def optrange(equation):
    # Comparing EQ1 (gadget auxiliary variable where equal to 0 or 1)
    check, var, range = opteq1(equation)
    if (check):
        return check, var, range

    # Future optimization

    return False, None, None

def reverseRange(rangelst, tolist = True):
    """Return the reserve of range e.g. Not(range)
    
    dict[, bool] -> list"""
    reserselist = []
    reversedict = {}

    for var in rangelst:
        reserselist.append(z3.Not(rangelst[var]))
        reversedict[var] = z3.Not(rangelst[var])

    if (tolist):
        return reserselist
    else:
        return reversedict
    
def optmaxbound(var, args):#r1csrelation, r1csvarrange, gadgetrelation):
    s = z3p.Solver()
    s.add(*args)
    s.add(var == 0)
    check_min = timeSolver(s)
    
    s = z3p.Solver()
    s.add(*args)
    s.add(var == MOD - 1)
    check_max = timeSolver(s)

    return check_min == 1 and check_max == 1
 
# def opteq2(equation):
#     OPT_VAR_1 = z3.Int("OPT_VAR_1")
#     OPT_VAR_2 = z3.Int("OPT_VAR_2")
#     OPT_VAR_3 = z3.Int("OPT_VAR_3")
#     OPT_VAR_4 = z3.Int("OPT_VAR_4")
#     EQ1 = (OPT_VAR_1 * OPT_VAR_2) % MOD == ((MOD - 1) * OPT_VAR_3 + OPT_VAR_4) % MOD

#     variables = get_vars(equation)

#     if (len(variables) != 4):
#         return False
    
#     var1, var2, var3, var4 = variables

#     s = z3p.Solver()
    
#     b1 = z3.Bool("b1")
#     b2 = z3.Bool("b2")

#     s.add(b1 == EQ1)
#     s.add(b2 == equation)
#     s.add(var1 == OPT_VAR_1)
#     s.add(var2 == OPT_VAR_2)
#     s.add(var3 == OPT_VAR_3)
#     s.add(var4 == OPT_VAR_4)
#     s.add(b1 != b2)

#     check = timeSolver(s)

#     if (check == 0):
#         return True
#     else:
#         return False

# def optconstraint(equation):
#     # Comparing EQ2
#     check = opteq2(equation)
    
#     if (check):
#         neweq = ""
#         if (str(equation.children()[0].children()[0].decl()) == "+"):
#             pass
#         elif (str(equation.children()[1].children()[0].decl()) == "+"):
#             se = equation.children()[1].children()[0]
            
#             if (se.children()[0].num_args() == 0):
#                 var1 = z3.simplify(se.children()[1]/(MOD-1))
#                 var2 = se.children()[0]
#             elif (se.children()[1].num_args() == 0):
#                 var1 = z3.simplify(se.children()[0]/(MOD-1))
#                 var2 = se.children()[1]
                
#             return True, equation.children()[0] == (var2 - var1) % MOD
    
#     return False, None
