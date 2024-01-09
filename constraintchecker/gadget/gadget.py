import gadget.gadgetlib1.basic_gadget as gt1
import gadget.gadgetlib2.gadget as gt2

class Gadget1(object):
    def __init__(self):        
        self.disjunction_gadget = gt1.Disjunction_Gadget

        self.conjunction_gadget = gt1.Conjunction_Gadget

        self.comparison_gadget = gt1.Comparison_Gadget

        self.inner_product_gadget = gt1.Inner_Product_Gadget

        self.loose_multiplexing_gadget = gt1.Loose_Multiplexing_Gadget

class Gadget2(object):
    def __init__(self):        
        self.AND_Gadget = gt2.AND_Gadget
    
        self.OR_Gadget = gt2.OR_Gadget

gadget1 = Gadget1()
gadget2 = Gadget2()