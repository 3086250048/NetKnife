<template>
  <div style="margin-left: 1vh;">
 
    <el-row >
      <el-col >
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
   

  <el-row type="flex" justify="start">
    <el-col :span="16">
    <el-button-group style="width: 100%;" >
      <el-button style="height: 5vh;width: 23%;font-size: 2vh;font-weight: 600;text-align: center;" :type="save_bt_style" class="create" @click="save_file" icon="el-icon-folder-add" size="small">
      保存
    </el-button>
      <el-button style="height: 5vh;width: 23%;font-size: 2vh;font-weight: 600;text-align: center" type="primary" class="delete" @click="delete_file" icon="el-icon-folder-delete" :disabled="del_able" size="small">
      删除
    </el-button>
      <el-button style="height: 5vh;width: 27%;font-size: 2vh;font-weight: 600;text-align: center" type="primary" class="open" @click="open_file" icon="el-icon-folder-opened" size="small">
      打开文件
    </el-button>
    <el-button style="height: 5vh;width: 27%;font-size: 2vh;font-weight: 600;text-align: center" type="primary" class="empty_add" @click="add_empty" icon="el-icon-view" size="small">
      新窗口+
    </el-button>
    </el-button-group>
    </el-col>

    <el-col :span="8">
      <el-button-group style="width: 100%;">
        <el-button style="height: 5vh;width: 50%;font-size: 2vh;font-weight: 600;text-align: center" :type="excute_bt_style" class="excute" @click="excute_file" :icon="excute_icon" size="small">
          运行
        </el-button>
        <el-button style="height: 5vh;width: 50%;font-size: 2vh;font-weight: 600;text-align: center"  type="info" class="excute" @click="show_excute_result" icon="el-icon-warning-outline" size="small">
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
      this.delete_netknife_file({code:code,name:this.name})
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
      this.$bus.$emit('show_excute_result')
    },
   
  },
  computed: {
    codemirror() {
      return this.$refs.myCm.codemirror;
    },
    file_name(){
      return this.$store.state.filecreateAbout.file_name
    },
  },
  mounted(){
    
    // 由于没有使用路由切换，组件不会销毁，这里的SET_VM需要多次调用，防止vuex中直接调用this的数据停留在最后一次加载的页面上
    this.SET_VM(this)

    setTimeout(()=>{
      this.$bus.$emit('create_tabs')
     
    },1)
    
    this.$bus.$on('change_excute_icon',(icon)=>{
      this.excute_icon=icon
    })
    this.$bus.$on('change_excute_style',(style)=>{
      this.excute_bt_style=style
    })
    this.$bus.$on('change_save_style',(style)=>{
      this.save_bt_style=style
    })
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
    this.$bus.$off('change_excute_icon')
    this.$bus.$off('change_excute_style')
    this.$bus.$off('change_save_style')
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
