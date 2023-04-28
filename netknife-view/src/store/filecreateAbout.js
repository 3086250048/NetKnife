import { send_post,pop_info, send_get,findNonexistentItems,combineFromStartAndEnd, areListsEqual} from './tools'

export const filecreateAbout={
    namespaced:true,
    actions:{
        save_netknife_file(context,code){
            context.state.code=code
            send_post('/check_netknife_file_if_exist',{'code':context.state.code},response=>{
                if(response.data==='SYNTAX_ERROR'){
                     context.state.vm.$message({
                         showClose: true,
                         message: '语法错误',
                         type: 'warning'
                       });
                    console.log('语法错误')
                }
                if(response.data==='NOT_EXIST'){
                    console.log('不存在')
                   context.commit('CREATE_NETKNIFE_FILE')
                }
                if(response.data==='EXIST'){
                    console.log('存在')
                    context.commit('UPDATE_NETKNIFE_FILE')
                }
               
         })
        },
        delete_netknife_file(context,payload){
            context.state.code=payload['code']
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
                    context.commit('DELETE_NETKNIFE_FILE',payload['name'])
                }
               
         })
        },
        
    },
    mutations:{         
        CREATE_NETKNIFE_FILE(state){
            send_post('/create_netknife_file',{
            'code':state.code
            },response=>{
                console.log(response.data)
                if(response.data==='SYNTAX_ERROR'){
                    state.vm.$message({
                        showClose: true,
                        message: '语法错误',
                        type: 'warning'
                      });
                    return
                }
                if(response.data==='ADD_FAULT'){
                    state.vm.$message({
                        showClose: true,
                        message: '创建失败',
                        type: 'error'
                      });
                    return
                }
                state.file_name=response.data           
                state.vm.$bus.$emit('change_title',state.file_name+'')
                state.vm.$bus.$emit('change_code',state.vm.name,state.code)
                if(!state.vm.excute_flag){
                    state.vm.save_bt_style='primary'
                    send_post('/get_netknife_code',{'file_name':state.vm.title},response=>{
                        state.vm.storage_code=response.data
                    })
                    state.vm.$message({
                        showClose: true,
                        message: '创建成功',
                        type: 'success'
                        });
                  
                }else{
                    state.vm.excute_flag=false
                    state.vm.save_bt_style='primary'
                    send_post('/get_netknife_code',{'file_name':state.vm.title},response=>{
                        state.vm.storage_code=response.data
                    })
                    state.vm.$bus.$emit('excute',state.file_name)
                
                }      
            })
        },
        DELETE_NETKNIFE_FILE(state,name){
            send_post('/delete_netknife_file',{
                'code':state.code
                },response=>{
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
                        state.vm.$bus.$emit('change_title','空窗口')
                        state.vm.$bus.$emit('change_code',name,`name:\npriority:\n\nconfig:{\n\n  send:{\n  read_timeout:10.0\n   }\n\n}\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`)
                        state.vm.storage_code=`NOT_EXIST`
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
                          return
                    }
                    if(response.data==='CHANGE_FAULT'){
                        state.vm.$message({
                            showClose: true,
                            message: '更新失败',
                            type: 'warning'
                          });
                          return
                    }
                    state.file_name=response.data
                    state.vm.$bus.$emit('change_title',state.file_name+'')
                    state.vm.$bus.$emit('change_code',state.vm.name,state.code)
                    console.log(state.vm.excute_flag)
                    if(!state.vm.excute_flag){
                        state.vm.save_bt_style='primary'
                        send_post('/get_netknife_code',{'file_name':state.vm.title},response=>{
                            state.vm.storage_code=response.data
                        })
                        state.vm.$message({
                            showClose: true,
                            message: '更新成功',
                            type: 'success'
                            });
                    }else{  
                        state.vm.excute_flag=false
                        state.vm.save_bt_style='primary'
                        send_post('/get_netknife_code',{'file_name':state.vm.title},response=>{
                            state.vm.storage_code=response.data
                        })
                        state.vm.$bus.$emit('excute',state.file_name)
                    }
                })
        },
        SET_VM(state,vm){
            state.vm=vm
            console.log(vm.title)
        }
        
    },
    state:{
        code:'',
        vm:'',
        file_name:'',
    }
}