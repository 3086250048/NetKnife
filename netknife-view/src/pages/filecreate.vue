<template>
  <div>
    <el-button type="primary" class="create" @click="showCode" size="small">
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


export default {
  name: "FileCreate",
  data() {
    return {
      code: `{\n  "name": "",\n  "rule": {}\n}`,
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
    showCode() {
      const code = this.codemirror.getValue();
      console.log(code);
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
