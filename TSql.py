'''
Created on Apr 6, 2013

@author: chenguangli
'''

'''
reference to an object that we can select from.
a SqlFrom can be a table from database, a cte, or even another query 
'''
class SqlFrom(object):
    def __init__(self, obj):
        self.obj = obj
        self.alias = ''
        
    def __str__(self):
        if isinstance(self.obj, SqlQuery) :
            return '({}) {}'.format(self.obj, self.alias)
        return '{} {}'.format(self.obj, self.alias)
            
'''
represent a table in database
'''
class SqlTable(object):
    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name
        
    def __str__(self):
        if self.namespace is not None and self.namespace != '':
            return '{}.{}'.format(self.namespace, self.name)
        else:
            return '{}'.format(self.name)

class SqlColumn(object):
    def __init__(self):
        self.owner = None
        self.columnable = None
        self.alias = None

class SqlQuery(object):
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
            
        
class TSqlObjectFactory:
    def __init__(self):
        pass
    
    def makeTable(self, entity):
        return SqlTable(entity.namespace, entity.entityName)
    
    def makeFrom(self, obj):
        return SqlFrom(obj)
    
    def makeQuery(self, entity):
        query = SqlQuery()
        query.queryFrom = self.makeFrom(entity)
        return query;
    
class PySqlObjFactory:
    factory = TSqlObjectFactory()
    
    