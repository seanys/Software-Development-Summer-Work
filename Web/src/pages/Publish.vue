<template>
<div>
  <el-container>
    <el-main>
      <div class="fullscreen-bg" style="background-image: url(&quot;https://n4-q.mafengwo.net/s14/M00/24/E6/wKgE2l1s1IaAVzLiAAW1OYt5QcI723.jpg?imageMogr2%2Finterlace%2F1&quot;);overflow:auto;">
      <el-card style="background-color:white;width:85%; margin: auto;margin-top: 100px;margin-bottom:100px;border-radius: 1px;padding: 20px 30px;" shadow="never">
        <div style="margin-top:20px;text-align:left;">
          <div style="display:inline;font-size:24px;font-weight:bold;margin-bottom: 25px;font-family: 'pingfang SC';">写游记</div>
          <el-button style="float:right;" type="primary" icon="el-icon-s-promotion" @click="publish()">发表</el-button>
        </div>
        <div style="margin-top:20px;text-align:left;">
          <el-input v-model="region" placeholder="地区" style="width:12%"></el-input>
          <el-input v-model="title" placeholder="标题" style="float:right;width:86%"
          maxlength="30"
          show-word-limit></el-input>
          
        </div>
        <!--
          给editor加key是因为给tinymce keep-alive以后组件切换时tinymce编辑器会显示异常，
          在activated钩子里改变key的值可以让编辑器重新创建
        -->
        <div style="margin-top:20px;text-align:left;">
          <editor id="tinymceEditor" :init="tinymceInit" v-model="content" :key="tinymceFlag"></editor>
        </div>
        <div style="margin-top:20px;text-align:left;">
          <el-input
            placeholder="摘要"
            v-model="summary"
            maxlength="54"
            show-word-limit
          ></el-input>
        </div>
      </el-card>
      </div>
    </el-main>
  </el-container>
    <el-dialog
    title="插入图片"
    :visible.sync="dialogVisible"
    width="50%">
    <span slot="footer" class="dialog-footer">
      <el-progress v-show="uploading" :text-inside="true" :stroke-width="20" :percentage="uploadPercent"></el-progress>
    </span>
      <el-upload
        v-loading="loading"
        class="upload-demo"
        action="https://upload.qiniup.com"
        ref="upload"
        list-type="picture-card"
        :data="uptoken"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        :on-progress="handleUploadProgress"
        :file-list="fileList">
        <i class="el-icon-upload"></i>
        <div slot="file" slot-scope="{file}">
          <img
            style="object-fit: cover;"
            class="el-upload-list__item-thumbnail"
            :src="file.url">
          <span class="el-upload-list__item-actions">
            <span
              @click="insertImage(file.url)"
            >
              <i class="el-icon-finished"></i>
            </span>
            <span
              @click="handleRemove(file)"
            >
              <i class="el-icon-delete"></i>
            </span>
          </span>
        </div>
      </el-upload>
  </el-dialog>
</div>
</template>
<script>
import tinymce from 'tinymce/tinymce'
import 'tinymce/themes/silver/theme'
import Editor from '@tinymce/tinymce-vue'

import 'tinymce/plugins/textcolor'
import 'tinymce/plugins/advlist'
import 'tinymce/plugins/table'
import 'tinymce/plugins/lists'
import 'tinymce/plugins/paste'
import 'tinymce/plugins/preview'
import 'tinymce/plugins/fullscreen'

