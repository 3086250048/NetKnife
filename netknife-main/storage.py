import sqlite3,os,uuid

class AppStorage():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance       
    def __init__(self) -> None:
        self.__path=os.path.dirname(os.path.abspath(__file__))+'/appdata.db'
        self.__add_login_info_sql='''INSERT INTO LOGININFO (ID,PROJECT,CLASS,AREA,PROTOCOL,PORT,USERNAME,PASSWORD,SECRET,IP_EXPRESSION)
                            VALUES (?,?,?,?,?,?,?,?,?,?);'''
        self.__check_project_sql='''SELECT PROJECT FROM LOGININFO WHERE PROJECT=?;'''  
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
    @classmethod
    def dynamic_sql(cls,init_sql,first_sql,loop_sql,data_dict):
        sql=''
        flag=True
        for k,v in data_dict.items():
            if v=='':
                continue
            if flag: 
                sql+=f'{init_sql} {first_sql} {k}=\'{v}\''
                flag=False
            else:
                sql+=f'{loop_sql} {k}=\'{v}\''
        return sql



    def oprate_sql(self,sql,data,call_back):
        try:
            con=sqlite3.connect(self.__path,check_same_thread=False)
            cur=con.cursor()
            cur.execute(sql,data)
            return call_back(cur,con) 
        except sqlite3.Error as e:
            print(e)
            con.rollback()
            return False
        finally:
            if cur:
                cur.close()
            if con:
                con.close()

    def add_login_info(self,login_dict):
        uid =str(uuid.uuid4())
        suid=''.join(uid.split('-'))
        value_list=list(login_dict.values())
        value_list.insert(0,suid)
        def callback(cur,con):
            con.commit()
            return True
        return self.oprate_sql(self.__add_login_info_sql,value_list,callback)

    def check_project(self,check_project_str):
        project_tuple=tuple([check_project_str])
        def callback(cur,con):
            result=cur.fetchall()
            if len(result)<=0:
                return True
            else:
                return False
        return self.oprate_sql(self.__check_project_sql,project_tuple,callback)    
    def check_where(self,where_dict):
        def callback(cur,con):
            result=cur.fetchall()
            print(result)
            if len(result)<=0:
                return True
            return False
        return self.oprate_sql(AppStorage.dynamic_sql('SELECT * FROM LOGININFO','WHERE','AND',where_dict),where_dict,callback)
    def update_data(self,where_dict,update_data_dict):
        def callback(cur,con):
            result=cur.fetchall()
            print(result)
            con.commit()
            return True
        where_sql=AppStorage.dynamic_sql('','where','and',where_dict)
        update_sql=AppStorage.dynamic_sql('update logininfo','set',',',update_data_dict)
        print(where_sql)
        print(update_sql)
        sql=update_sql+where_sql
        return self.oprate_sql(sql,update_data_dict,callback)
    def delete_data(self,where_dict):
        def callback(cur,con):
            con.commit()
            return True
        delete_sql=AppStorage.dynamic_sql('DELETE FROM LOGININFO','WHERE','AND',where_dict)
        return self.oprate_sql(delete_sql,where_dict,callback)
if __name__ == '__main__':
    ap=AppStorage()
    # s1.add_login_info()
    dic={'project': '212121212', 'class': '22', 'area': '22', 'protocol': '', 'port': '2', 'username': '2', 'password': '2', 'secret': '', 'ip_expression': ''}
    where_sql=AppStorage.dynamic_sql('','where','and',dic)
    update_sql=AppStorage.dynamic_sql('update logininfo','set',',',dic)
    print(update_sql+where_sql)