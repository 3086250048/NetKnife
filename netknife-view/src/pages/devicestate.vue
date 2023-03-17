<template>
    <div>
        <div>
            <el-button type="primary" icon="el-icon-search" ></el-button>
            <el-autocomplete
            style="width: 500px;margin-bottom: 10px;"
            v-model="input"
            :fetch-suggestions="querySearchAsync"
            placeholder="请输入项目名称"
            @select="handleSelect"
            ></el-autocomplete>
            
        </div>
        <ul>
        <li v-for="(project,i) in select_project_unit_list " > 
                <el-card class="box-card normal"  style="height: 40px;">
                    <div style="margin-top: -10px;">{{ project[0] }}</div>
                </el-card>   
                <el-card class="box-card" style="">
                    区域:{{ project[1].length>=50?project[1].slice(0,150)+'...':project[1] }}<br>
                    协议:{{ project[2].length>=50?project[2].slice(0,150)+'...':project[2] }}<br>
                    端口:{{ project[3].length>=50?project[3].slice(0,140)+'...':project[3] }}<br>
                    IP表达式:{{ project[4].length>=50?project[4].slice(0,150)+'...':project[4] }}
                </el-card>
        </li>
    </ul>
    </div>
    
</template>

<script>

import {mapActions, mapMutations} from 'vuex'

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

</style>