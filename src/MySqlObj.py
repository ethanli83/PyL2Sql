'''
Created on Apr 6, 2013

@author: chenguangli
'''

class Operator:
    add = 1
    substract = 2
    multiply = 3
    divide = 4
    equals= 5
    notEquals = 6
    lessThan = 7
    lessOrEquals = 8
    greatThan = 9
    greatOrEquals = 10
    andOptr = 11
    orOptr = 12
    
    @staticmethod
    def toMySqlOptr(optr):
        if optr == 1:
            return '+'
        if optr == 2:
            return '-'
        if optr == 3:
            return '*'
        if optr == 4:
            return '\\'
        if optr == 5:
            return '='
        if optr == 6:
            return '!='
        if optr == 7:
            return '<'
        if optr == 8:
            return '<='
        if optr == 9:
            return '>'
        if optr == 10:
            return '>='
        if optr == 11:
            return 'and'
        if optr == 12:
            return 'or'
        
class JoinType:
    innerJoin = 1
    leftJoin = 2
    leftOuterJoin = 3
    rightJoin = 4
    rightOuterJoin = 5
    
class L2Sql:
    @staticmethod
    def count(obj):
        pass
    
    @staticmethod
    def sum(obj):
        pass
    
    @staticmethod
    def avg(obj):
        pass
    
    @staticmethod
    def max(obj):
        pass
    
    @staticmethod
    def min(obj):
        pass
        
'''
reference to an object that we can select from.
a SqlFrom can be a table from database, a cte, or even another query 
'''
class MySqlSelectable(object):
    def __init__(self, obj, alias = ''):
        self._obj = obj
        self._alias = alias
        
    def __str__(self):
        if isinstance(self._obj, MySqlQuery) :
            sstr = '(\n'
            sstr += '\n'.join(['    ' + l for l in str(self._obj).splitlines()]) + '\n'
            sstr += ') ' + self._alias
            return sstr
        return '{} {}'.format(self._obj, self._alias)
    
    def toInstanceName(self):
        return self._alias if self._alias is not None and not self._alias.isspace() else str(self._obj)

class MySqlField(object):
    def __init__(self, instance, fieldName, fType = None):
        self._instance = instance
        self._field = fieldName
        self._type = fType
        self._alias = None
        
    def setAlias(self, alias):
        self._alias = alias
        
    def __str__(self, *args, **kwargs):
        instanceName = self._instance.toInstanceName()
        fstr = instanceName + "." + self._field
        if self._alias is not None:
            fstr += ' as ' + str(self._alias)
        return fstr

class MySqlFunc(object):
    def __init__(self, funcName):
        self._func = funcName
        self._instance = None
        self._param = None
        self._alias = None
    
    def setParam(self, param):
        self._param = param
    
    def setAlias(self, alias):
        self._alias = alias
        
    def __str__(self, *args, **kwargs):
        func = ''
        if self._instance is not None:
            func += str(self._instance) + '.'
        
        func += self._func + "("
        if self._param is not None:
            if isinstance(self._param, list) and len(self._param) > 0:
                func += ', '.join(str(p) for p in self._param)
            else:
                func += str(self._param)
        func += ')'
        
        if self._alias is not None:
            func += ' as ' + str(self._alias)
        
        return func
                

class MySqlConstant(object):
    def __init__(self, val):
        self._val = val
        
    def _getSqlValue(self):
        if isinstance(self._val, str):
            return "'" + self._val + "'"
        
        return self._val
    
    def __str__(self, *args, **kwargs):
        return str(self._getSqlValue());
    
class MySqlBinary(object):
    def __init__(self, left, operation, right):
        self._left = left
        self._optr = operation
        self._right = right
        
    def __str__(self, *args, **kwargs):
        return '(' +  str(self._left) + ' ' + Operator.toMySqlOptr(self._optr) + ' ' + str(self._right) + ')'
    
    '''
    returns the referred name of the selectable in the query
    for example, for the entity floor in select * from floor f
    the alias f is the refer name of entity floor in the query
    '''
    def toInstanceName(self):
        if self._alias is None or self._alias.isspace():
            return str(self._obj)
        else:
            return self._alias
            
'''
represent a table in database
'''
class MySqlTable(object):
    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name
        
    def __str__(self):
        if self.namespace is not None and self.namespace != '':
            return '{}.{}'.format(self.namespace, self.name)
        else:
            return '{}'.format(self.name)

class MySqlWhere(object):
    def __init__(self, binary):
        self._binary = binary
        
    def __str__(self):
        return "where " + str(self._binary)

class MySqlJoin(object):
    def __init__(self, selectable, joinType, condition):
        self._target = selectable
        self._joinType = joinType
        self._condition = condition
        
    def __str__(self, *args, **kwargs):
        join = ''
        if self._joinType == JoinType.innerJoin:
            join = 'inner join'
        if self._joinType == JoinType.leftJoin:
            join = 'left join'
        if self._joinType == JoinType.leftOuterJoin:
            join = 'left outer join'
        if self._joinType == JoinType.rightJoin:
            join = 'right join'
        if self._joinType == JoinType.rightOuterJoin:
            join = 'right outer join'
        
        join += ' ' + str(self._target) + ' on ' + str(self._condition)
        return join
        

class MySqlQuery(object):
    def __init__(self):
        self.selects = []
        self.queryFrom = None
        self.where = None
        self.joins = []
        self.groupBys = None
        self.orderBys = None
        self.ctes = None
    
    def __str__(self):
        sql = '';
        
        if self.ctes is not None and len(self.ctes) > 0:
            sql += str(self.ctes) + '\n'
        
        sql += 'select'
        
        if self.selects is None or len(self.selects) == 0:
            sql += ' *'
        else:
            for select in self.selects:
                sql += ' ' + str(select) + ','
            sql = sql[:-1] + ' '
        
        sql += '\nfrom ' + str(self.queryFrom) + '\n'
        
        if self.joins is not None and len(self.joins) > 0:
            for join in self.joins:
                sql += str(join) + '\n'
        
        if self.where is not None:
            sql += str(self.where) + '\n'
                
        if self.groupBys is not None:
            if isinstance(self.groupBys, list) and len(self.groupBys) > 0:
                sql += 'group by ' + ', '.join(str(gb) for gb in self.groupBys) + '\n'
            else:
                sql += 'group by ' + str(self.groupBys) + '\n'
            
        if self.orderBys is not None:
            if isinstance(self.orderBys, list) and len(self.orderBys) > 0:
                sql += 'order by ' + ', '.join(str(ob) for ob in self.orderBys) + '\n'
            else:
                sql += 'order by ' + str(self.orderBys) + '\n' 
            
        return sql
            
        
class MySqlObjectFactory:
    def __init__(self):
        pass
    
    def makeTable(self, entity):
        return MySqlTable(entity.namespace, entity.entityName)
    
    def makeSelectable(self, obj, alias = ''):
        return MySqlSelectable(obj, alias)
    
    def makeField(self, instance, fieldName):
        return MySqlField(instance, fieldName)
    
    def makeFunc(self, funcName):
        return MySqlFunc(funcName)
    
    def makeConstant(self, val):
        return MySqlConstant(val)
    
    def makeBinary(self, left, optr, right):
        return MySqlBinary(left, optr, right)
    
    def makeWhere(self, obj):
        return MySqlWhere(obj)
    
    def makeJoin(self, target, joinType, condition):
        return MySqlJoin(target, joinType, condition)
    
    def makeQuery(self): 
        return MySqlQuery()
    
class L2SqlObjFactory:
    factory = MySqlObjectFactory()
    
    