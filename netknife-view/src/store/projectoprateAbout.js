import { send_post,get_time, send_get } from "./tools";


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
        COMMIT_COMMAND(state,payload){
            state.loading_able=true
            state.response_data_list=[]
            state.textarea=''
            send_post('/commit_command',{
                'base_effect_range':state.choose_project[0],
                'mixunit':state.choose_mixunit,
                'mode':state.oprate_mode,
                'command':payload.command,
                'send_parameter':{
                    strip_prompt:payload.send_parameter.device_title_able,
                    strip_command:payload.send_parameter.command_able,
                    read_timeout:payload.send_parameter.read_timeout,
                },
                'path_parameter':{
                    txt_export_path:payload.path_parameter.txt_export_path,
                    ftp_root_path:payload.path_parameter.ftp_root_path,
                    ftp_upload_path:payload.path_parameter.ftp_upload_path,
                    ftp_download_path:payload.path_parameter.ftp_download_path
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
        SET_CHOOSE_MIXUNIT(state,mixunit){
            state.choose_mixunit=mixunit
        },
        SET_EFFECT(state,command){
            console.log(state.oprate_mode)
           if (this.time!==undefined){clearTimeout(this.time)}
           this.time=setTimeout(() => {
                send_post('/get_effect_data',{
                    'base_effect_range':state.choose_project[0],
                    'extra_effect_range':state.choose_mixunit,
                    'command':command,
                    'mode':state.oprate_mode
                },response=>{
                    state.effect_connect_percent=response.data['effect_connect_percent']
                },reason=>{  
                })
            }, 100);
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
        },
        GET_SEND_COMMAND_PARAMETER(){
            send_post('/')
        },
        SET_OPRATE_MODE(state,mode){
            state.oprate_mode=mode
        }
    },
    state:{
        textarea:'',
        choose_project:[],
        choose_mixunit:[],
        effect_connect_percent:0,
        response_data_list:[],
        response_date_time:'',
        loading_able:false,
        oprate_mode:'project'
    }
}
