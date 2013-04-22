'''
Created on Apr 21, 2013

@author: chenguangli
'''
import unittest
from Query import Query, L2MySqlTranslator
from Domain import Users, Requests

class TSqlObjectTests(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        
        u = Users()
        rq = Requests()
        query = Query(lambda : u). \
                    where(lambda : u.Id == 1 and u.LogonName == 'ethan.li'). \
                    innerJoin(lambda : rq, lambda : rq.RequesteeId == u.Id). \
                    select(lambda : { rq.RequesteeId, u.LogonName })
                    
        query.debugPrint()
        
    def testL2MySqlTranslatorTranslate(self):
        u = Users()
        query = Query(lambda : u).where(lambda : u.Id == 1)
        
        query.debugPrint()
        
        
if __name__ == "__main__":
    unittest.main()