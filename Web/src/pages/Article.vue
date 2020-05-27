<template>
  <div id="App" style="height: 100%;" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading">
    <div class="hidden-sm-and-down image-box" :style="{backgroundImage:'url(' + city.city_picture + ')'}">
      <div class="view_info" style="background-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 100%);">
        <div class="vi_con">
        </div>
      </div>
    </div>
    <div class="view_title hidden-sm-and-down">
      <h1 style="color:white;text-align: left;position: absolute;left:360px;top: -80px;">游记：{{article.title}}</h1>
      <div class="person" style="z-index:100;position: relative;top: -100px;">
        <img style="border-radius: 50%;border:3px solid #C0C4CC;" width="120" height="120" :src="userInfo.avatarUrl"
          alt="">
        <a target="_blank" href="/club/" style="margin-left:65px"></a>
        <strong>{{userInfo.nickname}}</strong>
        <div class="vc_time">
          <span class="time">{{publishTime}}</span>
        </div>
        <el-button @click.native="star" type="primary" v-if="alreadystar" icon="el-icon-star-on" style="margin-top: 17px;margin-left:19px"
          circle></el-button>
        <el-button @click.native="star" type="primary" v-if="!alreadystar" icon="el-icon-star-off" style="margin-top: 17px;margin-left:19px"
          circle></el-button>
        <el-popover
          placement="top"
          style="margin-left:17px;"
          width="200"
          trigger="hover">
          <div id="qrcode" />
          <el-button slot="reference" type="success" icon="el-icon-share" style="margin-top: 17px;"
          circle></el-button>
        </el-popover>
      </div>
    </div>

    <div class="content-box">
      <div class="hidden-md-and-up author-box" style="text-align: left;margin:70px 10px 40px 0px;position: relative;top:30px">
        <h1>攻略：{{article.title}}</h1>
        <strong>{{userInfo.nickname}}</strong>
        <div class="vc_time">
          <span class="time">{{publishTime}}</span>
        </div>
        <!-- <image :src="tour_picture"> -->
      </div>
      <div class="content-detail-box">
        <div style="border: 1px dashed #d7d7d7;padding:20px 40px;display:flex;" v-if="!loading">
          <div style="flex:1;">
            <i class="el-icon-user-solid"></i>
            <span style="margin-left:10px;">人数：2人</span>
          </div>
          <div style="margin-left:40px;flex:1;">
            <i class="el-icon-magic-stick"></i>
            <span style="margin-left:10px;">人均费用：{{price}}元</span>
          </div>
        </div>
        <div v-for="(paragraph,index) in article_detail" :key="paragraph" style="margin-top:30px;" :index="index">
          <img v-if="paragraph.content_type=='image'" style="max-height:500px;max-width:600px;" class="image-xs" :src="paragraph.content" />
          <p v-if="paragraph.content_type=='text'">{{paragraph.content}}</p>
          <p v-if="paragraph.content_type=='HTML'" v-html="paragraph.content"></p>
        </div>
      </div>
      <div style="float:right;max-width:300px;" class="hidden-sm-and-down" v-if="!loading">
        <div style="margin-bottom:10px;">相关目的地：{{city.name}}</div>
        <div style="width:300px;height:200px;background-size: cover;position: relative;" :style="{backgroundImage:'url(' + city.normal_picture + ')'}">
          <div class="view_info" style="background-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 100%);">
            <div style="color:white;text-align: left;font-size:20px;margin-left:20px;font-weight:bold;position:absolute;bottom:20px;">{{city.name}}市</div>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-container" v-if="!loading" style="bottom:0px;width:100%;">
      <div class="nav" style="font-weight:bold;"><span style="margin-right:40px;">“其实，我也想去看看五彩缤纷的世界”</span><span>环游梦 |
          您的行程智能规划助理</span></div>
      <div style="opacity: .6;margin-bottom: 3px;">
        <el-link :underline="false" style="font-size: 12px!important;color: #fff;">隐私策略</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" style="font-size: 12px!important;color: #fff;">服务条款</el-link>
        <el-divider direction="vertical"></el-divider>
        <el-link :underline="false" style="font-size: 12px!important;color: #fff;">安全策略</el-link>
      </div>
      <div style="color: #fff;font-size: 12px;opacity: .6;margin-top:0px;">Copyright © 2019-2019 YS MC WZL SY. All
        Rights Reserved. 羊山 马畅 王子路 孙岩 版权所有 | 沪ICP备17036807号-1</div>
    </div>
  </div>
