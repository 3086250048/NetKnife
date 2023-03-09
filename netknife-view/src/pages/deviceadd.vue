<template>
    <el-form ref="device_info" :mode="device_info" label-width="100px" label-position="left">
        <el-form-item label="设备所属项目">
            <el-input v-model="device_info.project"></el-input>
        </el-form-item>
        <el-form-item label="设备类型" >
            <el-select v-model="device_info.class" placeholder="请选择设备类型">
                <el-option label="Huawei" value=""></el-option>
                <el-option label="Ruijie" value=""></el-option>
                <el-option label="Cisco" value=""></el-option>
                <el-option label="Linux" value=""></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="设备层级">
            <el-select v-model="device_info.area" placeholder="请选择设备层级">
                <el-option label="出口区" value=""></el-option>
                <el-option label="安全区" value=""></el-option>
                <el-option label="核心区" value=""></el-option>
                <el-option label="汇聚区" value=""></el-option>
                <el-option label="接入区" value=""></el-option>
                <el-option label="服务器区" value=""></el-option>
                <el-option label="负载均衡区" value=""></el-option>
                <el-option label="设备管理区" value=""></el-option>
                <el-option label="流量监控区" value=""></el-option>
                <el-option label="业务增值区" value=""></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="连接协议"> 
            <el-select v-model="device_info.protocol">
                <el-option label="SSH" value=""></el-option>
                <el-option label="TELENET" value=""></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="端口号">
                <el-input v-model="device_info.port"></el-input>
        </el-form-item>
        <el-form-item label="用户名">
                <el-input v-model="device_info.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
                <el-input v-model="device_info.password"></el-input>
        </el-form-item>
        <el-form-item label="IP信息">
                <el-input v-model="device_info.password"></el-input>
        </el-form-item>
    </el-form>
</template>

<script>
export default{
    name:'DeviceAdd',
    data(){
        return {
            device_info:{
                project:'',
                class:'',
                area:'',
                protocol:'',
                port:'',
                username:'',
                password:'',
            }
        }
    },
    
}
</script>