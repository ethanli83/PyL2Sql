'''
Created on Apr 3, 2013

@author: chenguangli
'''

from TSql import PySqlObjFactory
from Utils import disassemble    

class Query:

    def __init__(self, entityLambda):
        codes = disassemble(entityLambda)
        
        self._aliasIndex = 0;    
                
        self._entity = entityLambda()
        self._valName = codes[0].arg.replace("(", "").replace(")", "")
        self._factory = PySqlObjFactory.factory
        
        self._valDict = []
        self._valDict.append((self._valName[0] + self._getAliasIndex(), self._valName, self._entity))
            
    def _getAliasIndex(self):
        self._aliasIndex += 1
        return str(self._aliasIndex)
    
    def _addToEntityDict(self, toLambda):
        codes = disassemble(toLambda)
        vName = codes[0].arg.replace("(", "").replace(")", "")
        entity = toLambda()
        eName = entity.entityName.lower()
        
        self._valDict.append((eName[0] + self._getAliasIndex(), vName, eName))
    
    def innerJoin(self, toLambda, condition):
        self._addToEntityDict(toLambda)
        return self
    
    def leftJoin(self, toLambda, condition):
        self._addToEntityDict(toLambda)
        return self
    
    def rightJoin(self, toLambda, condition):
        self._addToEntityDict(toLambda)
        return self

    def where(self, predicate):
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
        return sql
    
    def debugPrint(self):
        print(self.toSql())    
        print(self._valDict)
        