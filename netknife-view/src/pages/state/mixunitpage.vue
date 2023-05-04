<template>
    <div style="margin: 1vh;">
        <el-row type="flex"  v-if="mixunit_view_able">
            <el-col :span="2">
                    <el-button style="width: 100%;height: 6.6vh;font-size: 2vh;border-radius: 1vh;" @click="goback">返回</el-button>
            </el-col>
            <el-col :span="13" :push="3">
                <el-autocomplete
                prefix-icon="el-icon-search"
                style="width: 100%;"
                class="search"
                v-model="input"
                :popper-append-to-body="false"
                :fetch-suggestions="querySearchAsync"
                placeholder="输入任意单位名称进行搜索"
                @select="handleSelect"
                ></el-autocomplete>
            </el-col>
        </el-row>
        <el-row v-if="mixunit_view_able">
            <el-col :span="24">     
                <ul style="margin-top: 1vh;">
                    <li v-for="(mixunit,i) in mixunit_list" :key="i"> 
                        <el-card class="head_card">
                            <el-row type="flex"  justify="end">
                                <el-col :span="6">
                                    <el-button-group style="width: 100%;" >
                                        <el-button style="height: 6vh;width: 50%;font-size: 2vh;;font-weight: 600">
                                            文件状态
                                        </el-button>
                                        <el-button style="height: 6vh;width: 50%;font-size: 2vh;;font-weight: 600">
                                            挂载文件
                                        </el-button>
                                    </el-button-group>
                                </el-col>
                                <el-col :span="3">
                                    <el-button type="text"   style="height: 6vh;width: 100%;font-size: 2vh;;font-weight: 600"  @click="show_oprate_page(),set_choose_mixunit(mixunit)">CLI</el-button>
                                </el-col>
                            </el-row>
                        </el-card>   
                        <el-card class="body_card" style="height: 25vh;font-size: 2.3vh;">
                            <span>区域名称:{{ mixunit[3] }}</span><br>
                            <span>设备类型:{{ mixunit[2]}}</span><br>
                            <span>协议类型:{{ mixunit[4] }}</span><br> 
                            <span>端口号:{{ mixunit[5] }}</span><br>
                            <span>用户名:{{ mixunit[6] }}</span><br>
                            <span>密码:{{ mixunit[7] }}</span><br>
                            <span v-if="if_secret_able(mixunit[8])" >特权密码:{{ mixunit[8] }}</span><br v-if="if_secret_able(mixunit[8])">
                            <span>IP表达式:{{ mixunit[9] }}</span>
                        </el-card>   
                    </li>
                </ul>
            </el-col>
        </el-row>
        <router-view></router-view>
    </div>
</template>

<script>
import { mapMutations } from 'vuex'
export default{
    name:'MixUnitPage',
    data(){
        return {
            secret_able:false,
            input:''
        }
    },
    methods: {
        ...mapMutations('devicestateAbout',{SET_PROJECT_VIEW_ABLE:'SET_PROJECT_VIEW_ABLE'}),
        ...mapMutations('mixunitpageAbout',{GET_MIXUNIT_DATA:'GET_MIXUNIT_DATA',
                                        SET_MIXUNIT_VIEW_ABLE:'SET_MIXUNIT_VIEW_ABLE',
                                        GET_SEARCH_DATA:'GET_SEARCH_DATA',
                                        CHOOSE_CHANGE:'CHOOSE_CHANGE',
                                        ROLLBACK_MIXUNIT_LIST:'ROLLBACK_MIXUNIT_LIST',
                                        SET_MIXUNIT_LIST:'SET_MIXUNIT_LIST'}),
        ...mapMutations('projectoprateAbout',{SET_CHOOSE_MIXUNIT:'SET_CHOOSE_MIXUNIT',
                                            SET_OPRATE_MODE:'SET_OPRATE_MODE'}),
        goback(){
            console.log("触发了")
            this.SET_OPRATE_MODE('project')
            this.$router.push({
                name:'state',
            })
            this.SET_PROJECT_VIEW_ABLE(true)
        },
        if_secret_able(secret){
            if(secret.length){
                 return true
             }else{
                 return false
             }
        },
        show_oprate_page(){
            this.SET_MIXUNIT_VIEW_ABLE(false)
            this.SET_PROJECT_VIEW_ABLE(false)
            this.$router.push({
                name:'projectoprate',
            })
        },
        set_choose_mixunit(mixunit){
           this.SET_CHOOSE_MIXUNIT(mixunit)
        },
        querySearchAsync(queryString, cb) {
            let results=this.mixunit_search_list
            results = queryString ? results.filter(this.createStateFilter(queryString)) : results;
            cb(results);
        },
        createStateFilter(queryString) {
        return (item) => {
          return item.value.toLowerCase().match(queryString.toLowerCase());
        };
        },
        handleSelect(item) {
            this.CHOOSE_CHANGE({'project':this.$route.params.project,
                                'search':item.value})
        },
    },
    computed:{
        mixunit_list(){
            return this.$store.state.mixunitpageAbout.mixunit_list
        },
        mixunit_view_able(){
            return this.$store.state.mixunitpageAbout.mixunit_view_able
        },
        mixunit_search_list(){
            return this.$store.state.mixunitpageAbout.mixunit_search_list
        }
    },
    watch:{
        input(new_value,old_value){
            if(old_value!=='' && new_value===''){
                this.ROLLBACK_MIXUNIT_LIST()
            }
        }
    },
    beforeDestroy(){
        this.SET_MIXUNIT_LIST([])
        
    },
    mounted(){
        this.GET_MIXUNIT_DATA({'project':this.$route.params.project})
        this.GET_SEARCH_DATA(this.$route.params.project)
        this.SET_OPRATE_MODE('mixunit')
    }
}
</script>

<style lang="scss"  scoped>
li{
    list-style-type: none;
}
li:not(:first-child){
    margin-top: 8px;
} 
.head_button{
    float: right;
    margin-top: -14px;
    margin-left: 10px;
}
// 头部卡片
.head_card{
    height:6vh;
}
.head_card ::v-deep .el-card__body{
    padding: 0px;
}
// 

//  搜索框 
.search  ::v-deep .el-input__inner {
        height: 6.6vh;
        font-size: 2vh;
        padding-left: 4vh;
       
}
.search ::v-deep .el-input__icon {
        height: 100%;
        width: 3vh;
        font-size: 2vh;
        line-height: 100%;
        padding-top: 0.3vh;
        
      
}
::v-deep .el-autocomplete-suggestion li{
    padding: 0 1vh;
    margin: 0;
    line-height: 4vh;
    cursor: pointer;
    color: #606266;
    font-size: 2vh;
    list-style: none;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
   
}
::v-deep .el-autocomplete-suggestion__wrap {
    max-height: 20vh;
    padding: 1vh 0;
    box-sizing: border-box;
}
//
.success{
    float: left;
    margin-top: -5px;
    margin-left: -10px;
}
.error{
    float: left;
    margin-top: -5px;
    margin-left: 28px;
}

.warning{
    float: left;
    margin-top: -5px;
    margin-left: 28px;
}
</style>