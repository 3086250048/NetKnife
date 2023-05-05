import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filemanageAbout={
    namespaced:true,
    actions:{
    },
    mutations:{         
        SET_TITLE(state,title){
            state.title=title
        },
        HANDLER_RESPONSE_DATA(state,response_data){
            state.excute_response_data=[]
            for(let i=0;i<response_data.length;i++){
                console.log(response_data[i])
                state.excute_response_data.push(response_data[i])
            }
            console.log(state.excute_response_data)
            send_post('/add_netknife_excute_result',{'file_name':state.title,'excute_result':state.excute_response_data,'date_time':state.response_date_time})
        },
        SET_EXCUTE_TEXT(state,check_list){
            state.excute_text=''
            state.excute_response_data.forEach(element=>{
                check_list.forEach(e=>{
                    if(`${element.fun_name}${element.ip}${element.port}${element.type}`===e ){
                        
                        state.excute_text+=`设备类型:${element.type}  设备登录IP:${element.ip}  设备登录端口:${element.port}\n`
                        state.excute_text+=`时间:${state.response_date_time} 函数名:${element.fun_name}\n`
                        state.excute_text+=element.response+'\n\n'                   
                    }
                }) 
            });
        },
        SET_RESPONSE_DATE_TIME(state,time){
            state.response_date_time=time
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


    },
    state:{
        title:'',
        excute_response_data:[],
        excute_text:'',
        response_date_time:'',
        code_index:-1,
        history_code:'',
        history_code_count:0,
        all_excute_result_search_list:[],
        all_excute_result_list:[],
        full_excute_result_list:[]
    }
}