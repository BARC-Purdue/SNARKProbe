import os
import subprocess
import zlib

import extractor.libsnark.extractorConfig as config

from config import *

class GetLine(object):
    def __init__(self, src):
        """GetLine, str -> None"""
        self.abspath = os.path.dirname(os.path.abspath(__file__))
        
        self.src = src
        self.gdbfile = config.GETLINE_GDB

        self.line = -1

        self.clear()

    def clear(self):
        """Remove file generated by this class
        
        GetLine -> None"""
        if (os.path.exists(self.gdbfile)):
            os.remove(self.gdbfile)

    def gdbscript(self):
        """Generate GDB script to find the breakpoint line number by using gdb python library
        
        GetLine -> None"""
        compress = b'x\x9cm\x90\xc1N\xc30\x0c\x86\xef~\n+\xa7\x94\xb5\xd5vE\xe2\x158q\xeb&\xd4\xaen\xb1H\x9d\x92\xb8b\xbc=I\xb72\x81\xf0%\x8e\xf3\xf9w\xfc\xcf_\xfa\xe6\x05x\x9a}P\x1c\xfbnK\x03m\x99\x8f\x00=\xc76\xe2S\x06j\xba\xd0yQ\xb2f-F\x9a:G8\xb5,\xa6D\xf5\xafQ\x03\xcb\x98\xd8\x97\xb0P\x01g/J\xa2\xb9y\xe5\xeb\xfc>[s\x14S\xd4qv\xac\xd7\x1c\xa0\xed\xfb@1\x83\xcf^\x08\x06\x1f\x90\x91\x05C+#YGb7\xad\x02+<\x94\xb8/\xb1:\x14\x8f\x80)\x1c\x0b\xa5\xce\x8dh\xf8\xb4\x96y@k\x02\xa9\xc9B\x99\xb9\xe19\xee\xf3\x02\xd5\x03K\xdf:g\xcd\xfer\xfc\xdc\xa5MV\xb8\xd9\x9f~\xf0.P\xfb\x0e\xb0\x1e\x91\xf4\xaf\x19\x1d>\x18\xdcm\xa2\xff9\x91\x15e\x99\xd2\x9dE\xed\xa6s\xf7\xa3\xbe\x1b\x82\xa6h\xaa\xc3i\xdd\x13\xe0\xb7\xe9\xe4H\xe9\xfa\x9b\xec\xda\x1c\xb2\xdaM\xbbD\x92>\r0\xf9%\xa5\xf0\xb1\xb0~\x03\xb8\xf6\x97]'
        script = zlib.decompress(compress).decode("utf-8")
        
        f = open(self.gdbfile, "w")
        f.write(script)
        f.close()

    def runscript(self):
        """Run the GDB script
        
        GetLine -> int"""
        exit = subprocess.run(["gdb", "-batch", "-x", self.gdbfile, self.src], stdout = subprocess.PIPE)
        
        self.line = int(exit.stdout)

        return exit

    def getline(self):
        """Return the line number variable
        
        GetLine -> int"""
        return self.line

## if __name__ == "__main__":
##     # test case
##     src = "PATH"
## 
##     gl = GetLine(src)
##     gl.gdbscript()
##     gl.runscript()
##     line = gl.getline()
## 
##     print(line)