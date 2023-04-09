<template>
    <div style="height: 520px;">
        <el-empty description="没有代管理的项目" style="height: 500px;">
                <el-button type="primary" @click="forward_to_create">新建项目</el-button>
        </el-empty>
    </div>
</template>

<script>
export default{
    name:'Empty',
    methods:{
        forward_to_create(){
            this.$route.params.infopage.activeIndex='second'
            this.$router.push({
               name:'crud'
           })
       }
    },
}

</script>