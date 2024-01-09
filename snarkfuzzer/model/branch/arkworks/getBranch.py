import subprocess
import re
import os

import model.branch.libbranch as lb

from config import *

class ProgBranch(object):
    def __init__(self, libbranch, source):
        self.source = source
        self.libbranch = libbranch

        self.prebptgdb = os.path.join(BRANCH_MODEL_LOG, "prebpt.gdb")
        self.prebptlog = os.path.join(BRANCH_MODEL_LOG, "prebpt.log")
        
        self.structgdb = os.path.join(BRANCH_MODEL_LOG, "struct.gdb")
        self.structlog = os.path.join(BRANCH_MODEL_LOG, "struct.log")

        self.fcrreach = {}
        self.fcrvisit = {}
        
        self.setup()

    def setup(self):
        for file in (self.prebptgdb, self.prebptlog, self.structgdb, self.structlog):
            if (os.path.exists(file)):
                os.remove(file)
        
    def checkbptvalid(self):
        # Create gdb script and set breakpoint to check if breakpoint is available in gdb
        fcrdict = {}
        bid = 1
        
        f = open(self.prebptgdb, "w")
        f.write("set logging redirect on\n")
        f.write("set pagination off\n")
        f.write("set logging overwrite on\n")
        f.write("set logging file " + self.prebptlog + "\n")
        f.write("set breakpoint pending on\n")
        
        for fcr in self.libbranch.mixlist:
            fullpath = os.path.join(LIBRARY_PATH, fcr.path)
            
            command = "break " + fullpath + ":" + str(fcr.start)
            f.write(command + "\n")
            fcrdict[bid] = fcr
            self.fcrreach[fcr] = True
            bid += 1
            
        f.write("set logging on\n")
        f.write("info breakpoint\n")

        f.write("q\n")
        f.close()
        
        exit = subprocess.run(["rust-gdb", "-q", "-x", self.prebptgdb, self.source], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        # Keep valid gdb breakpoint
        f = open(self.prebptlog)
        content = f.readlines()
        f.close()
        
        # Get title index to split other line
        titleline = content[0]
        starti = [0]
        endi = []
        space = False
        for i in range(len(titleline)):
            if (titleline[i] != " " and space):
                space = False
                starti.append(i)
                endi.append(i)
            elif (titleline[i] == " "):
                space = True
        endi.append(-1)
        
        for gdbline in content[1:]:
            num = gdbline[starti[0]:endi[0]].strip("\n ")
            btype = gdbline[starti[1]:endi[1]].strip("\n ")
            disp = gdbline[starti[2]:endi[2]].strip("\n ")
            enb = gdbline[starti[3]:endi[3]].strip("\n ")
            address = gdbline[starti[4]:endi[4]].strip("\n ")
            what = gdbline[starti[5]:endi[5]].strip("\n ")
            
            if (num.isdigit() and address == "<MULTIPLE>"):
                continue
            else:
                bid = int(float(num))
                fcr = fcrdict[bid]
                
                if (address == "<PENDING>"):
                    self.fcrreach[fcr] = False
                    continue
    
                line = int(what.split(":")[-1])
                
                if (type(fcr) == lb.Return):
                    # Check if Return is valid
                    if (fcr.start != line):
                        self.fcrreach[fcr] = False
                
                else:
                    # Check if Function and Condition are valid
                    index = fcr.interval.index(fcr.start)
                    if (index + 1 >= len(fcr.interval)):
                        safeline = fcr.end
                    else:
                        safeline = fcr.interval[index + 1]
                    
                    if (line > safeline):
                        self.fcrreach[fcr] = False

    def findbranch(self):
        # Create gdb script and set breakpoint to find the coverage of branch model
        fcdict = {}
        bid = 1
        
        f = open(self.structgdb, "w")
        f.write("set logging redirect on\n")
        f.write("set pagination off\n")
        f.write("set logging overwrite on\n")
        f.write("set logging file " + self.structlog + "\n")
        f.write("set breakpoint pending on\n")
        
        for fcr in self.fcrreach:
            if (self.fcrreach[fcr]):
                fullpath = os.path.join(LIBRARY_PATH, fcr.path)
                
                # Add breakpoint for function
                command = "break " + fullpath + ":" + str(fcr.start)
                f.write(command + "\n")
                fcdict[bid] = fcr
                bid += 1

                self.fcrvisit[fcr] = False
                    
        f.write("set $_exitcode = -1\n")
        f.write("set logging on\n")
        f.write("run\n")
        f.write("while 1\n")
        f.write("\tif $_exitcode != -1\n")
        f.write("\t\tset logging off\n")
        f.write("\t\tquit\n")
        f.write("\tend\n")
        f.write("\tcontinue\n")
        f.write("end\n")

        f.write("q\n")
        f.close()
        
        exit = subprocess.run(["rust-gdb", "-q", "-x", self.structgdb, self.source], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        # read log
        f = open(self.structlog)
        read = f.read()
        f.close()
        content = read.split("\n\n")
        
        thrbp_patt = re.compile(r'Thread [0-9]+ .+ hit Breakpoint [0-9]+')
        
        for infoline in content:
            if (infoline.startswith("Breakpoint ") or thrbp_patt.search(infoline) != None):
                # pathline = re.findall(r'(\/.*?\.[\w:]+)', infoline)
                pathline = re.findall(r'(\/.*:[0-9]+)', infoline)
                line = int(pathline[0].split(":")[-1])
                
                match = re.search('Breakpoint (\d+)', infoline)
                bid = int(match.group(1))

                self.fcrvisit[fcdict[bid]] = True