'''
Created on Apr 21, 2013

@author: chenguangli
'''
import unittest
from Query import Query
from Domain import Users


class TSqlObjectTests(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        
        u = Users()
        query = Query(u = u).where(lambda : u.Id == 1 and u.LogonName == 'ethan.li') 
        print(query.toSql())
        


if __name__ == "__main__":
    unittest.main()