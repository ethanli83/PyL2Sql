'''
Created on Apr 3, 2013

@author: chenguangli
'''

from TSql import PySqlObjFactory
from Utils import disassemble    

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
    
    def toSql(self):
        factroy = self._factory;
        
        table = self._factory.makeTable(self._entity)
        sql = factroy.makeQuery(table)
        
        return sql;
        