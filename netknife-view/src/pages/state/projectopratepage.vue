<template>
    <div style="height: 92vh;width: 98%;margin-left: 1vh;margin-top: 1vh;overflow: hidden;">
    <el-row type="flex">
        <el-col :span="3">
            <el-button-group style=";width: 100%" >
                <el-button style="width: 60%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-back" size="mini"  @click="goBack($event)">返回</el-button>
                <el-button style="width: 40%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-setting" size="mini" @click="setting_dialog_able=true"></el-button>
            </el-button-group>
        </el-col>
        <el-col :span="13">
            <el-button-group style=";width: 100%" >
                <el-button v-for="title,i in base_title" :key="i" style=";height: 4.5vh;font-size: 2vh;" :type="title.type" size="mini"  @click="goBack($event,title.type)"> {{ title.label.length>30?title.label.slice(0,30)+'...':title.label }}</el-button>
            </el-button-group>
        </el-col>
        <el-col  :span="8 "  >
            <el-button-group style="width: 100%;">
            <el-button style=" width: 35%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-arrow-left" size="mini" @click="rollback_command" >上一条命令</el-button>
            <el-button  style=" width: 35%;height: 4.5vh;font-size: 2vh;" type="primary" size="mini" @click="next_command">下一条命令<i class="el-icon-arrow-right el-icon--right"></i></el-button>
            <el-button style=" width: 15%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-document" size="mini" @click="export_textarea"></el-button>
            <el-button style=" width: 15%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-search" size="mini" @click="search_command_handler" ></el-button>
            </el-button-group>
        </el-col>
    </el-row>

    <el-row type="flex">
        <el-col :span="24">
              <!-- 影响链接百分比的进度条 -->
              <el-progress class="isolation" style="width: 99.8%;" :text-inside="true" :stroke-width="progress_size" :format="format"  :percentage="effect_connect_percent"></el-progress>
        </el-col>
    </el-row>

    <el-row type="flex" >
        <el-col :span="24">
            <el-input 
            class="cli"
            v-model="command" :clearable="true" placeholder="请输入命令"
             @keyup.enter.native="commit_command"  @input="set_effect" >
            <template slot="prepend">CLI</template>
            </el-input><br>
        </el-col>
    </el-row>     
    <!-- 文字按钮 -->
    <el-dialog  title="设置参数" :visible.sync="setting_dialog_able" width="100vh">
        <div style="height: 10vh;">
        <el-button style=" width: 8vh;height: 4vh;font-size: 2vh;margin:0 4vh 0 1vh;"  type="text" @click="send_dialog_able = true">设置命令参数</el-button>
        <el-button style=" width: 8vh;height: 4vh;font-size: 2vh;" type="text" @click="path_dialog_able= true">设置文件路径参数</el-button>
        </div>
    </el-dialog>
    <!-- 弹出框 -->
    <el-dialog title="设置命令参数" :visible.sync="send_dialog_able" width="100vh" >
        
        <el-form :model="send_parameter">
            <el-row type="flex" >
                <el-col :span="8">
                    <el-form-item label="是否关闭显示命令" :label-width="'25vh'" >
                        <el-switch
                            class='switch_size'
                            v-model="send_parameter.command_able"
                            active-color="#13ce66">
                        </el-switch>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="命令输出的超时时间" :label-width="'25vh'" style="font-size: 3vh;">
                        <el-input-number  class='input_number_size' v-model="send_parameter.read_timeout" :min="0" :max="1000" label="读取回显的超时时间"></el-input-number>
                    </el-form-item>
                   
                </el-col>
            </el-row>
            <el-row type="flex">
                <el-col :span="8">
                    <el-form-item label="是否关闭设备提示符" :label-width="'25vh'">
                        <el-switch
                            class='switch_size'
                            v-model="send_parameter.device_title_able"
                            active-color="#13ce66">
                        </el-switch>
                    </el-form-item>
                </el-col>
                <el-col :span="8">
                    <el-form-item label="历史命令上限" :label-width="'25vh'">
                        <el-input-number class='input_number_size' v-model="send_parameter.COMMAND_HISTORY_LIMIT" :min="1" :max="9999" label="历史命令上限"></el-input-number>
                    </el-form-item>
                </el-col>
            </el-row>    
        </el-form>
        <el-row type="flex"  justify="center">
            <el-col :span="4">
                <el-button @click="sendcommand_handler_cancel" class="bt"  >取 消</el-button>
            </el-col>
            <el-col :span="4">
                <el-button type="primary" @click="sendcommand_handler_commit" class="bt">确 定</el-button>
            </el-col>
        </el-row>
    </el-dialog> 
    <el-dialog title="设置文件路径参数" :visible.sync="path_dialog_able" width="100vh" >
        <el-form :model="path_parameter">
            <el-form-item label="TXT导出路径"  :label-width="'25vh'">
                <el-input class="input_size"  placeholder="TXT文件导出路径" v-model="path_parameter.txt_export_path">
                    <template slot="prepend">PATH</template>
                </el-input>
            </el-form-item>
            <el-form-item label="FTP根路径"  :label-width="'25vh'">
                <el-input class="input_size"   placeholder="FTP根路径" v-model="path_parameter.ftp_root_path">
                    <template slot="prepend">PATH</template>
                </el-input>
            </el-form-item>
            <el-form-item label="FTP上传文件路径"  :label-width="'25vh'">
                <el-input class="input_size"  placeholder="FTP上传文件路径" v-model="path_parameter.ftp_upload_path">
                    <template slot="prepend">PATH</template>
                </el-input>
            </el-form-item>
            <el-form-item label="FTP下载文件路径"  :label-width="'25vh'">
                <el-input class="input_size"  placeholder="FTP下载文件路径" v-model="path_parameter.ftp_download_path">
                    <template slot="prepend">PATH</template>
                </el-input>
            </el-form-item>
        </el-form>
        <el-row type="flex"  justify="center">
            <el-col :span="4">
                <el-button @click="filepath_handler_cancel" class="bt"  >取 消</el-button>
            </el-col>
            <el-col :span="4">
                <el-button type="primary" @click="filepath_handler_commit" class="bt">确 定</el-button>
            </el-col>
        </el-row>
    </el-dialog>
    <!-- 搜索历史命令 -->
    <el-dialog  title="搜索历史命令" :visible.sync="search_command_history_able" width="120vh" >
        <el-row>
            <el-col :span="24">
                <el-autocomplete
                    class="search"
                    style="width: 100%;height: 4vh;z-index: 1;"
                    prefix-icon="el-icon-search"
                    v-model="input"
                    :popper-append-to-body="false"
                    :fetch-suggestions="querySearchAsync"
                    placeholder="输入命令或执行时间进行检索"
                    @select="handleSelect"
                    ></el-autocomplete>
            </el-col>
        </el-row>
        <div style="height:66vh;overflow: scroll;">
            <ul class="his_ul">
                <li  v-for="(item,i) in all_command_time_list " :key="i" > 
                    <el-card class="cmd_his_about" style="height: 10vh;width: 115vh;font-size: 2vh;" >
                        <el-button-group style="float: right;margin-top: -20px;margin-right:-20px;" >
                            <el-button style="width: 12vh;height: 4.5vh;font-size: 2vh;line-height: 1vh;" type="primary"  @click="show_history_command(item[0],item[1],i)" >查看</el-button>
                            <el-button style="width: 12vh;height: 4.5vh;font-size: 2vh;line-height: 1vh;" type="primary"  @click="delete_history_command(item[0],item[1],item[2],i)">删除</el-button>
                        </el-button-group>
                        命令:{{ item[0] }}<br>
                        执行时间:{{ item[1] }} <br>
                    </el-card>
                </li>
            </ul>
        </div>
    </el-dialog>
   
    <!-- 加载动画loading_able -->
    <div  element-loading-text="等待响应中...." v-loading="loading_able"></div> 
   
    <el-row type="flex" >
        <el-col :span="16">
             <!--输出框  -->
            <el-input
            style="width: 100%;font-size: 2.5vh;"
            type="textarea"
            :rows="30"
            v-model="textarea"
            resize="none"
            class="el_main--el_input"
            >
            </el-input>
        </el-col>
        <el-col :span="8">
             <!-- 输出选择列表框 -->
            <ul   class="el_main-ul" >
                <el-checkbox-group v-model="check_list" >
                    <li style="margin-left: 1vh;" v-for="item,index in response_data_list" :key="index" >
                        <el-checkbox  :style="check_cls_obj" :checked="true"  :label="item.type+item.ip+':'+item.port"  >   
                        {{ item.type }} {{item.ip}} {{ item.port }}
                        </el-checkbox>
                    </li>
                </el-checkbox-group>
            </ul>
        </el-col>
    </el-row>
    <el-row type="flex">
        <el-col :span=24>
            <div style="position: relative;top:-1vh; width: 100%;height: 1vh;background-color:#272822;" ></div>
        </el-col>
    </el-row>
    </div>
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
            input:'',
            progress_size:document.documentElement.clientHeight/150,
            check_cls_obj:{
                zoom:document.documentElement.clientHeight/600,
            }
            
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
        ...mapMutations('projectoprateAbout',{SET_OPRATE_MODE:'SET_OPRATE_MODE'}),
        goBack(event,title_type){
            // 通过菜单界面跳转
            if(!(title_type===undefined)){
                if(title_type==='primary'){
                    console.log('primary界面')
                    this.SET_OPRATE_MODE('project')
                    this.SET_PROJECT_VIEW_ABLE(true)
                    this.$router.push({
                    name:'state',
                    })
                    return
                }else{
                    console.log('mixunit界面')
                    this.SET_PROJECT_VIEW_ABLE(false)
                    this.SET_MIXUNIT_VIEW_ABLE(true)
                    this.$router.push({
                    name:'mixunit',
                    params:{
                        'project':this.choose_project[0]
                    }
                    })
                    return
                }
            }
            // 通过返回按钮跳转
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
            })
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
            })
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
            if(this.command_index<=-1){
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
                if(this.choose_project[0]===undefined) return ['NULL']
                return [{type:'primary',label:this.choose_project[0].slice(0,42)}]
            }else{
                if(this.choose_project[0]===undefined) return ['NULL','NULL','NULL']
                return [{type:'primary',label:this.choose_project[0].slice(0,42)},
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
                    console.log(response.data)
                    // 刷新页面
                    if (response.data==='RELOAD_PAGE') return
                    //正常
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
                })
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
                    // 刷新页面
                    if (response.data==='RELOAD_PAGE') return
                    // 正常
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
            // 刷新页面
            if (response.data==='RELOAD_PAGE') return
            // 正常
            this.path_parameter.txt_export_path=response.data[0][0]
            this.path_parameter.ftp_root_path=response.data[0][1]
            this.path_parameter.ftp_upload_path=response.data[0][2]
            this.path_parameter.ftp_download_path=response.data[0][3]
            send_post('/start_ftp_server',{'ftp_root_path':this.path_parameter.ftp_root_path})
        })
        send_post('/get_sendcommand_parameter',{
            'project':this.choose_project[0],
            // 'area':'None'
            'mode':this.oprate_mode,
            'area':this.choose_mixunit[3],
        },response=>{
            console.log(response.data)
            // 刷新页面
            if (response.data==='RELOAD_PAGE') return
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
        })
        this.SET_HISTORY_COMMAND_COUNT()
        const _this = this;
        window.onresize = ()=>{
            return (() => {
           
            _this.progress_size =document.documentElement.clientHeight/150;
            _this.check_cls_obj.zoom=document.documentElement.clientHeight/600;
            })();
        };
    },

}
</script>



