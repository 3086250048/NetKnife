<template>
    <div>
        <el-divider content-position="left">刪除数据</el-divider>
        <div class="popinfo">
            <DeviceDeletePopInfo></DeviceDeletePopInfo>
        </div>
        <el-form :inline=true ref="delete_info" :mode="delete_info" label-width="80px" label-position="rigth">
            <el-form-item label="项目名称">
                <el-input class="project_input" v-model="delete_info.project" placeholder="请输入项目名称">
                    <template slot="prepend">项目名称</template>
                </el-input>
            </el-form-item><br>
            <el-form-item label="设备信息" >
                <el-input class="input-with-select input" placeholder="自定义设备类型" v-model="delete_info.device_class">
                    <el-select class="select" v-model="delete_info.device_class" placeholder="类型" slot="prepend">
                        <el-option label="Huawei" value="huawei"></el-option>
                        <el-option label="Ruijie" value="ruijie"></el-option>
                        <el-option label="Cisco" value="cisco"></el-option>
                        <el-option label="Linux" value="linux"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-input class="input-with-select input" placeholder="自定义设备层级" v-model="delete_info.area" >
                    <el-select  class="select" placeholder="层级"  v-model="delete_info.area" slot="prepend" >
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
                <el-input class="input-with-select input" placeholder="请输入端口号" v-model="delete_info.port" >
                    <el-select  class="select" placeholder="协议"  v-model="delete_info.protocol" slot="prepend" >
                        <el-option label="SSH" value="ssh"></el-option>
                        <el-option label="TELNET" value="telnet"></el-option>
                        <el-option label="FTP" value="ftp"></el-option>
                        <el-option label="SCP" value="scp"></el-option>
                        <el-option label="TFTP" value="tftp"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input" v-model="delete_info.ip_expression"  placeholder="请输入IP">
                    <template slot="prepend">IP&ensp;&ensp;</template>
                    </el-input>
            </el-form-item><br>
            <el-form-item  label="用户信息">
                    <el-input class="input" v-model="delete_info.username" placeholder="请输入用户名">
                        <template slot="prepend">用户名</template>
                    </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input"  :show-password=true v-model="delete_info.password" placeholder="请输入密码" >
                        <template slot="prepend">密码</template>
                    </el-input>
            </el-form-item>
            <el-form-item  v-show="delete_info.device_class == 'cisco' | delete_info.device_class == 'ruijie'">
                    <el-input :show-password=true class="secret_input" placeholder="请输入特权密码" v-model="delete_info.secret">
                        <template slot="prepend">Secret</template>
                    </el-input>
            </el-form-item><br>
        </el-form><br>
        <el-button class="button" @click="remove">删除</el-button>
    </div>
</template>

<script>
import {mapActions, mapMutations} from 'vuex'
import devicedelete_pop_info from '../infopop/devicedelete_pop_info.vue'
export default{
    name:'DeviceDelete',
    components:{
        DeviceDeletePopInfo:devicedelete_pop_info
    },
    methods:{
        ...mapActions('devicedeleteAbout',{remove:'remove'}),
        ...mapMutations('devicedeleteAbout',{}),
    },
    computed:{
        delete_info(){
            return this.$store.state.devicedeleteAbout.delete_info
        },       
    },
    watch:{
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