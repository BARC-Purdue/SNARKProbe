import logging
import datetime

from config import *

class bcolors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    INFO = '\033[94m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class PrintColor(object):
    def __init__(self, file = None):
        """Create PrintColor class to print colored log
        
        PrintColor, str -> None"""
        self.file = file
        if (file != None):
            f = open(file, "w")
            f.close()
    
    def write(self, key, msg):
        """Write printing log to the log file
        
        PrintColor, str, str -> None"""
        if (self.file != None):
            f = open(self.file, "a")
            f.write(key + msg + "\n")
            f.close()
    
    def info(self, msg, level = 0):
        """Print info logging

        PrintColor, str[, int] -> None"""
        dot = "." * 4 * level
        print(f"{bcolors.INFO}" + "[INFO]    " + dot + msg + f"{bcolors.ENDC}")
        self.write("[INFO]    " + dot, msg)
    
    def warning(self, msg, level = 0):
        """Print warning logging

        PrintColor, str[, int] -> None"""
        dot = "." * 4 * level
        print(f"{bcolors.WARNING}" + "[WARNING] " + dot + msg + f"{bcolors.ENDC}")
        self.write("[WARNING] " + dot, msg)
    
    def error(self, msg, level = 0):
        """Print error logging

        PrintColor, str[, int] -> None"""
        dot = "." * 4 * level
        print(f"{bcolors.ERROR}" + "[ERROR]   " + dot + msg + f"{bcolors.ENDC}")
        self.write("[ERROR]   " + dot, msg)
    
    def white(self, msg, level = 0):
        """Print white logging

        PrintColor, str[, int] -> None"""
        dot = "." * 4 * level
        print(f"{bcolors.ENDC}" + "          " + dot + msg + f"{bcolors.ENDC}")
        self.write("          " + dot, msg)
        
    def testpass(self, msg, i):
        """Print test case is pass

        PrintColor, str, int -> None"""
        print(f"{bcolors.OKGREEN}" + "TEST " + str(i) + " PASS: " + msg + f"{bcolors.ENDC}")
        self.write("TEST " + str(i) + " PASS: ", msg)
    
    def testfail(self, msg, i):
        """Print test case is fail

        PrintColor, str, int -> None"""
        print(f"{bcolors.ERROR}" + "TEST " + str(i) + " FAIL: " + msg + f"{bcolors.ENDC}")
        self.write("TEST " + str(i) + " FAIL: ", msg)
    
    def testskip(self, msg, i):
        """Print test case is skipped

        PrintColor, str, int -> None"""
        print(f"{bcolors.WARNING}" + "TEST " + str(i) + " SKIP: " + msg + f"{bcolors.ENDC}")
        self.write("TEST " + str(i) + " FAIL: ", msg)

class LoggingColor(logging.Formatter):
    """Logging colored formatter"""

    GREY = '\x1b[38;21m'
    BLUE = '\x1b[38;5;39m'
    YELLOW = '\x1b[38;5;226m'
    RED = '\x1b[38;5;196m'
    BOLD_RED = '\x1b[31;1m'
    RESET = '\x1b[0m'

    def __init__(self, fmt):
        """Create the logging color

        LoggingColor, str -> None"""
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.GREY + self.fmt + self.RESET,
            logging.INFO: self.BLUE + self.fmt + self.RESET,
            logging.WARNING: self.YELLOW + self.fmt + self.RESET,
            logging.ERROR: self.RED + self.fmt + self.RESET,
            logging.CRITICAL: self.BOLD_RED + self.fmt + self.RESET
        }

    def format(self, record):
        """Create and return the logging format

        LoggingColor, logging.LogRecord -> str"""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        
        return formatter.format(record)

class Log(object):
    def __init__(self):
        """Create a colored log class

        Log[, bool] -> None"""    
        # Create custom logger logging all five levels
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Define format for logs
        if (LOGGING_DATE):
            fmt = '%(asctime)s| %(levelname)8s | %(message)s'
        else:
            fmt = '%(levelname)s: %(message)s'
        
        # Create stdout handler for logging to the console (logs all five levels)
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(LoggingColor(fmt))

        # Create file handler for logging to a file (logs all five levels)
        today = datetime.date.today()
        file_handler = logging.FileHandler('my_app_{}.log'.format(today.strftime('%Y_%m_%d')))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(fmt))

        # Add both handlers to the logger
        self.logger.addHandler(stdout_handler)
        self.logger.addHandler(file_handler)

    def debug(self, msg):
        """Print debug logging

        Log, str -> None"""
        self.logger.debug(msg)
    
    def info(self, msg):
        """Print info logging

        Log, str -> None"""
        self.logger.info(msg)
    
    def warning(self, msg):
        """Print warning logging

        Log, str -> None"""
        self.logger.warning(msg)
    
    def error(self, msg):
        """Print error logging

        Log, str -> None"""
        self.logger.error(msg)
    
    def critical(self, msg):
        """Print critical logging

        Log, str -> None"""
        self.logger.critical(msg)