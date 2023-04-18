<template>
    <el-empty description="新键窗口或打开文件开始编辑" style="height: 500px;">
                <el-button type="primary" @click="create_page">新建窗口</el-button>
                <el-button type="primary" @click="open_page">打开文件</el-button>
        </el-empty>
</template>

<script>
export default{
    name:'PageEmpty',
    methods:{
        create_page(){
            this.$router.push({
                name:'filemanage'
            })
        },
        open_page(){
        }
    },
}

</script>