</template>

<script>
  import axios from "axios"
  import QRCode from 'qrcodejs2'
  export default {
    name: "Article",
    data() {
      return {
        author: '',
        userInfo:{
          nickname:'',
          avatarUrl:''
        },
        html: "",
        logged: false,
        price: 0,
        article_id: 0,
        article_detail: ["文字", "文字"],
        article_exist: 1,
        publishTime:'',
        article: [],
        city: [],
        loading: true,
        alreadystar: false
      };
    },
    created() {
      this.article_id = this.$route.query.article_id;
      console.log(this.article_id);
      var that = this;
      axios
        .get("https://ly.inftime.cn/weapp/article", {
          params: {
            article_id: that.article_id
          }
        })
        .then(function(res) {
          console.log(res["data"]);
          that.loading = false
          if (res["data"]["code"] == 1) {
            that.article = res["data"]["data"]["article"];
            that.publishTime = res["data"]["data"]["article"]["publish_time"]; 
            that.city = res["data"]["data"]["city"];
            that.author = res["data"]["data"]["article"]['author_id'];
            that.article_detail = res["data"]["data"]["article_detail"];
            console.log(that.article_detail)
            console.log(that.author)
            if(that.author!='-1'){
              axios
                .get("https://ly.inftime.cn/weapp/info", {
                   params: {
                     user_id: that.author
                 }
               })
               .then(function(res) {
                    console.log(res)
                    that.userInfo.avatarUrl = res.data.imageurl
                    that.userInfo.nickname = res.data.nickname + ' - 上海'
               })
            }else{
              that.userInfo.avatarUrl = 'https://n1-q.mafengwo.net/s11/M00/93/1F/wKgBEFq0VaWADPq5ABNfAqrCDqM15.jpeg?imageMogr2%2Fthumbnail%2F%21200x200r%2Fgravity%2FCenter%2Fcrop%2F%21200x200%2Fquality%2F90'
              that.userInfo.nickname = 'C小菌 - 广州'
            }
          } else {
            that.article_exist = 0;
          }
          // var obj = response.data;
          // console.log(obj);
          // that.html = obj;
          // console.log(that.html);
        })
        .catch(function(error) {
          console.log(error);
        });
      axios
        .get("https://ly.inftime.cn/weapp/articlecollection", {
          params: {
            action: 1,
            article_id: that.article_id,
            user_id: localStorage.getItem('user_id')
          }
        })
        .then(function(res) {
          var obj = res.data
          console.log(obj)
          if (obj == true) {
            that.alreadystar = true
          } else {
            that.alreadystar = false
          }
          console.log(that.alreadystar)
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    mounted() {
      this.share(this.article_id)
      this.price = Math.floor(Math.random()*15+5)*100
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      star() {
        console.log(localStorage.getItem("logged"));
        if (localStorage.getItem("logged") == "true") {
          alert("未登录，请先登录");
        } else {
          let that = this;
          if (!that.alreadystar) {
            axios
              .get("https://ly.inftime.cn/weapp/Articlecollection", {
                params: {
                  article_id: that.article_id,
                  user_id: localStorage.getItem("user_id")
                }
              })
              .then(function(response) {
                console.log(response);
                that.alreadystar = true
                that.$notify({
                  title: '收藏成功',
                  message: '您可以点击收藏查看文章',
                  type: 'success',
                  position: 'top-right',
                  offset: 80
                });
              })
              .catch(function(error) {
                console.log(error);
              });
          } else {
            axios
              .get("https://ly.inftime.cn/weapp/Articledelete", {
                params: {
                  article_id: that.article_id,
                  user_id: localStorage.getItem("user_id")
                }
              })
              .then(function(response) {
                console.log(response);
                that.alreadystar = false
                that.$notify({
                  title: '成功',
                  message: '已取消收藏',
                  type: 'success',
                  position: 'top-right',
                  offset: 80
                })
              })
              .catch(function(error) {
                console.log(error);
              });
          }
        }
      },
      share(article_id) { 
        let qrcode = new QRCode('qrcode', {  
        width: 190,  
        height: 190, // 高度  
        text: 'https://ly.inftime.cn/#/article?article_id=' + article_id // 二维码内容  
        // render: 'canvas' // 设置渲染方式（有两种方式 table和canvas，默认是canvas）  
        // background: '#f0f'  
        // foreground: '#ff0'  
        })  
        console.log(qrcode)  
      }
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  @import url("../../static/main.css");
</style>
