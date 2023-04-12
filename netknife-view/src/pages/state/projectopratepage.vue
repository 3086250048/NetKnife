<template>
    <el-container class="el_container">
        <el-header  height="0px"  >
            <div class="title">
                    <el-tag
                    v-for="title,i in base_title"
                    :key="i"
                    effect="dark"
                    size="mini"
                    :type="title.type"
                    >
                    {{ title.label  }}
                    </el-tag><br>
            </div>     
        </el-header>
        <el-main class="el_main">
            <el-input class="el_main-el_input" v-model="command" clearable placeholder="请输入命令"
             @keyup.enter.native="commit_command"  @input="set_effect" >
            <template slot="prepend">CLI</template>
            </el-input><br>
            
            <!-- 影响链接百分比的进度条 -->
            <div class="el_main-div">
                <el-progress :text-inside="true" :stroke-width="5" :format="format" class="el_main-div-el_progress" :percentage="effect_connect_percent"></el-progress>
            </div>
            <!-- 文字按钮 -->
            <el-dialog title="设置参数" :visible.sync="setting_dialog_able" width="700px">
                <el-button  type="text" @click="send_dialog_able = true">设置命令参数</el-button>
                <el-button  type="text" @click="path_dialog_able= true">设置文件路径参数</el-button>
            </el-dialog>
            <!-- 弹出框 -->
            <el-dialog title="设置命令参数" :visible.sync="send_dialog_able" width="700px" >
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
                        <el-input-number v-model="send_parameter.read_timeout" :min="0" :max="1000" label="读取回显的超时时间"></el-input-number>
                    </el-form-item>
                    <el-form-item label="历史命令上限" :label-width="'140px'" style="position: absolute;top: 134px;left: -38px;">
                        <el-input-number v-model="send_parameter.COMMAND_HISTORY_LIMIT" :min="1" :max="9999" label="历史命令上限"></el-input-number>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="sendcommand_handler_cancel">取 消</el-button>
                    <el-button type="primary" @click="sendcommand_handler_commit">确 定</el-button>
                </div>
            </el-dialog> 
            <el-dialog title="设置文件路径参数" :visible.sync="path_dialog_able" width="700px" >
                <el-form :model="path_parameter">
                    <el-form-item label="TXT导出路径"  :label-width="'130px'">
                        <el-input  placeholder="TXT文件导出路径" v-model="path_parameter.txt_export_path">
                            <template slot="prepend">PATH</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="FTP根路径"  :label-width="'130px'">
                        <el-input  placeholder="FTP根路径" v-model="path_parameter.ftp_root_path">
                            <template slot="prepend">PATH</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="FTP上传文件路径"  :label-width="'130px'">
                        <el-input  placeholder="FTP上传文件路径" v-model="path_parameter.ftp_upload_path">
                            <template slot="prepend">PATH</template>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="FTP下载文件路径"  :label-width="'130px'">
                        <el-input  placeholder="FTP下载文件路径" v-model="path_parameter.ftp_download_path">
                            <template slot="prepend">PATH</template>
                        </el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="filepath_handler_cancel">取 消</el-button>
                    <el-button type="primary" @click="filepath_handler_commit">确 定</el-button>
                </div>
            </el-dialog>
            <!-- 搜索历史命令 -->
            <el-dialog title="搜索历史命令" :visible.sync="search_command_history_able" width="800px" >
                <el-autocomplete
                prefix-icon="el-icon-search"
                class="search"
                v-model="input"
                :fetch-suggestions="querySearchAsync"
                placeholder="输入命令或执行时间进行检索"
                @select="handleSelect"
                ></el-autocomplete>
                <div style="height: 350px;overflow: scroll;">
                    <ul>
                        <li v-for="(item,i) in all_command_time_list " :key="i" > 
                            <el-card class="box-card" >
                                <el-button-group style="float: right;margin-top: -20px;margin-right:-20px;" >
                                    <el-button type="primary" size="mini" @click="show_history_command(item[0],item[1],i)" >查看</el-button>
                                    <el-button type="primary" size="mini" @click="delete_history_command(item[0],item[1],item[2],i)">删除</el-button>
                                </el-button-group>
                                命令:{{ item[0] }}<br>
                                执行时间:{{ item[1] }} <br>
                            </el-card>
                        </li>
                    </ul>
                </div>
            </el-dialog>
            <!--输出框  -->
            <el-input
            type="textarea"
            :rows="18"
            v-model="textarea"
            resize="none"
            class="el_main--el_input"
            >
            </el-input>
            <!-- 加载动画 -->
            <div class="el_main-loading_div" element-loading-text="等待响应中...." v-loading="loading_able"></div>
            <!-- 历史命令按钮组 -->
            <el-button-group class="el_main-el_button_group">
            <el-button type="primary" icon="el-icon-arrow-left" size="mini" @click="rollback_command" >上一条命令</el-button>
            <el-button type="primary" size="mini" @click="next_command">下一条命令<i class="el-icon-arrow-right el-icon--right"></i></el-button>
            <el-button type="primary" icon="el-icon-document" size="mini" @click="export_textarea"></el-button>
            <el-button type="primary" icon="el-icon-search" size="mini" @click="search_command_handler" ></el-button>
            </el-button-group>
            <!-- 设置按钮组 -->
            <el-button-group class="el_main--el_button_group">
                <el-button type="primary" icon="el-icon-back" size="mini" @click="goBack">返回</el-button>
                <el-button type="primary" icon="el-icon-setting" size="mini" @click="setting_dialog_able=true"></el-button>
            </el-button-group>
            <!-- 输出选择列表框 -->
            <ul class="el_main-ul">
                <el-checkbox-group v-model="check_list" >
                    <li  v-for="item,index in response_data_list" :key="index" class="el_main-ul-li">
                        <el-checkbox :checked="true" :label="item.type+item.ip+':'+item.port" class="el_main-ul-li-el_checkbox" :border="true">
                        {{ item.type }} {{item.ip}} {{ item.port }}
                        </el-checkbox>
                    </li>
                </el-checkbox-group>
            </ul>
        </el-main>
    </el-container> 
