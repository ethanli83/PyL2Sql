from PyL2Sql.DataEntity import Entity


class Users(Entity):
    def __init__(self):
        self.namespace = ""
        self.database = "test"
        self.entityName = "Users"

        self.Id = None  
        self.LogonName = None
        self.Password = None
        self.TaId = None
        
class Requests(Entity):
    def __init__(self):
        self.namespace = None
        self.entityName = 'Requests'
        
        self.Id = 0;
        self.RequesteeId = 0
        self.RequesterId = 0
        self.Content = '' 



