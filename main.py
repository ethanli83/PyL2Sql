'''
Created on Apr 22, 2013

@author: chenguangli
'''

import dis
from Domain import Users
from Query import Query

def main(*arg, **karg):
    dis.dis(lambda u : u.id == 1 and u.name == 'th')
    
    u = Users()
    query = Query(lambda : u).where(lambda : u.Id == 1)
        
    query.debugPrint()

if __name__ == '__main__':
    main()