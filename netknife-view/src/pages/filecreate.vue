<template>
  <div>
    <el-button type="primary" class="create" @click="save_file" icon="el-icon-folder-add" size="small">
      保存
    </el-button>
    <el-button type="primary" class="delete" @click="delete_file" icon="el-icon-folder-delete" size="small">
      删除
    </el-button>
    <el-button type="primary" class="open" @click="open_file" icon="el-icon-folder-opened" size="small">
      打开文件
    </el-button>
    <el-button type="primary" class="empty_add" @click="add_empty" icon="el-icon-view" size="small">
      新窗口+
    </el-button>
    <el-button type="danger" class="excute" @click="excute_file" icon="el-icon-video-play" size="small">
      运行
    </el-button>
    <el-button type="danger" class="excute" @click="show_excute_result" icon="el-icon-warning-outline" size="small">
      执行结果
    </el-button>
    <codemirror
      id="codemirror"
      style="margin-left:-15px;
      margin-top: -15px;"  
      ref="myCm" 
      :value="code"
      :options="cmOptions"
      class="editor" 
      @input="change_text"
    >
    </codemirror>
  </div>
</template>

<script>
import codemirror from "codemirror";
import "codemirror/mode/meta";
import { mapMutations,mapActions } from 'vuex'
export default {
  name: "FileCreate",
  props:['title','name','code'],
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
       
       
      },
      delete_able:false,
      update_able:false,
      excute_flag:false
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
        this.SET_VM(this)
        this.$bus.$emit('switch_activeIndex','three')
        this.$router.push({
          name:'filestate'
        })
    },
    change_text(){
      localStorage[this.name]=JSON.stringify({name:this.name,title:this.title,code:this.codemirror.getValue()})
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
    }
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
    console.log('创建了')
    setTimeout(()=>{
      this.$bus.$emit('create_tabs')
  
    },1)

  },
  beforeDestroy(){
    console.log('Destory')
  }
};
</script>

<style>
.editor .CodeMirror {
  height: 800px;
  display: flex;
  max-height: 500px;
}
.create {
  position: relative;
  top:-10px
  
}
.delete{
  position: relative;
  top:-10px
}
.update{
  position: relative;
  top:-10px
}
.open{
  position: relative;
  top:-10px
}
.empty_add{
  position: relative;
  top:-10px;

}
.excute{
  position: relative;
  top:-10px;
  
}

</style>
