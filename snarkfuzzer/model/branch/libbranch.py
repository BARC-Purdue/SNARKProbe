from config import *

class Condition(object):
    def __init__(self, cid, start, end, fid, important, path):
        self.cid = int(cid)
        self.start = int(start)
        self.end = int(end)
        self.fid = int(fid)
        self.important = important == "IMPORTANT"
        self.path = path
        
        self.interval = []
        
    def __eq__(self, other):
        return type(self) == type(other) and self.cid == other.cid
    
    def __str__(self):
        return "Condition({}, {}, {}, {}, {})".format(self.cid, \
                                                      self.path, \
                                                      self.start, \
                                                      self.end, \
                                                      self.fid)
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        string = "Condition({}, {}, {}, {}, {})".format(self.cid, \
                                                        self.path, \
                                                        self.start, \
                                                        self.end, \
                                                        self.fid)
        return hash(string)
    
    def assigninterval(self, interval):
        self.interval = interval
    
class ConditionList(object):
    def __init__(self):
        self.conddict = {}
        self.condlist = []
    
    def __str__(self):
        return str(self.condlist)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        return iter(self.condlist)
        
    def append(self, cond : Condition):
        self.conddict[cond.cid] = cond
        self.condlist.append(cond)
        
    def getcond(self, cid):
        return self.conddict[cid]

class Return(object):
    def __init__(self, rid, start, end, fid, important, path):
        self.rid = int(rid)
        self.start = int(start)
        self.end = int(end)
        self.fid = int(fid)
        self.important = important == "IMPORTANT"
        self.path = path
        
    def __eq__(self, other):
        return type(self) == type(other) and self.rid == other.rid
    
    def __str__(self):
        return "Return({}, {}, {}, {}, {})".format(self.rid, \
                                                   self.path, \
                                                   self.start, \
                                                   self.end, \
                                                   self.fid)
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        string = "Return({}, {}, {}, {}, {})".format(self.rid, \
                                                     self.path, \
                                                     self.start, \
                                                     self.end, \
                                                     self.fid)
        return hash(string)
    
class ReturnList(object):
    def __init__(self):
        self.retndict = {}
        self.retnlist = []
    
    def __str__(self):
        return str(self.retnlist)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        return iter(self.retnlist)
        
    def append(self, retn : Return):
        self.retndict[retn.rid] = retn
        self.retnlist.append(retn)
        
    def getretn(self, rid):
        return self.retndict[rid]

class Function(object):
    def __init__(self, fid, start, end, fname, important, path):
        self.fid = int(fid)
        self.start = int(start)
        self.end = int(end)
        self.fname = fname
        self.important = important == "IMPORTANT"
        self.path = path
        
        self.condlist = ConditionList()
        self.retnlist = ReturnList()
        
        self.interval = [self.start]
        
    def __eq__(self, other):
        return type(self) == type(other) and self.fid == other.fid
    
    def __str__(self):
        return "Function({}, {}, {}, {}, {})".format(self.fid, \
                                                     self.path, \
                                                     self.start, \
                                                     self.end, \
                                                     self.fname)
    
    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        string = "Function({}, {}, {}, {}, {})".format(self.fid, \
                                                       self.path, \
                                                       self.start, \
                                                       self.end, \
                                                       self.fname)
        return hash(string)
    
    def addcond(self, cond : Condition):
        cond.interval = self.interval
        self.condlist.append(cond)
        self.interval.append(cond.start)
        self.interval.sort()
    
    def addretn(self, retn : Return):
        self.retnlist.append(retn)
    
class FunctionList(object):
    def __init__(self):
        self.funcdict = {}
        self.funclist = []
        
    def __iter__(self):
        pass
    
    def __str__(self):
        return str(self.funclist)
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        return iter(self.funclist)
        
    def append(self, func: Function):
        self.funcdict[func.fid] = func
        self.funclist.append(func)
        
    def getfunc(self, fid):
        return self.funcdict[fid]

class LibBranch(object):
    def __init__(self):
        self.funclist = FunctionList()
        self.pathlist = []

        self.mixlist = []
        
    def readScheme(self):
        f = open(SCHEME_BRANCH_PATH)
        content = f.readlines()
        f.close()
        
        for line in content[2:]:
            line = line.strip("\n")
            
            if (line.startswith("Relative Path: ")):
                path = line.split(": ")[1]
                self.pathlist.append(path)
                
            elif (line.upper().startswith("FUNCTION")):
                _, fid, start, end, fname, important = line.split(",")
                func = Function(fid, start, end, fname, important, path)
                self.funclist.append(func)
            
            elif (line.upper().startswith("CONDITION")):
                _, cid, start, end, fid, important = line.split(",")
                cond = Condition(cid, start, end, fid, important, path)
                
                func = self.funclist.getfunc(cond.fid)
                func.addcond(cond)
                
            elif (line.upper().startswith("RETURN")):
                _, rid, start, end, fid, important = line.split(",")
                retn = Return(rid, start, end, fid, important, path)
                
                func = self.funclist.getfunc(retn.fid)
                func.addretn(retn)
        
        self.pathlist.sort()

        # build mix list 
        for func in self.funclist:
            self.mixlist.append(func)

            for cond in func.condlist:
                self.mixlist.append(cond)
            
            for retn in func.retnlist:
                self.mixlist.append(retn)