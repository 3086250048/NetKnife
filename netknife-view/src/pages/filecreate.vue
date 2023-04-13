<template>
  <div>
    <el-button type="primary" class="create" @click="create_file" size="small">
      创建文件
    </el-button>
    <codemirror
      style="
      margin-left: -15px;
      margin-top: -15px;
      "
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
import { mapMutations} from 'vuex'

export default {
  name: "FileCreate",
  data() {
    return {
      code: ``,
      cmOptions: {
        tabSize: 4,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        mode: "default",
        lineWrapping: true,
        theme: "monokai",
      }
    };
  },
  
  methods: {
    ...mapMutations('filecreateAbout',{CREATE_NETKNIFE_FILE:'CREATE_NETKNIFE_FILE'}),
    create_file() {
      const code = this.codemirror.getValue();
      this.CREATE_NETKNIFE_FILE(code)
    }
  },
  computed: {
    codemirror() {
      return this.$refs.myCm.codemirror;
    }
  },
  mounted() {}
};
</script>

<style>
.editor .CodeMirror {
  height: 800px;
  display: flex;
  max-height: 500px;
}
.create {
  float: right;
  margin-right: -15px;
}
</style>
