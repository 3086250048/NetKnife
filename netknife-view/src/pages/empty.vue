<template>
    <el-main>
        <el-empty description="没有代管理的项目">
                <el-button type="primary" @click="forward_to_create">新建项目</el-button>
        </el-empty>
    </el-main>
</template>

<script>
export default{
    name:'Empty',
    methods:{
        forward_to_create(){
            this.$route.params.infopage.activeName='second'
            this.$router.push({
               name:'crud'
           })
       }
    },
}

</script>