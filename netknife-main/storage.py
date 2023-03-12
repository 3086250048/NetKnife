import sqlite3,os

class AppStorage():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance       
    def __init__(self) -> None:
        self.__path=os.path.dirname(os.path.abspath(__file__))+'/appdata.db'
        self.__add_login_info_sql=fr'''INSERT INTO LOGININFO (PROJECT,CLASS,AREA,PROTOCOL,PORT,USERNAME,PASSWORD,SECRET,IP_EXPRESSION)
                            VALUES (?,?,?,?,?,?,?,?,?)'''

        if not os.path.exists(self.__path):
            try:
                con=sqlite3.connect(self.__path)
                cur=con.cursor()
                cur.execute(
                    '''CREATE TABLE  LOGININFO(
                PROJECT        TEXT    PRIMARY KEY   NOT NULL,
                CLASS          TEXT    NOT NULL,
                AREA           TEXT    NOT NULL,
                PROTOCOL       TEXT    NOT NULL,
                PORT           TEXT    NOT NULL,
                USERNAME       TEXT    NOT NULL,
                PASSWORD     TEXT      NOT NULL,
                SECRET        TEXT     NOT NULL,
                IP_EXPRESSION   TEXT    NOT NULL
                );'''
                )
                con.commit()
                print('数据库创建成功')
            except sqlite3.Error as e:
                print(e)
                con.rollback()
            finally:
                if cur:
                    cur.close()
                if con:
                    con.close()
    def add_login_info(self,login_dict):
        try:
            value_tuple=tuple(login_dict.values())
            con=sqlite3.connect(self.__path,check_same_thread=False)
            cur=con.cursor()
            cur.execute(self.__add_login_info_sql,value_tuple)
            con.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            con.rollback()
            return False
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def select_login_info(self):
        return 1


if __name__ == '__main__':
    s1=AppStorage()
    # s1.add_login_info()
    info_gen=s1.select_login_info()
    for item  in info_gen:
        print(item)
