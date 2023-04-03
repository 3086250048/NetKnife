class AppAction():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance           
    def export(self,parameter,content):
        with open(parameter, "w") as file:
            file.write(content)
            print('写入了')
    def action_class_map(self,action_class,parameter,content):
        action_map={
            'export':self.export  
        }
        action_map[action_class](parameter,content)

    
    