'''
Created on Apr 21, 2013

@author: chenguangli
'''

import sys, dis
from io import StringIO

class MachineCode(object):
    def __init__(self):
        self.lineNum = 0
        self.commandOffSet = 0
        self.command = ''
        self.argOffSet = 0
        self.arg = ''
        
    def __str__(self, *args, **kwargs):
        return str(self.lineNum) + '\t' + str(self.commandOffSet) + ' ' + self.command + '\t' + str(self.argOffSet) + ' ' + self.arg
    
    @staticmethod
    def parse(cmd : str):
        code = MachineCode()
        cmd = cmd[1:len(cmd)]
        index = 1 if cmd[0].isspace() else 0
        val = ''
        for c in cmd:
            
            if not c.isspace():
                val += c
                continue
            
            if val != '' and not val.isspace():
                if '>>' in val:
                    val = ''
                    continue
                
                if index == 0:
                    code.lineNum = int(val) 
                elif index == 1:
                    code.commandOffSet = int(val)
                elif index == 2:
                    code.command = val
                elif index == 3:
                    code.argOffSet = int(val)
                else:
                    code.arg = val.replace("(", "").replace(")", "")
                val = ''
                index += 1
                continue
        
        return code
        
    

def disassemble(obj=None):
    stdout = sys.stdout
    
    sys.stdout = c1 = StringIO()
    dis.dis(obj)
    sys.stdout = stdout
    
    cmdStr = str(c1.getvalue())
    commands = cmdStr.splitlines()
    
    commandObjs = []
    for cmd in commands:
        commandObjs.append(MachineCode.parse(cmd))
    
    return commandObjs 