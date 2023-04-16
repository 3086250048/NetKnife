<template>
  <div>
    <el-button type="primary" class="create" @click="create_file" size="small">
      创建文件
    </el-button>
    <el-button type="primary" class="delete" @click="delete_file" size="small">
      删除文件
    </el-button>
    <el-button type="primary" class="update" @click="update_file" size="small">
      更新文件
    </el-button>
    <el-button type="primary" class="open" @click="open_file" size="small">
      打开文件
    </el-button>
    <el-button type="primary" class="empty_add" @click="add_empty" size="small">
      ＋新窗口
    </el-button>
    <codemirror
      style="margin-left:-15px;
      margin-top: -15px;"
      ref="myCm"
      :value="code"
      :options="cmOptions"
      class="editor"
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
  data() {
    return {
      code: `name:\npriority:\n\n\ntranslation:{\n\n\n}\n\njinja2:{\n\n\n}\n\nexcute:{\n\n}\n\n`,
      cmOptions: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: "default",
        lineWrapping: true,
        theme: "monokai",
      },
      title:''
    };
  },
  
  methods: {
    ...mapMutations('filecreateAbout',{
      SET_VM:'SET_VM'
    }),
    ...mapActions('filecreateAbout',{
      create_netknife_file:'create_netknife_file',
      delete_netknife_file:'delete_netknife_file',
      update_netknife_file:'update_netknife_file'
    }),
    create_file() {
      const code = this.codemirror.getValue();
      // change在CREATE_NETKNIFE_FILE里面
      this.create_netknife_file(code)
    },
    delete_file(){
      const code = this.codemirror.getValue();
      this.delete_netknife_file(code)
    },
    update_file(){
      const code = this.codemirror.getValue();
      this.update_netknife_file(code)
    },
    add_empty(){
      this.$bus.$emit('add')
    },
    open_file(){
      // 待完成打开逻辑
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
    this.SET_VM(this)
    console.log(this.$route.params.title)
    this.title=this.$route.params.title
    this.$bus.$on('change_title',(title)=>{
      this.title=title
    })
    console.log(this.title)
  },
  beforeDestroy(){
    this.$bus.$off('change_title')
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
</style>
