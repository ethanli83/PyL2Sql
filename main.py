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
    
    query = Query(lambda : u).where(lambda : u.Id + (u.Id * 3) > 100)
    query.debugPrint()
    
    '''
    select *
    from users u0
    where ((u0.Id = 1) or ((u0.Id = 2) and (u0.LogonName = 'ethan.li')))
    {'u': (<Domain.Users object at 0x1007c4350>, 'u0')}
    select *
    from users u0
    where ((u0.Id + (u0.Id * 3)) > 100)
    {'u': (<Domain.Users object at 0x1007c4350>, 'u0')}
    '''

if __name__ == '__main__':
    main()