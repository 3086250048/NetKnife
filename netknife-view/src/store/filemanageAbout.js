import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filemanageAbout={
    namespaced:true,
    actions:{
    },
    mutations:{         
        SET_TITLE(state,title){
            state.title=title
        },
        HANDLER_RESPONSE_DATA(state,payload){
            state.excute_response_data=[]
            state.excute_text=''
        
            for(let i=0;i<payload['response_data'].length;i++){
                // payload.vm.check_list.push(`${item.fun_name}${item.ip}${item.port}${item.type}`)
                state.excute_response_data.push(payload['response_data'][i])
            }
            console.log(state.response_date_time[payload.file_name])
            send_post('/add_netknife_excute_result',{'file_name':state.title,'excute_result':state.excute_response_data,'date_time':state.response_date_time[payload.file_name]})
        },
        SET_EXCUTE_TEXT(state,check_list){
            state.excute_text=''
            console.log(check_list)
            state.excute_response_data.forEach(element=>{
                check_list.forEach(e=>{
                    if(`${element.fun_name}${element.ip}${element.port}${element.type}`===e ){
                        
                        state.excute_text+=`设备类型:${element.type}  设备登录IP:${element.ip}  设备登录端口:${element.port}\n`
                        if(state.if_history_time){
                            state.excute_text+=`时间:${element.date_time} 函数名:${element.fun_name}\n`
                        }else{
                            state.excute_text+=`时间:${state.response_date_time[state.title]} 函数名:${element.fun_name}\n`
                        }
                      
                        state.excute_text+=element.response+'\n\n'                   
                    }
                }) 
            });
        },
        CLEAR_EXCUTE_TEXT(state){
            state.excute_text=''
        },
        SET_RESPONSE_DATE_TIME(state,payload){
            state.response_date_time[payload.file_name]=payload.date_time
        },
        SET_EXCUTE_RESPONSE_DATA(state,data){
            state.excute_response_data=data
        },
    // 导出按钮
    EXPORT_TEXTAREA(state,payload){
        if(payload.file_name.length<=0){
            payload.vm.$message({
                showClose: true,
                message: '导出失败。',
                type: 'error'
            });
            return
        }
        send_post('/export_excute_result_textarea',{
            'excute_text':state.excute_text,
            'file_name':payload.file_name,
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
    //历史命令按钮
    GET_ALL_EXCUTE_DATE_TIME(state,file_name){
        state.all_excute_date_time_list=[]
        state.all_excute_date_time_search_list=[]
        console.log(file_name)
        send_post('/get_all_excute_date_time',{
           'file_name':file_name
        },response=>{
            console.log(response.data)
            state.all_excute_date_time_search_list=response.data
            response.data.forEach(e=>{
                state.all_excute_date_time_list.push(e['value'])
            })
            state.full_excute_result_list=state.all_excute_date_time_list
        })

    },
    CHOOSE_CHANGE(state,item,file_name){
        send_post('/get_all_excute_date_time',{
        'file_name':file_name,
        'date_time':item
    },response=>{
        state.all_excute_date_time_list=[]
        response.data.forEach(e=>{
            state.all_excute_date_time_list.push(e.value)
        })
        })
    },
    ROLLBACK_EXCUTE_RESULT_LIST(state){
        state.all_excute_date_time_list=state.full_excute_result_list
    },
    SHOW_HISTORY_COMMAND(state,payload){
        state.excute_response_data=[]
        state.excute_text=''
        state.excute_index=payload.index
        send_post('/get_netknife_excute_result',{
            'file_name':payload.file_name,
            'date_time':payload.date_time
        },response=>{
            for(let i=0;i<response.data.length;i++){
                console.log(response.data[i])
                state.excute_response_data.push(response.data[i])
            }
        })

    },

    DELETE_HISTORY_COMMAND(state,payload){
        state.excute_response_data=[]
        state.excute_text=''
        state.command_index=-1
        send_post('/delete_netknife_excute_result',{
            'file_name':payload.file_name,
            'date_time':payload.date_time
        },response=>{
            if(response.data==='DELETE_NETKNIFE_EXCUTE_RESULT_SUCCESS'){     
                state.all_excute_date_time_list=[]
                state.all_command_time_search_list=[]              
                send_post('/get_all_excute_date_time',{
                    'file_name':payload.file_name
                 },response=>{
                     console.log(response.data)
                     state.all_excute_date_time_search_list=response.data
                     response.data.forEach(e=>{
                         state.all_excute_date_time_list.push(e['value'])
                     })
                     state.full_excute_result_list=state.all_excute_date_time_list
                 })

                send_post('/get_all_excute_date_count',{
                  'file_name':payload.file_name
                },response=>{
                    state.history_excute_result_count=response.data    
                })
                
            }
        })
    },

    SET_IF_HISTORY_TIME(state,bool){
        state.if_history_time=bool
    },

    // 回退和前进历史命令功能
    ROLLBACK_COMMAND(state,file_name){
        state.excute_index+=1
        state.excute_response_data=[]
        state.excute_text=''
        send_post('/get_history_netknife_excute_result',{
            'file_name':file_name,
            'index':state.excute_index,
        },response=>{
            state.if_history_time=true
            state.excute_response_data=response.data
        })
        
    },
    NEXT_COMMAND(state,file_name){
        state.excute_index-=1
        state.excute_response_data=[]
        state.excute_text=''
        send_post('/get_history_netknife_excute_result',{
            'file_name':file_name,
            'index':state.excute_index
        },response=>{
            state.if_history_time=true  
            state.excute_response_data=response.data
        })
     
    },

    SET_HISTORY_EXCUTE_RESULT_COUNT(state,file_name){
        send_post('/get_all_excute_date_count',{
            'file_name':file_name
          },response=>{
              state.history_excute_result_count=response.data    
              console.log(state.history_excute_result_count)
          })
    },
    SET_EXCUTE_INDEX(state,number){
        state.excute_index=number
    }

    },
    state:{
        title:'',
        excute_response_data:[],
        excute_text:'',
        response_date_time:{},
        excute_index:-1,
        history_excute_result_count:0,
        all_excute_date_time_list:[],
        all_excute_date_time_search_list:[],
        full_excute_result_list:[],
        if_history_time:false
    }
}