import { send_post,pop_info } from "./tools";


export const  devicestateAbout={
    namespaced:true,
    actions:{},
    mutations:{
        GET_PROJECT_UNIT_LIST(state){
            send_post('/get_project_unit_data',{},response=>{
                state.project_unit_list=response.data
                console.log(state.project_unit_list)
            },reason=>{
            })
        }
    },
    state:{
        project_unit_list:[]
    }


}
