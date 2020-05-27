<template>
  <div class="box" style="margin-top:20px;">
    <el-card style="margin-top:20px;padding-top:10px;padding-left:17px;" shadow="never">
      <div style="line-height:40px;margin-bottom:10px;text-align: left;">
        <span class="demonstration" style="color:#909399;font-size:14px;">从</span>
        <SearchCascader style="width:150px;" mode='1' />
        <span class="demonstration" style="color:#909399;font-size:14px;">前往</span>
        <SearchCascader style="width:150px;" mode='2' />
        <el-button type="primary" style="float:right;margin-right:30px;" @click="startNow()">显示方案</el-button>
      </div>
    </el-card>
    <el-card style="margin-top:40px;" v-if="start" shadow="never">
      <div style="font-size:24px;text-align:left;font-weight:bold;margin-left:30px;display:flex">
        <div style="flex:1;">交通选择</div>
        <!-- <el-button type="primary" style="float:right;margin-right:30px;" @click="getRoutes()">规划方案</el-button> -->
      </div>
      <div style="overflow:auto;margin-top:10px;">
        <p style="color:#909399;font-size:15px;margin-top:30px;" v-if="routes.length==0">您还没有收藏过{{departure}}->{{destination}}的交通方案</p>
        <el-row :gutter="40" style="margin:10px;">
          <el-col :span="12" v-for="route in routes" :key="route">
            <el-card style="margin-bottom: 20px;">
              <div slot="header" class="clearfix text">
                <span>{{route.total}}</span>
                <el-button v-show="!route.confirmed" @click="confirmRoute(route)" style="float: right; padding: 3px 0;"
                  type="text">确认</el-button>
                <el-button v-show="route.confirmed" style="float: right; padding: 3px 0;color:#67C23A" type="text"
                  @click="confirmRoute(route)">已确认</el-button>
              </div>
              <!-- 暂时不考虑中途路线 -->
              <div class="text item" style="line-height:24px">{{route.go[0]}}</div>
              <div class="text item" style="line-height:24px">{{route.back[0]}}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-card style="margin-top:40px;" v-if="start" shadow="never">
      <div style="font-size:24px;text-align:left;font-weight:bold;margin-left:30px;display:flex">
        <div style="flex:1;">景点选择</div>
        <!-- <el-button type="primary" style="float:right;margin-right:30px;" @click="getRoutes()">规划方案</el-button> -->
      </div>
      <div style="overflow:auto;margin-top:10px;">
        <p style="color:#909399;font-size:15px;margin-top:30px;" v-if="tours.length==0">您还没有收藏过{{destination}}的行程</p>
        <el-row :gutter="40" style="margin:10px;">
          <el-col :span="12" v-for="tour in tours" :key="tour">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="tour.photo" style="width:100%;" />
              <div style="padding: 14px;">
                <span>{{tour.title}}</span>
                <el-button v-show="!tour.confirmed" @click="confirmTour(tour)" style="float: right; padding: 3px 0;"
                  type="text">确认</el-button>
                <el-button v-show="tour.confirmed" style="float: right; padding: 3px 0;color:#67C23A" type="text"
                  @click="confirmTour(tour)">已确认</el-button>
                <div class="bottom clearfix">
                  <time class="time">{{tour.description}}</time>
                  <el-button v-if="false" type="text" class="button" @click="importTour(tour.tour)">查看行程</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <el-card style="margin-top:40px;" v-if="start" shadow="never">
      <div style="font-size:24px;text-align:left;font-weight:bold;margin-left:30px;display:flex">
        <div style="flex:1;">住宿选择</div>
        <!-- <el-button type="primary" style="float:right;margin-right:30px;" @click="getRoutes()">规划方案</el-button> -->
      </div>
      <div style="overflow:auto;margin-top:10px;">
        <p style="color:#909399;font-size:15px;margin-top:30px;" v-if="hotels.length==0">您还没有收藏过{{destination}}的住宿点</p>
        <el-row :gutter="40" style="margin:10px;">
          <el-col :span="12" v-for="hotel in hotels" :key="hotel">
            <el-card style="margin-bottom: 20px;">
              <div slot="header" class="clearfix text">
                <span>{{hotel.total}}</span>
                <el-button v-show="!hotel.confirmed" @click="confirmHotel(hotel)" style="float: right; padding: 3px 0;"
                  type="text">确认</el-button>
                <el-button v-show="hotel.confirmed" style="float: right; padding: 3px 0;color:#67C23A" type="text"
                  @click="confirmRoute(hotel)">已确认</el-button>
              </div>
              <div class="text item" style="line-height:24px">{{hotel.detail}}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <el-card style="margin-top:40px;" v-if="start" shadow="never">
      <div style="font-size:24px;text-align:left;font-weight:bold;margin-left:30px;display:flex">
        <div style="flex:1;">最终方案</div>
        <div v-if="false" style="float:right;margin-right:30px;font-size:16px;color:#409EFF" @click="starFunc()">
          导出行程单
          <i v-if="star" class="el-icon-star-on" style="margin-left:10px;margin-right:10px;"></i>
          <i v-if="!star" class="el-icon-star-off" style="margin-left:10px;margin-right:10px;"></i>
        </div>
      </div>
      <div style="overflow:auto;margin-top:10px;">
        <p style="color:#909399;font-size:15px;margin-top:30px;" v-if="strategies.length==0">确认交通、景点、住宿信息后，方案会自动生成</p>
        <el-row :gutter="40" style="margin:10px;">
          <el-col :span="12" v-for="(strategy,index) in strategies" :key="strategy">
            <el-card style="width:440px;margin-bottom: 20px;">
              <div slot="header" class="clearfix text">
                <span>方案 {{index+1}}</span>
                <el-button v-if="!strategy.added" style="float: right; padding: 3px 0;" type="text" @click="saveStrategy(strategy)">保存</el-button>
                <el-button v-if="strategy.added" style="float: right; padding: 3px 0;color:#67C23A" type="text">已保存</el-button>
              </div>
              <div class="text item">{{strategy.detail}}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <div style="height:50px;"></div>
  </div>
