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
        self.__get_project_list_sql='''SELECT PROJECT FROM LOGININFO GROUP BY PROJECT ;'''
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
                IP_EXPRESSION   TEXT    NOT NULL,
                UNIQUE(PROJECT,AREA,PORT,PROTOCOL,IP_EXPRESSION)
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
    def dynamic_sql_return (cls,init_sql,first_sql,loop_sql,data_dict):
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
        
    @classmethod
    def dynamic_sql_yield (cls,init_sql,first_sql,field_sql,data_list):
        sql=''
        for v in data_list:
            sql+=f'{init_sql} {first_sql} {field_sql}=\'{v}\''
            yield sql
            sql=''

    def oprate_sql(self,sql,data,call_back,*args):
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

    def check_quads(self,check_quads_dict):
        sql=AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',check_quads_dict)
        def callback(cur,con):
            result=cur.fetchall()
            if len(result)<=0:
                return True
            else:
                return False
        return self.oprate_sql(sql,check_quads_dict,callback)    
    def check_where(self,where_dict):
        def callback(cur,con):
            result=cur.fetchall()
            print(result)
            if len(result)<=0:
                return True
            return False
        return self.oprate_sql(AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',where_dict),where_dict,callback)
    def update_data(self,where_dict,update_data_dict):
        def callback_after(cur,con):
            con.commit()
            return True
        where_sql=AppStorage.dynamic_sql_return('','where','and',where_dict)
        update_sql=AppStorage.dynamic_sql_return('update logininfo','set',',',update_data_dict)
        sql=update_sql+where_sql
        return self.oprate_sql(sql,{},callback_after)

    def delete_data(self,where_dict):
        def callback(cur,con):
            con.commit()
            return True
        delete_sql=AppStorage.dynamic_sql_return('DELETE FROM LOGININFO','WHERE','AND',where_dict)
        return self.oprate_sql(delete_sql,where_dict,callback)
    
    def get_project_unit_list(self):
        def callback(cur,con):
            return cur.fetchall()
        project_list=[ v[0] for v in self.oprate_sql(self.__get_project_list_sql,{},callback)[1:]]

        project_sql_gen=AppStorage.dynamic_sql_yield('select project,area,protocol,port,ip_expression from logininfo','where','project',project_list)
        lis=[]
        for _ in range(len(project_list)):
            def callback(cur,con):
                return cur.fetchall()
            project_sql=project_sql_gen.__next__()
            lis+=[self.oprate_sql(project_sql,{},callback)]
        dic={'project':'','area':'','protocol':'','port':'',"ip_expression":''}
        result=[]
        for i in lis:
            n=0
            for j in i:    
                if n!=0:
                    if j[0] not in dic['project']:
                        dic['project']+=j[0] 
                    if j[1] not in dic['area']:
                        dic['area']+=' 、'+j[1]
                    if j[2] not in  dic['protocol']:
                        dic['protocol']+='  ； '+j[2]
                    if j[3] not in  dic['port']:
                        dic['port']+='  ； '+j[3]
                    if j[4] not in dic['ip_expression']:
                        dic['ip_expression']+='  ； '+j[4]
                else:
                    if j[0] not in dic['project']:
                        dic['project']+=j[0]
                    if j[1] not in dic['area']:
                        dic['area']+=j[1]
                    if j[2] not in dic['protocol']:
                        dic['protocol']+=j[2]
                    if j[3] not in dic['port']:
                        dic['port']+=j[3]
                    if j[4] not in dic['ip_expression']:
                        dic['ip_expression']+=j[4]
                n+=1
            result+=[list(dic.values())]
            dic={'project':'','area':'','protocol':'','port':'',"ip_expression":''}
        return result
    def get_all_project_list(self):
        def callback(cur,con):
            return cur.fetchall()
        _lis= self.oprate_sql('SELECT DISTINCT project FROM LOGININFO;',{},callback)[1:]
        result= [ {'value':v[0]} for v in _lis]
        return result
     

        
        
if __name__ == '__main__':
    ap=AppStorage()
    # s1.add_login_info()
    # dic={'project': '212121212', 'class': '22', 'area': '22', 'protocol': '', 'port': '2', 'username': '2', 'password': '2', 'secret': '', 'ip_expression': ''}
    # where_sql=AppStorage.dynamic_sql('','where','and',dic)
    # update_sql=AppStorage.dynamic_sql('update logininfo','set',',',dic)
    # print(update_sql+where_sql)
    # project_list=ap.get_project_unit_tuple()
    # list1=[ v[0] for v in list]
    print(ap.get_project_unit_list())
    # AppStorage.dynamic_sql_yield('select * from logininfo','where',)