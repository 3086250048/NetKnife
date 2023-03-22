import { send_get,send_post,pop_info } from "./tools";

export const  devicestateAbout={
    namespaced:true,
    actions:{},
    mutations:{
        GET_PROJECT_UNIT_LIST(state){
            send_post('/get_project_unit_data',{},response=>{
                state.project_unit_list=response.data
                state.select_project_unit_list=state.project_unit_list
                send_post('/get_all_project_data',{},response=>{
                    state.all_project_list=response.data
                },reason=>{})
            },reason=>{})
        },
        CHOOSE_CHANGE(state,project){
            state.project_unit_list.forEach(element => {
                if (element[0] === project){
                       state.select_project_unit_list =[element]       
                    return
                }
            });
        },
        ROLLBACK_SELECT_PROJECT_UNIT_LIST(state){
            state.select_project_unit_list=state.project_unit_list
        },
        SET_PROJECT_VIEW_ABLE(state,boolen){
            state.project_view_able=boolen     
        },

    },
    state:{
        project_unit_list:[],
        all_project_list:[],
        select_project_unit_list:[],
        project_view_able:true,
  
       

    }


}
