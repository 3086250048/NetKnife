<template>
    <div>
        <DeviceCrudPopInfo></DeviceCrudPopInfo>
        <el-tabs type="border-card" style="height: 520px;">
        <el-tab-pane label="新建项目"><DeviceCreate></DeviceCreate></el-tab-pane>
        <el-tab-pane label="更新项目">消息中心</el-tab-pane>
        <el-tab-pane label="删除项目">角色管理</el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import DeviceCrudPopInfo from './infopop/devicecrud_infopop.vue'
import DeviceCreate from './crud/devicecreate.vue'
export default{
    name:'DeviceCrud',
    components:{
        DeviceCrudPopInfo:DeviceCrudPopInfo,
        DeviceCreate:DeviceCreate
    },
}
</script>
<style>
    .popinfo{
        height: 40px;
    }
</style>


