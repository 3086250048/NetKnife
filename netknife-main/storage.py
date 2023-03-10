import sqlite3,os
from  data import AppInfo

pub_data=AppInfo()


class AppStorage():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance       
    def __init__(self) -> None:
        self.__path=os.path.dirname(os.path.abspath(__file__) )
        self.__db=sqlite3.connect(f'{self.__path}/appdata.db',check_same_thread=False)
        self.__cur=self.__db.cursor()
        self.__operate=self.__cur.execute
        if not os.path.exists(f'{self.__path}/appdata.db'):
            self.__operate('''CREATE TABLE  LOGININFO(
                PROJECT        TEXT    PRIMARY KEY   NOT NULL,
                CLASS          TEXT    NOT NULL,
                AREA           TEXT    NOT NULL,
                PROTOCOL       TEXT    NOT NULL,
                PORT           TEXT    NOT NULL,
                USERNAME       TEXT    NOT NULL,
                PASSWORD     TEXT      NOT NULL,
                IP             TEXT    NOT NULL
                );''')
            self.__db.commit()

    def add_login_info(self):
        try:
            self.__operate(f"INSERT INTO LOGININFO (PROJECT,CLASS,AREA,PROTOCOL,PORT,USERNAME,PASSWORD,IP)\
                            VALUES ('{pub_data.login_dict['project']}',\
                                    '{pub_data.login_dict['class']}',\
                                    '{pub_data.login_dict['area']}',\
                                    '{pub_data.login_dict['protocol']}',\
                                    '{pub_data.login_dict['port']}',\
                                    '{pub_data.login_dict['username']}',\
                                    '{pub_data.login_dict['password']}',\
                                    '{pub_data.login_dict['ip']}',\
                                    '{pub_data.login_dict['secret']}',\
                                    )")
            self.__db.commit()
            return True
        except:
            return False

    def select_login_info(self):
        cursor= self.__operate("SELECT * FROM LOGININFO")
        return cursor


if __name__ == '__main__':
    s1=AppStorage()
    # s1.add_login_info()
    info_gen=s1.select_login_info()
    for item  in info_gen:
        print(item)
