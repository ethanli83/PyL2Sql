'''
Created on Apr 3, 2013

@author: chenguangli
'''

from Utils import disassemble    
from TSql import L2SqlObjFactory

class L2MySqlTranslator(object):
    def __init__(self, factory):
        self._factory = factory

class L2SqlTranslator(object):
    @staticmethod
    def makeTranslator(factory):
        return L2MySqlTranslator(factory)

class Query:

    def __init__(self, entityLambda):
        self._valDict = []
        self._aliasIndex = 0;    
        
        self._factory = L2SqlObjFactory.factory
        self._translator = L2SqlTranslator.makeTranslator(self._factory)
        
        self._entity = self._addToEntityDict(entityLambda)
            
    def _getAliasIndex(self):
        self._aliasIndex += 1
        return str(self._aliasIndex)
    
    def _addToEntityDict(self, toLambda):
        codes = disassemble(toLambda)
        
        vName = codes[0].arg
        entity = toLambda()        
        eName = entity.entityName.lower()
        
        self._valDict.append((eName[0] + self._getAliasIndex(), vName, entity))
        return entity
    
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
        