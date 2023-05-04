<template>
  <div style="margin: 1vh;">
      <el-row type="flex">
        <el-col :offset="5" :span="24">
            <el-autocomplete
            prefix-icon="el-icon-search"
            class="search"
            style="width: 70%;"
            v-model="input"
            :popper-append-to-body="false"
            :fetch-suggestions="querySearchAsync"
            placeholder="输入文件名称进行搜索"
            @select="handleSelect"
            ></el-autocomplete>
        </el-col>
      </el-row>
      <el-row>
        <el-col>
          <div class="netknife_ul">
              <ul>
                  <li v-for="item,index in netknife_data" :key="index">
                    <el-card style="height: 10vh;">
                      <el-row type="flex" justify="end">
                        <el-col :span =4 :pull="8">
                          <el-tag style="min-width: 100%;text-align: center;height: 10vh;line-height: 10vh;font-size: 2vh;font-weight: 900;"  >{{ item['netknife'][0].length>35?item['netknife'][0].slice(0,35)+'...':item['netknife'][0] }}</el-tag>
                        </el-col>
                        <el-col :span="1" :pull="13" >
                          <el-tag style="min-width: 100%;text-align: center;height: 10vh;line-height: 10vh;font-size: 2vh;font-weight: 900;"  type="danger"  >{{ item['netknife'][1]}}</el-tag>
                        </el-col>
                        <el-col :span="8">
                          <el-button-group style="width: 100%;">
                            <el-button style="width: 25%;height: 10vh;font-size: 2vh;;font-weight: 400"  :disabled="!item['config'].length>0"  @click="show_config(item['config'])"  :class="item['config_class']">配置</el-button>
                            <el-button style="width: 25%; height: 10vh;font-size: 2vh;;font-weight: 400"  :disabled="!item['translation'].length>0"  @click="show_translation(item['translation'])"  :class="item['translation_class']">转换</el-button>
                            <el-button style="width: 25%;height: 10vh;font-size: 2vh;;font-weight: 400"  :disabled="!item['jinja2'].length>0"  @click="show_jinja2(item['jinja2'])"  :class="item['jinja2_class']">函数</el-button>
                            <el-button style="width: 25%;height: 10vh;font-size: 2vh;;font-weight: 400" :disabled="!item['excute'].length>0"  @click="show_excute(item['excute'])"  :class="item['excute_class']">执行</el-button>
                          </el-button-group>
                        </el-col>
                        <el-col :span="2">
                          <el-button style="width: 100%;height: 10vh;font-size: 2vh;;font-weight: 600;text-align: center;" type="text" @click="open_file(item)">打开文件</el-button>
                        </el-col>
                      </el-row>     
                    </el-card>
                  </li>
              </ul>
            </div>
        </el-col>
      </el-row>
      <el-dialog title="Translation" :visible.sync="translation_pop_able" width="120vh">
      <el-table style="font-size: 2vh;line-height: 2vh;" :data="file_data" height="60vh"  :cell-style="{padding:'2vh 2vh 2vh 0' }"  stripe>
        <el-table-column property="type" label="类型" min-width="10%"></el-table-column>
        <el-table-column property="before" label="转换前" min-width="40%" ></el-table-column>
        <el-table-column property="after" label="转换后" min-width="40%" ></el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="Jinja2" :visible.sync="jinja2_pop_able" width="120vh">
      <el-table style="font-size: 2vh;line-height: 2vh;" :data="file_data" height="60vh"  :cell-style="{padding:'2vh 2vh 2vh 0' }"  stripe>
        <el-table-column property="fun_name" label="函数名" min-width="20%"></el-table-column>
        <el-table-column property="fun_text" label="函数体" min-width="80%"></el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="Excute" :visible.sync="excute_pop_able" width="120vh">
      <el-table style="font-size: 2vh;line-height: 2vh;" :data="file_data" height="60vh"  :cell-style="{padding:'2vh 2vh 2vh 0' }"  stripe>
        <el-table-column property="cmd" label="执行命令" min-width="33%" ></el-table-column>
        <el-table-column property="parameter" label="参数" min-width="33%"></el-table-column>
        <el-table-column property="condition" label="执行条件" min-width="33%"></el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog title="Config" :visible.sync="config_pop_able" width="120vh">
      <el-table style="font-size: 2vh;line-height: 2vh;" :data="file_data" height="60vh"  :cell-style="{padding:'2vh 2vh 2vh 0' }"  stripe>
        <el-table-column property="parameter_class" label="参数类型" min-width="33%"></el-table-column>
        <el-table-column property="parameter_key" label="参数键" min-width="33%"></el-table-column>
        <el-table-column property="parameter_value" label="参数值" min-width="33%"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { mapMutations} from 'vuex'
