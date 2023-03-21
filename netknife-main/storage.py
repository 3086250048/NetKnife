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
        
        #初始化创建数据库和表
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

    #返回一个sql语句,要求附带数据
    #例子:
    #init_sql=select * from logininfo | first_sql=where | loop_sql=and
    #data_dict={'project':'a',area:'',protocol:'b'}
    #得到 select * from logininfo where project=a and protocol=b
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
    
    #迭代出一个sql语句
    #例子:
    #init_sql=select * from logininfo | first_sql=where | field_sql=project
    #data_list=['a','b','c']
    #迭代三次得到
    #1.select * from logininfo where project=a
    #2.select * from logininfo where project=b
    #3.select * from logininfo where project=c
    @classmethod
    def dynamic_sql_yield (cls,init_sql,first_sql,field_sql,data_list):
        sql=''
        for v in data_list:
            sql+=f'{init_sql} {first_sql} {field_sql}=\'{v}\''
            yield sql
            sql=''

    #执行sql语句,data可以传入空字典{},call_back为执行sql语句之后的回调函数
    #返回:回调函数决定,发生异常返回False
    #传入:sql语句,sql数据{}(可为空),回调函数(决定返回数值)
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

    #向数据库中插入数据
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:'',ip_expression:'',username:'',password:'',secret:''} 
    def add_login_info(self,login_dict)->bool:
        uid =str(uuid.uuid4())
        suid=''.join(uid.split('-'))
        value_list=list(login_dict.values())
        value_list.insert(0,suid)
        def callback(cur,con):
            con.commit()
            return True
        return self.oprate_sql(self.__add_login_info_sql,value_list,callback)

    #检查数据库中是否存在某个最小单元
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:'',ip_expression:''} 
    def check_quads(self,check_quads_dict)->bool:
        sql=AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',check_quads_dict)
        def callback(cur,con):
            result=cur.fetchall()
            if len(result)<=0:
                return True
            else:
                return False
        return self.oprate_sql(sql,check_quads_dict,callback)    
    
    #检查数据库中是否存在某条记录
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:''....} 
    def check_where(self,where_dict)->bool:
        def callback(cur,con):
            result=cur.fetchall()
            if len(result)<=0:
                return True
            return False
        return self.oprate_sql(AppStorage.dynamic_sql_return('SELECT * FROM LOGININFO','WHERE','AND',where_dict),where_dict,callback)
    
    #更新数据库中某条记录
    #返回:布尔值
    #传入:
    #条件数据:{'projet':'',area:'',protocol:'',port:''....} 
    #更新数据:{'projet':'',area:'',protocol:'',port:''....}
    def update_data(self,where_dict,update_data_dict)->bool:
        def callback_after(cur,con):
            con.commit()
            return True
        where_sql=AppStorage.dynamic_sql_return('','where','and',where_dict)
        update_sql=AppStorage.dynamic_sql_return('update logininfo','set',',',update_data_dict)
        sql=update_sql+where_sql
        return self.oprate_sql(sql,{},callback_after)

    #删除数据库中某条记录
    #返回:布尔值
    #传入:{'projet':'',area:'',protocol:'',port:''....}
    def delete_data(self,where_dict) -> bool:
        def callback(cur,con):
            con.commit()
            return True
        delete_sql=AppStorage.dynamic_sql_return('DELETE FROM LOGININFO','WHERE','AND',where_dict)
        return self.oprate_sql(delete_sql,where_dict,callback)
    
    #得到数据库中以project为查询条件的最小单元列表
    #返回:[['projetc1','area1 、area2','protocol1 ; protocol2','port1 ; port2','ip_expression'],[...]]
    def get_project_unit_list(self) -> list:
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
    
    #获取数据库中所有的项目名称
    #返回:[{'value':'project1'},{'value':'project2'},{'project3':'project3'}]
    def get_all_project_list(self)-> list:
        def callback(cur,con):
            return cur.fetchall()
        _lis= self.oprate_sql('SELECT DISTINCT project FROM LOGININFO;',{},callback)[1:]
        result= [ {'value':v[0]} for v in _lis]
        return result

    #获取数据库中满足某个查询条件时的ip_expression表达式。
    #返回:[1.1.1.1,192.168.1.1-100%2,....]
    #传入:{'project':'','area':'','protocol':'','port':'','ip_expression':'',....}
    def get_effect_ip_expression_list(self,effect_range_dict) -> list:
        effect_number_sql=AppStorage.dynamic_sql_return('SELECT IP_EXPRESSION FROM LOGININFO','WHERE','AND',effect_range_dict)
        def callback(cur,con):
            return cur.fetchall()
        result_lis=[ v[0] for v in self.oprate_sql(effect_number_sql,{},callback)]
        return result_lis
       
    #获取登录设备时需要的信息。
    #返回:{'class':'','protocol':'','port':'','ip_expression':'','username':‘’,'password':'','secret':''}
    #传入:{'project':'','area':'','protocol':'','port':'','ip_expression':'',.....}
    def get_full_login_list(self,effect_range_dict):
        effect_number_sql=AppStorage.dynamic_sql_return('SELECT CLASS,PROTOCOL,PORT,IP_EXPRESSION,USERNAME,PASSWORD,SECRET FROM LOGININFO','WHERE','AND',effect_range_dict)
        def callback(cur,con):
            return cur.fetchall()
        result=self.oprate_sql(effect_number_sql,{},callback)
        return result

    def select_count(self):
        def callback(cur,con):
            return cur.fetchall()
        result=self.oprate_sql('select count(*) from logininfo',{},callback)
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