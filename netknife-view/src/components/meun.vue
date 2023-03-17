<template>
    <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="设备信息" name="first"><DeviceInfo></DeviceInfo> </el-tab-pane>
        <el-tab-pane label="命令行管理CLI" name="second"><DeviceOprate></DeviceOprate></el-tab-pane>
    </el-tabs>
</template>
<script>
import deviceinfo from '../pages/deviceinfo.vue'
import deviceoprate from '@/pages/deviceoprate.vue'
export default{
    name:'Meun',
    components:{
        DeviceInfo:deviceinfo,
        DeviceOprate:deviceoprate
    },
    data(){
        return{
                activeName:'first' 
        }
    },
    methods:{
        handleClick(tab,event){
            console.log(this.activeName)
        },
    }
}
</script>