class Disjunction_Gadget(object):
    def __init__(self, inputs = None, output = None):
        self.inputs = inputs
        self.output = output

class Conjunction_Gadget(object):
    def __init__(self, inputs = None, output = None):
        self.inputs = inputs
        self.output = output

class Comparison_Gadget(object):
    def __init__(self, B):
        self.B = B

class Inner_Product_Gadget(object):
    def __init__(self, A = None, B = None, size = None):
        self.A = A
        self.B = B
        self.size = size

class Loose_Multiplexing_Gadget(object):
    def __init__(self):
        pass
