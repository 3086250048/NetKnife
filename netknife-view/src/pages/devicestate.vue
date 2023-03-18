<template>
    <el-container>
        <el-header>
            <el-button type="primary" icon="el-icon-search" ></el-button>
            <el-autocomplete
            style="width: 500px;margin-bottom: 10px;"
            v-model="input"
            :fetch-suggestions="querySearchAsync"
            placeholder="请输入项目名称"
            @select="handleSelect"
            ></el-autocomplete>
        </el-header>
        <el-main>
            <ul>
                <li v-if="able" v-for="(project,i) in select_project_unit_list " > 
                    <el-card class="box-card  head_card " >
                        <div style="margin-top: -10px;">
                            {{ project[0] }}
                                <el-button type="primary" class="head_button" @click="show_mix_unit_page">显示最小操作单元</el-button>
                                <el-button type="primary" class="head_button" @click="show_oprate_page">操作</el-button>
                        </div>
                    </el-card>   
                    <el-card class="box-card" style="">
                                区域:{{ project[1].length>=150?project[1].slice(0,150)+'...':project[1] }}<br>
                                协议:{{ project[2].length>=150?project[2].slice(0,150)+'...':project[2] }}<br>
                                端口:{{ project[3].length>=140?project[3].slice(0,140)+'...':project[3] }}<br>
                                IP表达式:{{ project[4].length>=150?project[4].slice(0,150)+'...':project[4] }}
                    </el-card>
                </li>
            </ul>
            <router-view></router-view>
        </el-main>
    </el-container>    
</template>

<script>

import { mapMutations} from 'vuex'

export default{
    name:'DeviceState',
    data() {
        return{
            able:true,
            input:'',
            };
    },
    methods:{
        show_mix_unit_page(){
            this.able=false
            this.$router.push({
                name:'mixunit'
            })
        },
        show_oprate_page(){
            this.able=false
            this.$router.push({
                name:'projectoprate'
            })
        },
       
        ...mapMutations('devicestateAbout',{GET_PROJECT_UNIT_LIST:'GET_PROJECT_UNIT_LIST',
                                            CHOOSE_CHANGE:'CHOOSE_CHANGE',
                                            ROLLBACK_SELECT_PROJECT_UNIT_LIST:'ROLLBACK_SELECT_PROJECT_UNIT_LIST'}),


        querySearchAsync(queryString, cb) {
        
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
li:not(:first-child){
    margin-top: 8px;
}

.normal{
    background-color:#409EFF;
}
.success{
    background-color: #67C23A;
}
.warning{
    background-color:#E6A23C ;
}
.error{
    background-color: #F56C6C;
}

.head_card{
    height: 40px;
}
.head_button{
    height: 40px;
    float: right;
    margin-left: 10px;
    margin-top: -6px;
}
</style>