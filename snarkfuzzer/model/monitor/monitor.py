import subprocess
import threading
import os
import shutil
import re
import time

from config import *

class Monitor(object):
    def __init__(self, source, newbranch):
        self.abspath = os.path.dirname(os.path.abspath(__file__))

        self.source = source
        self.newbranch = newbranch

        self.paramfile = os.path.join(MONITOR_LOG, "paramfile.txt")
        self.valgrindlog = os.path.join(MONITOR_LOG, "valgrindlog.txt")
        self.gdbscript = os.path.join(MONITOR_LOG, "script.gdb")
        self.logfile = os.path.join(MONITOR_LOG, "monitor_log.txt")
        #self.transcript = os.path.join(MONITOR_LOG, "transcript.txt")

        self.schemevarlist = {"generator":[], "prover":[], "verifier":[]}

        self.setup()

    def setup(self):
        if (os.path.exists(MONITOR_LOG)):
            shutil.rmtree(MONITOR_LOG)

        os.mkdir(MONITOR_LOG)

        self.readScheme()

    def readScheme(self):
        f = open(SCHEME_VALUE_PATH)
        content = f.readlines()
        f.close()
        
        while ("\n" in content):
            content.remove("\n")
            
        for info in content:
            if (info[0] == "#"):
                continue
            
            info = info.split("#")[0].strip("\n ")
            
            if (info.startswith("Generator Variables")):
                varpart = "generator"
                continue
            elif (info.startswith("Prover Variables")):
                varpart = "prover"
                continue
            elif (info.startswith("Verifier Variables")):
                varpart = "verifier"
                continue
            
            _, _, vname, vpath, vline = info.strip("\n").split(",")
            if (vpath in ["GENERATOR", "PROVER", "VERIFIER"]):
                vpath = self.source = getattr(self.source, vpath.lower()).path
                vline = self.source = getattr(self.source, vpath.lower()).line
            vline = int(vline) + 1
            if ("()" in vname):
                continue

            self.schemevarlist[varpart].append((vname, vpath, vline))

        f.close()

    def create_valgrind(self, sourcepath):
        def valgrind():
            exit = subprocess.run(["valgrind", "--vgdb-error=0", "--log-file=" + self.valgrindlog, sourcepath], stdout = subprocess.PIPE)

        t1 = threading.Thread(target = valgrind)
        t1.start()

    def gengdbscript(self):
        f = open(self.gdbscript, "w")
        f.write("source " + os.path.join(self.abspath, "watchgdb.py"))
        f.close()

    def watchonevar(self, param):
        sourcepath, vname, vpath, vline = param
        
        self.create_valgrind(sourcepath)
        self.gengdbscript()

        vardict = {}
        vardict["vname"] = vname
        vardict["vpath"] = vpath
        vardict["vline"] = vline

        f = open(self.paramfile, "w")
        f.write(str(vardict))
        f.close()
        
        if (LIBRARY.upper() == "LIBSNARK"):
            exit = subprocess.run(["gdb", "-q", "-x", self.gdbscript, sourcepath], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        elif (LIBRARY.upper() == "BELLMAN"):
            exit = subprocess.run(["rust-gdb", "-q", "-x", self.gdbscript, sourcepath], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
        result = exit.stdout.decode('utf-8')

        valuechange = result.strip("\n").split("\n")[-1]
        
        return valuechange == "True"

    def watchvar(self):
        result = {"generator":{}, "prover":{}, "verifier":{}}
        
        log_f = open(self.logfile, "w")

        varset = []
        for part in self.schemevarlist.keys():
            if (self.newbranch[part]):
                for varinfo in self.schemevarlist[part]:
                    vname, _, _ = varinfo
                    if (vname in varset):
                        continue
                    varset.append(vname)

                    sourcepath = getattr(self.source, "generator").path

                    param = [sourcepath, *varinfo]
                    
                    start_time = time.time()
                    
                    valuechange = self.watchonevar(param)
                    
                    log_f.write("Watching {} spent {}\n".format(vname, time.time()-start_time))
                    log_f.flush()

                    result[part][vname] = valuechange
            
                    print("Monitor result: {} - {}".format(vname, valuechange))
                    
        log_f.close()            
        return result
