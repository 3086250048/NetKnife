import sqlite3,os
from  data import AppInfo

pub_data=AppInfo()


class AppStorage():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance       
    def __init__(self) -> None:
        if not os.path.exists('./appdata.db'):
            self.__db=sqlite3.connect('./appdata.db')
            self.__cur=self.__db.cursor()
            self.__operate=self.__cur.execute
            self.__operate('''CREATE TABLE  LOGININFO(
                PROJECT        TEXT    PRIMARY KEY   NOT NULL,
                CLASS          TEXT    NOT NULL,
                AREA           TEXT    NOT NULL,
                PROTOCOL       TEXT    NOT NULL,
                PORT           TEXT    NOT NULL,
                USERNAME       TEXT    NOT NULL,
                PASSWORD     TEXT      NOT NULL
                );''')
            self.__db.commit()
            self.__db.close()

    def add_login_info(self):
            print(pub_data.login_dict)
            # self.__operate(f"INSERT INTO LOGININFO (PROJECT,CLASS,AREA,PROTOCOL,PORT,USERNAME,PASSWORD,IP)\
            #         VALUES ({pub_data.login_dict['project']},\
            #                 {pub_data.login_dict['class']},\
            #                 {pub_data.login_dict['area']},\
            #                 {pub_data.login_dict['protocol']},\
            #                 {pub_data.login_dict['username']},\
            #                 {pub_data.login_dict['password']},\
            #                 {pub_data.login_dict['ip']})")
            # self.__db.commit()
            # self.__db.close()
    def select_login_info(self):
            pass

if __name__ == '__main__':
    print(os.getcwd())
    s=AppStorage()
    s1=AppStorage()
    print(id(s)==id(s1))