export default{
    data(){
        return{
            activeNames: [],
            translation_pop_able:false,
            jinja2_pop_able:false,
            excute_pop_able:false,
            config_pop_able:false,
            file_data:[],
            input:''
        }
    },
    name:'FileState',
    methods:{
        ...mapMutations('filestateAbout',{
          GET_NETKNIFE_DATA:'GET_NETKNIFE_DATA',
          CHOOSE_CHANGE:'CHOOSE_CHANGE',
          ROLLBACK_NETKNIFE_DATA:'ROLLBACK_NETKNIFE_DATA'
        }),
        handleChange(val) {
        console.log(val);
        },
        show_translation(data){
            this.file_data=[]
            this.translation_pop_able=true
            data.forEach(element => {
                this.file_data.push({'type':element[0],'before':element[1],'after':element[2]})
            });
        },
        show_jinja2(data){
          this.file_data=[]
          this.jinja2_pop_able=true
          let fun_dict={}
          for(let i=0;i<data.length;i++){
            if(!fun_dict.hasOwnProperty(data[i][0])){
                fun_dict[data[i][0]]=data[i][1]
              }else{
                fun_dict[data[i][0]]+=`;${data[i][1]}`
              }
          }
          Object.entries(fun_dict).forEach((item,index)=>{
            this.file_data.push({'fun_name':item[0],'fun_text':item[1]})
          })
        },
        show_excute(data){
          this.file_data=[]
          this.excute_pop_able=true
          data.forEach(element=>{
            this.file_data.push({'cmd':element[0],'parameter':element[1],'condition':element[2]})
          })
        },
        open_file(item){
          this.$bus.$emit('switch_activeIndex','open_file',item)
        },
        show_config(data){
          this.file_data=[]
          this.config_pop_able=true
          data.forEach(element => {
              this.file_data.push({'parameter_class':element[0],'parameter_key':element[1],'parameter_value':element[2]})
          });
        },
        querySearchAsync(queryString, cb) {
        let search_data=[]
        for(let i=0;i<this.netknife_data.length;i++){
          search_data.push({'value':this.netknife_data[i]['netknife'][0]})
        }
        let results=search_data
        results = queryString ? results.filter(this.createStateFilter(queryString)) : results;
        cb(results);
        },
        createStateFilter(queryString) {
        return (item) => {
          return item.value.toLowerCase().match(queryString.toLowerCase());
        };
        },
        handleSelect(item) {
            this.CHOOSE_CHANGE(item.value)
        },
    },
    computed:{
        netknife_data(){
          return this.$store.state.filestateAbout.netknife_data
        },
       
    },
    watch:{
      input(new_value,old_value){
        if(old_value!=='' && new_value===''){
            this.ROLLBACK_NETKNIFE_DATA()
        }
      }
    },
    mounted(){
      this.GET_NETKNIFE_DATA()
    }
}

</script>

<style lang="scss" scoped>
// 卡片
::v-deep .el-card__body, .el-main {
    padding: 0;
}
//  
// pop
::v-deep .el-table .cell {
    box-sizing: border-box;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: normal;
    word-break: break-all;
    line-height: 3vh;
  
}
// pop头文字
::v-deep .el-dialog__header {
    padding: 2vh 2vh 1vh;
}
::v-deep .el-dialog__title {
    line-height: 2vh;
    font-size: 2vh;
    font-weight: 900;
    color: #303133;
}
//pop body
::v-deep .el-dialog__body {
    padding:2vh;
    color: #606266;
    font-size: 2vh;
    font-weight: 600;
    word-break: break-all;
}
// 


// 搜索框
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





// 
li{
  list-style-type: none;
}
li:not(:first-child){
    margin-top: 8px;
} 


.netknife_ul{
  margin-top: 20px;
}
</style>