</template>

<script>
  import SearchCascader from "./SearchCascader";
  import Detail from "./Detail";
  import axios from "axios"
  export default {
    name: "Comprehensive",
    components: {
      Detail,
      SearchCascader
    },
    data() {
      return {
        logged: false,
        dialogVisible: false,
        dialogText: "",
        star: true,
        hotelConfirmed: null,
        routeConfirmed: null,
        tourConfirmed: null,
        strategies: [],
        routes: [],
        hotels: [],
        tours: [],
        start: false, //是否点击显示按钮
      };
    },
    computed: {
      departure: function() {
        return this.$store.state.departure;
      },
      destination: function() {
        return this.$store.state.city;
      },
      allConfirmed: function() {
        return ((this.routeConfirmed != null) &&
          (this.hotelConfirmed != null) &&
          (this.tourConfirmed != null));
      }
      /* 2019/08/02 v1.2 以下数据存储由Vuex迁移至数据库
      routes:function(){
        return this.$store.state.transport;
      },
      hotels:function(){
        return this.$store.state.accommodation;
      },
      sights:function(){
        let sightsarray=[];
        let pois=this.$store.state.points;
        for(let i=0;i<pois.length;i++){
          for(let j=0;j<pois[i].length;j++){
            if(pois[i][j].detail.deep_type && pois[i][j].detail.deep_type=='SCENIC'){
              sightsarray.push({
                name:pois[i][j].detail.name,
                type:'info'
              })
            }
          }
        }
      return sightsarray;
      },
      */
    },
    watch: {
      allConfirmed: function(val) {
        if (val == true) {
          this.addStrategy();
        }
      }
    },
    methods: {
      starFunc() {
        if (!this.star)
          this.$notify({
            title: '好',
            message: 'OK',
            type: 'success',
            position: 'top-right',
            offset: 80
          });
        this.star = !this.star
      },
      confirmHotel(hotel) {
        hotel.confirmed = !hotel.confirmed;
        for (let i = 0; i < this.hotels.length; i++) {
          if (hotel == this.hotels[i])
            continue;
          this.hotels[i].confirmed = false;
        }
        if (hotel.confirmed) {
          this.hotelConfirmed = hotel;
        } else {
          this.hotelConfirmed = null;
        }
      },
      confirmRoute(route) {
        route.confirmed = !route.confirmed;
        for (let i = 0; i < this.routes.length; i++) {
          if (route == this.routes[i])
            continue;
          this.routes[i].confirmed = false;
        }
        if (route.confirmed) {
          this.routeConfirmed = route;
        } else {
          this.routeConfirmed = null;
        }
      },
      confirmTour(tour) {
        tour.confirmed = !tour.confirmed;
        for (let i = 0; i < this.tours.length; i++) {
          if (tour == this.tours[i])
            continue;
          this.tours[i].confirmed = false;
        }
        if (tour.confirmed) {
          this.tourConfirmed = tour;
        } else {
          this.tourConfirmed = null;
        }
      },
      addStrategy() {
        let newStrategy = {
          title: this.departure + '->' + this.destination + ' ' + this.$store.state.totalDays + '日之旅',
          detail: this.tourConfirmed.title + '，' + this.routeConfirmed.description + '，' + this.routeConfirmed.total +
            '，' + this.hotelConfirmed.total,
          added: false,
        }
        this.strategies.push(newStrategy);
      },
      saveStrategy(s) {
        let that = this;
        if (s.added == false) {
          axios.get('https://ly.inftime.cn/weapp/routecollection', {
              params: {
                action: 1,
                user_id: localStorage.getItem('user_id'),
                title: s.title,
                introduce: s.detail,
                slights: JSON.stringify(this.$store.getters.exportData),
                traffic: JSON.stringify(this.routes),
                hotel: JSON.stringify(this.hotels),
              },
            })
            .then(function(response) {
              s.added = true;
              that.$notify({
                title: '方案已保存',
                message: '可在“我的->历史”中查看',
                type: 'success',
                position: 'top-right',
                offset: 80
              });
            })
            .catch(function(error) {
              console.log(error);
            });
        }
      },
      getRoutes() {
        //从数据库中获取收藏的路线
        let that = this;
        axios
          .get("https://ly.inftime.cn/weapp/collections", {
            params: {
              action: 3,
              user_id: localStorage.getItem('user_id'),
              type: 1, //1:route 2:plan 3:hotel
              fromcity: that.departure,
              tocity: that.destination,
            }
          })
          .then(function(response) {
            console.log(response);
            if (response.data && response.data.length > 0) {
              for (let i = 0; i < response.data.length; i++) {
                let route = JSON.parse(response.data[i].content);
                that.routes.push(route);
              }
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      },
      getHotels() {
        //从数据库中获取收藏的宾馆
        let that = this;
        axios
          .get("https://ly.inftime.cn/weapp/collections", {
            params: {
              action: 3,
              user_id: localStorage.getItem('user_id'),
              type: 3, //1:route 2:plan 3:hotel
              tocity: that.destination,
            }
          })
          .then(function(response) {
            if (response.data && response.data.length > 0) {
              for (let i = 0; i < response.data.length; i++) {
                let hotel = JSON.parse(response.data[i].content);
                that.hotels.push(hotel);
              }
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      },
      getTours() {
        //从数据库中获取收藏的路线
        let that = this;
        axios
          .get("https://ly.inftime.cn/weapp/collections", {
            params: {
              action: 3,
              user_id: localStorage.getItem('user_id'),
              type: 2, //1:route 2:plan 3:hotel
              tocity: that.destination,
            }
          })
          .then(function(response) {
            if (response.data && response.data.length > 0) {
              for (let i = 0; i < response.data.length; i++) {
                let result = (response.data[i].content);
                let tour = {
                  tour: result,
                  title: JSON.parse(result).city,
                  description: JSON.parse(result).city + JSON.parse(result).totalDays + '日游',
                  photo: 'http://ww2.sinaimg.cn/large/006tNc79gy1g5ke773s2zj30rs0fkttk.jpg',
                  confirmed: false,
                };
                that.tours.push(tour);
              }
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      },
      importTour(tour) {},
      startNow() {
        console.log('Loading... From', this.departure, 'to', this.destination);
        this.getRoutes();
        this.getHotels();
        this.getTours();
        this.start = true;
      }
    },
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .label {
    display: inline-block;
    width: 90px;
    color: #99a9bf;
  }

  .box {
    max-width: 1080px !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    position: relative !important;
    box-sizing: border-box;
  }

  .demonstration {
    margin-right: 20px;
    margin-left: 20px;
    font-weight: bold;
  }

  @media screen and (max-width: 768px) {
    .box {
      max-width: 1080px !important;
      padding-left: 0px !important;
      padding-right: 0px !important;
      position: relative !important;
      box-sizing: border-box;
    }
  }
</style>
