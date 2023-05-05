<template>
    <div style="margin: 1vh;">
      <el-row type="flex">
        <el-col :span="24">
          <el-tabs class="size-icon" style="width: 100%;" v-model="activename" type="card" closable @tab-remove="remove" @tab-click="record_index" >
              <el-tab-pane
                style="width: 100%;"
                v-for="(item, index) in tabs"
                :key='item.name'
                :label="item.title"
                :name="item.name" 
              >
              <Filecreate :title="item.title" :name="item.name" :code="item.code"  :del_able="item.title==='空窗口'"></Filecreate>
              </el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
      <!-- 执行结果 -->
      <el-drawer
        title="执行结果"
        :visible.sync="pop_able"
        direction="btt"
        size="90%"
        >
        <el-row type="flex">
            <el-col  :span="24"  >
              <el-button-group style="width: 100%;">
              <el-button style=" width: 20%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-arrow-left" size="mini" @click="rollback_command" >上一条命令</el-button>
              <el-button  style=" width: 20%;height: 4.5vh;font-size: 2vh;" type="primary" size="mini" @click="next_command">下一条命令<i class="el-icon-arrow-right el-icon--right"></i></el-button>
              <el-button style=" width: 20%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-document" size="mini" @click="export_textarea"></el-button>
              <el-button style=" width: 20%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-search" size="mini" @click="search_command_handler" ></el-button>
              <el-button style="width: 20%;height: 4.5vh;font-size: 2vh;" type="primary" icon="el-icon-setting" size="mini" @click="setting_dialog_able=true"></el-button>
              </el-button-group>
            </el-col>
        </el-row>
        
        <el-row type="flex" >
          <el-col :span="16">
                <!--输出框  -->
              <el-input
              style="width: 100%;font-size: 2.5vh;"
              type="textarea"
              :rows="32"
              resize="none"
              v-model="excute_text"
              
              class="el_main--el_input"
              >
              </el-input>
          </el-col>
          <el-col :span="8">
                <!-- 输出选择列表框 -->
              <ul   class="el_main-ul" >
                  <el-checkbox-group v-model="check_list" >
                      <li  v-for="item,index in excute_response_data" :key="index" >
                          <el-checkbox  :checked="true" :label="item.fun_name+item.ip+item.port+item.type"  >
                            函数:{{item.fun_name}} IP:{{item.ip}} 设备类型:{{item.type}} 
                          </el-checkbox>
                      </li>
                  </el-checkbox-group>
                    </ul>
                  </el-col>
            </el-row>
            <el-row type="flex">
          <el-col :span=24>
              <div style="position: relative;top:-1vh; width: 100%;height: 1vh;background-color:#272822;" ></div>
          </el-col>
        </el-row>
      </el-drawer>
      <el-dialog  title="设置参数" :visible.sync="setting_dialog_able" width="100vh">
          <el-form :model="setting_parameter">
            <el-form-item label="TXT导出路径"  :label-width="'25vh'">
                <el-input class="input_size"  placeholder="TXT文件导出路径" v-model="setting_parameter.txt_export_path">
                    <template slot="prepend">PATH</template>
                </el-input>
            </el-form-item>
          </el-form>
          <el-row type="flex"  justify="center">
            <el-col :span="4">
                <el-button @click="setting_handler_cancel" class="bt"  >取 消</el-button>
            </el-col>
            <el-col :span="4">
                <el-button type="primary" @click="setting_handler_commit" class="bt">确 定</el-button>
            </el-col>
        </el-row>
    </el-dialog>
    </div>
</template>

<script>

import { mapMutations} from 'vuex'
import filecreate from '@/pages/filecreate.vue'
import { send_post } from '@/store/tools'
import { get_time } from '@/store/tools'


