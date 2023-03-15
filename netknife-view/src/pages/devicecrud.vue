<template>
    <div  class="crud_div">
        <el-tabs type="border-card">
        <el-tab-pane label="新建项目"><DeviceCreate></DeviceCreate></el-tab-pane>
        <el-tab-pane label="更新项目"><DeviceUpdate></DeviceUpdate></el-tab-pane>
        <el-tab-pane label="删除项目"> <DeviceDelete></DeviceDelete> </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import DeviceCreate from './crud/devicecreate.vue'
import DeviceUpdate from './crud/deviceupdate.vue';
import DeviceDelete from './crud/devicedelete.vue';
export default{
    name:'DeviceCrud',
    components:{
        DeviceCreate:DeviceCreate,
        DeviceUpdate:DeviceUpdate,
        DeviceDelete:DeviceDelete
    },
}
</script>
<style scoped>
   .curd_div{
    background-color: #DCDFE6;
   }
</style>


