import shutil
import subprocess

import model.branch.libbranch as lb
import model.branch.database as db

from config import *


if (LIBRARY.upper() == "LIBSNARK"):
    import model.branch.libsnark.getBranch as gb
elif (LIBRARY.upper() == "BELLMAN"):
    import model.branch.bellman.getBranch as gb
elif (LIBRARY.upper() == "ARKWORKS"):
    import model.branch.arkworks.getBranch as gb
else:
    raise Exception

class BranchModel(object):
    def __init__(self):
        self.database = db.Database()
        self.libbranch = lb.LibBranch()

        self.setup()

    def setup(self):
        if (os.path.exists(BRANCH_MODEL_LOG)):
            shutil.rmtree(BRANCH_MODEL_LOG)
            
        os.makedirs(BRANCH_MODEL_LOG)

        self.libbranch.readScheme()

        for fcr in self.libbranch.mixlist:
            self.database.add(fcr)
    
    def getbranch(self, source):
        def getonebranch(targetfile):
            bm = gb.ProgBranch(self.libbranch, targetfile)
            
            bm.checkbptvalid()
            bm.findbranch()
            
            newbranch = self.processdata(targetfile, bm.fcrvisit)

            return newbranch

        newbranchlist = {}
        
        # generator file
        newbranch1 = getonebranch(source.generator.path)
        newbranchlist["generator"] = newbranch1

        # prover file
        exit = subprocess.call(["diff", source.prover.path, source.generator.path], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if (exit != 0):
            newbranch2 = getonebranch(source.prover.path)
            newbranchlist["prover"] = newbranch2
        else:
            newbranchlist["prover"] = newbranch1

        # verifier file
        exit1 = subprocess.call(["diff", source.verifier.path, source.generator.path], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        exit2 = subprocess.call(["diff", source.verifier.path, source.prover.path], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        if (exit1 == 0):
            newbranchlist["verifier"] = newbranch1
        elif (exit2 == 0):
            newbranchlist["verifier"] = newbranch2
        else: #if (exit1 != 0 and exit2 != 0):
            newbranch3 = getonebranch(source.verifier.path)
            newbranchlist["verifier"] = newbranch3

        return newbranchlist
    
    def processdata(self, targetfile, fcrvisit):
        self.database.resetstat()

        for fcr in fcrvisit:
            if (fcrvisit[fcr]):
                prog = targetfile.split("/")[-1]
                self.database.addvisit(fcr, prog)
                
        self.database.showstat()

        return self.database.newbranch
                
