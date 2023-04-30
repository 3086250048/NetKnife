<template>
    <div >
    <el-row type="flex" v-if="project_view_able" >
        <el-col :push="5" :span="24"  >
            <el-autocomplete
            prefix-icon="el-icon-search"
            style="width: 60%;margin-top: 20px;"
            v-model="input"
            :fetch-suggestions="querySearchAsync"
            placeholder="输入项目名称进行搜索"
            @select="handleSelect"
            ></el-autocomplete>
        </el-col>
    </el-row>
    <el-row  v-if="project_view_able">
        <el-col :span="22" :push="1">
                <ul style="margin-top: 20px;" >
                    <li  v-for="(project,i) in select_project_unit_list " :key="i" > 
                        <el-row style="display: flex;flex-direction: column;">
                            <el-col>
                                <el-card style="height: 8vh;" >
                                    <el-row type="flex" justify="start" >
                                        <el-col :span="4" >
                                            <el-tag class="screen_change" style="min-width: 100%;height:5vh; text-align: center;font-size: 2vh;line-height: 5vh;">
                                                {{  project[0].length>39 ? project[0].slice(0,30)+'...':project[0] }}
                                            </el-tag>
                                        </el-col>
                                        <el-col  :span="3" :offset="10" :pull="2">
                                            <el-badge style="width:100%" :value="101" :max="99"  type="primary" class="screen_change">
                                                <el-button style="width: 100%;height:5vh; text-align: center;font-size: 2vh;line-height: 2vh;">挂载文件</el-button>
                                            </el-badge>
                                        </el-col>
                                        <el-col :span="4" :pull="1" >
                                            <el-button class="screen_change" type="primary" style="width: 100%;height:5vh; text-align:center;font-size: 2vh;line-height: 2vh;"  @click="show_mix_unit_page(project[0]),set_choose_project(project)">
                                                显示最小操作单元
                                            </el-button>
                                        </el-col>
                                        <el-col :span="3">
                                            <el-button class="screen_change" type="primary" style="width: 100%;height:5vh; text-align: center;font-size: 2vh;line-height: 2vh;"  @click="show_oprate_page(),set_choose_project(project)">
                                            操作
                                            </el-button>
                                        </el-col>
                                    </el-row>
                                </el-card>   
                            </el-col>
                            <el-col>
                                <el-card class="box-card" style="height: 20vh;font-size: 3vh;" >
                                    区域:{{ project[1].length>=150?project[1].slice(0,150)+'...':project[1] }}<br>
                                    协议:{{ project[2].length>=150?project[2].slice(0,150)+'...':project[2] }}<br>
                                    端口:{{ project[3].length>=140?project[3].slice(0,140)+'...':project[3] }}<br>
                                    IP表达式:{{ project[4].length>=150?project[4].slice(0,150)+'...':project[4] }}
                                </el-card>
                            </el-col>
                        </el-row>
                    </li>
                </ul>
         </el-col>
    </el-row>
           
        <router-view></router-view>
    </div>   
</template>

<script>

import { mapMutations} from 'vuex'

export default{
    name:'DeviceState',
    data() {
        return{
            input:'',
            };
    },
    methods:{
        ...mapMutations('devicestateAbout',{GET_PROJECT_UNIT_LIST:'GET_PROJECT_UNIT_LIST',
                                            CHOOSE_CHANGE:'CHOOSE_CHANGE',
                                            ROLLBACK_SELECT_PROJECT_UNIT_LIST:'ROLLBACK_SELECT_PROJECT_UNIT_LIST',
                                            SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('projectoprateAbout',{SET_CHOOSE_PROJECT:'SET_CHOOSE_PROJECT',
                                                SET_OPRATE_MODE:'SET_OPRATE_MODE'}),
        ...mapMutations('mixunitpageAbout',{SET_MIXUNIT_VIEW_ABLE:'SET_MIXUNIT_VIEW_ABLE'}),
      
        show_mix_unit_page(project){
            this.SET_PROJECT_VIEW_ABLE(false)
            this.SET_MIXUNIT_VIEW_ABLE(true)
            this.SET_OPRATE_MODE('mixunit')
            this.$router.push({
                name:'mixunit',
                params:{
                    'project':project
                }
            })
        },

        show_oprate_page(){
            this.SET_PROJECT_VIEW_ABLE(false)
            this.$router.push({
                name:'projectoprate',
            })
          
        },
       
        set_choose_project(project){
            this.SET_CHOOSE_PROJECT(project)
        },

        querySearchAsync(queryString, cb) {
        console.log(this.all_project_list)
        let results=this.all_project_list
        results = queryString ? results.filter(this.createStateFilter(queryString)) : results;
        cb(results);
        },
        createStateFilter(queryString) {
        return (item) => {
          return item.value.toLowerCase().match(queryString.toLowerCase());
        };

        },
        handleSelect(item) {
            this.CHOOSE_CHANGE(item.value)
        },
    },
    computed:{
        select_project_unit_list(){
            return this.$store.state.devicestateAbout.select_project_unit_list 
        },
        project_unit_list(){
            return this.$store.state.devicestateAbout.project_unit_list
        },
        all_project_list(){
            return this.$store.state.devicestateAbout.all_project_list
        },
        project_view_able(){
            return this.$store.state.devicestateAbout.project_view_able
        },
        empty_able(){
            return this.$store.state.devicestateAbout.empty_able
        }

    },
    watch:{
        input(new_value,old_value){
            if(old_value!=='' && new_value===''){
                this.ROLLBACK_SELECT_PROJECT_UNIT_LIST()
            }
        }
    },
    mounted(){        
        this.GET_PROJECT_UNIT_LIST()
        
    }
}

</script>

<style scoped>
li{
    list-style-type: none;
}



@media (min-width:600px) { 
    .screen_change{
        margin-top: -6px;
    }
} 
@media (min-width:900px) { 
    .screen_change{
        margin-top: 0px;
    }
} 
@media (min-width:1200px) { 
    .screen_change{
        margin-top: 5px;
    }
 }
 

@media (min-width:1500px) { 
    .screen_change{
        margin-top: 8px;
    }

 }
 @media (min-width:1800px) { 
    .screen_change{
        margin-top: 20px;
    }

 }
 @media (min-width:1900px) { 
    .screen_change{
        margin-top: 30px;
    }

 }
 @media (min-width:2500px) { 
    .screen_change{
        margin-top: 50px;
    }

 }

</style>