import axios from "axios";
export default {
  name: 'Publish',
  components: {
    'editor': Editor
  },
  data () {
    return {
      tinymceFlag: 1,
      tinymceInit: {},
      fileList: [],
      title: '',
      content: '',
      summary:'',
      region:'',
      dialogVisible: false,
      loading: false,
      uploading: false,
      uploadPercent: 0,
      uptoken: {
        token: '',
      },
    }
  },
  methods: {
    // 插入图片至编辑器
    insertImage (src) {
      console.log('image src: ',src)
      tinymce.execCommand('mceInsertContent', false, `<img width="400px" src=${src}>`)
    },
    // 获取七牛云token
    getUptoken (){
      let that = this
      axios.post(
        'https://ly.inftime.cn/weapp/uploadfile')
          .then(function(response) {
          that.uptoken.token = response.data
          console.log('uptoken: ',that.uptoken.token)
      })
    },
    // 图片上传成功后回调
    handleUploadSuccess(res, file) {
      let imageUrl = 'http://pw5w2wzrm.bkt.clouddn.com/'+res.key
      file.url = imageUrl
      this.fileList.push(file)
      this.loading = false
      console.log('upload successfully: ',imageUrl)
      this.uploading = false
    },
    // 图片上传失败后回调
    handleUploadError(res, file) {
      this.loading = false
      this.$notify.error({
          title: '错误',
          message: '图片上传失败，请稍后再试',
          offset: 80
      });
      console.log('upload error: ',res)
      this.uploading = false
    },
    // 删除图片
    handleRemove(file){
      console.log('image removed: ',file)
      this.fileList.splice(this.fileList.indexOf(file),1)
    },
    // 上传过程中
    handleUploadProgress(event, file, fileList){
      this.uploadPercent = parseInt(event.percent)
      console.log(event)
    },
    // 图片上传前设置动画
    beforeUpload(){
      this.uploadPercent = 0
      this.uploading = true
      this.loading = true
    },
    // 发表文章
    publish(){
      let that = this;
      let params = new URLSearchParams();
      if(that.fileList.length==0){
        that.$notify.warning({
          title: '提示',
          message: '请至少上传一张图片作为封面图片',
          offset: 80
        });
      }else{
        params.append("place", that.region);
        params.append("title", that.title);
        params.append("user_id", localStorage.getItem('user_id'));
        params.append("content", '<html>'+that.content+'</html>');
        params.append("image", that.fileList[0].url);
        params.append("introduce", that.summary);
        axios
          .post("https://ly.inftime.cn/weapp/upload", params, {})
          .then(function(response) {
            console.log('new article id: ',response.data)
            that.$router.push({path:'/article?article_id=' + response.data})
          })
          .catch(function(error) {
            console.log(error)
              that.$notify.error({
              title: '错误',
              message: '服务器开小差了，请稍后再试',
              offset: 80
              });
          });
      }
    }
  },
  created () {
    const that = this
    this.tinymceInit = {
      skin_url: '/static/tinymce/skins/ui/oxide',
      language_url: '/static/tinymce/langs/zh_CN.js',
      language: 'zh_CN',
      height: 400,
      browser_spellcheck: true, // 拼写检查
      branding: false, // 去水印
      // elementpath: false,  //禁用编辑器底部的状态栏
      statusbar: false, // 隐藏编辑器底部的状态栏
      paste_data_images: true, // 允许粘贴图像
      menubar: false, // 隐藏最上方menu
      plugins: 'advlist table lists paste preview',
      toolbar: 'fontselect fontsizeselect forecolor backcolor bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | imageUpload quicklink h2 h3 blockquote table numlist bullist preview fullscreen',
      /**
       * 下面方法是为tinymce添加自定义插入图片按钮
       * 将图片先上传到存储云上，再将图片的存储地址放入编辑器内容
       */
      setup: (editor) => {
        editor.ui.registry.addButton('imageUpload', {
          tooltip: '插入图片',
          icon: 'image',
          onAction: () => {
            that.getUptoken()
            that.dialogVisible=true
          }
        })
      }
    }
  },
  activated () {
    this.tinymceFlag++
  },
  mounted () {

  }
}
</script>

<style scoped>
  .fullscreen-bg {
    background-position: 50% 50%;
    background-size: cover;
    bottom: 0;
    right: 0;
    position: fixed;
    position: absolute\9;
    width: 100%\9;
    height: 100%\9;
    overflow: hidden;
    left: 0;
    top: 0;
  }

  .el-main {
    background-color: rgb(255, 255, 255);
    text-align: center;
    line-height: 50px;
    margin-top: 100px;
  }

  a {
  text-decoration: none;
  }
</style>
