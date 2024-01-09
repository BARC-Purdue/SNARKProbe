import os
import subprocess
import shutil

from config import *

class Extractor(object):
    def __init__(self, source):
        self.source = source
        
        if (os.path.exists(VALUE_EXTRACTOR_LOG)):
            shutil.rmtree(VALUE_EXTRACTOR_LOG)
            
        os.makedirs(VALUE_EXTRACTOR_LOG)

        self.setup()

    def setup(self):
        if (RAW_DATA):
            if (os.path.exists(VALUE_DATA_ROOT_PATH)):
                shutil.rmtree(VALUE_DATA_ROOT_PATH)

            os.mkdir(VALUE_DATA_ROOT_PATH)
            os.mkdir(VALUE_DATA_PATH)
            os.mkdir(VALUE_DATA_RAW_PATH)
        else:
            if (os.path.exists(VALUE_DATA_PATH)):
                shutil.rmtree(VALUE_DATA_PATH)

            os.mkdir(VALUE_DATA_PATH)

    def genScheme(self, part, schemepath):
        f = open(SCHEME_VALUE_PATH)
        content = f.readlines()
        f.close()

        f = open(schemepath, "w")
        
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
            
            if (part == varpart):
                f.write(info + "\n")

        f.close()
    
    def runscript(self):
        parts = ["generator", "prover", "verifier"]
        pathlist  = {"generator": self.source.generator.path, "prover": self.source.prover.path, "verifier": self.source.verifier.path}

        for part in parts:
            if (LIBRARY.upper() == "LIBSNARK"):
                extractgdb = os.path.join(VALUE_EXTRACTOR_LOG, "extract_{}.gdb".format(part))
                currscheme = os.path.join(VALUE_EXTRACTOR_LOG, "scheme_{}.txt".format(part))
                transcript = os.path.join(VALUE_EXTRACTOR_LOG, "transcript_{}.log".format(part))

                self.genScheme(part, currscheme)
                
                input(">>>>1")
                f = open(extractgdb, "w")
                f.write("set $part = \"{}\"\n".format(part))
                f.write("set $schemepath = \"{}\"\n".format(currscheme))
                f.write("set $progname = \"{}\"\n".format(self.source.progname))
                f.write("source " + os.path.join(VALUE_MODEL_PATH, "extractor", "libsnark", "extractvar.py"))
                f.close()
                
                subprocess.run(["gdb", "-q", "-x", extractgdb, pathlist[part]])
                #exit = subprocess.run(["gdb", "-q", "-x", extractgdb, pathlist[part]], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

                input(">>>>2")
                gdbscript = exit.stdout.decode("utf-8")

                f = open(transcript, "w")
                f.write(gdbscript)
                f.close()

                exitmode = gdbscript.strip("\n").split("\n")[-1]
                if (exitmode != "exited normally"):
                    raise OSError(exitmode)
            
            elif (LIBRARY.upper() == "BELLMAN"):
                extractgdb = os.path.join(VALUE_EXTRACTOR_LOG, "extract_{}.gdb".format(part))
                currscheme = os.path.join(VALUE_EXTRACTOR_LOG, "scheme_{}.txt".format(part))
                transcript = os.path.join(VALUE_EXTRACTOR_LOG, "transcript_{}.log".format(part))
                paramfile = os.path.join(VALUE_EXTRACTOR_LOG, "paramfile.txt")

                self.genScheme(part, currscheme)
                
                f = open(extractgdb, "w")
                # f.write("file " + pathlist[part] + "\n")
                # f.write("set $part = \"{}\"\n".format(part))
                # f.write("set $schemepath = \"{}\"\n".format(currscheme))
                # f.write("set $progname = \"{}\"\n".format(self.source.progname))
                f.write("source " + os.path.join(VALUE_MODEL_PATH, "extractor", "bellman", "extractvar.py"))
                f.close()

                f = open(paramfile, "w")
                param = {"part": part, "schemepath": currscheme, "progname": self.source.progname}
                f.write(str(param))
                f.close()
                
                #subprocess.run(["rust-gdb", "-q", "-x", extractgdb, pathlist[part]])
                exit = subprocess.run(["rust-gdb", "-q", "-x", extractgdb, pathlist[part]], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

                gdbscript = exit.stdout.decode("utf-8")

                f = open(transcript, "w")
                f.write(gdbscript)
                f.close()

                exitmode = gdbscript.strip("\n").split("\n")[-1]
                if (exitmode != "exited normally"):
                    raise OSError(exitmode)

            elif (LIBRARY.upper() == "ARKWORKS"):
                extractgdb = os.path.join(VALUE_EXTRACTOR_LOG, "extract_{}.gdb".format(part))
                currscheme = os.path.join(VALUE_EXTRACTOR_LOG, "scheme_{}.txt".format(part))
                transcript = os.path.join(VALUE_EXTRACTOR_LOG, "transcript_{}.log".format(part))
                paramfile = os.path.join(VALUE_EXTRACTOR_LOG, "paramfile.txt")

                self.genScheme(part, currscheme)
                
                f = open(extractgdb, "w")
                # f.write("file " + pathlist[part] + "\n")
                # f.write("set $part = \"{}\"\n".format(part))
                # f.write("set $schemepath = \"{}\"\n".format(currscheme))
                # f.write("set $progname = \"{}\"\n".format(self.source.progname))
                f.write("source " + os.path.join(VALUE_MODEL_PATH, "extractor", "arkworks", "extractvar.py"))
                f.close()

                f = open(paramfile, "w")
                param = {"part": part, "schemepath": currscheme, "progname": self.source.progname}
                f.write(str(param))
                f.close()
                
                #subprocess.run(["rust-gdb", "-q", "-x", extractgdb, pathlist[part]])
                exit = subprocess.run(["rust-gdb", "-q", "-x", extractgdb, pathlist[part]], stdout = subprocess.PIPE, stderr = subprocess.PIPE)

                gdbscript = exit.stdout.decode("utf-8")

                f = open(transcript, "w")
                f.write(gdbscript)
                f.close()

                exitmode = gdbscript.strip("\n").split("\n")[-1]
                if (exitmode != "exited normally"):
                    raise OSError(exitmode)
                
            else:
                raise Exception