'''
Created on Apr 22, 2013

@author: chenguangli
'''

import dis
from Domain import Users, Requests
from Query import Query

def main(*arg, **karg):
    #dis.dis(lambda u : { 'uid' : u.Id, 'ln' : u.LogonName })
    
    u = Users()
    query = Query(lambda : u).where(lambda : u.Id == 1 or (u.Id == 2 and u.LogonName == 'ethan.li')).select(lambda : { u.Id, u.LogonName })
    query.debugPrint()
    
    rq = Requests()
    query = Query(lambda : u).innerJoin(lambda : rq, lambda : rq.RequesteeId == u.Id).where(lambda : u.Id + (u.Id * 3) > 100 and rq.RequesterId == 2)
    query.debugPrint()
    
    '''
    print out:
    select *
    from users u0
    where ((u0.Id = 1) or ((u0.Id = 2) and (u0.LogonName = 'ethan.li')))
    {'u': (<Domain.Users object at 0x1007c43d0>, 'u0')}
    select *
    from users u0
    inner join Requests r1 on (r1.RequesteeId = u0.Id)
    where (((u0.Id + (u0.Id * 3)) > 100) and (r1.RequesterId = 2))
    {'u': (<Domain.Users object at 0x1007c43d0>, 'u0'), 'rq': (<Domain.Requests object at 0x1007ecd10>, 'r1')}
    '''

if __name__ == '__main__':
    main()