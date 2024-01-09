import os
import shutil
import subprocess

#import model.value.watchpoint as wp
import model.value.checker.checker as check
import model.value.extractor.extractor as extract

from config import *

class ValueModel(object):
    def __init__(self, source):
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        self.extractgdb = os.path.join(VALUE_MODEL_LOG, "extract.gdb")

        self.source = source
        
    def varextractor(self):
        input(">>>>")
        extractor = extract.Extractor(self.source)
        input(">>>>")
        extractor.runscript()

    def valuecheck(self):
        # value check
        checker = check.Checker(self.source)
        checker.readScheme()
        checker.readVariables()
        checker.protocol()
