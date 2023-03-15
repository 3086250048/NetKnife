<template>
    <ul >
        <li v-for="(project,i) in project_unit_list " > 
            <el-card class="box-card">    
            <el-descriptions :title="project[0]">
                <el-descriptions-item label="区域" >{{ project[1] }}</el-descriptions-item>
                <el-descriptions-item label="协议" >{{ project[2] }}</el-descriptions-item>
                <el-descriptions-item label="端口" >{{ project[3] }}</el-descriptions-item>
                <el-descriptions-item label="IP地址表达式">{{ project[4] }}</el-descriptions-item>
            </el-descriptions>
            </el-card>
        </li>
    </ul>
</template>

<script>
import {mapActions, mapMutations} from 'vuex'
export default{
    name:'DeviceState',
    methods:{
        ...mapMutations('devicestateAbout',{GET_PROJECT_UNIT_LIST:'GET_PROJECT_UNIT_LIST'})
    },
    computed:{
        project_unit_list(){
            return this.$store.state.devicestateAbout.project_unit_list
        }
    },
    mounted(){
      this.GET_PROJECT_UNIT_LIST()
    },
}

</script>
<style scoped>
li{
    list-style-type: none;
}
li:not(:first-child){
    margin-top: 8px;
}


</style>