<template>
  <div style="margin-left: 1vh;">
 
    <el-row  type="flex">
      <el-col  :span="24">
        <codemirror
      id="codemirror"
      ref="myCm" 
      :value="code"
      :options="cmOptions"
      class="editor" 
      @input="change_text"
    >
    </codemirror>

      </el-col>
    </el-row>
   

  <el-row type="flex" justify="start" >
    <el-col :span="24">
    <el-button-group style="width: 100%;" >
      <el-button style="height: 5vh;width: 13%;font-size: 2vh;font-weight: 600;text-align: center;" :type="save_bt_style" class="create" @click="save_file" icon="el-icon-folder-add" size="small">
      保存
    </el-button>
      <el-button :disabled="del_final_able" style="height: 5vh;width: 13%;font-size: 2vh;font-weight: 600;text-align: center" type="primary" class="delete" @click="delete_file" icon="el-icon-folder-delete"  size="small">
      删除
    </el-button>
      <el-button :disabled="open_file_able" style="height: 5vh;width: 15%;font-size: 2vh;font-weight: 600;text-align: center" type="primary" class="open" @click="open_file" icon="el-icon-folder-opened" size="small">
      打开文件
    </el-button>
    <el-button  style="height: 5vh;width: 15%;font-size: 2vh;font-weight: 600;text-align: center" type="primary" class="empty_add" @click="add_empty" icon="el-icon-view" size="small">
      新窗口+
    </el-button>
    <el-button :disabled="excute_able" style="height: 5vh;width: 22%;font-size: 2vh;font-weight: 600;text-align: center" :type="excute_bt_style" class="excute" @click="excute_file" :icon="excute_icon" size="small">
      运行
    </el-button>
    <el-button  style="height: 5vh;width: 22%;font-size: 2vh;font-weight: 600;text-align: center"  type="primary" class="excute" @click="show_excute_result" icon="el-icon-warning-outline" size="small">
      执行结果
    </el-button>
    </el-button-group>
    </el-col>
  </el-row>
    
  </div>
</template>

<script>
import { send_post } from "@/store/tools";
import codemirror from "codemirror";
import "codemirror/mode/meta";
import { mapMutations,mapActions } from 'vuex'
// 折叠
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/foldcode'
import 'codemirror/addon/fold/foldgutter'
import 'codemirror/addon/fold/brace-fold'
import 'codemirror/addon/fold/comment-fold'

