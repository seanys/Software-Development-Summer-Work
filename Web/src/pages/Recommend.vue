<template>
  <div>
  <div class="box">
    <div style="margin-top:20px;" name="chooseForYou">
      <div style="font-size:24px;text-align:left;font-weight:bold;">为您精选</div>
      <div style="font-size:16px;text-align:left;margin-top:0px;color:#606266;">智能的算法选择您可能喜欢的旅行</div>
      <el-image style="height: 300px;border-radius:4px;margin-top:20px;" src="https://liuxue.ef.com.cn/sitecore/__~/media/efcom/2017/lt/destinations/United-States/New-York/Stage/LT_Dest_NYC_Stage_desktop.jpg"
        fit="cover"></el-image>
      <div style="font-size:12px;text-align:left;">@拍摄于纽约</div>
      <el-row :gutter="20" style="margin-top:20px;">
        <el-col :span="12" :xs="24" style="margin-bottom:20px" v-for="rec in recommends" :key="rec">
          <el-card :body-style="{ padding: '0px' }">
            <img :src="rec.photo" @click="toplanview(rec)" class="image" />
            <div style="padding: 14px;">
              <span>{{rec.location}}</span>
              <div class="bottom clearfix">
                <time class="time">{{ rec.price }}</time>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div style="margin-top:60px;" name="lowPricePlanning">
      <div style="font-size:24px;text-align:left;font-weight:bold;">低价规划</div>
      <div style="font-size:16px;text-align:left;margin-top:0px;color:#606266;">低价环游世界</div>
      <el-row :gutter="20" style="margin-top:20px;">
        <el-col :span="8" v-for="rec in lowprice" :xs="24" style="margin-bottom:20px" :key="rec">
          <el-card :body-style="{ padding: '0px' }">
            <img :src="rec.photo" @click="toplan(rec)" class="image" />
            <div style="padding: 14px;">
              <span>{{rec.location}}</span>
              <div class="bottom clearfix" style="line-height:17px;">
                <time class="time">{{ rec.detail }}</time>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div style="margin-top:60px;" name="lowPricePlanning">
      <div style="font-size:24px;text-align:left;font-weight:bold;">住宿点</div>
      <div style="font-size:16px;text-align:left;margin-top:0px;color:#606266;">方便旅游的住宿区域推荐</div>
      <el-row :gutter="20" style="margin-top:20px;">
        <el-col :span="8" v-for="rec in hotels" :xs="24" style="margin-bottom:20px" :key="rec">
          <el-card :body-style="{ padding: '0px' }">
            <img :src="rec.photo" class="image img-responsive" />
            <div style="padding: 14px;">
              <span>{{rec.location}}</span>
              <div class="bottom clearfix">
                <time class="time">{{ rec.detail }}</time>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div style="height:50px;"></div>

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
  export default {
    name: "Recommend",
    created() {
      var that = this;
      axios
        .get("https://ly.inftime.cn/weapp/route")
        .then(function(response) {
          let obj = response.data.routes
          console.log(obj)
          that.recommends = []
          console.log(obj.length)
          for (var i = 0; i < obj.length; i++) {
            let rec = {
              id: obj[i].id,
              location: obj[i].city,
              price: obj[i].title + '\n' + obj[i].description,
              photo: obj[i].photo
            }
            that.recommends.push(rec)
          };
        })
        .catch(function(error) {
          console.log(error);
        })
    },
    data() {
      return {
        activeIndex: 1,
        activeIndex2: 1,
        visible: false,
        logged: false,
        recommends: [{
            id: 0,
            location: "上海",
            price: "6000元/5天",
            photo: "http://n4-q.mafengwo.net/s6/M00/B2/18/wKgB4lJ1MdWABIHAAAysp_8i80o98.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          },
          {
            id: 0,
            location: "日本",
            price: "6000元/5天",
            photo: "http://p4-q.mafengwo.net/s10/M00/6C/17/wKgBZ1k70MGAOGPUABQGfSedfQ411.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          }
        ],
        lowprice: [{
            location: "三亚",
            detail: "无需通宵候机，可3000元内实现十天的机票+住宿",
            photo: "http://n2-q.mafengwo.net/s10/M00/CE/81/wKgBZ1iSnCeAK7aoAA9lMtvV9Rc77.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          },
          {
            location: "重庆",
            detail: "1000元规划重庆游玩线路",
            photo: "http://n1-q.mafengwo.net/s8/M00/33/41/wKgBpVXV5oWALnhvAA9H2b9e99I77.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          },
          {
            location: "苏州",
            detail: "300元送你一个小桥流水人家",
            photo: "http://b2-q.mafengwo.net/s6/M00/50/2C/wKgB4lJab8OAE1MgAAQzNptgEhI79.jpeg?imageMogr2%2Fthumbnail%2F%21690x370r%2Fgravity%2FCenter%2Fcrop%2F%21690x370%2Fquality%2F100"
          }
        ],
        hotels: [{
            location: "成都市中心套房",
            detail: "交通便捷，俯瞰城市，高性价比选择",
            photo: "http://ww2.sinaimg.cn/large/006tNc79gy1g4xlrr4gq1j31i30u04qp.jpg"
          },
          {
            location: "台州市小别墅",
            detail: "感受沿海台州的海鲜与美味",
            photo: "http://ww1.sinaimg.cn/large/006tNc79gy1g4xm6mr2msj31hj0u0tps.jpg"
          },
          {
            location: "京都榻榻米",
            detail: "最佳住宿地点，便捷游玩京都",
            photo: "http://ww4.sinaimg.cn/large/006tNc79gy1g4xm7mjdfpj31hz0u0qgb.jpg"
          }
        ]
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      toplanview(recommends) {
        this.$router.push({
          //核心语句
          path: "/planview",
          query: {
            tour_id: recommends.id //跳转的路径
          },
        })
      },
      toplan(recommends) {
        this.$router.push({
          //核心语句
          path: "/planning/city",
          query: {
            destination: recommends.location //跳转的路径
          }
        })
      }
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  @import url("../../static/main.css");

  .box {
    max-width: 1080px !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    position: relative !important;
    box-sizing: border-box;
  }

  .img-responsive {
    display: block;
    max-width: 100%;
    height: auto;
  }

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
</style>
