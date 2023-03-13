import sqlite3,os,uuid

class AppStorage():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance       
    def __init__(self) -> None:
        self.__path=os.path.dirname(os.path.abspath(__file__))+'/appdata.db'
        self.__add_login_info_sql=fr'''INSERT INTO LOGININFO (ID,PROJECT,CLASS,AREA,PROTOCOL,PORT,USERNAME,PASSWORD,SECRET,IP_EXPRESSION)
                            VALUES (?,?,?,?,?,?,?,?,?,?)'''
        self.__check_project_sql=fr'''SELECT PROJECT FROM LOGININFO WHERE PROJECT=?'''
        if not os.path.exists(self.__path):
            try:
                con=sqlite3.connect(self.__path)
                cur=con.cursor()
                cur.execute(
                    '''CREATE TABLE  LOGININFO(
                ID             TEXT    PRIMARY KEY NOT NULL,
                PROJECT        TEXT    NOT NULL,
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
                uid =str(uuid.uuid4())
                suid=''.join(uid.split('-'))
                cur.execute(self.__add_login_info_sql,[suid]*10)
                con.commit()
                print('-----------------创建成功-------------------')
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
            uid =str(uuid.uuid4())
            suid=''.join(uid.split('-'))
            value_list=list(login_dict.values())
            value_list.insert(0,suid)
            con=sqlite3.connect(self.__path,check_same_thread=False)
            cur=con.cursor()
            cur.execute(self.__add_login_info_sql,value_list)
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
    def check_project(self,check_project_str):       
        try:
            project_tuple=tuple([check_project_str])
            con=sqlite3.connect(self.__path,check_same_thread=False)
            cur=con.cursor()
            cur.execute(self.__check_project_sql,project_tuple)
            result=cur.fetchall()
            if len(result)<=0:
                return True  
            else:
                return False
        except sqlite3.Error as e:
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
