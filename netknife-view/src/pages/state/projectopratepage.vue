<template>
    <el-container class="el_container">
        <el-header  height="15px"  >
            <div class="el_header-div" >
                <el-button class="el_header-div-el_button" @click="goBack">返回</el-button>
                <div class="el_header-div-div" >
                    <h1  class="el_header-div-div-h1">
                        当前所在项目:{{ choose_project[0].slice(0,22) }}
                    </h1>
                </div>
            </div>
        </el-header>
        <el-main class="el_main">
            <el-input class="el_main-el_input" v-model="command" clearable placeholder="请输入命令"
             @keyup.enter.native="commit_command"  @input="set_effect" >
            <template slot="prepend">CLI</template>
            </el-input><br>
            <div class="el_main-div">
                <span>影响连接百分比</span>
                <el-progress class="el_main-div-el_progress" :percentage="effect_connect_percent"></el-progress>
            </div>
            <!-- <div class="el_main--div">
                <span>设备执行进度</span>
                <el-progress class="el_main--div-el_progress" :percentage="response_percent"></el-progress>
            </div> -->
            
            <el-button style="position:absolute;top:144px" type="text" @click="send_dialog_able = true">设置发送命令参数</el-button>
            <el-dialog title="设置发送命令参数" :visible.sync="send_dialog_able" width="700px" >
                <el-form :model="send_parameter">
                    <el-form-item label="是否关闭显示命令" :label-width="'130px'" style="margin-left: -20px;">
                        <el-switch
                            v-model="send_parameter.command_able"
                            active-color="#13ce66">
                        </el-switch>
                    </el-form-item>
                    <el-form-item label="是否关闭设备提示符" :label-width="'140px'" style="position:absolute;left: 170px;top:84px">
                        <el-switch
                            v-model="send_parameter.device_title_able"
                            active-color="#13ce66">
                        </el-switch>
                    </el-form-item>
                    <el-form-item label="命令输出的超时时间" :label-width="'140px'" style="position: absolute;top: 84px;left: 356px;">
                        <el-input-number v-model="send_parameter.read_timeout" :min="10" :max="1000" label="读取回显的超时时间"></el-input-number>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="send_dialog_able = false">取 消</el-button>
                    <el-button type="primary" @click="send_dialog_able = false">确 定</el-button>
                </div>
            </el-dialog>    

            <el-button style="position:absolute;top:144px;left: 250px;" type="text" @click="action_dialog_able= true">设置文件路径参数</el-button>
            <el-dialog title="设置文件路径参数" :visible.sync="action_dialog_able" width="700px" >
                <el-form :model="action_parameter">
                    <el-form-item label="EXPORT导出路径"  :label-width="'130px'">
                        <el-input  placeholder="export文件导出路径" v-model="action_parameter.export_file_path">
                            <template slot="prepend">PATH</template>
                        </el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="action_dialog_able = false">取 消</el-button>
                    <el-button type="primary" @click="action_dialog_able = false">确 定</el-button>
                </div>
            </el-dialog>    

            <el-input
            type="textarea"
            :rows="15"
            v-model="textarea"
            resize="none"
            class="el_main--el_input"
            >
            </el-input>
            <div class="el_main-loading_div" element-loading-text="等待响应中...." v-loading="loading_able"></div>
            <ul class="el_main-ul">
                <el-checkbox-group v-model="check_list" >
                    <li  v-for="item,index in response_data_list" :key="index" class="el_main-ul-li">
                        <el-checkbox :label="item.type+item.ip+':'+item.port" class="el_main-ul-li-el_checkbox" :border="true">
                        {{ item.type }} {{item.ip}} {{ item.port }}
                        </el-checkbox>
                    </li>
                </el-checkbox-group>
            </ul>
        </el-main>
    </el-container> 
</template>

<script>
import { mapMutations } from 'vuex'

export default {
    name:'ProjectOprate',
    data(){
        return {
            command:'',
            check_list:[],
            response_percent:0,
            send_dialog_able:false,
            action_dialog_able:false,
            send_parameter:{
                device_title_able:false,
                command_able:false,
                read_timeout:10
            },
            action_parameter:{
                export_file_path:'C:/Users/30862/Desktop/',
            }
            ,
     
        }
    },
    methods:{
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('projectoprateAbout',{COMMIT_COMMAND:'COMMIT_COMMAND',
        SET_EFFECT:'SET_EFFECT',SET_TEXT_AREA:'SET_TEXT_AREA',SET_GO_BACK_STATE:'SET_GO_BACK_STATE'}),
        goBack(){
            this.$router.push({
                name:'state',
            })
        },
        commit_command(){
            this.check_list=[]
            this.COMMIT_COMMAND({
                command:this.command,
                send_parameter:this.send_parameter,
                action_parameter:this.action_parameter
            })
        },
        set_effect(){
            this.SET_EFFECT(this.command)
        },
        // 关于命令发送参数函数
       
    },
    computed:{
        able(){
            return this.$store.state.devicestateAbout.able
        },
        textarea(){
            return this.$store.state.projectoprateAbout.textarea
        },
        project_name(){
            return this.$store.state.projectoprateAbout.choose_project[0]
        },
        effect_connect_percent(){
            return this.$store.state.projectoprateAbout.effect_connect_percent
        },
        choose_project(){
            return this.$store.state.projectoprateAbout.choose_project
        },
        response_data_list(){
            return this.$store.state.projectoprateAbout.response_data_list
        },
        loading_able(){
            return this.$store.state.projectoprateAbout.loading_able
        }
    },
    beforeDestroy(){
        
        this.SET_GO_BACK_STATE()
        // 销毁前将PROJECT_VIEW_ABLE设置为true
        this.SET_PROJECT_VIEW_ABLE(true)
        
    },
    watch:{
        check_list(new_value){
            this.SET_TEXT_AREA(new_value)
        }
    },
    mounted(){
        this.set_effect()
    }
}
</script>

<style scoped>
    

    .el_container{
        margin-left: -28px;
        margin-top: -20px;
        height: 500px;
        width: 990px;
       
    }
 
    .el_header-div-el_button{
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
    }
    .el_header-div-div{
        margin-left:80px;
        margin-top: -40px;
    }
    .el_header-div-div-h1{
        font-size:30px;
       
    }
    .el_main{
        margin-top: 25px;  
    }
    .el_main-el_input  {
        
        margin-top: -10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
    }

    .el_main-div{
        margin-top: -5px;
        margin-left: 320px;
    }
    .el_main-div-el_progress{
        width: 200px;
        margin-left: 130px;
        margin-top: -20px;
    
    }
    .el_main--div{
        margin-left: 330px;
        margin-top: -20px;
    }
    .el_main--div-el_progress{
        width: 200px;
        margin-left: 110px;
        margin-top: -20px; 
       
    }
    .el_main--el_input{
        margin-top: 10px;
        font-size: larger;
        width: 650px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
        
    }
    .el_main-ul{
        position: absolute;
        left: 789px;
        top:180px;
        width: 300px;
        height: 362px;
        overflow-y:scroll;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    }
    .el_main-ul-li{
        list-style: none;
        margin-bottom: 3px;
    }
    .el_main-ul-li-el_checkbox{
        width: 300px;
    }
    .el_main-loading_div{
        position: relative;
        left: 330px;
        top:-220px
    }
</style>