<template>
    <el-container class="el_container">
        <el-header  height="15px"  >
            <div class="el_header-div" >
                <el-button class="el_header-div-el_button" @click="goBack">返回</el-button>
                <div class="el_header-div-div" >
                    <h1  class="el_header-div-div-h1">
                        当前所在项目:{{ choose_project[0].slice(0,25) }}
                    </h1>
                </div>
            </div>
        </el-header>
        <el-main>
            <el-input class="el_main-el_input" v-model="command" clearable placeholder="请输入内容"
             @keyup.enter.native="commit_command" @input="set_effect">
            <template slot="prepend">CLI</template>
            </el-input><br>
            <div class="el_main-div">
                <span>影响连接百分比</span>
                <el-progress class="el_main-div-el_progress" :percentage="effect_connect_percent"></el-progress>
            </div>
            <div class="el_main--div">
                <span>设备执行进度</span>
                <el-progress class="el_main--div-el_progress" :percentage="96"></el-progress>
            </div>
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
           
        }
    },
    methods:{
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('projectoprateAbout',{COMMIT_COMMAND:'COMMIT_COMMAND',
        SET_EFFECT:'SET_EFFECT',SET_TEXT_AREA:'SET_TEXT_AREA',SET_GO_BACK_STATE:'SET_GO_BACK_STATE'}),
        goBack(){
            this.commit_command=false
            this.SET_GO_BACK_STATE()
            this.$router.push({
                name:'state',
            })
        },
        commit_command(){
            this.check_list=[]
            this.COMMIT_COMMAND(this.command)
        },
        set_effect(){
            this.SET_EFFECT(this.command)
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
        response_data_list(){
            return this.$store.state.projectoprateAbout.response_data_list
        },
        loading_able(){
            return this.$store.state.projectoprateAbout.loading_able
        }
    },
    beforeDestroy(){
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
        margin-left: -30px;
    }
    .el_header-div{
        margin-top: -20px;
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
    .el_main-el_input{
        margin-top: -10px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
    }
    .el_main-div{
        margin-top: -5px;
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
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
    }
    .el_main-ul{
        position: relative;
        width: 300px;
        left: 660px;
        top: -363px;
        overflow-y:scroll;
        height: 362px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
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