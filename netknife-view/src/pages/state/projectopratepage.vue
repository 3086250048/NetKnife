<template>
    <div>
        <div style="margin-bottom: 20px;">
            <el-button @click="goBack">返回</el-button>
            <div style="margin-left: 80px;margin-top: -30px;">
                <span>影响连接百分比</span><el-progress style="width: 300px;margin-left: 130px;margin-top: -20px;" :percentage="effect_connect_percent"></el-progress>
            </div>
            <div style="margin-left: 500px;margin-top: -20px;">
                <span>设备执行进度</span><el-progress style="width: 300px;margin-left: 110px;margin-top: -20px;" :percentage="96"></el-progress>
            </div>
        </div>
        <el-input  v-model="command" clearable placeholder="请输入内容" @change="commit_command" @input="set_effect">
            <template slot="prepend">CLI</template>
        </el-input><br>
        <el-input
        type="textarea"
        :rows="25"
        v-model="textarea"
        resize="none"
        class="info_box"
        style="font-size: larger;"
        >
        </el-input>
    </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default {
    name:'ProjectOprate',
    data(){
        return {
            command:'',
      
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
            this.SET_PROJECT_VIEW_ABLE(true)
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
        }
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