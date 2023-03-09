const { defineConfig } = require('@vue/cli-service')
const path = require('path')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,  //关闭语法检查
  assetsDir:process.env.NODE_ENV === 'production'? '../static' : 'static',
  publicPath: process.env.NODE_ENV === 'production'? './' : '/',
  outputDir: path.resolve(__dirname,'../templates')

})