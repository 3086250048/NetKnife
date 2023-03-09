<template>
     <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="设备信息" name="first"> <DeviceInfo></DeviceInfo> </el-tab-pane>
    <el-tab-pane label="管理设备" name="second"><DeviceManage></DeviceManage></el-tab-pane>
  </el-tabs>
</template>
<script>
import deviceinfo from '../pages/deviceinfo.vue'
import devicemanage from '../pages/devicemanage.vue'
export default{
    name:'Meun',
    components:{
        DeviceInfo:deviceinfo,
        DeviceManage:devicemanage
    },
    data(){
        return{
                activeName:'first' 
        }
    },
    methods:{
        handleClick(tab,event){
            console.log(this.activeName)
        }
    }
}
</script>