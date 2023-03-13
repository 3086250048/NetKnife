<template>
    <div>
        <el-divider content-position="left">新建数据</el-divider>
        <div class="popinfo">
            <DeviceCreatePopInfo></DeviceCreatePopInfo>
        </div>
        <el-form :inline=true ref="device_info" :mode="device_info" label-width="80px" label-position="rigth">
            <el-form-item label="项目名称">
                <el-input class="project_input" v-model="device_info.project" placeholder="请输入项目名称">
                    <template slot="prepend">项目名称</template>
                </el-input>
            </el-form-item><br>
            <el-form-item label="设备信息" >
                <el-input class="input-with-select input" placeholder="自定义设备类型" v-model="device_info.device_class">
                    <el-select class="select" v-model="device_info.device_class" placeholder="类型" slot="prepend">
                        <el-option label="Huawei" value="huawei"></el-option>
                        <el-option label="Ruijie" value="ruijie"></el-option>
                        <el-option label="Cisco" value="cisco"></el-option>
                        <el-option label="Linux" value="linux"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-input class="input-with-select input" placeholder="自定义设备层级" v-model="device_info.area" >
                    <el-select  class="select" placeholder="层级"  v-model="device_info.area" slot="prepend" >
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
                </el-input>
            </el-form-item><br>
            <el-form-item label="连接信息"> 
                <el-input class="input-with-select input" placeholder="请输入端口号" v-model="device_info.port" >
                    <el-select  class="select" placeholder="协议"  v-model="device_info.protocol" slot="prepend" >
                        <el-option label="SSH" value="ssh"></el-option>
                        <el-option label="TELNET" value="telnet"></el-option>
                        <el-option label="FTP" value="ftp"></el-option>
                        <el-option label="SCP" value="scp"></el-option>
                        <el-option label="TFTP" value="tftp"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input" v-model="device_info.ip_expression"  placeholder="请输入IP或域名">
                    <template slot="prepend">IP&ensp;&ensp;</template>
                    <el-select  class="checkselect" v-model="device_info.check_protocol" placeholder="检查协议"  slot="prepend" >
                        <el-option label="TCP" value="tcp"></el-option>
                        <el-option label="ICMP" value="icmp"></el-option>
                    </el-select>
                    <el-button class="checkbutton" slot="append" icon="el-icon-search" @click="checkip"></el-button>
                    </el-input>
            </el-form-item><br>
            <el-form-item  label="用户信息">
                    <el-input class="input" v-model="device_info.username" placeholder="请输入用户名">
                        <template slot="prepend">用户名</template>
                    </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input"  :show-password=true v-model="device_info.password" placeholder="请输入密码" >
                        <template slot="prepend">密码</template>
                    </el-input>
            </el-form-item>
            <el-form-item  v-show="device_info.device_class == 'cisco' | device_info.device_class == 'ruijie'">
                    <el-input :show-password=true class="secret_input" placeholder="请输入特权密码" v-model="device_info.secret">
                        <template slot="prepend">Secret</template>
                    </el-input>
            </el-form-item><br>
            <el-button class="button" @click="commit">创建</el-button>
        </el-form>
    </div>
</template>
<script>
import {mapActions, mapMutations} from 'vuex'
import devicecreate_pop_info from '../infopop/devicecreate_pop_info.vue'
export default{
    name:'DeviceCreate',
    components:{
        DeviceCreatePopInfo:devicecreate_pop_info
    },
    methods:{
        ...mapActions('deviceaddAbout',{commit:'commit',checkip:'checkip'}),
        ...mapMutations('deviceaddAbout',{CHECK_IP_EXPRESSION_POP_INFO:'CHECK_IP_EXPRESSION_POP_INFO',CHECK_PORT_RANGE_POP_INFO:'CHECK_PORT_RANGE_POP_INFO',CHECK_PROJECT_POP_INFO:'CHECK_PROJECT_POP_INFO'}),
    },
    computed:{
        device_info(){
            return this.$store.state.deviceaddAbout.device_info
        },
        project(){
            return this.device_info.project
        },
        device_class(){
            return this.device_info.device_class
        },
        area(){
            return this.device_info.area
        },
        protocol(){
            return this.device_info.protocol
        },
        port(){
            return this.device_info.port
        },
        username(){
            return this.device_info.username
        },
        password(){
            return this.device_info.password
        },
        secret(){
            return this.device_info.secret
        },
        ip_expression(){
            return this.device_info.ip_expression
        },
        check_protocol(){
            return this.device_info.check_protocol
        }
    },
    watch:{
        ip_expression(){
           this.CHECK_IP_EXPRESSION_POP_INFO()
        },
        port(){
            this.CHECK_PORT_RANGE_POP_INFO()
        },
        project(){
            this.CHECK_PROJECT_POP_INFO()
        }

    },
    mounted(){        
    }
}
</script>
<style scoped>
    .select{
        width: 100px;
    }
    .input{
        width: 400px;
    }
    .project_input{
        width: 810px;
    }
    .secret_input{
        width: 300px;
    }
    .button{
        width: 100px;
        margin-left: 80px;
    }
    .checkbutton{
        width: 60px;
    }
    .checkselect{
        width: 105px
    }   
    .popinfo{
        height: 40px;
    }
</style>