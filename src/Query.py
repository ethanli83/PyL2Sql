'''
Created on Apr 3, 2013

@author: chenguangli
'''
import inspect
from PyL2Sql.Utils import MachineCode, disassemble
from PyL2Sql.DataEntity import Entity
from PyL2Sql.MySqlObj import Operator, L2SqlObjFactory, JoinType



class L2MySqlTranslator(object):
    def __init__(self):
        self._lambdaArgs = {}
        
    def _buildArgsDict(self, lam):
        lamArgs = inspect.getfullargspec(lam)
        count = len(lamArgs[0])
        if count < 1:
            return
        
        args = lamArgs[0]
        vals = lamArgs[3]
        self._lambdaArgs = {}
        for i in range(0, count):
            self._lambdaArgs[args[i]] = vals[i]
            

    def translate(self, lam, factory, selectableDict):  
        self._buildArgsDict(lam)
              
        cmds = disassemble(lam)
        result = self._translateCommands(cmds, selectableDict, factory)
        if isinstance(result, tuple):
            return result[0]
        return result
    
    def _translateCommands(self, cmds, selectableDict, factory, eIndex = -1):
        stack = []
        i = 0
        globalIdentifier = object()
        while i < len(cmds):
            cmd = MachineCode.parse(cmds[i])
            
            # stop if the caller of the function told us that
            # we only need to process these commands till this line
            if cmd.commandOffSet == eIndex:
                break
            
            if cmd.command == 'LOAD_FAST' or cmd.command == 'LOAD_DEREF':
                if cmd.arg in selectableDict:
                    entity = selectableDict[cmd.arg]
                    if isinstance(entity[0], Entity) :
                        #entity will be a tuple in which the first item is the entity and second one is alias
                        table = factory.makeTable(entity[0])
                        expr = factory.makeSelectable(table, entity[1])
                        stack.append(expr)
                    else:
                        expr = factory.makeSelectable(entity[0], entity[1])
                        stack.append(expr)
                else:
                    if cmd.arg in self._lambdaArgs:
                        expr = factory.makeConstant(self._lambdaArgs[cmd.arg])
                        stack.append(expr)
                    
            if cmd.command == 'LOAD_ATTR':
                fieldName = cmd.arg
                instance = stack.pop()
                
                if instance == globalIdentifier:
                    stack.append(globalIdentifier)
                    expr = factory.makeFunc(fieldName)
                else:
                    expr = factory.makeField(instance, fieldName)
                    
                stack.append(expr)
            
            if cmd.command == 'CALL_FUNCTION':
                params = []
                while 1:
                    param = stack.pop()
                    if param == globalIdentifier:
                        expr = params.pop()
                        break
                    params.append(param)
                expr.setParam(params)
                stack.append(expr) 
            
            if cmd.command == 'LOAD_CONST' or (cmd.command == 'LOAD_GLOBAL' and cmd.arg != 'L2Sql'):
                val = cmd.arg
                expr = factory.makeConstant(val)
                stack.append(expr)
            
            if cmd.command == 'COMPARE_OP':
                right = stack.pop()
                left = stack.pop()
                expr = None
                if cmd.arg == '==':
                    expr = factory.makeBinary(left, Operator.equals, right)
                if cmd.arg == '!=':
                    expr = factory.makeBinary(left, Operator.notEquals, right)
                if cmd.arg == '<':
                    expr = factory.makeBinary(left, Operator.lessThan, right)
                if cmd.arg == '<=':
                    expr = factory.makeBinary(left, Operator.lessOrEquals, right)
                if cmd.arg == '>':
                    expr = factory.makeBinary(left, Operator.greatThan, right)
                if cmd.arg == '>=':
                    expr = factory.makeBinary(left, Operator.greatOrEquals, right)
                if expr is not None:
                    stack.append(expr)
                    
            # process calculation operator
            if cmd.command == 'BINARY_ADD':
                right = stack.pop()
                left = stack.pop()
                expr = factory.makeBinary(left, Operator.add, right)
                stack.append(expr)
                
            if cmd.command == 'BINARY_SUBTRACT':
                right = stack.pop()
                left = stack.pop()
                expr = factory.makeBinary(left, Operator.substract, right)
                stack.append(expr)
                
            if cmd.command == 'BINARY_MULTIPLY':
                right = stack.pop()
                left = stack.pop()
                expr = factory.makeBinary(left, Operator.multiply, right)
                stack.append(expr)
                
            if cmd.command == 'BINARY_DIVIDE':
                right = stack.pop()
                left = stack.pop()
                expr = factory.makeBinary(left, Operator.divide, right)
                stack.append(expr)
            
            # process logic binary operation
            optr = ''
            if cmd.command == 'JUMP_IF_FALSE_OR_POP':
                optr = Operator.andOptr
            
            if cmd.command == 'JUMP_IF_TRUE_OR_POP':
                optr = Operator.orOptr
                
            if cmd.command == 'JUMP_IF_FALSE_OR_POP' or cmd.command == 'JUMP_IF_TRUE_OR_POP':
                jumpTo = cmd.argOffSet
                result = self._translateCommands(cmds[i + 1 : len(cmds)], selectableDict, factory, jumpTo)
                
                left = stack.pop()
                right = result[0]
                expr = factory.makeBinary(left, optr, right)
                
                stack.append(expr)
                i += result[1]
            
            # process commands that builds a list of select columns    
            if cmd.command == 'BUILD_SET':
                return stack
            
            if cmd.command == 'BUILD_MAP':
                expr = []
                stack.append(expr)
                
            if cmd.command == 'STORE_MAP':
                alias = stack.pop()
                field = stack.pop()
                field.setAlias(alias)
                
                selectList = stack.pop()
                selectList.append(field)
                stack.append(selectList)
            
            #process aggregation func call
            if cmd.command == 'LOAD_GLOBAL' and cmd.arg == 'L2Sql':
                stack.append(globalIdentifier)
                
                
            i += 1
                                 
        return (stack.pop(), i)    
    

