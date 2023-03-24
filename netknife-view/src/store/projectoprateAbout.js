import { send_post,get_time } from "./tools";


export const  projectoprateAbout={
    namespaced:true,
    actions:{},
    mutations:{
        SET_GO_BACK_STATE(state){
            state.textarea=''
            state.response_data_list=[]
            state.effect_connect_percent=0
            state.loading_able=false
        },
        COMMIT_COMMAND(state,command,parameter_dict){
            state.loading_able=true
            state.response_data_list=[]
            state.textarea=''
            send_post('/commit_command',{
                'base_effect_range':state.choose_project[0],
                'command':command,
                'parameter':{
                    expect_string:'none',
                    read_timeout:10.0,
                    delay_factor:'none',
                    max_loops:'none',
                    auto_find_prompt:true,
                    strip_prompt:true,
                    strip_command:true,
                    normalize:true,
                    use_textfsm:false,
                    textfsm_template:'none',
                    use_ttp:false,
                    ttp_template:'none',
                    use_genie:false,
                    cmd_verify:true,
                }
            },response=>{
                state.loading_able=false
                state.response_data_list=[]
                state.response_data_list=response.data
                state.response_date_time=get_time()
            },reason=>{
                state=false
            
            })
        },
        SET_CHOOSE_PROJECT(state,project){
            state.choose_project=project
        },
        SET_EFFECT(state,command){
           if (this.time!==undefined){clearTimeout(this.time)}
           this.time=setTimeout(() => {
                send_post('/get_effect_data',{
                    'base_effect_range':state.choose_project[0],
                    'command':command,
                    
                },response=>{
                    state.effect_connect_percent=response.data['effect_connect_percent']
                },reason=>{  
                })
            }, 300);
        },
        SET_TEXT_AREA(state,check_list){
            state.textarea=''
            let flag=true
            state.response_data_list.forEach(item => {
                check_list.forEach(e=>{
                    if(item.type+item.ip+':'+item.port===e ){
                        if(flag){
                            state.textarea+=`===============================================================================\n设备类型:${item.type}  设备登录IP:${item.ip}  设备登录端口:${item.port}\n时间:${state.response_date_time}\n===============================================================================`+item.response
                            flag=false
                        }else{
                            state.textarea+=`\n===============================================================================\n设备类型:${item.type}  设备登录IP:${item.ip}  设备登录端口:${item.port}\n时间:${state.response_date_time}\n===============================================================================`+item.response
                        }
                       
                    }
                }) 
            });
        }
    },
    state:{
        textarea:'',
        choose_project:[],
        effect_connect_percent:0,
        response_data_list:[],
        response_date_time:'',
        loading_able:false
    }
}
