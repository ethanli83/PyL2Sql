'''
Created on Apr 22, 2013

@author: chenguangli
'''

import dis
from Domain import Users
from Query import Query

def main(*arg, **karg):
    #dis.dis(lambda u : (u.id if u.id > 0 else u.idd) == 1)
    
    u = Users()
    query = Query(lambda : u).where(lambda : u.Id == 1 or (u.Id == 2 and u.LogonName == 'ethan.li'))
        
    query.debugPrint()

if __name__ == '__main__':
    main()