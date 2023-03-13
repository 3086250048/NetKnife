<template>
    <div>
        <el-alert
        v-show="pop_able"
        :title="pop_title"
        :type="pop_type">
        </el-alert>
    </div>
</template>
<script>
export default{
    name:'DeviceCrudPopInfo',
    computed:{
        pop_able(){
            return this.$store.state.deviceaddAbout.pop_info.able
        },
        pop_title(){
            return this.$store.state.deviceaddAbout.pop_info.title
       },
       pop_type(){
            return this.$store.state.deviceaddAbout.pop_info.type
       }
    },
    mounted(){
    //   test
    }
}
</script>
