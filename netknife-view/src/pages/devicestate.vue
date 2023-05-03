<template>
    <div style="margin: 1vh;">
    <el-row type="flex" v-if="project_view_able" >
        <el-col :offset="5" :span="24"  >
            <el-autocomplete
            class="search_input"
            prefix-icon="el-icon-search"
            style="width: 70%;"
            v-model="input"
            :fetch-suggestions="querySearchAsync"
            :popper-append-to-body="false"
            placeholder="输入项目名称进行搜索"
            @select="handleSelect"
            ></el-autocomplete>
        </el-col>
    </el-row>
    <el-row  v-if="project_view_able">
        <el-col :span="24" >
                <ul style="margin-top: 1vh;" >
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
                                            <el-badge class="bt_tag_change" style="width:100%" :value="101" :max="99"  type="primary" >
                                                <el-button class="screen_change" style="width: 100%;height:5vh; text-align: center;font-size: 2vh;line-height: 2vh;">挂载文件</el-button>
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

<style lang="scss" scoped>
li{
    list-style-type: none;
}

.search_input ::v-deep .el-input__inner {
        height: 6.6vh;
        font-size: 2vh;
        padding-left: 4vh;
       
}
.search_input ::v-deep .el-input__icon {
        height: 100%;
        width: 3vh;
        font-size: 2vh;
        line-height: 100%;
        padding-top: 0.3vh;
        
      
}
 ::v-deep .el-badge__content {
    border-radius: 1vh;
    color: #FFF;
    display: inline-block;
    font-size: 2vh;
    height: 3vh;
    line-height: 3vh;
    padding: 0 6px;
    text-align: center;
    white-space: nowrap;
    border: 1px solid #FFF;
    margin-top: 0.5vw;
    margin-right: 2vh;
}
::v-deep .el-autocomplete-suggestion li{
    padding: 0 1vh;
    margin: 0;
    line-height: 4vh;
    cursor: pointer;
    color: #606266;
    font-size: 2vh;
    list-style: none;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
   
}
::v-deep .el-autocomplete-suggestion__wrap {
    max-height: 20vh;
    padding: 1vh 0;
    box-sizing: border-box;
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
    ::v-deep .el-badge__content {
    border-radius: 1vh;
    color: #FFF;
    display: inline-block;
    font-size: 2vh;
    height: 3vh;
    line-height: 3vh;
    padding: 0 6px;
    text-align: center;
    white-space: nowrap;
    border: 1px solid #FFF;
    margin-top: 1.5vw;
    margin-right: 2vh;
    }

 }
 @media (min-width:2500px) { 
    .screen_change{
        margin-top: 55px;
    }
    ::v-deep .el-badge__content {
    border-radius: 1vh;
    color: #FFF;
    display: inline-block;
    font-size: 2vh;
    height: 3vh;
    line-height: 3vh;
    padding: 0 6px;
    text-align: center;
    white-space: nowrap;
    border: 1px solid #FFF;
    margin-top: 1.5vw;
    margin-right: 2vh;
    }
 }

</style>