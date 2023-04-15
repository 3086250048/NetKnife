import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filecreateAbout={
    namespaced:true,
    actions:{
        create_netknife_file(context,code){
            context.state.code=code
            send_post('/check_netknife_file_if_exist',{'code':context.state.code},response=>{
                   if(response.data==='SYNTAX_ERROR'){
                        context.state.vm.$message({
                            showClose: true,
                            message: '语法错误',
                            type: 'warning'
                          });
                   }
                   if(response.data==='EXIST'){
                        context.state.vm.$message({
                            showClose: true,
                            message: '文件已经存在',
                            type: 'warning'
                        });
                   }
                   if(response.data==='NOT_EXIST'){
                        context.commit('CREATE_NETKNIFE_FILE')
                   }
            })
        },
        delete_netknife_file(context,code){
            context.state.code=code
            send_post('/check_netknife_file_if_exist',{'code':context.state.code},response=>{
                if(response.data==='SYNTAX_ERROR'){
                     context.state.vm.$message({
                         showClose: true,
                         message: '语法错误',
                         type: 'warning'
                       });
                }
                if(response.data==='NOT_EXIST'){
                    context.state.vm.$message({
                        showClose: true,
                        message: '文件不存在',
                        type: 'warning'
                    });
                }
                if(response.data==='EXIST'){
                    context.commit('DELETE_NETKNIFE_FILE')
                }
               
         })
        },
        update_netknife_file(context,code){
            context.state.code=code
            send_post('/check_netknife_file_if_exist',{'code':context.state.code},response=>{
                if(response.data==='SYNTAX_ERROR'){
                     context.state.vm.$message({
                         showClose: true,
                         message: '语法错误',
                         type: 'warning'
                       });
                }
                if(response.data==='NOT_EXIST'){
                    context.state.vm.$message({
                        showClose: true,
                        message: '文件不存在',
                        type: 'warning'
                    });
                }
                if(response.data==='EXIST'){
                    context.commit('UPDATE_NETKNIFE_FILE')
                }
               
         })
        }
    },
    mutations:{         
        CREATE_NETKNIFE_FILE(state){
            console.log(state.code)
            send_post('/create_netknife_file',{
            'code':state.code
            },response=>{
                if(response.data==='SYNTAX_ERROR'){
                    state.vm.$message({
                        showClose: true,
                        message: '语法错误',
                        type: 'warning'
                      });
                }
                else if(response.data==='ADD_FAULT'){
                    state.vm.$message({
                        showClose: true,
                        message: '创建失败',
                        type: 'error'
                      });
                }
                else{
                    state.file_name=response.data
                    state.vm.$message({
                        showClose: true,
                        message: '创建成功',
                        type: 'success'
                        });
                    state.vm.$bus.$emit('change',state.file_name+'')
                }
            })
        },
        DELETE_NETKNIFE_FILE(state){
            send_post('/delete_netknife_file',{
                'code':state.code
                },response=>{
                    console.log(response.data)
                    if(response.data==='DELETE_FAULT'){
                        state.vm.$message({
                            showClose: true,
                            message: '删除失败',
                            type: 'warning'
                          });
                    }
                    if(response.data==='DELETE_SUCCESS'){
                        state.vm.$message({
                            showClose: true,
                            message: '删除成功',
                            type: 'success'
                          });
                    }
                })
        },
        UPDATE_NETKNIFE_FILE(state){
            send_post('/change_netknife_file',{
                'code':state.code
                },response=>{
                    if(response.data==='SYNTAX_ERROR'){
                        state.vm.$message({
                            showClose: true,
                            message: '语法错误',
                            type: 'warning'
                          });
                    }
                    if(response.data==='CHANGE_FAULT'){
                        state.vm.$message({
                            showClose: true,
                            message: '更新失败',
                            type: 'warning'
                          });
                    }
                    if(response.data==='CHANGE_SUCCESS'){
                        state.vm.$message({
                            showClose: true,
                            message: '更新成功',
                            type: 'success'
                          });
                    }
                })
        },
        SET_VM(state,vm){
            state.vm=vm
        }
    },
    state:{
        code:'',
        vm:'',
        file_name:''
    }
}