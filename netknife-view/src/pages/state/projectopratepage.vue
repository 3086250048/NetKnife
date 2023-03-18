<template>
    <div>
        <el-page-header @back="goBack" content="操作"></el-page-header><br>
        <el-input v-model="command" clearable placeholder="请输入内容" @change="commit_command">
            <template slot="prepend">CLI</template>
        </el-input><br>
        <el-input
        type="textarea"
        :rows="25"
        v-model="textarea"
        resize="none"
        class="info_box"
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
        ...mapMutations('projectoprateAbout',{COMMIT_COMMAND:'COMMIT_COMMAND'}),
        goBack(){
            this.$router.push({
                name:'state',
            })
            this.SET_PROJECT_VIEW_ABLE(true)
        },
        commit_command(){
            this.COMMIT_COMMAND(this.command)
        }
    },
    computed:{
        able(){
            return this.$store.state.devicestateAbout.able
        },
        textarea(){
            return this.$store.state.projectoprateAbout.textarea
        }
    },
}
</script>

<style>
    .info_box{
        width: 800px;
        margin-top: 10px;
    }
</style>