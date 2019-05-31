from models import ModelBase

class UserData(ModelBase):

    def __init__(self, uid):
        self.uid = uid
        self._attrs = {
            'name':'',
            'password':'',
            'reg_time':'',
        }

    def wangwudi(self):
        pass








