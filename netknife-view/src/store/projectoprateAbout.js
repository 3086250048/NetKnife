import { send_post,pop_info } from "./tools";

export const  projectoprateAbout={
    namespaced:true,
    actions:{},
    mutations:{
        COMMIT_COMMAND(state,command){
            send_post('/commit_command',{
                'command':command
            },response=>{
                state.textarea=''
                state.textarea=response.data
            },reason=>{})
        }
    },
    state:{
        textarea:'test'
    }
}
