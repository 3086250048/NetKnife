<template>
    <div style="height: 105vh;">
        <el-divider content-position="left">更新条件</el-divider>
        <el-form :inline=true ref="where_info" :mode="where_info" label-width="6vw" label-position="rigth">
            <el-form-item label="项目名称">
                <el-input class="project_input" v-model="where_info.project" placeholder="请输入项目名称">
                    <template slot="prepend">项目名称</template>
                </el-input>
            </el-form-item><br>
            <el-form-item label="设备信息" >
                <el-input class="input-with-select input" placeholder="自定义设备类型" v-model="where_info.device_class">
                    <el-select class="select" v-model="where_info.device_class" placeholder="类型" slot="prepend">
                        <el-option label="Huawei" value="huawei"></el-option>
                        <el-option label="Ruijie" value="ruijie"></el-option>
                        <el-option label="Cisco" value="cisco"></el-option>
                        <el-option label="Linux" value="linux"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-input class="input-with-select input" placeholder="自定义设备层级" v-model="where_info.area" >
                    <el-select  class="select" placeholder="层级"  v-model="where_info.area" slot="prepend" >
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
                <el-input class="input-with-select input" placeholder="请输入端口号" v-model="where_info.port" >
                    <el-select  class="select" placeholder="协议"  v-model="where_info.protocol" slot="prepend" >
                        <el-option label="SSH" value="ssh"></el-option>
                        <el-option label="TELNET" value="telnet"></el-option>
                        <el-option label="FTP" value="ftp"></el-option>
                        <el-option label="SCP" value="scp"></el-option>
                        <el-option label="TFTP" value="tftp"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input" v-model="where_info.ip_expression"  placeholder="请输入IP">
                    <template slot="prepend">IP&ensp;&ensp;</template>
                    </el-input>
            </el-form-item><br>
            <el-form-item  label="用户信息">
                    <el-input class="input" v-model="where_info.username" placeholder="请输入用户名">
                        <template slot="prepend">用户名</template>
                    </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input"  :show-password=true v-model="where_info.password" placeholder="请输入密码" >
                        <template slot="prepend">密码</template>
                    </el-input>
            </el-form-item>
            <el-form-item  label="特权密码" v-show="where_info.device_class == 'cisco' | where_info.device_class == 'ruijie'">
                    <el-input :show-password=true class="secret_input" placeholder="请输入特权密码" v-model="where_info.secret">
                        <template slot="prepend">Secret</template>
                    </el-input>
            </el-form-item>
        </el-form>
        <el-divider content-position="left">更新数据</el-divider>
        <div class="popinfo">
            <DeviceUpdatePopInfo></DeviceUpdatePopInfo>
        </div>
        <el-form :inline=true ref="update_info" :mode="update_info" label-width="6vw" label-position="rigth">
            <el-form-item label="项目名称">
                <el-input class="project_input" v-model="update_info.project" placeholder="请输入项目名称">
                    <template slot="prepend">项目名称</template>
                </el-input>
            </el-form-item><br>
            <el-form-item label="设备信息" >
                <el-input class="input-with-select input" placeholder="自定义设备类型" v-model="update_info.device_class">
                    <el-select class="select" v-model="update_info.device_class" placeholder="类型" slot="prepend">
                        <el-option label="Huawei" value="huawei"></el-option>
                        <el-option label="Ruijie" value="ruijie"></el-option>
                        <el-option label="Cisco" value="cisco"></el-option>
                        <el-option label="Linux" value="linux"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-input class="input-with-select input" placeholder="自定义设备层级" v-model="update_info.area" >
                    <el-select  class="select" placeholder="层级"  v-model="update_info.area" slot="prepend" >
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
                <el-input class="input-with-select input" placeholder="请输入端口号" v-model="update_info.port" >
                    <el-select  class="select" placeholder="协议"  v-model="update_info.protocol" slot="prepend" >
                        <el-option label="SSH" value="ssh"></el-option>
                        <el-option label="TELNET" value="telnet"></el-option>
                        <el-option label="FTP" value="ftp"></el-option>
                        <el-option label="SCP" value="scp"></el-option>
                        <el-option label="TFTP" value="tftp"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input" v-model="update_info.ip_expression"  placeholder="请输入IP">
                    <template slot="prepend">IP&ensp;&ensp;</template>
                    </el-input>
            </el-form-item><br>
            <el-form-item  label="用户信息">
                    <el-input class="input" v-model="update_info.username" placeholder="请输入用户名">
                        <template slot="prepend">用户名</template>
                    </el-input>
            </el-form-item>
            <el-form-item >
                    <el-input class="input"  :show-password=true v-model="update_info.password" placeholder="请输入密码" >
                        <template slot="prepend">密码</template>
                    </el-input>
            </el-form-item>
            <el-form-item label="特权密码" v-show="update_info.device_class == 'cisco' | update_info.device_class == 'ruijie'">
                    <el-input :show-password=true class="secret_input" placeholder="请输入特权密码" v-model="update_info.secret">
                        <template slot="prepend">Secret</template>
                    </el-input>
            </el-form-item><br>
            <el-button class="button" @click="update">更新</el-button>
        </el-form><br>
    </div>
