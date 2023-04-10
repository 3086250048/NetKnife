import { send_post,get_time, send_get, pop_info } from "./tools";


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
            state.command_index=-1
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
                console.log('发送add_command_history')
                send_post('/add_command_history',{
                    'project':state.choose_project[0],
                    'area':payload.choose_mixunit[3],
                    'protocol':payload.choose_mixunit[4],
                    'port':payload.choose_mixunit[5],
                    'ip_expression':payload.choose_mixunit[9],
                    'mode':state.oprate_mode,
                    'command':payload.command,
                    'response':state.response_data_list,
                    'date_time':state.response_date_time
                },response=>{
                    if (response.data==='LIMIT'){
                        state.vm.$message({
                            showClose: true,
                            message: '记录的命令已经达到上限,将删除最早的一条命令后继续记录',
                            type: 'warning'
                          });
                    }
                    send_post('/get_command_history_count',{
                        'project':state.choose_project[0],
                        'area':payload.choose_mixunit[3],
                        'protocol':payload.choose_mixunit[4],
                        'port':payload.choose_mixunit[5],
                        'ip_expression':payload.choose_mixunit[9],
                        'mode':state.oprate_mode,
                    },response=>{
                        state.history_command_count=response.data
                    })
                },reason=>{
                    console.log(reason)
                })
                console.log("已经发送")
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
                            state.textarea+=`===============================================================================\n设备类型:${item.type}  设备登录IP:${item.ip}  设备登录端口:${item.port}\n时间:${state.response_date_time}\n===============================================================================`+'\n'+item.response
                            flag=false
                        }else{
                            state.textarea+=`\n===============================================================================\n设备类型:${item.type}  设备登录IP:${item.ip}  设备登录端口:${item.port}\n时间:${state.response_date_time}\n===============================================================================`+'\n'+item.response
                        }
                       
                    }
                }) 
            });
        },
        SET_OPRATE_MODE(state,mode){
            state.oprate_mode=mode
        },
        ROLLBACK_COMMAND(state){
            state.command_index+=1
            state.response_data_list=[]
            state.textarea=''
            state.history_command=''
            send_post('/get_command_history',{
                'mode':state.oprate_mode,
                'project':state.choose_project[0],
                'area':state.choose_mixunit[3],
                'protocol':state.choose_mixunit[4],
                'port':state.choose_mixunit[5],
                'ip_expression':state.choose_mixunit[9],
                'index':state.command_index,
            },response=>{
                state.loading_able=false
                state.response_data_list=response.data['response']
                state.response_date_time=response.data['date_time']
                state.history_command=response.data['command']
            })
            
        },
        NEXT_COMMAND(state){
            state.command_index-=1
            state.response_data_list=[]
            state.textarea=''
            state.history_command=''
            send_post('/get_command_history',{
                'mode':state.oprate_mode,
                'project':state.choose_project[0],
                'area':state.choose_mixunit[3],
                'protocol':state.choose_mixunit[4],
                'port':state.choose_mixunit[5],
                'ip_expression':state.choose_mixunit[9],
                'index':state.command_index
            },response=>{
                state.loading_able=false
                state.response_data_list=response.data['response']
                state.response_date_time=response.data['date_time']
                state.history_command=response.data['command']
            })
         
        },
        SET_COMMAND_INDEX(state,index){
            state.command_index=index
        },
        SET_HISTORY_COMMAND_COUNT(state){
            send_post('/get_command_history_count',{
                'project':state.choose_project[0],
                'area':state.choose_mixunit[3],
                'protocol':state.choose_mixunit[4],
                'port':state.choose_mixunit[5],
                'ip_expression':state.choose_mixunit[9],
                'mode':state.oprate_mode,
            },response=>{
                console.log(response.data)
                state.history_command_count=response.data
               
            })
        },
        EXPORT_TEXTAREA(state,payload){
            if(payload.command.length<=0){
                payload.vm.$message({
                    showClose: true,
                    message: '导出失败。',
                    type: 'error'
                  });
                return
            }
            send_post('/export_textarea',{
                'textarea':state.textarea,
                'command':payload.command,
                'txt_export_path':payload.txt_export_path
            },response=>{
                if(response.data==='EXPORT_SUCCESS'){
                    payload.vm.$message({
                        showClose: true,
                        message: '导出成功',
                        type: 'success'
                      });
                }else{
                    payload.vm.$message({
                        showClose: true,
                        message: '导出失败',
                        type: 'error'
                      });
                }
            })
        },
        GET_ALL_COMMAND_TIME(state){
            state.all_command_time_list=[]
            state.all_command_time_search_list=[]
            send_post('/get_all_command_time',{
                'project':state.choose_project[0],
                'area':state.choose_mixunit[3],
                'protocol':state.choose_mixunit[4],
                'port':state.choose_mixunit[5],
                'ip_expression':state.choose_mixunit[9],
                'mode':state.oprate_mode,
            },response=>{
                console.log(response.data)
                response.data.forEach(e=>{
                    state.all_command_time_search_list.push({'value':`${e.value[0]} | ${e.value[1]}`})
                    state.all_command_time_list.push([e.value[0],e.value[1],e.value[2]])
                })
                state.full_all_command_time_list=state.all_command_time_list
            })
        },
        CHOOSE_CHANGE(state,item){
            send_post('/get_all_command_time',{
            'project':state.choose_project[0],
            'area':state.choose_mixunit[3],
            'protocol':state.choose_mixunit[4],
            'port':state.choose_mixunit[5],
            'ip_expression':state.choose_mixunit[9],
            'mode':state.oprate_mode,
            'search':item.value,
        },response=>{
            state.all_command_time_list=[]
            response.data.forEach(e=>{
                state.all_command_time_list.push([e.value[0],e.value[1],e.value[2]])
            })
            })
        },
        ROLLBACK_MIXUNIT_LIST(state){
            state.all_command_time_list=state.full_all_command_time_list
        },
        SHOW_HISTORY_COMMAND(state,payload){
            state.response_data_list=[]
            state.textarea=''
            state.history_command=''
            state.command_index=payload.index
            send_post('/get_command_history',{
                'mode':state.oprate_mode,
                'project':state.choose_project[0],
                'area':state.choose_mixunit[3],
                'protocol':state.choose_mixunit[4],
                'port':state.choose_mixunit[5],
                'ip_expression':state.choose_mixunit[9],
                'command':payload.command,
                'date_time':payload.date_time
            },response=>{
                state.loading_able=false
                state.response_data_list=response.data['response']
                state.response_date_time=response.data['date_time']
                state.history_command=response.data['command']
            })
        },
        DELETE_HISTORY_COMMAND(state,payload){
            state.response_data_list=[]
            state.textarea=''
            state.history_command=''
            state.command_index=-1
            send_post('/delete_history_command',{
                'mode':state.oprate_mode,
                'id':payload.id,
                'project':state.choose_project[0],
                'area':state.choose_mixunit[3],
                'protocol':state.choose_mixunit[4],
                'port':state.choose_mixunit[5],
                'ip_expression':state.choose_mixunit[9],
                'command':payload.command,
                'date_time':payload.date_time
            },response=>{
                if(response.data==='DELETE_SUCCESS'){     
                    state.all_command_time_list=[]
                    state.all_command_time_search_list=[]              
                    send_post('/get_all_command_time',{
                        'project':state.choose_project[0],
                        'area':state.choose_mixunit[3],
                        'protocol':state.choose_mixunit[4],
                        'port':state.choose_mixunit[5],
                        'ip_expression':state.choose_mixunit[9],
                        'mode':state.oprate_mode,
                    },response=>{
                        response.data.forEach(e=>{
                            state.all_command_time_search_list.push({'value':`${e.value[0]} | ${e.value[1]}`})
                            state.all_command_time_list.push([e.value[0],e.value[1],e.value[2]])
                        })
                        state.full_all_command_time_list=state.all_command_time_list
                    })

                    send_post('/get_command_history_count',{
                        'project':state.choose_project[0],
                        'area':state.choose_mixunit[3],
                        'protocol':state.choose_mixunit[4],
                        'port':state.choose_mixunit[5],
                        'ip_expression':state.choose_mixunit[9],
                        'mode':state.oprate_mode,
                    },response=>{
                        state.history_command_count=response.data    
                    })
                    
                }
            })
        },
        SET_VM(state,vm){
            state.vm=vm
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
        oprate_mode:'project',
        command_index:-1,
        history_command:'',
        history_command_count:0,
        all_command_time_list:[],
        all_command_time_search_list:[],
        full_all_command_time_list:[],
        vm:{}

    }
}
