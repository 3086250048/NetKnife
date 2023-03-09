<template>
        <ul v-infinite-scroll="load">
            <li v-for="i in count"> 
                <el-descriptions title="设备连接块">
                    <el-descriptions-item label="IP">{{  }}</el-descriptions-item>
                    <el-descriptions-item label="协议和端口">{{  }}</el-descriptions-item>
                    <el-descriptions-item label="设备层级">{{  }}</el-descriptions-item>
                    <el-descriptions-item label="设备类型">{{  }}</el-descriptions-item>
                    <el-descriptions-item label="项目名称">{{  }}</el-descriptions-item>
                </el-descriptions>
            </li>
        </ul>
</template>

<script>
export default{
    name:'DeviceState',
    data(){
        return {
            count:0
        }
    },
    methods:{
        load(){
            this.count+=2
        }
    }
}

</script>