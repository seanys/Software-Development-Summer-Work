<template>
  <el-container>
    <el-aside class="hidden-xs-only" width="200px" style="margin-left:20px;margin-right:20px;position:fixed;margin-left:100px;margin-right:50px;margin-top:20px;">
      <el-card style="margin-top:20px;padding:0" :body-style="{ padding: '0px' }" shadow="never">
        <el-menu default-active="1" class="el-menu-vertical-demo" :router="true" style="border:none;">
          <el-menu-item index="1" route="/planning/route">
            <i class="el-icon-discover"></i>
            <span slot="title">交通</span>
          </el-menu-item>
          <el-menu-item index="2" route="/planning/city">
            <i class="el-icon-office-building"></i>
            <span slot="title">城市</span>
          </el-menu-item>
          <el-menu-item index="3" route="/planning/comprehensive">
            <i class="el-icon-map-location"></i>
            <span slot="title">综合</span>
          </el-menu-item>
        </el-menu>
      </el-card>
      <el-button icon="el-icon-star-on" @click="myStarVisible=true" style="position:fixed;bottom:70px;left:130px;" type="primary"
        plain round>已收藏</el-button>
    </el-aside>
    <el-container>
      <el-main class="main-container">
            <!-- <p class="hidden-sm-and-up">该页面的手机版本仍在排版</p> -->

        <keep-alive class="hidden-xs-only">
          <router-view></router-view>
        </keep-alive>
        <div class="hidden-sm-and-up">
          <Route />
          <City />
          <Comprehensive />
        </div>
      </el-main>
    </el-container>

    <el-dialog title="已收藏" :visible.sync="myStarVisible" style="max-height:600px;overflow-y:scroll;">
      <p v-if="starText!=''">{{starText}}</p>
      <el-row :gutter="20" style="margin:10px;">
        <el-col :span="12" v-for="star in stars" :key="star">
          <el-card :body-style="{ padding: '0px' }">
            <div style="padding: 14px;">
              <span>类型：{{star.type}}</span>
              <div class="bottom clearfix">
                <p class="time">{{star.title}}</p>
                <p class="time">收藏时间：{{star.time}}</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-dialog>
  </el-container>
</template>

<script>
  import axios from "axios";
  import City from "./Planning/City.vue";
  import Route from "./Planning/Route.vue";
  import Comprehensive from "./Planning/Comprehensive.vue";
  export default {
    name: "Planning",
    components: {
      City,
      Route,
      Comprehensive
    },
    data() {
      return {
        myStarVisible: false,
        starText: '',
        stars: [],
      };
    },
    mounted: function() {
      this.getStars();
      if (this.$route.query.destination) {
        this.$store.state.city = this.$route.query.destination;
      }
    },
    methods: {
      getStars() {
        let that = this;
        axios
          .get("https://ly.inftime.cn/weapp/collections", {
            params: {
              action: 3,
              user_id: localStorage.getItem('user_id'),
            }
          })
          .then(function(response) {
            if (response.data && response.data.length > 0) {
              for (let i = 0; i < response.data.length; i++) {
                let result = response.data[i];
                switch (result.type) {
                  case '1':
                    {
                      var star = {
                        type: '交通',
                        title: JSON.parse(result.content).total,
                        time: result.id
                      };
                      break;
                    }
                  case '2':
                    {
                      var star = {
                        type: '行程',
                        title: JSON.parse(result.content).city + JSON.parse(result.content).totalDays + '日游',
                        time: result.id
                      };
                      break;
                    }
                  case '3':
                    {
                      var star = {
                        type: '住宿',
                        title: JSON.parse(result.content).name,
                        time: result.id
                      };
                      break;
                    }
                }
                that.stars.push(star);
              }
            } else {
              that.starText = '这里空空如也，快添加第一个收藏吧！'
            }
          })
          .catch(function(error) {});
      }
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .flow_box {
    overflow-x: scroll;
    overflow-y: hidden;
    white-space: nowrap;
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

  .main-container {
    margin-left: 320px;
    margin-right: 40px;
  }

  @media screen and (max-width: 768px) {
    .main-container {
      margin-left: 0px;
      margin-right: 0px;
    }
  }
</style>