</template>

<script>
import { send_get, send_post } from '@/store/tools'
import { mapMutations } from 'vuex'

export default {
    name:'ProjectOprate',
    data(){
        return {
            command:'',
            check_list:[],
            response_percent:0,
            send_dialog_able:false,
            path_dialog_able:false,
            send_parameter:{
                device_title_able:false,
                command_able:false,
                read_timeout:10,
                COMMAND_HISTORY_LIMIT:500
            },
            path_parameter:{
                txt_export_path:'',
                ftp_root_path:'',
                ftp_upload_path:'',
                ftp_download_path:''
            },
            setting_dialog_able:false,
            search_command_history_able:false,
            input:''
        }
    },
    methods:{
        format(){
            return ``
        },
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('projectoprateAbout',{
            COMMIT_COMMAND:'COMMIT_COMMAND',
            SET_EFFECT:'SET_EFFECT',
            SET_TEXT_AREA:'SET_TEXT_AREA',
            SET_GO_BACK_STATE:'SET_GO_BACK_STATE',
            SET_CHOOSE_MIXUNIT:'SET_CHOOSE_MIXUNIT',
            SET_CHOOSE_PROJECT:'SET_CHOOSE_PROJECT',
            ROLLBACK_COMMAND:'ROLLBACK_COMMAND',
            NEXT_COMMAND:'NEXT_COMMAND',
            SET_COMMAND_INDEX:'SET_COMMAND_INDEX',
            SET_HISTORY_COMMAND_COUNT:'SET_HISTORY_COMMAND_COUNT',
            EXPORT_TEXTAREA:'EXPORT_TEXTAREA',
            GET_ALL_COMMAND_TIME:'GET_ALL_COMMAND_TIME',
            ROLLBACK_MIXUNIT_LIST:'ROLLBACK_MIXUNIT_LIST',
            CHOOSE_CHANGE:'CHOOSE_CHANGE',
            SHOW_HISTORY_COMMAND:'SHOW_HISTORY_COMMAND',
            DELETE_HISTORY_COMMAND:'DELETE_HISTORY_COMMAND',
            SET_VM:'SET_VM'
        }),
        ...mapMutations('mixunitpageAbout',{SET_MIXUNIT_VIEW_ABLE:'SET_MIXUNIT_VIEW_ABLE'}),
        goBack(){
            if(this.choose_mixunit.length>0){
                this.SET_PROJECT_VIEW_ABLE(false)
                this.SET_MIXUNIT_VIEW_ABLE(true)
                this.$router.push({
                name:'mixunit',
                params:{
                    'project':this.choose_project[0]
                }
                })
            }else{
                this.SET_PROJECT_VIEW_ABLE(true)
                this.$router.push({
                name:'state',
                })
            }

        },
        //提交命令
        commit_command(){
            if(this.command.length<=0){
                this.$message({
                    showClose: true,
                    message: '命令不能为空',
                    type: 'warning'
                });
                return
            }
            this.check_list=[]
            this.COMMIT_COMMAND({
                command:this.command,
                send_parameter:this.send_parameter,
                path_parameter:this.path_parameter,
                choose_mixunit:this.choose_mixunit
            })
        },
        set_effect(){
            this.SET_EFFECT(this.command)
        },
        sendcommand_handler_cancel(){
            this.send_dialog_able=false
        },
        sendcommand_handler_commit(){
           
            send_post('/change_sendcommand_parameter',{
                'where':{
                    'project':this.choose_project[0],
                    // 'area':'None',
                    'mode':this.oprate_mode,
                    'area':this.choose_mixunit[3]
                },
                'update':{
                    device_title_able:this.send_parameter.device_title_able,
                    command_able:this.send_parameter.command_able,
                    read_timeout:this.send_parameter.read_timeout,
                    COMMAND_HISTORY_LIMIT:this.send_parameter.COMMAND_HISTORY_LIMIT
                }
            },response=>{
                console.log(response.data)
                this.send_dialog_able=false
            },reason=>{})
        },
        filepath_handler_cancel(){
            this.path_dialog_able=false
        },
        filepath_handler_commit(){
            
            send_post('/change_filepath_parameter',{
                'where':{
                    'project':this.choose_project[0],
                    // 'area':'None',
                    'mode':this.oprate_mode,
                    'area':this.choose_mixunit[3]
                },
                'update':{
                    'txt_export_path': this.path_parameter.txt_export_path,
                    'ftp_root_path':this.path_parameter.ftp_root_path,  
                    'ftp_upload_path':this.path_parameter.ftp_upload_path,
                    'ftp_download_path':this.path_parameter.ftp_download_path,
                }
            },response=>{
                console.log(response.data)
                this.path_dialog_able=false
            },reason=>{})
        },
        rollback_command(){
            if(this.command_index>=this.history_command_count-1){
                this.$message({
                    showClose: true,
                    message: '已经是最早的一条命令了',
                    type: 'warning'
                });
                return
            }
            this.check_list=[]
            this.ROLLBACK_COMMAND()
            console.log(this.command_index)
        },
        next_command(){
            if(this,this.command_index<=-1){
                this.$message({
                    showClose: true,
                    message: '没有更多命令了',
                    type: 'warning'
                });
                return
            }
            if(this.command_index<=0){
                this.$message({
                    showClose: true,
                    message: '已经是最后一条命令了',
                    type: 'warning'
                });
                return
            }
            this.check_list=[]
            this.NEXT_COMMAND(this)
            console.log(this.command_index)
        },
        export_textarea(){
            this.EXPORT_TEXTAREA({
                'command':this.command,
                'vm':this,
                'txt_export_path':this.path_parameter.txt_export_path
            })
        },
        search_command_handler(){
            this.search_command_history_able=true
            this.input=''
            this.GET_ALL_COMMAND_TIME()
        },
        querySearchAsync(queryString, cb) {
            let results=this.all_command_time_search_list
            results = queryString ? results.filter(this.createStateFilter(queryString)) : results;
            cb(results);
        },
        createStateFilter(queryString) {
        return (item) => {
          return item.value.toLowerCase().match(queryString.toLowerCase());
        };
        },
        handleSelect(item) {
            this.CHOOSE_CHANGE(item)
        },
        show_history_command(command,date_time,i){
            this.check_list=[]
            this.search_command_history_able=false
            this.SHOW_HISTORY_COMMAND({
                'command':command,
                'date_time':date_time,
                'index':i
            })

        },
        delete_history_command(command,date_time,id,i){
            this.check_list=[]
            this.DELETE_HISTORY_COMMAND({
                'command':command,
                'date_time':date_time,
                'id':id,
                'index':i
            })
        }

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
        choose_mixunit(){
            return this.$store.state.projectoprateAbout.choose_mixunit
        },
        response_data_list(){
            return this.$store.state.projectoprateAbout.response_data_list
        },
        loading_able(){
            return this.$store.state.projectoprateAbout.loading_able
        },
        base_title(){
            if(this.choose_mixunit.length===0 ){
                return [{type:'',label:this.choose_project[0].slice(0,42)}]
            }else{
                return [{type:'',label:this.choose_project[0].slice(0,42)},
                        {type:'success',label:this.choose_mixunit[3]},
                        {type:'danger',label:`${this.choose_mixunit[4]}://${this.choose_mixunit[9]}:${this.choose_mixunit[5]}`}
                    ]
            }
        },
        oprate_mode(){
            return this.$store.state.projectoprateAbout.oprate_mode
        },
        command_index(){
            return this.$store.state.projectoprateAbout.command_index
        },
        history_command(){
            return this.$store.state.projectoprateAbout.history_command
        },
        history_command_count(){
            return this.$store.state.projectoprateAbout.history_command_count
        },
        all_command_time_search_list(){
            return this.$store.state.projectoprateAbout.all_command_time_search_list
        },
        all_command_time_list(){
            return this.$store.state.projectoprateAbout.all_command_time_list
        },
        
   

    },
    beforeDestroy(){
        send_get('/stop_ftp_serve')
        this.SET_CHOOSE_MIXUNIT([])
        this.SET_GO_BACK_STATE()
        this.SET_COMMAND_INDEX(-1)        
    },
    watch:{
        check_list(new_value){
            this.SET_TEXT_AREA(new_value)
        },
        send_dialog_able(new_value){
            //  if(new_value){
                send_post('/get_sendcommand_parameter',{
                    'project':this.choose_project[0],
                    // 'area':'None'
                    'mode':this.oprate_mode,
                    'area':this.choose_mixunit[3],
                },response=>{
                    if(response.data[0][0]=='False'){
                        this.send_parameter.device_title_able=false
                    }else{
                        this.send_parameter.device_title_able=true
                    }
                    if(response.data[0][1]=='False'){
                        this.send_parameter.command_able=false
                    }else{
                        this.send_parameter.command_able=true
                    }
                    this.send_parameter.read_timeout=response.data[0][2]
                    this.send_parameter.COMMAND_HISTORY_LIMIT=response.data[0][3]
                },reason=>{})
            // }
            console.log(this.send_parameter)
        },
        path_dialog_able(new_value){
            // if(new_value){
                send_post('/get_filepath_parameter',{
                    'project':this.choose_project[0],
                    // 'area':'None'
                    'mode':this.oprate_mode,
                    'area':this.choose_mixunit[3],
                },response=>{
                    this.path_parameter.txt_export_path=response.data[0][0]
                    this.path_parameter.ftp_root_path=response.data[0][1]
                    this.path_parameter.ftp_upload_path=response.data[0][2]
                    this.path_parameter.ftp_download_path=response.data[0][3]
                },reason=>{})
            // }
        },
        history_command(new_value){
            this.command=new_value
          
        },
        input(new_value,old_value){
            if(old_value!=='' && new_value===''){
                this.ROLLBACK_MIXUNIT_LIST()
            }
        },
    },
    mounted(){
        this.SET_VM(this)
        this.set_effect()
        // 加载初始化参数
        send_post('/get_filepath_parameter',{
            'project':this.choose_project[0],
            // 'area':'None'
            'mode':this.oprate_mode,
            'area':this.choose_mixunit[3],
        },response=>{
            console.log(response.data)
            this.path_parameter.txt_export_path=response.data[0][0]
            this.path_parameter.ftp_root_path=response.data[0][1]
            this.path_parameter.ftp_upload_path=response.data[0][2]
            this.path_parameter.ftp_download_path=response.data[0][3]
            send_post('/start_ftp_server',{'ftp_root_path':this.path_parameter.ftp_root_path})
        },reason=>{})
        send_post('/get_sendcommand_parameter',{
            'project':this.choose_project[0],
            // 'area':'None'
            'mode':this.oprate_mode,
            'area':this.choose_mixunit[3],
        },response=>{
            if(response.data[0][0]=='False'){
                this.send_parameter.device_title_able=false
            }else{
                this.send_parameter.device_title_able=true
            }
            if(response.data[0][1]=='False'){
                this.send_parameter.command_able=false
            }else{
                this.send_parameter.command_able=true
            }
            this.send_parameter.read_timeout=response.data[0][2]
            this.send_parameter.COMMAND_HISTORY_LIMIT=response.data[0][3]
        },reason=>{})
        this.SET_HISTORY_COMMAND_COUNT()
    },

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
        font-size:22px;
        margin-top: 4px;
    }
    .el_main{
        margin-top: 25px;  
    }
    .el_main-el_input  {
        position: absolute;
        width: 970px;
        margin-top: -17px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
    }

    .el_main-div{
        position: absolute;
       
    }
    .el_main-div-el_progress{
        width:300px;
        margin-top: 30px;
        margin-left: 668px;
    }
    .el_main--div{
        margin-left: 330px;
        margin-top: -20px;
    }
    /* .el_main--div-el_progress{
        width: 200px;
        margin-left: 110px;
        margin-top: -20px; 
       
    } */
    .el_main--el_input{
        position: absolute;
        top: 168px;
        font-size: larger;
        width: 660px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
        
    }
    .el_main-ul{
        position: absolute;
        left: 789px;
        top:170px;
        width: 300px;
        height: 430px;
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
        position: absolute;
        left: 840px;
        top:340px;
        width:200px
    }
    .el_main-el_button_group{
        position: absolute;
        top: 136px;
        left: 789px;
    }
    .el_main--el_button_group{
        position: absolute;
        top: 136px;
        left: 122px;
    }
    .search{
        width: 760px;
        position: absolute;
        top: 45px;
    }
    li{
    list-style-type: none;
    margin-top: 2px;
    }
    li:first-child{
        margin-top: 10px;
    }
    .title{
        font-size: 20px; 
    }
    
    
    
</style>