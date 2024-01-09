import fuzzing.snarkfuzz as sfuzz
import model.branch.branchModel as branch
import model.value.valueModel as value
import model.monitor.monitor as monitor
import utils.modelsource as ms

import time


def main():
    sf = sfuzz.SnarkFuzz()
    
    bm = branch.BranchModel()

    while (True):
        print("### Generating a new seed as input ... ###")
        source = sf.get()

        # Branch Model
        # print("### Checking the coverage in branch model ... ###")
        # newbranch = bm.getbranch(source)

        # # Monitor
        # print("### Monitoring the value change after extraing variables ... ###")
        # # mo = monitor.Monitor(source, newbranch)
        # # result = mo.watchvar()
        
        # Value Model
        print("### Evaluating the protocol caculations in value models ... ###")
        vm = value.ValueModel(source)
        vm.varextractor()
        vm.valuecheck()

        # print("Finish All")
        # input(">")
        # # break
    
    f.close()
main()