<style lang="scss" scoped>

//历史命令搜索框
.search ::v-deep .el-input__inner {
        height: 5vh;
        font-size: 2vh;
        padding-left: 4vh;
        border-radius: 0.8vh;
       
}
.search ::v-deep .el-input__icon {
        height: 100%;
        width: 3vh;
        font-size: 2vh;
        line-height: 100%;
        padding-top: 0.3vh;
        
      
}
 ::v-deep .el-autocomplete-suggestion li{
    padding: 0 1vh;
    margin: 0;
    line-height: 4vh;
    cursor: pointer;
    color: #606266;
    font-size: 2vh;
    list-style: none;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
   
}
::v-deep .el-autocomplete-suggestion__wrap {
    max-height: 20vh;
    padding: 1vh 0;
    box-sizing: border-box;
}
// 
// dialog框相关
::v-deep .el-form-item__label {
    text-align: center;
    vertical-align: middle;
    float: left;
    font-size: 2vh;
    color: #606266;
    line-height: 4.3vh;
    padding: 0 12px 0 0;
    box-sizing: border-box;
}
 ::v-deep .el-dialog__title {
    line-height: 2vh;
    font-size:2vh;
    color: #303133;
    margin: 1vh;
}

  ::v-deep .el-dialog__header {
    padding: 2vh 2vh 1vh;
}

  ::v-deep .el-dialog__body {
    padding: 3vh 2.2vh;
    color: #606266;
    font-size: 1vh;
    word-break: break-all;
}
// 

 ::v-deep .el-dialog__headerbtn {
    position: absolute;
    top: 2vh;
    right: 2vh;
    padding: 0;
    background: 0 0;
    border: none;
    outline: 0;
    cursor: pointer;
    font-size: 2vh;
}

    .tag:nth-child(1){
        height: 4.5vh;
        border-radius: 0.5vh 0 0 0.5vh;
        font-size: 2vh;
        line-height: 4vh;
        text-align: center;
        // margin-top: 1vh;
        // margin-left: 1vh;
    }
     .tag:nth-child(3){
        height: 4.5vh;
        border-radius: 0 0.5vh 0.5vh 0;
        font-size: 2vh;
        line-height: 4vh;
        text-align: center;
        // margin-top: 1vh;
        // margin-left: 1vh;
    }
    .tag{
        height: 4.5vh;
        border-radius: 0;
        font-size: 2vh;
        line-height: 4vh;
        text-align: center;
      
    }
    
    .cli{
        // margin: 1vh;
    }
    .cli ::v-deep .el-input__inner {
        -webkit-appearance: none;
        background-color: #272822;
        background-image: none;
        border-radius: 0;
        border: 0.2vh solid #272822;
        box-sizing: border-box;
        color: #ffffff;
        display: inline-block;
        outline: 0;
        padding: 0 3vh;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
        height: 7vh;
        width: 100%;
        font-size: 4vh; 
        font-weight: 400;
    } 
    .cli ::v-deep  .el-input-group__prepend{
        background-color: #272822;
        color: #909399;
        vertical-align: middle;
        display: table-cell;
        position: relative;
        border: 0.2vh solid #272822;
        border-right: 0;
        border-radius: 0;
        padding-left: 5VH;
        white-space: nowrap;
        font-size: 4vh;
        text-align: center;

    }
    
   ::v-deep .el-input__suffix {
        height: 4vh;
        right: 5vh;
        transition: all .3s;
        pointer-events: none;
    }
    ::v-deep  .el-input__clear {
    color: #C0C4CC;
    font-size:3vh;
    margin-top: 0.3vh;
    cursor: pointer;
    transition: color .2s cubic-bezier(.645,.045,.355,1);
    }
    .isolation{
        margin-top: -1vh;
    }
    
    .el_main-div{
        position: absolute;
       
    }
    .el_main-div-el_progress{
        width:300px;
        margin-top: 30px;
        margin-left: 668px;
    }
    // 输出框
    .el_main--el_input{
        font-size: larger;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);

    }

    ::v-deep .el-textarea__inner {
        display: block;
        resize: vertical;
        padding: 0px 0px;
        line-height: 1;
        box-sizing: border-box;
        width: 100%;
        font-size: inherit;
        font-weight: 900;
        color: #ffffff;
        background-color: #272822;
        background-image: none;
        border: 1px solid #272822;
        border-radius: 0;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
    }

    //

    // 选择框
    ::v-deep .el-checkbox__input.is-checked+.el-checkbox__label {
    color: #ffffff;
        }
    ::v-deep .el-checkbox__input.is-checked .el-checkbox__inner, .el-checkbox__input.is-indeterminate .el-checkbox__inner {
    background-color: #272822;
    border-color: #272822;
    }
    .el_main-ul{
       border-bottom:0.3vh solid #272822;
        width:100%;
        height: 75vh;
        overflow-y:scroll;
        background-color: #272822;
        box-shadow: 0 1vh 4vh rgba(0, 0, 0, .12), 0 0 1vh rgba(0, 0, 0, .04);
    }
    ::v-deep .el-checkbox.is-bordered {

        padding: 9px 20vh 9px 12vh;

    }
    // 进度加载圈
   ::v-deep .el-loading-spinner {
    top: 50%;
    margin-top: 25vh;
    margin-left: -28vh;
    width: 100%;
    text-align: center;
    position: absolute;
    }
   ::v-deep  .el-loading-spinner .el-loading-text {
    color: #ffffff;
    margin: 0.5vh 0;
    font-size: 2vh;
    }
   ::v-deep .el-loading-spinner .circular {
    height: 10vh;
    width: 10vh;
    animation: loading-rotate 2s linear infinite;
    }
    // /////////////////////////////////////
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

    li{
    list-style-type: none;
    margin-top: 2px;
    }
    li:first-child{
        margin-top: 10px;
    }
   
    @media (min-width:900px) { 
           .switch_size{
            margin-top: -3vh;
            margin-left: -1vh;
            }
            .cmd_his_about {
                line-height: 2.5vh;
            }
          
    }
    @media (min-width:1200px) { 
        ::v-deep  .el-input__clear {
        color: #C0C4CC;
        font-size:3vh;
        margin-top: 1vh;
        margin-right: 1vw;
        cursor: pointer;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
        .isolation{
            margin-top: -0.4vh;
        }
        .switch_size{
            zoom:1.2;
            margin-top: -0.5vh;
        }
        .input_number_size{
          
            zoom:1.2;
            margin-top: -1vh;
        }
        .bt{
            zoom:1.2
        }
        .input_size{
            zoom: 1.2;
            margin-left: -1.2vh;
           
        }
     
    }
    @media (min-width:1500px) { 
        ::v-deep  .el-input__clear {
        color: #C0C4CC;
        font-size:3vh;
        margin-top: 1.6vh;
        margin-right: 1vw;
        cursor: pointer;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
        .isolation{
            margin-top: -0.3vh;
        }
        .input_number_size{
            zoom:1.3;
            margin-top: -0.3vh;
        }
        .bt{
            zoom:1.4
        }
        .input_size{
            zoom: 1.4;
        }
    }
    @media (min-width:1800px) { 
        ::v-deep  .el-input__clear {
        color: #C0C4CC;
        font-size:3vh;
        margin-top: 2.2vh;
        margin-right: 1vw;
        cursor: pointer;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
        .isolation{
            margin-top: 0.15vh;
        }
        .switch_size{
            zoom:2;
            margin-top: 0.3vh;
        }
        .input_number_size{
            zoom:2;
            margin-top:-0.3vh;
          
        }
        .bt{
            zoom:2
        }
        .input_size{
            zoom: 2;
        }
        .cmd_his_about {
                line-height: 3vh;
            }
    }
    @media (min-width:2200px) { 
        ::v-deep  .el-input__clear {
        color: #C0C4CC;
        font-size:3vh;
        margin-top: 2.6vh;
        margin-right: 1vw;
        cursor: pointer;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
        .isolation{
            margin-top: 0.4vh;
        }
        .switch_size{
            zoom:2;
            margin-top:0.3vh;
        }
        .input_number_size{
            zoom:2;
           
        }
        .bt{
            zoom:2
        }
        .input_size{
            zoom: 2;
        }
        .cmd_his_about {
                line-height: 3.5vh;
            }
    }
    @media (min-width:2400px) { 
        ::v-deep  .el-input__clear {
        color: #C0C4CC;
        font-size:3vh;
        margin-top: 2.6vh;
        margin-right: 1vw;
        cursor: pointer;
        transition: color .2s cubic-bezier(.645,.045,.355,1);
        }
        .isolation{
            margin-top: 0.4vh;
        }
        .switch_size{
            zoom:2.5;
            margin-top: 0.3vh;
        }
        .input_number_size{
            zoom:2.5;
           
        }
        .bt{
            zoom:2.5
        }
        .input_size{
            zoom: 2.5;
        }
    }
    
</style>



