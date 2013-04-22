'''
Created on Apr 3, 2013

@author: chenguangli
'''

class Entity:
    def __init__(self):
        self.namespace = None
        self.entityName = ''


class Users(Entity):
    def __init__(self):
        self.namespace = None
        self.entityName = 'users'
        
        self.Id = 0
        self.LogonName = ''
        self.Password = ''

class Requests(Entity):
    def __init__(self):
        self.namespace = None
        self.entityName = 'Requests'
        
        self.Id = 0;
        self.RequesteeId = 0
        self.RequesterId = 0
        self.Content = '' 


