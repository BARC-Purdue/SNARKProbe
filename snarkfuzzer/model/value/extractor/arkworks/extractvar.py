import os
import importlib.util
import sys
import gdb
import traceback
import ast

sys.path.append(os.getcwd())
from config import *

class Variable(object):
    def __init__(self, pvar, vtype, lvar, file, line, part):
        self.pvar = pvar
        self.vtype = vtype
        self.lvar = lvar
        self.file = file
        self.line = line
        self.part = part
        
    def __str__(self):
        return "Variable({}, {}, {}, {})".format(self.pvar, self.vtype, self.lvar, self.part)
    
    def __repr__(self):
        return str(self)
    
class Extractor(object):
    def __init__(self):
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        #info = gdb.execute("info file", to_string = True)
        #path = info.split("\n")[0].split('"')[1]
        self.progname = "" #str(gdb.parse_and_eval("$progname")).strip("\"")
        
        self.extract = {}
        self.actualbpts = {}
        
        self.pptr = None
        self.param = {}
        
        self.setup()
        
    def setup(self):
        spec = importlib.util.spec_from_file_location("prettyprint", os.path.join(self.abspath, "prettyprint.py"))
        pptr = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pptr)
        self.pptr = pptr

        paramfile = os.path.join(VALUE_EXTRACTOR_LOG, "paramfile.txt")
        f = open(paramfile)
        content = f.read()
        f.close()
        self.param = ast.literal_eval(content)
        
        self.part = self.param["part"] #str(gdb.parse_and_eval("$part")).strip("\"")
        self.progname = self.param["progname"]

        self.refined_output = os.path.join(VALUE_DATA_PATH, self.progname, self.part)
        self.logfile = os.path.join(VALUE_EXTRACTOR_LOG, "extractvar_gdblog.txt")
        os.makedirs(self.refined_output)
        if (RAW_DATA):
            self.raw_output = os.path.join(VALUE_DATA_RAW_PATH, self.progname, self.part)
            os.makedirs(self.raw_output)

        self.gdbsetup()
    
    def gdbsetup(self):
        gdb.execute("set logging file " + self.logfile)
        gdb.execute("set logging overwrite off")
        gdb.execute("set pagination off")
        gdb.execute("set logging off")
        gdb.execute("set logging on")
    
    def readScheme(self):
        schemepath = self.param["schemepath"]

        f = open(schemepath)
        content = f.readlines()
        f.close()
        
        while ("\n" in content):
            content.remove("\n")
            
        for info in content:
            if (info[0] == "#"):
                continue
            
            info = info.split("#")[0].strip("\n ")
        
            pvar, vtype, lvar, file, line = info.split(",")
            if (file in ["GENERATOR", "PROVER", "VERIFIER"]):
                file = self.source = getattr(self.source, file.lower()).path
                line = self.source = getattr(self.source, file.lower()).line
            line = int(line) + 1
            
            if (file not in self.extract):
                self.extract[file] = {}
            if (line not in self.extract[file]):
                self.extract[file][line] = []
                
            var = Variable(pvar, vtype, lvar, file, line, self.part)
            self.extract[file][line].append(var)
    
    def setbreakpoint(self):
        setbpts = {}
        
        for file in self.extract:
            for line in self.extract[file]:
                spec = os.path.join(LIBRARY_PATH, file) + ":" + str(line)
                bpt = gdb.Breakpoint(spec)
                print("here is bpt.number: {}".format(bpt.number))
                setbpts[bpt.number] = self.extract[file][line]
        
        read = gdb.execute("info breakpoint", to_string = True)
        
        info = read.split("\n")
        while "" in info:
           info.remove("")

        titleline = info[0]
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
        
        for gdbline in info[1:]:
            print("current gdbline: {}".format(gdbline))
            num = gdbline[starti[0]:endi[0]].strip("\n ")
            btype = gdbline[starti[1]:endi[1]].strip("\n ")
            disp = gdbline[starti[2]:endi[2]].strip("\n ")
            enb = gdbline[starti[3]:endi[3]].strip("\n ")
            address = gdbline[starti[4]:endi[4]].strip("\n ")
            what = gdbline[starti[5]:].strip("\n ")
            
            pathline = what.split(" at ")[-1]
            
            print("here is num: {}".format(num))
            
            print("here is pathline: {}".format(pathline))
            if (not num.isdigit()): continue # skiping mutliple bps, like 2.1 (only 2 is valid index in setbpts)
            self.actualbpts[pathline] = setbpts[int(num)]

    def collectvars(self):
        gdb.execute("set $_exitcode = -1")
        
        gdb.execute("run")
        
        # read list of variables that require finish command
        if (os.path.exists()):
        needfinish 
        
        while (True):
            exitcode = gdb.parse_and_eval("$_exitcode")
            
            if (int(exitcode) != -1):
                break
            
            read = gdb.execute("where", to_string = True)
            
            info = read.split("\n")[0].split(" at ")[-1]
            
            if (info in self.actualbpts):
                for var in self.actualbpts[info]:
                	# check if need to run finish command
                	
                	#	gdb.execute("finish")
                	
                    # Save refined data
                    func = getattr(self.pptr, var.vtype)
                    refineddata = func(var.lvar)
                    
                    refinedpath = os.path.join(self.refined_output, var.pvar + ".txt")
                    
                    f = open(refinedpath, "w")
                    f.write(var.pvar + "\n")
                    f.write(var.lvar + "\n")
                    f.write(str(refineddata))
                    f.close()

                    # Save raw data
                    if (RAW_DATA):
                        rawpath = os.path.join(self.raw_output, var.pvar + ".txt")

                        rawdata = gdb.parse_and_eval(var.lvar)

                        f = open(rawpath, "w")
                        f.write(var.pvar + "\n")
                        f.write(var.lvar + "\n")
                        f.write(str(rawdata))
                        f.close()

            gdb.execute("continue")
            
            print("***executed in-loop continue")
            
        sys.stdout.write("exited normally")
        gdb.execute("quit")

if __name__ == "__main__":
    try:
        e = Extractor()
        print("***readScheme")
        e.readScheme()
        print("***setbreakpoint")
        e.setbreakpoint()
        print("\n***collectvars")
        e.collectvars()
    except:
        print("***gdb killed")
        gdb.execute("kill")

        ex_type, ex_value, ex_traceback = sys.exc_info()

        trace = traceback.extract_tb(ex_traceback)
        stack_trace = "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[-1][0], trace[-1][1], trace[-1][2], trace[-1][3])

        stdout = "{}: {} at {}".format(ex_type.__name__, ex_value, stack_trace)
        sys.stdout.write(stdout)
        
        gdb.execute("quit")
