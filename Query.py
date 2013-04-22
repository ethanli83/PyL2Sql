'''
Created on Apr 3, 2013

@author: chenguangli
'''

from Utils import disassemble, MachineCode
from MySqlObj import L2SqlObjFactory, MySqlObjectFactory, Operator
from Domain import Entity

class L2MySqlTranslator(object):
    def __init__(self):
        pass

    def translate(self, lam, factory : MySqlObjectFactory, selectableDict):        
        stack = []
        
        for obj in disassemble(lam):
            cmd = MachineCode.parse(obj)
            
            if cmd.command == 'LOAD_FAST' or cmd.command == 'LOAD_DEREF':
                entity = selectableDict[cmd.arg]
                if isinstance(entity[0], Entity) :
                    #entity will be a tuple in which the first item is the entity and second one is alias
                    table = factory.makeTable(entity[0])
                    expr = factory.makeSelectable(table, entity[1])
                    
                    stack.append(expr)
                    
            if cmd.command == 'LOAD_ATTR':
                fieldName = cmd.arg
                instance = stack.pop()
                
                expr = factory.makeField(instance, fieldName)
                stack.append(expr)
                
            if cmd.command == 'LOAD_CONST':
                val = cmd.arg
                expr = factory.makeConstant(val)
                stack.append(expr)
            
            if cmd.command == 'COMPARE_OP':
                right = stack.pop()
                left = stack.pop()
                if cmd.arg == '==':
                    expr = factory.makeBinary(left, Operator.equals, right)
                    stack.append(expr)
                    
        
        return stack.pop()

class L2SqlTranslator(object):
    translator = L2MySqlTranslator() 

class Query:

    def __init__(self, entityLambda):
        self._selectableDict = {}
        self._aliasIndex = 0;    
        
        self._factory = L2SqlObjFactory.factory
        self._translator = L2SqlTranslator.translator
        
        tup = self._addToEntityDict(entityLambda)
        self._entity = tup[0]
        self._entityAlias = tup[1]
        
        table = self._factory.makeTable(self._entity)
        query = self._factory.makeQuery()
        query.queryFrom = self._factory.makeSelectable(table, self._entityAlias)
        
        self._query = query
            
    def _getAlias(self, entity : Entity):
        alias = entity.entityName.lower()[0] + str(self._aliasIndex)
        self._aliasIndex += 1
        return alias
    
    '''
    add entity to entity dictionary, the dictionary is used to keep track of
    entity from which the query selects, and all entities that the query joined on
    dictionary's key is the variable name that people passed in
    its value is a tuple containing the actual entity object and its alias in query
    '''
    def _addToEntityDict(self, toLambda):
        codes = disassemble(toLambda)
        command = MachineCode.parse(codes[0])
        vName = command.arg
        entity = toLambda()        
        
        t = (entity, self._getAlias(entity))
        self._selectableDict[vName] = t
        return t
    
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
        binary = self._translator.translate(predicate, self._factory, self._selectableDict)
        where = self._factory.makeWhere(binary)
        self._query.where = where
        return self
    
    def select(self, selector):
        return self
    
    def grooupBy(self, selector):
        return self
    
    def orderBy(self, selector):
        return self    
    
    def toSql(self):        
        return self._query
    
    def debugPrint(self):
        print(self.toSql())    
        print(self._selectableDict)
        