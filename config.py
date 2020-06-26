import sys
from define import DEFINE

class config:
    DEFAULT_PORT = 23
    DEFAULT_MODE = 1
    
    def __init__(self, filename):
        self.config = dict(port = config.DEFAULT_PORT, mode = config.DEFAULT_MODE)
        if filename == None:
            return
        else:
            try:
                with open(filename) as rfile:
                    lins = rfile.readlines()
                self.read_config(lins)
            except Exception as e:
                print("read config error:" + str(e), file=sys.stderr)
                return
        

    def read_config(self, lines):
        for line in lines:
            (key, delm, val) = line.partition('=')
            if val != "":
                key = key.strip().lower()
                val = val.strip()
                if self.check_val(key, val) == True:
                    self.config[key] = int(val)
                else:
                    pass
            else:
                pass

    def check_val(self, key, val):
        if key == DEFINE.KEY_PORT:
            return self.in_range(val, 0, 27)
        elif key == DEFINE.KEY_MODE:
            return self.in_range(val, 1, 2)
        else:
            return False

    def in_range(self, val, minval, maxval):
        if val.isdecimal():
            v = int(val)
            if v >= minval and v <= maxval:
                return True
            else:
                return False
        else:
            return False

        
                
        

