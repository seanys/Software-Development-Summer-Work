<template>
  <div>
    <el-carousel height="500px" style="z-index:0" indicator-position="outside" interval="10000">
      <el-carousel-item v-for="item in images" :key="item">
        <span @click="toCommunity" class="top-text">{{item.introducation}}</span>
        <span @click="toCommunity" class="next-text">{{item.attach}}</span>
        <img :src="item.photo" class="hidden-xs-only" />
        <img :src="item.small_photo" class="hidden-sm-and-up" />
      </el-carousel-item>
    </el-carousel>
    <div class="search-area">
      <div class="search-box" name="searchArea">
        <el-card name="searchBox" shadow="always">
          <div>
            <el-radio v-model="radio" label="1">最低价</el-radio>
            <el-radio v-model="radio" label="2">舒适型</el-radio>
          </div>
          <div name="searchInput" style="display:flex;">
            <SearchCascader class="search-input" style="outline:none;width: 100%;border: none;font-weight:bold;font-size: 18px"
              mode="2" />
            <el-button type="primary" class="hidden-xs-only" style="margin: 13px;font-weight:bold;margin-left:30px;font-size: 16px !important;"
              @click="search">搜索方案</el-button>
          </div>
          <el-button type="primary" class="hidden-sm-and-up" style="margin: 10px 0 0 0;font-weight:bold;font-size: 16px !important;width: 100%;"
            @click="search">搜索方案</el-button>
        </el-card>
      </div>
      <p style="font-size:20px;">推荐行程</p>
      <el-row :gutter="20" style="margin:10px;">
        <el-col :span="8" :xs="24" style="margin-bottom:30px" v-for="rec in recommends" :key="rec">
          <el-card :body-style="{ padding: '0px' }" @click="startplan">
            <img :src="rec.photo" class="image" />
            <div style="padding: 14px;">
              <span>{{rec.location}}</span>
              <div class="bottom clearfix">
                <time class="time" style="font-size:15px;margin-bottom:10px;">{{ rec.price }}</time>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <!-- <div style="height:50px;"></div> -->
    <div class="footer-container">
      <div class="nav" style="font-weight:bold;">
        <span style="margin-right:40px;">“其实，我也想去看看五彩缤纷的世界”</span>
        <span>环游梦 | 您的行程智能规划助理</span>
      </div>
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
  import SearchCascader from "./Planning/SearchCascader";
  export default {
    name: "Travel",
    components: {
      SearchCascader
    },
    data() {
      return {
        activeIndex: 1,
        activeIndex2: 1,
        sliderValue: 0,
        visible: false,
        logged: false,
        images: [{
            introducation: "@东京",
            attach: "东京都的回忆",
            photo: "http://ww2.sinaimg.cn/large/006tNc79ly1g4xbbtod27j31hc0hs498.jpg",
            small_photo: "https://tva1.sinaimg.cn/large/006y8mN6ly1g6d12c6qszj30ku0ewtbk.jpg"
          },
          {
            introducation: "@摩洛哥",
            attach: "梦想与现实的交错",
            photo: "http://ww4.sinaimg.cn/large/006tNc79ly1g4xbd6efxoj31hc0hsdqz.jpg",
            small_photo: "https://tva1.sinaimg.cn/large/006y8mN6ly1g6d16ajbu9j30m80esn36.jpg"
          },
          {
            introducation: "@撒哈拉沙漠",
            attach: "最完美的毕业之旅",
            photo: "http://ww1.sinaimg.cn/large/006tNc79ly1g4xbdcb6k7j31hc0hs7d3.jpg",
            small_photo: "https://tva1.sinaimg.cn/large/006y8mN6ly1g6d19shbhsj30nm0hpwhf.jpg"
          },
          {
            introducation: "@云南",
            attach: "小众陶瓷艺术",
            photo: "http://ww4.sinaimg.cn/large/006tNc79ly1g4xbdglbbhj31hc0hs17c.jpg",
            small_photo: "https://tva1.sinaimg.cn/large/006y8mN6ly1g6d15vgju5j30i20fnjt5.jpg"
          }
        ],
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
        ],
        aimLocation: "",
        radio: "1"
      };
    },
    methods: {
      search() {
        this.$router.push({
          path: "/planning"
        });
      },
      startplan() {
        this.$router.push({
          path: "/planning"
        });
      },
      toCommunity() {
        window.open("http://ly.inftime.cn//#/community", "_blank");
        // this.$router.push({path:'/community'})
      }
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both;
  }

  .footer-container {
    height: 150px;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background-color: #1f2530;
    padding: 0 20px;
    color: #fff;
  }

  .footer-container .nav {
    font-size: 14px;
    margin-bottom: 15px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    opacity: 0.8;
  }

  .top-text {
    z-index: 10;
    position: fixed;
    color: white;
    left: 110px;
    top: 100px;
    font-size: 28px;
    font-weight: bold;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.9);
  }

  .next-text {
    z-index: 10;
    position: fixed;
    color: white;
    left: 110px;
    top: 140px;
    font-size: 28px;
    font-weight: bold;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.9);
  }

  .search-box {
    margin-top: 15px;
    margin-bottom: 110px;
    position: relative !important;
    display: inline-block !important;
    width: 90%;
    background-color: white;
    height: 115px;
    border-radius: 6px;
  }

  .search-area {
    margin-top: -225px !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
  }

  .search-input{
    margin-top:15px;margin-left:20px;
  }

  @media screen and (max-width: 768px) {
    .search-area {
      margin-top: -260px !important;
      padding-left: 10px !important;
      padding-right: 10px! important;
    }

    .search-box {
      margin-top: 15px;
      margin-bottom: 120px;
      position: relative !important;
      display: inline-block !important;
      width: 90%;
      background-color: white;
      border-radius: 6px;
    }

    .top-text {
      z-index: 10;
      position: fixed;
      color: white;
      left: 60px;
      top: 100px;
      font-size: 28px;
      font-weight: bold;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.9);
    }

    .next-text {
      z-index: 10;
      position: fixed;
      color: white;
      left: 60px;
      top: 140px;
      font-size: 28px;
      font-weight: bold;
      text-shadow: 0 1px 3px rgba(0, 0, 0, 0.9);
    }

    .search-input{
      margin-top:0px;margin-left:0px;margin-top: 20px;
    }

  }
</style>
