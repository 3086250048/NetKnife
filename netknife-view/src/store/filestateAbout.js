import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filestateAbout={
    namespaced:true,
    actions:{
    },
    mutations:{    
        GET_NETKNIFE_DATA(state){
            send_get('/get_netknife_file_data',response=>{
                if (response.data==='NOT_EXIST'){return}
                state.netknife_data=response.data
                state.netknife_data.forEach(e=>{
                    if(e['translation'].length<=0){
                        e['translation_class']='el-icon-circle-close'
                    }else{
                      e['translation_class']='el-icon-success'
                    }
                    if(e['jinja2'].length<=0){
                        e['jinja2_class']='el-icon-circle-close'
                    }else{
                      e['jinja2_class']='el-icon-success'
                    }
                    if(e['excute'].length<=0){
                        e['excute_class']='el-icon-circle-close'
                    }else{
                      e['excute_class']='el-icon-success'
                    } 
                    if(e['config'].length<=0){
                        e['config_class']='el-icon-circle-close'
                    }else{
                        e['config_class']='el-icon-success'
                    }
                })
            })   
        }
        
    },
    state:{
        netknife_data:[]
    }
}