</template>
<script>
import {mapActions, mapMutations} from 'vuex'
import deviceupdate_pop_info from '../infopop/deviceupdate_pop_info.vue'
export default{
    name:'DeviceUpdate',
    components:{
        DeviceUpdatePopInfo:deviceupdate_pop_info
    },
    methods:{
        ...mapActions('deviceupdateAbout',{update:'update'}),
        ...mapMutations('deviceupdateAbout',{
            IP_EXPRESSION_POP_INFO:'IP_EXPRESSION_POP_INFO',
            PORT_POP_INFO:'PORT_POP_INFO'
        }),
    },
    computed:{
        where_info(){
            return this.$store.state.deviceupdateAbout.where_info
        },
        update_info(){
            return this.$store.state.deviceupdateAbout.update_info
        },
        ip_expression(){
            return this.update_info.ip_expression
        },
        port(){
            return this.update_info.port
        }
    },
    watch:{
        ip_expression(){
            this.IP_EXPRESSION_POP_INFO()
        },  
        port(){
            this.PORT_POP_INFO()
        }
    },
    mounted(){        
    }
}
</script>

<style scoped>
    .popinfo{
    height: 2vh;
    margin-bottom:5vh;
    }
    .input{
        width: 40vw;
        height: 2.75vh;
        
    }
    .project_input{
        width:80vw;
        height: 2.75vh;
        
    }
    .secret_input{
        width: 40vw;
        height: 2.75vh
    }
    .button{
        width: 10vw;
        height: 5vh;
        border-radius: 1vh;
        
        line-height: 1vh;
        font-size: 2vh;
        margin-left: 11vh;
        margin-top: 1.5vh;
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
        outline: 0;
        padding: 0 3vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 5vh;
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
        height: 5vh;
        line-height: 3.5vh;
        width: 73vw;
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
        outline: 0;
        padding: 0 3vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 5vh;
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
        height: 5vh;
        line-height: 5vh;
        width: 7.5vw;
        font-size: 2vh;
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
        z-index: 1;
    }

 
    
    ::v-deep .el-form-item__label{
        text-align: center;
        vertical-align: middle;
        float: left;
        font-size: 2vh;
        color: #606266;
        line-height: 0.2vh;
        padding: 2.6vh 12px 0 0;
        box-sizing: border-box;  
        z-index: 10000;
    }

   

::v-deep .el-form-item__content{
    line-height: 0px;
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


.select ::v-deep .el-select__caret{
    color: #C0C4CC;
    font-size: 1.8vh;
    margin-right: 0.48vh;
    line-height: 2vh;
    transition: transform .3s;
    transform: rotateZ(180deg);
    cursor: pointer;
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

/* 密码框眼睛 */
::v-deep .el-input .el-input__clear {
    color: #C0C4CC;
    font-size: 2.2vh;
    margin-top: -0.8vh;
    cursor: pointer;
    transition: color .2s cubic-bezier(.645,.045,.355,1);
    }

@media (min-width:1100px) { 
   
}
      

@media (min-width:1200px) { 
          /* 密码框眼睛 */
        ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        font-size: 2.2vh;
        margin-top: -0.02vh;
        cursor: pointer;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:1400px) { 
       /* 密码框眼睛 */
       ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        cursor: pointer;
        font-size: 2.2vh;
        margin-top: -0.1vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:1500px) { 
 /* 密码框眼睛 */
 ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        cursor: pointer;
        font-size: 2.2vh;
        margin-right: 1vh;
        margin-top: 0.3vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:1700px) { 
    /* 密码框眼睛 */
    ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        cursor: pointer;
        font-size: 2.2vh;
        margin-right: 1.5vh;
        margin-top: 0.6vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:2200px) { 
      /* 密码框眼睛 */
      ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        cursor: pointer;
        font-size: 2.2vh;
        margin-right:1.8vh ;
        margin-top:1.2vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:3400px) { 
      /* 密码框眼睛 */
      ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        cursor: pointer;
        font-size: 2.2vh;
        margin-right: 2.2vh;
        margin-top: 1.8vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:4500px) { 
    
}
</style>