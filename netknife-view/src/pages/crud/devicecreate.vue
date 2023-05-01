<template>
    <div style="height: 100vh;">
        <el-divider content-position="left" style="font-size: 2vh;">新建数据</el-divider>
        <div class="popinfo">
            <DeviceCreatePopInfo></DeviceCreatePopInfo>
        </div>
        <el-form :inline=true ref="device_info" :mode="device_info" label-width="6vw" label-position="rigth">
            <el-form-item label="项目名称">
                <el-input class="project_input" v-model="device_info.project" placeholder="请输入项目名称">
                    <template slot="prepend">项目名称</template>
                </el-input>
            </el-form-item><br>
            <el-form-item label="设备信息" >
                <el-input class="input-with-select input" placeholder="自定义设备类型" v-model="device_info.device_class">
                    <el-select  :popper-append-to-body="false" class="select" v-model="device_info.device_class" placeholder="类型" slot="prepend">
                        <el-option label="Huawei" value="huawei"></el-option>
                        <el-option label="H3c" value="h3c"></el-option>
                        <el-option label="Ruijie" value="ruijie"></el-option>
                        <el-option label="Cisco" value="cisco"></el-option>
                        <el-option label="Linux" value="linux"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-input class="input-with-select input" placeholder="自定义设备层级" v-model="device_info.area" >
                    <el-select   :popper-append-to-body="false" class="select" placeholder="层级"  v-model="device_info.area" slot="prepend" >
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
                    <el-select   :popper-append-to-body="false" class="select" placeholder="协议"  v-model="device_info.protocol" slot="prepend" >
                        <el-option label="SSH" value="ssh"></el-option>
                        <el-option label="TELNET" value="telnet"></el-option>
                        <el-option label="FTP" value="ftp"></el-option>
                        <el-option label="SCP" value="scp"></el-option>
                        <el-option label="TFTP" value="tftp"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="ip_input" v-model="device_info.ip_expression"  placeholder="请输入IP或域名">
                    <template class="ip_prepend" slot="prepend">IP</template>
                    <el-select  :popper-append-to-body="false"  class="ip_select" v-model="device_info.check_protocol" placeholder="检查协议"  slot="prepend" >
                        <el-option label="TCP" value="tcp"></el-option>
                        <el-option label="ICMP" value="icmp"></el-option>
                    </el-select>
                    <el-button class="ip_append" slot="append" icon="el-icon-search" @click="checkip"></el-button>
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
            <el-form-item label="特权密码"  v-show="device_info.device_class == 'cisco' | device_info.device_class == 'ruijie'">
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
        ...mapMutations('deviceaddAbout',{
            PROJECT_POP_INFO:'PROJECT_POP_INFO',
            AREA_POP_INFO:'AREA_POP_INFO',
            IP_EXPRESSION_POP_INFO:'IP_EXPRESSION_POP_INFO',
            PROTOCOL_POP_INFO:'PROTOCOL_POP_INFO',
            PORT_POP_INFO:'PORT_POP_INFO',
                                            }),
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
        ip_expression:{
            handler(){
                this.IP_EXPRESSION_POP_INFO()
            }
        },
        port:{
    
            handler(){
            this.PORT_POP_INFO()
            }
        },
        protocol:{
       
            handler(){
            this.PROTOCOL_POP_INFO()
            }
        },
        area:{
            
            handler(){
                this.AREA_POP_INFO()  
            }
        },
        project:{
            handler(){
                this.PROJECT_POP_INFO()
            }
        },
       

    },
    mounted(){        
    }
}
</script>
<style scoped>
   .popinfo{
    height: 3vh;
    margin-bottom:2vh;
    }
    .input{
        width: 40vw;
        height: 5.5vh;
        margin-top: 3vh;
        
    }

    .ip_input{
       
        width: 40vw;
        height: 5.5vh;
        margin-top: 3vh;
      
    }
    .project_input{
        margin-top: 3vh;
        width:80vw;
        height: 5.5vh;
   
    }
    .secret_input{
        width: 40vw;
        height: 5.5vh;
        margin-top: 3vh;
    
    }
    .button{
        width: 10vw;
        height: 7vh;
        border-radius: 1vh;
        
        line-height: 1vh;
        font-size: 2vh;
        margin-left: 11vh;
        margin-top: 3vh;
    }
   
    
  

    ::v-deep .el-divider__text{
        font-size: 2vh;
        font-weight: 600;
        padding:2vh
    }
    .input ::v-deep .el-input__inner {
        -webkit-appearance: none;
        background-color: #FFF;
        background-image: none;
        border-radius: 0 1vh 1vh 0;
        border: 0.15vh solid #DCDFE6;
        box-sizing: border-box;
        color: #606266;
        display: inline-block;
        height: 40px;
        line-height: 40px;
        outline: 0;
        padding: 0 3vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 7vh;
        width: 30vw;
        font-size: 2vh; 
    }
    .project_input ::v-deep .el-input__inner {
        -webkit-appearance: none;
        background-color: #FFF;
        background-image: none;
        border-radius: 0 1vh 1vh 0;
        border: 0.15vh solid #DCDFE6;
        box-sizing: border-box;
        color: #606266;
        display: inline-block;
        outline: 0;
        padding: 0 3vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 7vh;
        line-height: 7vh;
        width: 73vw;
        font-size: 2vh;
    }
    
    .ip_input ::v-deep .el-input__inner{
        -webkit-appearance: none;
        background-color: #FFF;
        background-image: none;
        border: 0.15vh solid #DCDFE6;
        box-sizing: border-box;
        color: #606266;
        display: inline-block;
        outline: 0;
        padding: 0 5vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 7vh;
        line-height: 7vh;
        width:23vw;
        font-size: 2vh;
        
    }
    .ip_select ::v-deep .el-input__inner{
        -webkit-appearance: none;
        background-color: #FFF;
        background-image: none;
        border: 0.15vh solid #DCDFE6;
        box-sizing: border-box;
        color: #606266;
        display: inline-block;
        outline: 0;
        padding: 0 5vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 7vh;
        line-height: 7vh;
        width:8.4vw;
        font-size: 2vh;
    }
    .secret_input ::v-deep .el-input__inner{
        -webkit-appearance: none;
        background-color: #FFF;
        background-image: none;
        border-radius: 0 1vh 1vh 0;
        border: 0.15vh solid #DCDFE6;
        box-sizing: border-box;
        color: #606266;
        display: inline-block;
        height: 40px;
        line-height: 40px;
        outline: 0;
        padding: 0 3vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 7vh;
        width: 30vw;
        font-size: 2vh; 
        
    }
    .select ::v-deep .el-input__inner{
        -webkit-appearance: none;
        background-color: #FFF;
        background-image: none;
        border-radius: 1vh;
        border: 0.15vh solid #DCDFE6;
        box-sizing: border-box;
        color: #606266;
        display: inline-block;
        outline: 0;
        padding: 0  1vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 7vh;
        line-height: 7vh;
        width: 7.5vw;
        font-size: 2vh;
    }
    .select ::v-deep .el-select__caret{
        color: #C0C4CC;
        font-size: 1.8vh;
        margin-right: 0.48vh;
        
        transition: transform .3s;
        transform: rotateZ(180deg);
        cursor: pointer;
    }

    .ip_select ::v-deep .el-select__caret{
        color: #C0C4CC;
        font-size: 2vh;
        margin-right: 0.48vh;
        transition: transform .3s;
        transform: rotateZ(180deg);
        cursor: pointer;
    }
    ::v-deep  .el-input-group__prepend{
        background-color: #F5F7FA;
        color: #909399;
        vertical-align: middle;
        display: table-cell;
        position: relative;
        border: 0.15vh solid #DCDFE6 ;
        border-right: 0;
        border-radius:1vh 0 0 1vh;
        padding: 0 3vh;
        width: 16vh;
        white-space: nowrap;
        font-size: 2vh;
        text-align: center;

    }

    ::v-deep .el-input-group__append{
        background-color: #F5F7FA;
        color: #909399;
        vertical-align: middle;
        display: table-cell;
        position: relative;
        border: 0.15vh solid #DCDFE6 ;
        border-left: 0;
        border-radius:0 1vh 1vh 0;
        padding: 0 4.9vh;
        width: 3vh;
        white-space: nowrap;
        font-size: 2vh;
        text-align: center;
    }
    
    ::v-deep .el-form-item__label{
        text-align: center;
        vertical-align: middle;
        float: left;
        font-size: 2vh;
        color: #606266;
        line-height: 6vh;
        padding: 3.3vh 12px 0 0;
        box-sizing: border-box;  

    }

    .el-select-dropdown__item {
    font-size:2vh;
    padding:2vh 0.5vh;
    position: relative;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: #606266;
    height: 2vh;
    line-height: 2vh;
    box-sizing: border-box;
    cursor: pointer;
}
::v-deep .el-divider--horizontal {
    display: block;
    height: 1px;
    width: 100%;
    z-index: 0;
    margin: 0;
    margin-top: 1vh;
    margin-bottom: 4vh;
    
   
}
</style>