export default{
  components:{Filecreate:filecreate},
  name:"FileManage",
  data(){
    return {
        base_code:`name:\npriority:\n\nconfig:{\n\n  send:{\n  read_timeout:10.0\n   }\n\n}\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`,
        activename:'0',
        tabs:[
        ],
        tabindex:-1,
        storage_tabs:[],
        index_list:[],
        pop_able:false,
        check_list:[],
        //保留让使用者可以自由调整输出框内的文字大小
        // check_cls_obj:{
        //         zoom:document.documentElement.clientHeight/600,
        //     }
        //自由调整执行结果输出框
        setting_dialog_able:false,
        search_command_history_able:false,
        input:'',
        response_title:'',
        setting_parameter:{
          txt_export_path:'',
        }
        
    }
  },
  methods:{
    ...mapMutations('filemanageAbout',{
      SET_TITLE:'SET_TITLE',
      HANDLER_RESPONSE_DATA:'HANDLER_RESPONSE_DATA',
      SET_EXCUTE_TEXT:'SET_EXCUTE_TEXT',
      SET_RESPONSE_DATE_TIME:'SET_RESPONSE_DATE_TIME',
      SET_EXCUTE_RESPONSE_DATA:'SET_EXCUTE_RESPONSE_DATA',
    // 弹出框
      GET_ALL_COMMAND_TIME:'GET_ALL_COMMAND_TIME',
      EXPORT_TEXTAREA:'EXPORT_TEXTAREA'
    
    }),

    record_index(tab){
      this.activename=tab.name
      localStorage.setItem('last_key',this.activename)
    },
    remove(targetName){
        let tabs = this.tabs;
        console.log(this.tabs.length)
        if (tabs.length<=1){
          this.$router.push({
            name:'pageempty'
          })
        }
        let activeName = this.activename;
        if (activeName === targetName) {
          tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
              let nextTab = tabs[index + 1] || tabs[index - 1];
              if (nextTab) {
                activeName = nextTab.name;
              }
              if((this.tabs.length>1)){
                localStorage.setItem('last_key',nextTab['name'])
              }
            } 
          });
        }
        this.activename = activeName;
        this.tabs = tabs.filter(tab => tab.name !== targetName);
        delete localStorage[targetName]
        if((this.tabs.length===0 && typeof(localStorage['last_key'])!=='undefined') || localStorage['last_key'] === targetName ){
          delete localStorage['last_key']
        }
       
    },
    handler_response_data(response_data){
      this.$bus.$emit('change_excute_icon','el-icon-video-play')
      this.$bus.$emit('change_excute_style','primary')
      this.pop_able=true
      this.SET_RESPONSE_DATE_TIME(get_time())
      this.HANDLER_RESPONSE_DATA(response_data)
    },
    search_command_handler(){
            this.search_command_history_able=true
            this.input=''
            this.GET_ALL_COMMAND_TIME()
        },
    export_textarea(){
        this.EXPORT_TEXTAREA({
            'command':this.response_title,
            'vm':this,
            'txt_export_path':this.txt_export_path
        })
    },
    next_command(){
            if(this,this.command_index<=-1){
                this.$message({
                    showClose: true,
                    message: '没有更多命令了',
                    type: 'warning'
                });
                return
            }
            if(this.command_index<=0){
                this.$message({
                    showClose: true,
                    message: '已经是最后一条命令了',
                    type: 'warning'
                });
                return
            }
            this.check_list=[]
            this.NEXT_COMMAND(this)
            console.log(this.command_index)
        },
    rollback_command(){
        if(this.command_index>=this.history_command_count-1){
            this.$message({
                showClose: true,
                message: '已经是最早的一条命令了',
                type: 'warning'
            });
            return
        }
        this.check_list=[]
        this.ROLLBACK_COMMAND()
        console.log(this.command_index)
    },
    setting_handler_cancel(){
            this.setting_dialog_able=false
        },
    setting_handler_commit(){ 
          send_post('/change_netknife_parameter',{
              'where':{
                  'file_name':this.title,
              },
              'update':{
                  'txt_export_path': this.setting_parameter.txt_export_path,
              }
          },response=>{
              console.log(response.data)
              this.setting_dialog_able=false
          })
        }
  }, 
  watch:{
    check_list(new_value){
      this.SET_EXCUTE_TEXT(new_value)
    },
  },
  computed:{
    excute_response_data(){
      return this.$store.state.filemanageAbout.excute_response_data
    },
    excute_text(){
      return this.$store.state.filemanageAbout.excute_text
    }
  },
  mounted(){
     //将localStorage中的页面状态信息读入列表，用于被页面迭代创建
     Object.entries(localStorage).forEach(([key,value])=>{
        if(key!=='last_key' ){
          this.tabindex=Math.max(this.tabindex,parseInt(key))
          this.index_list.push(parseInt(key))
          this.storage_tabs.push(JSON.parse(value))
        }
      })
      //排序索引列表保证创建页面的顺序
      this.index_list.sort(function(a,b){
      return b-a
      })
      console.log(this.tabs)
      // 向编辑页面添加新窗口
      this.$bus.$on('add',()=>{
        let newTabName = ++this.tabindex+ '';
        let tab_obj={
          name: newTabName,
          title: `空窗口`,
          code:this.base_code,
        }
        this.tabs.push(tab_obj);
        this.activename = newTabName;
        localStorage.setItem(tab_obj['name'],JSON.stringify(tab_obj))
        localStorage['last_key']=newTabName
      }),
      //点击保存按钮或删除按钮时更改Tab的titile
      this.$bus.$on('change_title',(file_name)=>{
          this.tabs.forEach(tab=>{
            if(tab.name==this.activename){
              tab.title=file_name
              const ori_tab_obj=JSON.parse(localStorage[tab.name])
              ori_tab_obj['title']=file_name
              localStorage[tab.name]=JSON.stringify(ori_tab_obj)
            }
          })    
      })
      //点击删除按钮时,将编辑框中的代码重置为初始代码
      this.$bus.$on('change_code',(name,code)=>{
        console.log(name)
        console.log(code)
        this.tabs.forEach(tab=>{
          console.log(tab['name'])
            if(tab['name']===name){
              tab['code']=code
            }
        })
      })
     
      //判断是否是第一次打开页面
      let open_file_flag=true
      //迭代创建Tab
      this.$bus.$on('create_tabs',()=>{
            if(typeof(localStorage['last_key'])!=='undefined' && this.index_list.length===0){
              this.activename=localStorage['last_key']
              return
            }
          const tab= JSON.parse(localStorage[this.index_list.pop()+''])
          let newTabName =tab['name']
          let tab_obj={
            name: newTabName,
            title:tab['title'],
            code:tab['code']
          }
          //判断是否从文件状态的“打开文件”按钮跳转来,open_file_flag防止新建窗口时依然用打开文件时的文件名
          if (tab_obj.name===localStorage['last_key'] && this.$route.params.item && open_file_flag){
            open_file_flag=false
            tab_obj.title=this.$route.params.item['netknife'][0]
            send_post('/get_raw_code',{'file_name':tab_obj.title},response=>{
                      tab_obj.code=response.data
                      localStorage[tab_obj.name]=JSON.stringify(tab_obj)
                      this.tabs.push(tab_obj);
                      this.activename = newTabName;
                    })
          }else{
            this.tabs.push(tab_obj);
            this.activename = newTabName;
          }
          
      })
      //延迟1毫秒，防止子节点先于父节点加载
      setTimeout(()=>{
        this.$bus.$emit('create_tabs')
      },1)
      //当localstorage中没有数据时，删除last_key
      if(localStorage.length===0){
        if(this.$route.params.item){
            console.log(this.$route.params.item)
            
          let newTabName = ++this.tabindex+ '';
          let tab_obj={
            name: newTabName,
            title:this.$route.params.item['netknife'][0],
            code:'',
          }
          send_post('/get_raw_code',{'file_name':tab_obj.title},response=>{
            tab_obj.code=response.data
            localStorage[tab_obj.name]=JSON.stringify(tab_obj)
            this.tabs.push(tab_obj);
            this.activename = newTabName;
          })
          localStorage['last_key']=newTabName
        }else{
          this.$bus.$emit('add')
        }
         
      }
      this.$bus.$on('excute',(file_name)=>{
        this.$bus.$emit('change_excute_icon','el-icon-video-pause')
        this.$bus.$emit('change_excute_style','warning')
        send_post('/excute_netknife_file',{'file_name':file_name},response=>{
            if(response.data==='FILE_NOT_EXIST'){
              this.$message({
                showClose: true,
                message: '请保存后运行',
                type: 'error'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            if(response.data==='EXCUTE_NOT_EXIST'){
              this.$message({
                showClose: true,
                message: 'Excute中没有等待执行的语句',
                type: 'warning'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            if(response.data==='LOCAL_FUN_NOT_EXIST'){
              this.$message({
                showClose: true,
                message: 'Excute中存在本地Jinja2中不存在的函数',
                type: 'warning'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            if(response.data==='IMPORT_FUN_NOT_EXIST'){
              this.$message({
                showClose: true,
                message: 'Excute中导入的Jinja2函数不存在',
                type: 'warning'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            if(response.data==='EXCUTE_FAULT'){
              this.$message({
                showClose: true,
                message: '执行失败',
                type: 'error'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            if(response.data==='NOT_CHOOSE_EFFECT_RANGE'){
              this.$message({
                showClose: true,
                message: 'Excute中存在无指定范围的指令',
                type: 'warning'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            if(response.data==='MIXUNIT_NOT_EXIST'){
              this.$message({
                showClose: true,
                message: 'Excute中存在指定范围无效的指令',
                type: 'warning'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            console.log(response.data)
            if(response.data==='JINJA2_REPEAT_IMPORT'){
              this.$message({
                showClose: true,
                message: 'JINJA2函数中存在循环引用',
                type: 'warning'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            if(response.data==='TRANSLATION_REPEAT_IMPORT'){
              this.$message({
                showClose: true,
                message: 'TRANSLATION函数中存在循环引用',
                type: 'warning'
              });
              this.$bus.$emit('change_excute_icon','el-icon-video-play')
              this.$bus.$emit('change_excute_style','primary')
              return
            }
            this.handler_response_data(response.data)
        })
      })
      this.$bus.$on('show_excute_result',(file_name)=>{
        this.pop_able=true
        this.response_title=file_name
      })
      this.$bus.$on('clear_check_list',()=>{
        this.check_list=[]
      })
      this.$bus.$on('clear_excute_response_data',()=>{
        this.SET_EXCUTE_RESPONSE_DATA([])
      })


      send_post('/get_netknife_parameter',{
            'file_name':this.response_title,
        },response=>{
          this.setting_parameter=response.data
        })
      //保留让使用者可以自由调整输出框内的文字大小
      // const _this = this;
      //   window.onresize = ()=>{
      //       return (() => {
      //       _this.check_cls_obj.zoom=document.documentElement.clientHeight/600;
      //       })();
      //   };
  },
  beforeDestroy(){
      this.$bus.$off('add')
      this.$bus.$off('change_title')
      this.$bus.$off('change_code')
      this.$bus.$off('excute')
      this.$bus.$off('show_excute_result')
      this.$bus.$off('clear_check_list')
      this.$bus.$off('clear_excute_response_data')
  }
}
</script>

<style lang="scss" scoped>
// tabs标签页头
::v-deep .el-tabs__header {
    padding: 0.1vh 1vh;
    position: relative;
    margin: 0 0 0 0;
}
// 按钮
::v-deep .el-button{
  border-radius: 0;
}
//标签体
::v-deep .el-tabs__item {
    text-align: center;
   
    height: 5vh;
    box-sizing: border-box;
    line-height: 5vh;
    display: inline-block;
    list-style: none;
    font-size: 2vh;
    font-weight: 600;
    color: #303133;
    position: relative;
}
::v-deep .el-tabs__item.is-active {
    color: #409EFF;
}
::v-deep .el-tabs__item:hover {
    color: #409EFF;
}
::v-deep .el-tabs--card>.el-tabs__header .el-tabs__item.is-closable:hover {
    padding-left: 4vh;
    padding-right: 4vh;
    
}
::v-deep .el-tabs--card>.el-tabs__header .el-tabs__item .el-icon-close {
    position: relative;
    font-size: 2vh;
    width: 0;
    height: 14px;
    vertical-align: middle;
    line-height: 15px;
    overflow: hidden;
    top: -1px;
    left: -2px;
    transform-origin: 100% 50%;
}

::v-deep .el-tabs--card>.el-tabs__header .el-tabs__item.is-active.is-closable{

  height: 5vh;
  line-height: 5vh;
}

::v-deep .el-tabs--card>.el-tabs__header .el-tabs__item.is-closable:hover .el-icon-close{
  width: 2vh;
  height: 2vh;
  line-height: 2vh;
}

// 

// 执行结果弹出框
::v-deep .el-drawer__header{
  margin-bottom: 0;
  padding-bottom: 0;
}



//
 // 输出框
 .el_main--el_input{
        font-size: larger;
        box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);

    }

    ::v-deep .el-textarea__inner {
        display: block;
        resize: vertical;
        padding: 0px 0px;
        line-height: 1;
        box-sizing: border-box;
        width: 100%;
        font-size: inherit;
        font-weight: 900;
        color: #ffffff;
        background-color: #272822;
        background-image: none;
        border: 1px solid #272822;
        border-radius: 0;
        transition: border-color .2s cubic-bezier(.645,.045,.355,1);
    }

    //
     // 选择框
     ::v-deep .el-checkbox__input.is-checked+.el-checkbox__label {
    color: #ffffff;
        }
    ::v-deep .el-checkbox__input.is-checked .el-checkbox__inner, .el-checkbox__input.is-indeterminate .el-checkbox__inner {
    background-color: #272822;
    border-color: #272822;
    }
    .el_main-ul{
       border-bottom:0.3vh solid #272822;
        width:100%;
        height: 80vh;
        overflow-y:scroll;
        background-color: #272822;
        box-shadow: 0 1vh 4vh rgba(0, 0, 0, .12), 0 0 1vh rgba(0, 0, 0, .04);
    }
    // ::v-deep .el-checkbox.is-bordered {

    //     padding: 9px 20vh 9px 12vh;

    // }
    // //
    // .el_main-ul-li{
    //     list-style: none;
    //     margin-bottom: 3px;
    // }
    // .el_main-ul-li-el_checkbox{
    //     width: 400px;
    // }
</style>