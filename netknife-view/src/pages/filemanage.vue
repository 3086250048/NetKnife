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
      <!-- 如何通过last_key防止pop页面跨文件弹出 -->
      <el-drawer
        :title=pop_title
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
                            函数:{{item.fun_name}} IP:{{item.ip}} PORT:{{item.port}} 设备类型:{{item.type}} 
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
      <!-- 设置按钮 -->
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

     <!-- 搜索历史命令 -->
     <el-dialog  title="搜索历史命令" :visible.sync="search_command_history_able" width="120vh" >
        <el-row>
            <el-col :span="24">
                <el-autocomplete
                    class="search"
                    style="width: 100%;height: 4vh;z-index: 1;"
                    prefix-icon="el-icon-search"
                    v-model="input"
                    :popper-append-to-body="false"
                    :fetch-suggestions="querySearchAsync"
                    placeholder="输入执行时间进行检索"
                    @select="handleSelect"
                    ></el-autocomplete>
            </el-col>
        </el-row>
        <div style="height:66vh;overflow: scroll;">
            <ul class="his_ul">
                <li  v-for="(item,i) in all_excute_date_time_list " :key="i" > 
                    <el-card class="cmd_his_about" style="height: 10vh;width: 115vh;font-size: 2vh;" >
                        <el-button-group style="float: right;margin-top: -20px;margin-right:-20px;" >
                            <el-button style="width: 12vh;height: 4.5vh;font-size: 2vh;line-height: 1vh;" type="primary"  @click="show_history_command(item,i)" >查看</el-button>
                            <el-button style="width: 12vh;height: 4.5vh;font-size: 2vh;line-height: 1vh;" type="primary"  @click="delete_history_command(item,i)">删除</el-button>
                        </el-button-group>
                        执行时间:{{ item}} <br>
                    </el-card>
                </li>
            </ul>
        </div>
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
        },
        excute_time:'',
        pop_title:'执行结果',
        excute_file_list:[],  
        
        
    }
  },
  methods:{
    ...mapMutations('filemanageAbout',{
      SET_TITLE:'SET_TITLE',
      HANDLER_RESPONSE_DATA:'HANDLER_RESPONSE_DATA',
      SET_EXCUTE_TEXT:'SET_EXCUTE_TEXT',
      SET_RESPONSE_DATE_TIME:'SET_RESPONSE_DATE_TIME',
      SET_EXCUTE_RESPONSE_DATA:'SET_EXCUTE_RESPONSE_DATA',
    //待实现函数
      //导出文件按钮
      EXPORT_TEXTAREA:'EXPORT_TEXTAREA',

      // 历史命令按钮相关
      GET_ALL_EXCUTE_DATE_TIME:'GET_ALL_EXCUTE_DATE_TIME',
      CHOOSE_CHANGE:'CHOOSE_CHANGE',
      SHOW_HISTORY_COMMAND:'SHOW_HISTORY_COMMAND',
      DELETE_HISTORY_COMMAND:'DELETE_HISTORY_COMMAND',
      ROLLBACK_EXCUTE_RESULT_LIST:'ROLLBACK_EXCUTE_RESULT_LIST',
      SET_IF_HISTORY_TIME:'SET_IF_HISTORY_TIME',
      CLEAR_EXCUTE_TEXT:'CLEAR_EXCUTE_TEXT',
      // 命令前进和后退按钮相关
      NEXT_COMMAND:'NEXT_COMMAND',
      ROLLBACK_COMMAND:'ROLLBACK_COMMAND',
      SET_COMMAND_INDEX:'SET_COMMAND_INDEX'
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

    // set_excute_button_normal_state(file_name){
    //   this.$bus.$emit('change_excute_icon','el-icon-video-play',file_name)
    //   this.$bus.$emit('change_excute_style','primary',file_name)
    //   this.$bus.$emit('change_excute_able',false,file_name)
    // },

    handler_response_data(response_data,file_name){
      this.check_list=[]
      //从执行文件队列中删除此file_name文件
      delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
      //判断队列中的文件是否都已经执行完毕
      console.log(this.excute_file_list)
      // JS中删除列表中的元素还会留下一个‘empty’需要使用filter过滤(filter默认过滤empty等值)
      if(this.excute_file_list.filter(e=>e).length===0){
          this.$bus.$emit('all_excute_done')
          this.excute_file_list=[]
      }

      //改变已经执行完成文件的页面UI
      this.$bus.$emit('change_excute_state',false,file_name)
      
      //弹窗
      // 防止在弹窗和所在文件不一致的问题(其他数据照常处理)
      // if(JSON.parse(localStorage[localStorage['last_key']])['title']===file_name){
        this.pop_able=true
        //设置当前操作的文件名称(主动点击会设置一次,运行完毕会被动设置一次)
        this.response_title=file_name
      // }

      // 设置时间戳的模式，一个是查看历史命令时用数据库中的时间，另外一种是实时模式使用执行文件时的时间
      this.SET_IF_HISTORY_TIME(false)
      // 设置操作的文件名(vuex中使用)
      this.SET_TITLE(file_name)
      // 对response_data数据进行处理
      
      this.HANDLER_RESPONSE_DATA({'response_data':response_data,'file_name':file_name})
     
    
    },

    //搜索按钮相关函数
    search_command_handler(){
            this.search_command_history_able=true
            this.input=''
            console.log(this.response_title)
            this.GET_ALL_EXCUTE_DATE_TIME(this.response_title)
        },
        querySearchAsync(queryString, cb) {
            let results=this.all_excute_date_time_search_list
            results = queryString ? results.filter(this.createStateFilter(queryString)) : results;
            cb(results);
        },
        createStateFilter(queryString) {
        return (item) => {
          return item.value.toLowerCase().match(queryString.toLowerCase());
        };
        },
        handleSelect(item) {
            this.CHOOSE_CHANGE(item.value,this.response_title)
        },
        show_history_command(date_time,i){
            this.SET_IF_HISTORY_TIME(true)
            this.check_list=[] 
            this.search_command_history_able=false
            this.SHOW_HISTORY_COMMAND({
                'file_name':this.response_title,
                'date_time':date_time,
                'index':i
            })

        },
        delete_history_command(date_time,i){
            this.check_list=[]
            this.DELETE_HISTORY_COMMAND({
                'file_name':this.response_title,
                'date_time':date_time,
                'index':i
            })
        },
  //导出按钮
    export_textarea(){
        this.EXPORT_TEXTAREA({
            'file_name':this.response_title,
            'vm':this,
            'txt_export_path':this.setting_parameter.txt_export_path
        })
    },
  //执行结果回退和前进按钮
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
  // 设置按钮
    setting_handler_cancel(){
            this.setting_dialog_able=false
        },
    setting_handler_commit(){ 
          send_post('/change_netknife_parameter',{
              'where':{
                  'file_name':this.response_title,
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
        console.log(new_value)
        this.SET_EXCUTE_TEXT(new_value)
    },
    input(new_value,old_value){
            if(old_value!=='' && new_value===''){
                this.ROLLBACK_EXCUTE_RESULT_LIST()
            }
    },
    setting_dialog_able(new_value){
            // if(new_value){
                send_post('/get_netknife_parameter',{
                  "file_name":this.response_title
                },response=>{
                    // 正常
                    console.log(response.data)
                    this.setting_parameter=response.data
                })
    },
    pop_able(new_value){
      if(new_value===false){
        this.CLEAR_EXCUTE_TEXT()
        // this.check_list=[]
        this.SET_EXCUTE_RESPONSE_DATA([])
      }
    },
    response_title(new_value){
      this.pop_title=`${new_value}的执行结果`
    }
  },
  computed:{
    excute_response_data(){
      return this.$store.state.filemanageAbout.excute_response_data
    },
    excute_text(){
      return this.$store.state.filemanageAbout.excute_text
    },
    // 搜索按钮
    code_index(){
        return this.$store.state.filemanageAbout.code_index
    },
    history_code(){
        return this.$store.state.filemanageAbout.history_code
    },
    history_code_count(){
        return this.$store.state.filemanageAbout.history_code_count
    },
    all_excute_date_time_search_list(){
        return this.$store.state.filemanageAbout.all_excute_date_time_search_list
    },
    all_excute_date_time_list(){
        return this.$store.state.filemanageAbout.all_excute_date_time_list
    },
    // 
  },
  beforeDestroy(){
    this.SET_COMMAND_INDEX(-1) 
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
        console.log(file_name)
        this.$bus.$emit('change_excute_state',true,file_name)
        // 控制执行文件
        if(this.excute_file_list.indexOf(file_name)!==-1){
          this.$bus.$emit('change_excute_state',false,file_name)
          this.$message({
                showClose: true,
                message: '此文件已在队列中运行',
                type: 'warning'
              });
          return 
        }else{
          this.excute_file_list.push(file_name)
          // 设置执行时候的时间
          this.SET_RESPONSE_DATE_TIME({file_name:file_name,date_time:get_time()})
          send_post('/excute_netknife_file',{'file_name':file_name},response=>{
            this.file_name=file_name
              if(response.data==='FILE_NOT_EXIST'){
                this.$message({
                  showClose: true,
                  message: '请保存后运行',
                  type: 'error'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='EXCUTE_NOT_EXIST'){
                this.$message({
                  showClose: true,
                  message: 'Excute中没有等待执行的语句',
                  type: 'warning'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='LOCAL_FUN_NOT_EXIST'){
                this.$message({
                  showClose: true,
                  message: 'Excute中存在本地Jinja2中不存在的函数',
                  type: 'warning'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='IMPORT_FUN_NOT_EXIST'){
                this.$message({
                  showClose: true,
                  message: 'Excute中导入的Jinja2函数不存在',
                  type: 'warning'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='EXCUTE_FAULT'){
                this.$message({
                  showClose: true,
                  message: '执行失败',
                  type: 'error'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='NOT_CHOOSE_EFFECT_RANGE'){
                this.$message({
                  showClose: true,
                  message: 'Excute中存在无指定范围的指令',
                  type: 'warning'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='MIXUNIT_NOT_EXIST'){
                this.$message({
                  showClose: true,
                  message: 'Excute中存在指定范围无效的指令',
                  type: 'warning'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='JINJA2_REPEAT_IMPORT'){
                this.$message({
                  showClose: true,
                  message: 'JINJA2函数中存在循环引用',
                  type: 'warning'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(response.data==='TRANSLATION_REPEAT_IMPORT'){
                this.$message({
                  showClose: true,
                  message: 'TRANSLATION函数中存在循环引用',
                  type: 'warning'
                });
                delete this.excute_file_list[this.excute_file_list.indexOf(file_name)]
                this.$bus.$emit('change_excute_state',false,file_name)
                return
              }
              if(this.pop_able===true){
                console.log(11111111111111111111111111111111111)
                this.pop_able=false
                setTimeout(() => {
                  this.handler_response_data(response.data,file_name)
                }, 1);
              }else{
              this.handler_response_data(response.data,file_name)
              }
            
              
          })
        }
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

//历史命令搜索框
.search ::v-deep .el-input__inner {
        height: 5vh;
        font-size: 2vh;
        padding-left: 4vh;
        border-radius: 0.8vh;
       
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


// dialog框相关
::v-deep .el-form-item__label {
    text-align: center;
    vertical-align: middle;
    float: left;
    font-size: 2vh;
    color: #606266;
    line-height: 4.3vh;
    padding: 0 12px 0 0;
    box-sizing: border-box;
}
 ::v-deep .el-dialog__title {
    line-height: 2vh;
    font-size:2vh;
    color: #303133;
    margin: 1vh;
}

  ::v-deep .el-dialog__header {
    padding: 2vh 2vh 1vh;
}

  ::v-deep .el-dialog__body {
    padding: 3vh 2.2vh;
    color: #606266;
    font-size: 1vh;
    word-break: break-all;
}
// 



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