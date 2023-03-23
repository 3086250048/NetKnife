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
                state.response_data_list=response.data
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
        },
        SET_TEXT_AREA(state,check_list){
            state.textarea=''
            state.response_data_list.forEach(item => {
                check_list.forEach(e=>{
                    if(item.type+item.ip+':'+item.port===e){
                        state.textarea+=item.response
                    }
                }) 
            });
        }
    },
    state:{
        textarea:'',
        choose_project:[],
        effect_connect_percent:0,
        response_data_list:[]
    }
}
