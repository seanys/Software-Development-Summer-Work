<template>
  <div>
    <div id="App">
      <div class="hidden-sm-and-down image-box" :style="{backgroundImage:'url(' + tour_picture + ')'}">
        <div class="view_info" style="background-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 100%);">
          <div class="vi_con">
          </div>
        </div>
      </div>
      <div class="view_title hidden-sm-and-down">
        <h1 style="color:white;text-align: left;position: absolute;left:360px;top: -80px;">攻略：{{title}}</h1>
        <div class="person" style="z-index:100;position: relative;top: -100px;">
          <img style="border-radius: 50%;border:3px solid #C0C4CC;" width="120" height="120" src="https://tva1.sinaimg.cn/large/006y8mN6gy1g6nbxxn83ij30u00u2dnz.jpg"
            alt="">
          <a target="_blank" href="/club/" style="margin-left:65px"></a>
          <strong>规划猫-智能规划</strong>
          <div class="vc_time">
            <span class="time">2019-07-09 18:04</span>
          </div>
        </div>
      </div>
      <div class="main-box">
        <div class="hidden-md-and-up author-box" style="text-align: left;margin:0px 20px">
          <h1>攻略：{{title}}</h1>
          <strong>规划猫-智能规划</strong>
          <div class="vc_time">
            <span class="time">2019-07-09 18:04</span>
          </div>
          <!-- <image :src="tour_picture"> -->
        </div>
        <div class="route-box">
          <div style="position:relative;top:20px;height:500px">
            <PlanByDay mode="1" />
          </div>
          <div class="city-box">
            <City :tourView='tour' />
          </div>
        </div>
      </div>
    </div>

    <div class="main-box rec-box">
      <div style="margin-bottom:20px;font-size:20px;font-weight: bold;width:100%">其他推荐：</div>
      <el-row :gutter="20" class="row-bg" justify="space-between">
        <el-col :span="8" :xs="24" style="margin-bottom:30px" v-for="rec in recommends" :key="rec">
          <div style="height:200px;background-size: cover;position: relative;flex:1" :style="{backgroundImage:'url(' + rec_picture + ')'}">
            <div class="view_info" style="background-image: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.7) 100%);">
              <div style="color:white;text-align: left;font-size:20px;margin-left:20px;font-weight:bold;position:absolute;bottom:20px;">上海市三日游</div>
            </div>
          </div>
        </el-col>
      </el-row>

    </div>
    <div class="footer-container" v-if="!loading" style="bottom:0px;width:100%;">
      <div class="nav" style="font-weight:bold;"><span style="margin-right:40px;">“其实，我也想去看看五彩缤纷的世界”</span><span>环游梦
          | 您的行程智能规划助理</span></div>
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
  import City from "./Planning/City"
  import PlanByDay from "./Planning/City/PlanByDay"
  import axios from "axios"
  export default {
    name: "PlanView",
    components: {
      City,
      PlanByDay,
    },
    data() {
      return {
        tour_picture: "https://tva1.sinaimg.cn/large/006y8mN6gy1g6nawm8nfbj30w50aqjuu.jpg",
        rec_picture: "https://images.shobserver.com/news/690_390/2018/6/1/0a662a97-4325-4099-aac6-6f8d0e08f4e2.jpg",
        tour_id: 0,
        tour: null,
        title: '',
        description: '',
        percent: 0, //取值0-100
        photo: null,
        loading: false,
        city: '',
        recommends: [{
            location: "罗马",
            price: "10000元/10天",
            photo: "http://n2-q.mafengwo.net/s8/M00/C9/2B/wKgBpVWSmTCAJ1UxABLtsygmoSk43.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          },
          {
            location: "上海",
            price: "2000元/5天",
            photo: "http://n4-q.mafengwo.net/s6/M00/B2/18/wKgB4lJ1MdWABIHAAAysp_8i80o98.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          },
          {
            location: "日本",
            price: "5000元/10天",
            photo: "http://p4-q.mafengwo.net/s10/M00/6C/17/wKgBZ1k70MGAOGPUABQGfSedfQ411.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          }
        ]
      };
    },
    created() {
      this.tour_id = this.$route.query.tour_id;
      this.loadTour(this.tour_id);
    },
    methods: {
      loadTour(tour_id) {
        let that = this;
        axios.get('https://ly.inftime.cn/weapp/route', {
            params: {
              id: tour_id,
            },
          })
          .then(function(response) {
            if (response.data.routes && response.data.routes.length > 0) {
              let tour = response.data.routes[0];
              that.city = tour.city;
              that.title = tour.title;
              that.description = tour.description;
              that.photo = tour.photo;
              that.percent = tour.percent;
              that.tour = tour.tour;
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      },
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  @import url("../../static/main.css");


</style>
