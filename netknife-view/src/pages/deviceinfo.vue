<template>
    <el-tabs v-model="activeName" type="card" tab-position="left" @tab-click="handleClick">
        <el-tab-pane label="设备状态" name="first"> </el-tab-pane>
        <el-tab-pane label="管理设备" name="second"><DeviceCrud></DeviceCrud></el-tab-pane>
    </el-tabs>
</template>

<script>
import devicestate from './devicestate.vue';
import devicecrud from './devicecrud.vue';
export default{
    name:'DeviceInfo',
    components:{
        DeviceState:devicestate,
        DeviceCrud:devicecrud
    },
    data(){
        return {
            activeName:'first'
        }
    },
    methods:{
        handleClick(){

        }
    }
}
</script>