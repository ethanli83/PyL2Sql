'''
Created on Apr 3, 2013

@author: chenguangli
'''
import dis, sys

from io import StringIO
from TSql import PySqlObjFactory

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
                    code.arg = val
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
            
    

class Query:

    def __init__(self, entityFunc):
        codes = disassemble(entityFunc)
                
        self._entity = entityFunc()
        self._valName = codes[0].arg.replace("(", "").replace(")", "")
        self._factory = PySqlObjFactory.factory
            
    def innerJoin(self, to, condition):
        return self
    
    def leftJoin(self, condition):
        codes = disassemble(condition)
        return self
    
    def rightJoin(self, to, condition):
        return self

    def where(self, predicate):
        codes = disassemble(predicate)
        return self
    
    def select(self, selector):
        return self
    
    def grooupBy(self, selector):
        return self
    
    def orderBy(self, selector):
        return self
    
    def _printLambda(self, l):
        print(dis.dis(l))
    
    
    def toSql(self):
        factroy = self._factory;
        
        table = self._factory.makeTable(self._entity)
        sql = factroy.makeQuery(table)
        
        return sql;
        