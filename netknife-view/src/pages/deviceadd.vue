<template>
    <el-form :inline=true ref="device_info" :mode="device_info" label-width="100px" label-position="left">
        <el-form-item label="项目名称">
            <el-input style="width: 800px;" v-model="device_info.project"><template slot="prepend">Project</template></el-input>
        </el-form-item><br>
        <el-form-item label="设备信息" >
            <el-select v-model="device_info.class" placeholder="请选择设备类型">
                <el-option label="Huawei" value="huawei"></el-option>
                <el-option label="Ruijie" value="ruijie"></el-option>
                <el-option label="Cisco" value="cisco"></el-option>
                <el-option label="Linux" value="linux"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item>
            <el-select v-model="device_info.area" placeholder="请选择设备层级">
                <el-option label="出口区" value="outlet"></el-option>
                <el-option label="安全区" value="security"></el-option>
                <el-option label="核心区" value="core"></el-option>
                <el-option label="汇聚区" value="convergence"></el-option>
                <el-option label="接入区" value="access"></el-option>
                <el-option label="服务器区" value="server"></el-option>
                <el-option label="负载均衡区" value="balance"></el-option>
                <el-option label="设备管理区" value="manage"></el-option>
                <el-option label="流量监控区" value="monitor"></el-option>
                <el-option label="业务增值区" value="value"></el-option>
            </el-select>
        </el-form-item><br>
        <el-form-item label="连接信息"> 
            <el-input placeholder="请输入端口号" v-model="device_info.port" class="input-with-select">
                <el-select  style="width: 150px;" placeholder="请选择协议"  v-model="device_info.protocol" slot="prepend" >
                    <el-option label="SSH" value="ssh"></el-option>
                    <el-option label="TELNET" value="telnet"></el-option>
                    <el-option label="FTP" value="ftp"></el-option>
                    <el-option label="SCP" value="scp"></el-option>
                    <el-option label="TFTP" value="tftp"></el-option>
                </el-select>
            </el-input>
        </el-form-item>
        <el-form-item >
                <el-input v-model="device_info.ip">
                <template slot="prepend">IP/Domain</template>
                <el-button slot="append" icon="el-icon-search" @click="check"></el-button>
                </el-input>
        </el-form-item><br>
        <el-form-item  label="连接信息">
                <el-input style="width: 366px;" v-model="device_info.username"><template slot="prepend">UserName</template></el-input>
        </el-form-item>
        <el-form-item >
                <el-input  style="width: 366px;" v-model="device_info.password"><template slot="prepend">PassWord</template></el-input>
        </el-form-item><br>
        <el-button style="margin-left: 100px;" @click="commit">创建</el-button>
    </el-form>
</template>

<script>
import axios from 'axios'
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
                ip:''
            },
            
        }
    },
    methods:{

        commit(){
            axios({
                method:'POST',
                url:'http://127.0.0.1:3000/commit',
                data:{
                    project:this.device_info.project,
                    class:this.device_info.class,
                    area:this.device_info.area,
                    protocol:this.device_info.protocol,
                    port:this.device_info.port,
                    username:this.device_info.username,
                    password:this.device_info.password,
                    ip:this.device_info.ip
                }
            }).then(response=>console.log(response))
            .catch(reason=>{console.log(reason)})
        },
        check(){
            axios({
                method:'POST',
                url:'http://127.0.0.1:3000/check',
                data:{
                    ip:this.device_info.ip
                }
            }).then(response=>console.log(response))
            .catch(reason=>{console.log(reason)})
        }
    }
    
}
</script>
<style>

</style>