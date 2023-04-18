<template>
    <el-empty description="开始创建第一个Netknife文件" style="height: 500px;">
                <el-button type="primary" @click="forward_filemanage">创建文件</el-button>
        </el-empty>
</template>

<script>
export default{
    name:'FileEmpty',
    methods:{
        forward_filemanage(){
            this.$bus.$emit('switch_activeIndex','four')
            this.$router.push({
                name:'filemanage'
            })
        }
    },
}

</script>