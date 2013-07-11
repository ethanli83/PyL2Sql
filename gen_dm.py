'''
Created on May 18, 2013

@author: chenguangli
'''

import sys, getopt, os
import pymysql
from genericpath import isfile

class DatabaseColumn:
    def __init__(self):
        self.columnName = ''
        self.type = ''
        self.defaultValue = None
        self.isPrimaryKey = False
        self.isUnique = False
        self.isNullable = False
        
class DatabaseTable:
    def __init__(self):
        self.tableName = ''
        self.database = ''
        self.columns = []
        
    def toClassStr(self):
        classStr = 'class ' + self.tableName + '(Entity):\n'
        classStr += '    def __init__(self):\n'
        classStr += '        self.namespace = "''"\n'
        classStr += '        self.database = "' + self.database + '"\n'
        classStr += '        self.entityName = "' + self.tableName + '"\n'
        classStr += '\n'
        
        for column in self.columns:
            classStr += '        self.' + column.columnName + ' = None\n'
        return classStr

def generateDb(argv):
    host = 'localhost'
    port = 3306
    database = 'test'
    oFile = './DataModel.py'
    user = 'root'
    password = 'password'
        
    try:
        opts, args = getopt.getopt(argv, '', ['host=', 'port=', 'db=', 'user=', 'password=', 'ofile='])
    except getopt.GetoptError:
        print(getopt.GetoptError.msg)
        sys.exit(2)
    for key, val in opts:
        if key == '--host':
            host = val
        elif key == '--port':
            port = int(val)
        elif key == '--db':
            database = val
        elif key == '--ofile':
            oFile = val
            
    
    print(host, port, database, oFile)
    
    tableSelect = 'show tables from %s;'%(database)
    
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database)
    
    tableFetcher = conn.cursor()
    tableFetcher.execute(tableSelect)
    
    # fetch all tables and columns from database
    # and build table schema
    tables = []
    for table in tableFetcher.fetchall():
        tableName = table[0]
        print(tableName)
        
        columnFetcher = conn.cursor()
        columSelect = 'show columns from %s from %s;'%(tableName, database)
        columnFetcher.execute(columSelect)
        
        dbTable = DatabaseTable()
        dbTable.database = database
        dbTable.tableName = tableName
        for col in columnFetcher.fetchall():
            column = DatabaseColumn()
            column.columnName = col[0]
            column.type = col[1]
            column.isNullable = bool(col[2])
            column.isPrimaryKey = col[3] == 'PRI'
            column.isUnique = col[3] == 'UNI'
            
            dbTable.columns.append(column)
        
        tables.append(dbTable)
    
    # create data model classes
    
    if isfile(oFile):
        os.remove(oFile)
    
    fileBuf = open(oFile, mode='w')
    
    fileBuf.write('from PyL2Sql.DataEntity import Entity\n\n')
    for table in tables:
        fileBuf.write(table.toClassStr())
    
    fileBuf.close()     
    
    tableFetcher.close()
    conn.close()
            

if __name__ == '__main__':
    print(sys.argv[1:])
    generateDb(sys.argv[1:])
