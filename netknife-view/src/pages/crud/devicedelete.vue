<template>
    <div style="height: 100vh;">
        <el-divider content-position="left">刪除数据</el-divider>
        <div class="popinfo">
            <DeviceDeletePopInfo></DeviceDeletePopInfo>
        </div>
        <el-form :inline=true ref="delete_info" :mode="delete_info" label-width="6vw" label-position="rigth">
            <el-form-item label="项目名称">
                <el-input class="project_input" v-model="delete_info.project" placeholder="请输入项目名称">
                    <template slot="prepend">项目名称</template>
                </el-input>
            </el-form-item><br>
            <el-form-item label="设备信息" >
                <el-input class="input-with-select input" placeholder="自定义设备类型" v-model="delete_info.device_class">
                    <el-select :popper-append-to-body="false" class="select" v-model="delete_info.device_class" placeholder="类型" slot="prepend">
                        <el-option label="Huawei" value="huawei"></el-option>
                        <el-option label="Ruijie" value="ruijie"></el-option>
                        <el-option label="Cisco" value="cisco"></el-option>
                        <el-option label="Linux" value="linux"></el-option>
                    </el-select>
                </el-input>
            </el-form-item>
            <el-form-item>
                <el-input class="input-with-select input" placeholder="自定义设备层级" v-model="delete_info.area" >
                    <el-select :popper-append-to-body="false" class="select" placeholder="层级"  v-model="delete_info.area" slot="prepend" >
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
                    <el-select :popper-append-to-body="false" class="select" placeholder="协议"  v-model="delete_info.protocol" slot="prepend" >
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
            <el-form-item label="特权密码" v-show="delete_info.device_class == 'cisco' | delete_info.device_class == 'ruijie'">
                    <el-input :show-password=true class="secret_input" placeholder="请输入特权密码" v-model="delete_info.secret">
                        <template slot="prepend">Secret</template>
                    </el-input>
            </el-form-item><br>
            <el-button class="button" @click="remove">删除</el-button>
        </el-form><br>
        
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
    font-size: 1.8vh;
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
    padding: 0 3vh;
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


 /* 密码框眼睛 */
 ::v-deep .el-input .el-input__clear {
    color: #C0C4CC;
    font-size: 3vh;
    cursor: pointer;
    transition: color .2s cubic-bezier(.645,.045,.355,1);
    }

@media (min-width:1100px) { 
   
}
      

@media (min-width:1200px) { 
          /* 密码框眼睛 */
        ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        font-size: 3vh;
        cursor: pointer;
        margin-top: 0.1vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:1400px) { 
       /* 密码框眼睛 */
       ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        font-size: 3vh;
        cursor: pointer;
        margin-top: 0.2vh;
        margin-right: 0.5vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:1500px) { 

}
@media (min-width:1700px) { 
    /* 密码框眼睛 */
    ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        font-size: 3vh;
        cursor: pointer;
        margin-top: 1vh;
        margin-right: 1vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:2200px) { 
      /* 密码框眼睛 */
      ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        font-size: 3vh;
        cursor: pointer;
        margin-top: 2vh;
        margin-right: 2vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:3400px) { 
      /* 密码框眼睛 */
      ::v-deep .el-input .el-input__clear {
        color: #C0C4CC;
        font-size: 3vh;
        cursor: pointer;
        margin-top: 2.5vh;
        margin-right: 2.5vh;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
}
@media (min-width:4500px) { 
    
}
</style>