class L2SqlTranslator(object):
    translator = L2MySqlTranslator() 

class Query:

    def __init__(self, entityLambda):
        self._selectableDict = {}
        self._aliasIndex = 0;    
        
        self._factory = L2SqlObjFactory.factory
        self._translator = L2SqlTranslator.translator
        
        query = self._factory.makeQuery()
        
        tup = self._addToEntityDict(entityLambda)
        query.queryFrom = self._getSelectable(tup)
        
        self._query = query
            
    def _getSelectable(self, tup):
        entity = tup[0]
        alias = tup[1]
        
        if isinstance(entity, Entity):
            table = self._factory.makeTable(entity)
            return self._factory.makeSelectable(table, alias)
        elif isinstance(entity, Query):
            return self._factory.makeSelectable(entity.toSql(), alias)
            
    def _getAlias(self, entity):
        if isinstance(entity, Entity):
            alias = entity.entityName.lower()[0] + str(self._aliasIndex)
        else:
            alias = 'q' + str(self._aliasIndex)
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
    
    def innerJoin(self, toLambda, conditionLam):
        tup = self._addToEntityDict(toLambda)
        joinTarget = self._getSelectable(tup)
        condition = self._translator.translate(conditionLam, self._factory, self._selectableDict)
        join = self._factory.makeJoin(joinTarget, JoinType.innerJoin, condition)
        self._query.joins.append(join)
        return self
    
    def leftJoin(self, toLambda, conditionLam):
        self._addToEntityDict(toLambda)
        return self
    
    def rightJoin(self, toLambda, conditionLam):
        self._addToEntityDict(toLambda)
        return self

    def where(self, predicate):
        binary = self._translator.translate(predicate, self._factory, self._selectableDict)
        where = self._factory.makeWhere(binary)
        self._query.where = where
        return self
    
    def select(self, selector):
        self._query.selects = self._translator.translate(selector, self._factory, self._selectableDict)
        return self
    
    def groupBy(self, selector):
        self._query.groupBys = self._translator.translate(selector, self._factory, self._selectableDict)
        return self
    
    def orderBy(self, selector):
        self._query.orderBys = self._translator.translate(selector, self._factory, self._selectableDict)
        return self    
    
    def toSql(self):        
        return self._query 
    
    def debugPrint(self):
        print(str(self._query))   