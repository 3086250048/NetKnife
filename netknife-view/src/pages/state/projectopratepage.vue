<template>
    <el-container style="margin-left: -30px;" >
        <el-header height="15px"  >
            <div style="margin-top: -20px;">
                <el-button @click="goBack">返回</el-button>
                <div style="margin-left:80px;margin-top: -40px;" > <h1  style="font-size:30px;">当前所在项目:{{ choose_project[0].slice(0,80) }}</h1></div>
            </div>
        </el-header>
        <el-main>
            <el-input style="margin-top: -10px;margin-bottom: 10px;" v-model="command" clearable placeholder="请输入内容" @change="commit_command" @input="set_effect">
            <template slot="prepend">CLI</template>
            </el-input><br>
            <div style="margin-top: -5px;">
                    <span>影响连接百分比</span><el-progress style="width: 200px;margin-left: 130px;margin-top: -20px;" :percentage="effect_connect_percent"></el-progress>
            </div>
            <div style="margin-left: 330px;margin-top: -20px;">
                <span>设备执行进度</span><el-progress style="width: 200px;margin-left: 110px;margin-top: -20px;" :percentage="96"></el-progress>
            </div>
            <el-input
            type="textarea"
            :rows="15"
            v-model="textarea"
            resize="none"
            class="info_box"
            style="font-size: larger;width: 650px;"
            >
            </el-input>
            <ul style="position: relative;left: 660px;top: -363px;overflow-y:scroll;height: 362px;">
                <li v-for="ip in ip_list" :key="ip" style="list-style: none;margin-bottom: 3px;">
                    <el-checkbox style="width: 300px;" :border="true"  >{{ip}}</el-checkbox>
                </li>
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
            ip_list:['192.168.1.0','192.168.2.0','192.168.3.0','192.168.4.0','192.168.5.0','192.168.6.0','192.168.7.0','192.168.8.0','192.168.9.0','192.168.10.0','192.168.11.0']
        }
    },
    methods:{
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('projectoprateAbout',{COMMIT_COMMAND:'COMMIT_COMMAND',SET_EFFECT:'SET_EFFECT'}),
        goBack(){
            this.COMMIT_COMMAND('')
            this.$router.push({
                name:'state',
            })
        },
        commit_command(){
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
        }
    },
    beforeDestroy(){
        // 销毁前将PROJECT_VIEW_ABLE设置为true
        this.SET_PROJECT_VIEW_ABLE(true)
    },
    mounted(){
        this.set_effect()
    }
}
</script>

<style>
    .info_box{
        width: 800px;
        margin-top: 10px;
    }
</style>