export default{
  name: "FileCreate",
  props:['title','name','code','del_able'],
  data() {
    return {
      cmOptions: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: 'text/javascript',
        lineWrapping: true,
        theme: "monokai",
        foldGutter: true,
        gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter', 'CodeMirror-lint-markers'],
      },
      delete_able:false,
      update_able:false,
      excute_flag:false,
      excute_icon:'el-icon-video-play',
      excute_bt_style:'primary',
      save_bt_style:'primary',
      storage_code:'',
      base_code:`name:\npriority:\n\nconfig:{\n\n  send:{\n  read_timeout:10.0\n   }\n\n}\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`,
      excute_able:false,
      real_time_title:'',

      // 执行时禁用
      open_file_able:false,
      real_del_able:false,
     
    };
  },
  methods: {
    ...mapMutations('filecreateAbout',{
      SET_VM:'SET_VM'
    }),
    ...mapActions('filecreateAbout',{
      save_netknife_file:'save_netknife_file',
      delete_netknife_file:'delete_netknife_file',
    }),
    save_file(){
      this.SET_VM(this)
      this.excute_flag=false
      const code=this.codemirror.getValue()
      this.save_netknife_file(code)
    },
    delete_file(){
      this.SET_VM(this)
      const code = this.codemirror.getValue();
      this.delete_netknife_file({code:code,name:this.name,title:this.title})
    },
    add_empty(){
      this.SET_VM(this)
      this.$bus.$emit('add')
    },
    open_file(){
        
        this.$bus.$emit('switch_activeIndex','three')
    },
    change_text(){
      localStorage[this.name]=JSON.stringify({name:this.name,title:this.title,code:this.codemirror.getValue()})

      if(this.storage_code==='NOT_EXIST'){
        if (this.codemirror.getValue()!==this.base_code){
          this.save_bt_style='warning'
        }else{
          this.save_bt_style='primary'
        }
        return
      }
      if(this.codemirror.getValue()!==this.storage_code){
        this.save_bt_style='warning'
      }else{
        this.save_bt_style='primary'
      }
    },
    excute_file(){
   
      this.SET_VM(this)
      this.excute_flag=true
      const code=this.codemirror.getValue()
      this.$bus.$emit('clear_check_list')
      this.$bus.$emit('clear_excute_response_data')
      this.save_netknife_file(code)
      
    },
    show_excute_result(){
      this.$bus.$emit('show_excute_result',this.title)
    },
   
  },
  computed: {
    codemirror() {
      return this.$refs.myCm.codemirror;
    },
    file_name(){
      return this.$store.state.filecreateAbout.file_name
    },
    del_final_able(){
      if(this.del_able){
        return true
      }{
        if(this.real_del_able){
          return true
        }else{
          return false
        }

      }
    }
  },
  mounted(){
    
    // 由于没有使用路由切换，组件不会销毁，这里的SET_VM需要多次调用，防止vuex中直接调用this的数据停留在最后一次加载的页面上
    this.SET_VM(this)

    setTimeout(()=>{
      this.$bus.$emit('create_tabs')
     
    },1)

    this.$bus.$on('all_excute_done',()=>{
        this.open_file_able=false
        this.real_del_able=false
    })

    this.$bus.$on('change_excute_state',(bool,file_name)=>{
         
          if(bool){
            // 全局禁用
            this.open_file_able=true
            this.real_del_able=true
        
            if(this.real_time_title+''===file_name+''){
            //用户停留页面禁用
              this.excute_icon='el-icon-video-pause'
              this.excute_bt_style='warning'
              this.excute_able=true
             
            }
          }else{
       
             if(this.real_time_title+''===file_name+''){
              //用户所在页面启用
              this.excute_icon='el-icon-video-play'
              this.excute_bt_style='primary'
              this.excute_able=false
            }

          }
        }
    )

    // this.$bus.$on('change_excute_icon',(icon,file_name)=>{
    //   console.log(file_name)
    //   console.log(this.title)
    //   if(this.real_time_title+''===file_name+''){
    //     this.excute_icon=icon
    //   }
   
    // })
    // this.$bus.$on('change_excute_style',(style,file_name)=>{
    //   if(this.real_time_title+''===file_name+''){
    //     this.excute_bt_style=style
    //   }

    // })
    // //防止连续点击执行按钮,导致数据库中同一时间对应多个表项导致删除时一次性删除多条表项
    // this.$bus.$on('change_excute_able',(bool,file_name)=>{
    //   if(this.real_time_title+''===file_name+''){
    //     this.excute_able=bool
    //   }
    // })
    //这个应该是在本文件改的，暂时保留
    this.$bus.$on('change_save_style',(style)=>{
      this.save_bt_style=style
    })
    //
   console.log(`title是:${this.title}`)
    send_post('/get_netknife_code',{'file_name':this.title},response=>{
      this.storage_code=response.data
      if(this.storage_code==='NOT_EXIST'){
        if (this.codemirror.getValue()!==this.base_code){
          this.save_bt_style='warning'
        }else{
          this.save_bt_style='primary'
        }
        return
      }
      if (this.codemirror.getValue()!==this.storage_code){
        this.save_bt_style='warning'
      }else{
        this.save_bt_style='primary'
      }
    })
  },
  created(){
    console.log( `create时的title${this.title}`)
  },
  beforeDestroy(){
    console.log('Destory')
    // this.$bus.$off('change_excute_icon')
    // this.$bus.$off('change_excute_style')
    // this.$bus.$off('change_excute_able')
    // 这个应该是在文件改的
    this.$bus.$off('change_save_style')
    this.$bus.$off('change_excute_state')
    this.$bus.$off('all_excute_done')
  }
};
</script>

<style>
.editor .CodeMirror {
  height: 80vh;
  
}
</style>

<style lang="scss" scoped>


// 按钮
::v-deep .el-button{
  border-radius: 0;
}

//

.create {

  
}
.delete{

}
.update{

}
.open{

}
.empty_add{
 
}
.excute{

  
}

</style>
