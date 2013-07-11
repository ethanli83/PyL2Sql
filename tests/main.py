'''
Created on Apr 22, 2013

@author: chenguangli
'''

import pymysql
from PyL2Sql.Query import Query
from PyL2Sql.MySqlObj import L2Sql
from tests.TestDataModel import Users, Requests

def main(*arg, **karg):
    #dis.dis(lambda u : { uid : u.Id, ln : u.LogonName * 56, Cnt: L2Sql.count(1) })
    
    u = Users()
    
    uid = 1
    query = Query(lambda : u).\
                where(lambda uid=uid: u.Id == uid) 
                
                
    print(query.toSql())
    
    query = Query(lambda : u).\
                where(lambda : u.Id == 1 or (u.Id == 2 and u.LogonName == 'ethan.li')).\
                select(lambda : { 'Id': u.Id, 'Name': u.LogonName, 'Cnt': L2Sql.count(1) }).\
                groupBy(lambda : { u.Id, u.LogonName }).\
                orderBy(lambda : { u.LogonName, u.Cnt }) 
                
                
    print(query.toSql())
    
    rq = Requests()
    query = Query(lambda : u).\
                innerJoin(lambda : rq, lambda : rq.RequesteeId == u.Id).\
                where(lambda : u.Id + (u.Id * 3) > 100 and rq.RequesterId == 2).\
                groupBy(lambda : { rq.RequesteeId }).\
                select(lambda : { id: rq.RequesteeId, sum: L2Sql.sum(u.Id) })
                
                
    print(query.toSql())
    rq = query
    query0 = Query(lambda : u).\
                innerJoin(lambda : rq, lambda : rq.Id == u.Id).\
                where(lambda : u.Id + (u.Id * 3) > 100 and rq.RequesterId == 2).\
                groupBy(lambda : { rq.RequesteeId }).\
                select(lambda : { id: rq.RequesteeId, sum: L2Sql.sum(u.Id) })
                
                
    print(query0.toSql())
    
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='password', db='test')
    cur = conn.cursor()
    
    q = Query(lambda : u)
    cur.execute(str(q.toSql()))
    
    # print cur.description
    
    # r = cur.fetchall()
    # print r
    # ...or...
    for row in cur.fetchall():
        print(row)
    
    cur.close()
    conn.close()
    
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