import solver.r1csRelation as rr
import gadget.gadget as gt

from config import *

class GadgetRelation(object):
    def __init__(self):
        self.equations = []

    def addGadget(self, gadget, r1csrelation: rr.R1CSRelation):
        """Create the special gadget rule equation
        
        GadgetRelation, str, R1csRelation -> None"""        
        rr = r1csrelation
        
        if (isinstance(gadget, gt.gadget1.disjunction_gadget)):
            cprint.info("R1CS is formatted by disjunction gadget", 1)
            cprint.info("No further action is required for disjunction gadget", 2)
        
        elif (isinstance(gadget, gt.gadget1.conjunction_gadget)):
            cprint.info("R1CS is formatted by conjunction gadget", 1)
            cprint.info("No further action is required for conjunction gadget", 2)
        
        elif (isinstance(gadget, gt.gadget1.comparison_gadget)):
            cprint.info("R1CS is formatted by comparison gadget", 1)
            cprint.info("Set variable " + gadget.B + " as maximum value", 2)
            index = r1csrelation.allocate.index(gadget.B)
            
            equation = rr.private_var[index] == rr.private_value[index]
            if (equation not in self.equations):
                self.equations.append(equation)
        
        elif (isinstance(gadget, gt.gadget1.inner_product_gadget)):
            cprint.info("R1CS is formatted by inner product gadget", 1)
            cprint.info("No further action is required for inner product gadget", 2)
            
        elif (isinstance(gadget, gt.gadget1.loose_multiplexing_gadget)):
            cprint.warning("Loose multiplexing gadget has not been tested yet; error may exist", 1)
            pass
        
        elif (isinstance(gadget, gt.gadget2.AND_Gadget)):
            cprint.info("R1CS is formatted by AND gadget", 1)
            cprint.info("No further action is required for AND gadget", 2)
            
        elif (isinstance(gadget, gt.gadget2.OR_Gadget)):
            cprint.info("R1CS is formatted by OR gadget", 1)
            cprint.info("No further action is required for OR gadget", 2)
        
        else:
            cprint.info("Does not support gadget " + str(type(gadget)), 1)
            raise ValueError("Does not support gadget " + str(type(gadget)))
            
    def __bool__(self):
        """return bool result of class (if there is extra relation in gadget)
        
        GadgetRelation -> bool"""
        return len(self.equations) != 0

