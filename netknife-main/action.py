class AppAction():
    def __new__(cls,*args, **kwds):
        if not hasattr(cls,'_instance'):
            cls._instance=super().__new__(cls,*args,**kwds)
        return cls._instance           
    def export(self,parameter,content):
        with open(parameter, "w") as file:
            file.write(content)
    def action_main(self,action_command,parameter,content):
        action_map={
            'export':self.export
        }
        action_map[action_command](parameter,content)

    
    