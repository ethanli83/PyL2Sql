'''
Created on Apr 6, 2013

@author: chenguangli
'''
from Domain import Entity


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
            return '({}) {}'.format(self._obj, self._alias)
        return '{} {}'.format(self._obj, self._alias)
    
    def toInstanceName(self):
        return self._alias if self._alias is not None and not self._alias.isspace() else str(self._obj)

class MySqlField(object):
    def __init__(self, instance : MySqlSelectable, fieldName, fType = None):
        self._instance = instance
        self._field = fieldName
        self._type = fType
        
    def __str__(self, *args, **kwargs):
        instanceName = self._instance.toInstanceName()
        return instanceName + "." + self._field
    
class MySqlConstant(object):
    def __init__(self, val):
        self._val = val
        
    def __str__(self, *args, **kwargs):
        return self._val.__str__();
    
class MySqlBinary(object):
    def __init__(self, left, operation, right):
        self._left = left
        self._optr = operation
        self._right = right
        
    def __str__(self, *args, **kwargs):
        return '(' +  str(self._left) + ' ' + Operator.toMySqlOptr(self._optr) + ' ' + str(self._right) + ')'
    
    '''
    returns the refered name of the selectable in the query
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

class MySqlColumn(object):
    def __init__(self):
        self.owner = None
        self.columnable = None
        self.alias = None

class MySqlWhere(object):
    def __init__(self, binary):
        self._binary = binary
        
    def __str__(self):
        return "where " + str(self._binary)

class MySqlQuery(object):
    def __init__(self):
        self.selects = None
        self.queryFrom = None
        self.where = None
        self.joins = None
        self.groupBys = None
        self.orderBys = None
        self.ctes = None
    
    def __str__(self):
        sql = '';
        
        if self.ctes is not None:
            sql += str(self.ctes) + '\n'
        
        sql += 'select'
        
        if self.selects is None:
            sql += ' *\n'
        else:
            for select in self.selects:
                sql += str(select) + '\n'
        
        sql += 'from ' + str(self.queryFrom) + '\n'
        
        if self.joins is not None:
            for join in self.joins:
                sql += str(join) + '\n'
        
        if self.where is not None:
            sql += str(self.where)
                
        if self.groupBys is not None:
            sql += 'group by ' + ', '.join(str(gb) for gb in self.groupBys) + '\n'
            
        if self.orderBys is not None:
            sql += 'order by ' + ', '.join(str(ob) for ob in self.orderBys) + '\n' 
            
        return sql
            
        
class MySqlObjectFactory:
    def __init__(self):
        pass
    
    def makeTable(self, entity : Entity):
        return MySqlTable(entity.namespace, entity.entityName)
    
    def makeSelectable(self, obj, alias = ''):
        return MySqlSelectable(obj, alias)
    
    def makeField(self, instance, fieldName):
        return MySqlField(instance, fieldName)
    
    def makeConstant(self, val):
        return MySqlConstant(val)
    
    def makeBinary(self, left, optr, right):
        return MySqlBinary(left, optr, right)
    
    def makeWhere(self, obj):
        return MySqlWhere(obj)
    
    def makeQuery(self):
        return MySqlQuery()
    
class L2SqlObjFactory:
    factory = MySqlObjectFactory()
    
    