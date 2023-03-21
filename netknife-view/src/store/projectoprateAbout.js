import { send_post,pop_info } from "./tools";


export const  projectoprateAbout={
    namespaced:true,
    actions:{},
    mutations:{
        COMMIT_COMMAND(state,command){
            //goback的时候清空textarea中内容
            if(command===''){
                state.textarea=''
                state.effect_connect_percent=0
                return
            }
            //
            send_post('/commit_command',{
                'base_effect_range':state.choose_project[0],
                'command':command
            },response=>{
                console.log(response.data)
                state.textarea=''
                state.textarea=response.data.toString()
            },reason=>{
            
            })
        },
        SET_CHOOSE_PROJECT(state,project){
            state.choose_project=project
        },
        SET_EFFECT(state,command){
           if (this.time!==undefined){clearTimeout(this.time)}
           this.time=setTimeout(() => {
                send_post('/get_effect_data',{'base_effect_range':state.choose_project[0],'command':command},response=>{
                    console.log(response.data)
                    state.effect_connect_percent=response.data['effect_connect_percent']
        
                },reason=>{  
                })
            }, 300);
        }
    },
    state:{
        textarea:'test',
        choose_project:[],
        effect_connect_percent:0
    }
}
