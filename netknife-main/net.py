from netmiko import ConnectHandler
from storage import AppStorage

storage=AppStorage()

def net_checkip():
    if 1 :
        return True
    else:
        return False

class AppNet():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance     
    def __init__(self) :
        self.__login_list=[{'device_type':item[1],
                            'host':item[7],
                            'username':item[5],
                            'password':item[6],
                            'port':item[4],
                            'secret':item[8]
                            }
                            for item in  storage.select_login_info()]

