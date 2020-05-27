<template>
  <div style="display:block;margin-left:0px;">
    <el-card style="margin-top:20px;" shadow="never" v-if="tourView==null && tours.length>0">
      <div style="font-size:24px;text-align:left;font-weight:bold;margin-left:30px;display:flex">
        <div style="flex:1;">{{destination}}经典旅游行程推荐</div>
      </div>
      <div style="overflow:auto;margin-top:10px;">
        <el-row :gutter="20" style="margin:10px;">
          <el-col :span="12" v-for="tour in tours" :key="tour">
            <el-card :body-style="{ padding: '0px' }">
              <img :src="tour.photo" class="image" />
              <div style="padding: 14px;">
                <span>{{tour.title}}</span>
                <div class="bottom clearfix">
                  <time class="time">{{tour.description}}</time>
                  <el-button type="text" class="button" @click="importTour(tour.tour)">查看行程</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
    <el-card style="margin-top:20px;" shadow="never">
      <div style="font-size:24px;text-align:left;font-weight:bold;display:flex;margin-left: 30px;" class="margin-left-xs">
        <div style="flex:1;">行程规划</div>
        <span style="float:right;font-size:16px;color:#409EFF;margin-right:20px;" class="star-xs" @click="starFunc">
          收藏该行程
          <i v-if="star" class="el-icon-star-on" style="margin-left:10px;margin-right:10px;"></i>
          <i v-if="!star" class="el-icon-star-off" style="margin-left:10px;margin-right:10px;"></i>
        </span>
      </div>
      <div style="margin-left:30px;margin-top:20px;" class="margin-left-xs">
        <div v-for="(day, n) in this.$store.state.points" :key="n" style="line-height:30px;" class="flex-obver-xs">
          <div style="font-size:16px;text-align:left;flex:4;">
            <span style="font-weight:bold;">第{{n+1}}天</span>
            <!--n为数组下标-->
            <span>：预计基础支出 {{dailyCost[n][3]}} 元，交通费用 {{dailyCost[n][1]}} 元，交通时间 {{dailyCost[n][2]}}</span>
          </div>
          <div type="primary" :underline="false" style="font-size:15px;text-align:right;flex:1;margin-right:25px;">
            <el-link type="primary" :underline="false">
              <span @click="checkDetail(n)" style="margin-right: 10px;">详情</span>
            </el-link>
            <el-link type="primary" :underline="false">
              <span @click="showDay(n)" style="margin-right: 10px;">修改</span>
            </el-link>
            <el-link type="danger" :underline="false">
              <span @click="deleteDay(n)">删除</span>
            </el-link>
          </div>
        </div>
        <el-link type="primary" :underline="false" style="color:#46A0FC;font-size:15px;margin-top:10px;float: left;margin-bottom:20px;">
          <span @click="addDay">添加行程</span>
          <i class="el-icon-plus"></i>
        </el-link>
      </div>
    </el-card>
    <!-- <div style="text-align:left;margin-top:15px;margin-left:50px;font-size:15px;">
      <span>{{destination}}线路推荐：</span>
      <el-link  type="info" :underline="false" v-for="tour in tours" :key="tour">
        <span @click="deleteDay" style="margin-right: 10px;font-size:15px;top: -2px;position: relative;">{{tour.title}}</span>
      </el-link>
      <span style="float:right;margin-right:50px">隐藏</span>
    </div> -->
    <el-dialog v-loading="loading" element-loading-background="rgba(255, 255, 255, 1)" element-loading-text="经典行程，马上呈现"
      style="font-weight:bold;font-size:20px;" :visible.sync="chooseDay" :fullscreen="tourView==null?true:false">
      <p>选择第{{nowDay+1}}天行程</p>
      <keep-alive>
        <router-view />
      </keep-alive>
      <p>已选择</p>
      <el-row :gutter="20" style="height:100px;" class="flow_box">
        <div>
          <el-card :body-style="{ padding: '0px' }" style="width:250px;display:inline-block;margin-right:20px;margin-bottom:40px;"
            v-for="(choice,index) in choices" :key="choice" :index="index">
            <div style="padding: 14px;">
              <span style="font-weight:bold;" @click="showPointDetail(index)">{{choice.detail.name}}</span>
              <i style="float: left;" class="el-icon-aim" @click="setCenter(index)"></i>
              <i style="float: right;" class="el-icon-close" @click="deletePoint(index)"></i>
              <div class="bottom clearfix">
                <time class="time" @click="showPointDetail(index)">{{choice.detail.type.split(';')[choice.detail.type.split(';').length-1]}}</time>
              </div>
            </div>
          </el-card>
        </div>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleCancel()">取 消</el-button>
        <el-button type="primary" @click="chooseDay=false">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog title="行程详情" style="font-size:20px;" :visible.sync="detailShow" width="75%">
      <Detail :day='detailDay' />
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailShow = false">取 消</el-button>
        <el-button type="primary" @click="detailShow = false">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" :width="dialogWidth">
      <el-rate disabled show-score v-model="dialogScore" :score-template="dialogScore" v-if="dialogScore>0"></el-rate>
      <span v-html="dialogText"></span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
    <!-- <div name="2" v-loading="loading">
          <template slot="title" >
            <span style="font-weight:bold;font-size: 24px;float:left;margin-left:10px;">行程规划</span>
          </template>
          <div v-if="planByDay" style="width:100%;margin:auto;margin-top:20px;">
            <router-view></router-view>
          </div>
    </div>-->
    <el-card v-if="tourView==null" style="margin-top:40px;" shadow="never">
      <div style="font-size:24px;text-align:left;font-weight:bold;margin-left:30px;display:flex" class="margin-left-xs">
        <div style="flex:1;">住宿选择</div>
        <el-button type="primary" style="float:right;margin-right:30px;" @click="searchHotel()">{{firstRecommend?"住宿推荐":"换一批"}}</el-button>
      </div>
      <div style="overflow:auto;margin-top:10px;">
        <p style="color:#909399;font-size:15px;margin-top:30px;" v-if="hotels.length==0">选择行程后即可推荐住宿</p>
        <div style="margin-top:20px;">
          <el-row :gutter="40" style="margin:10px;">
            <el-col :span="12" v-for="hotel in hotels" :key="hotel">
              <el-card style="width:100%;margin-bottom: 20px;height:140px;">
                <div slot="header" class="clearfix text">
                  <span style="font-weight:bold;font-size:16px;">{{hotel.total}}</span>
                  <div style="position:relative;top:-22px;">
                    <el-button v-if="!hotel.added" style="float: right; padding: 3px 0;" @click="addHotel(hotel)" type="text">收藏</el-button>
                    <el-button v-if="hotel.added" style="float: right; padding: 3px 0;color:#F56C6C" type="text" @click="addHotel(hotel)">取消</el-button>
                  </div>
                </div>
                <div class="text item" style="font-size:14px;color:#606266;">{{hotel.detail}}</div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-card>
    <div style="height:30px;"></div>
  </div>
</template>

<script>
  import {
    isNullOrUndefined
  } from 'util';
  import Detail from "./Detail";
  import mapContainer from "./City/MapContainer"
  import axios from "axios";
  export default {
    name: "City",
    components: {
      Detail,
      mapContainer,
    },
    props: ['tourView'],
    data() {
      return {
        logged: false,
        loading: false,
        departure: "",
        //planByDay: true,
        //activeName: ["1", "2"],
        lastSearch: null, //上次酒店查询时间
        tours: [],
        star: false,
        chooseDay: false, //显示地图对话框
        // sights: [],
        hotels: [],
        startTime: "",
        firstRecommend: true, //首次推荐住宿
        detailShow: false,
        adding: false, //是否正在添加行程，每次显示地图对话框时设置
        detailDay: 0, //显示哪天的详情
        plan_id: '',
        //以下为points详细信息对话框参数
        dialogVisible: false,
        dialogTitle: "",
        dialogText: "",
        dialogScore: "",
        dialogWidth: "30%",
      };
    },
    computed: {
      choices: function() {
        return this.$store.state.points[this.$store.state.nowDay];
      },
      nowDay: function() { //nowDay为数组下标，呈现给用户时应+1
        return this.$store.state.nowDay;
      },
      destination: function() {
        return this.$store.state.city;
      },
      sights: function() {
        let sightsarray = [];
        let pois = this.$store.state.points;
        for (let i = 0; i < pois.length; i++) {
          for (let j = 0; j < pois[i].length; j++) {
            if (
              pois[i][j].detail.deep_type &&
              pois[i][j].detail.deep_type == "SCENIC"
            ) {
              sightsarray.push({
                name: pois[i][j].detail.name,
                type: "info"
              });
            }
          }
        }
        return sightsarray;
      },
      dailyCost: function() {
        let dailyCost = [];
        let transportTime = 0;
        for (let n = 0; n < this.$store.state.points.length; n++) {
          let day = this.$store.state.points[n];
          let cost = [0, 0, '', 0]; //0门票支出 1路费支出 2时间支出（文字描述） 3其他支出
          for (let i = 0; i < day.length; i++) {
            if (day[i].detail.deep_type == "SCENIC") {
              cost[0] += parseFloat(day[i].detail.scenic.price);
            }
            if (i > 0) {
              cost[1] += this.getPriceData(day[i])[1];
              if(day[i].transfer.type){
                switch (day[i].transfer.type) {
                  case 'bus':
                    transportTime += day[i].transfer.plan.plans[0].time;
                    break;
                  case 'driving':
                    transportTime += day[i].transfer.plan.routes[0].time;
                    break;
                }
              }
            }
            let otherData = this.getPriceData(day[i])[3];
            if (parseFloat(otherData) > 0)
              cost[3] += parseFloat(otherData);
          }
          if (transportTime >= 3600)
            cost[2] += parseInt(transportTime / 3600) + ' 小时 ';
          cost[2] += parseInt((transportTime % 3600) / 60) + ' 分钟';

          dailyCost.push(cost);
        }
        return dailyCost;
      }
    },
    mounted: function() {
      this.searchTour(this.$store.state.city);
    },
    watch: {
      destination: function(newCity) {
        this.searchTour(newCity);
      },
      tourView: function(tour) {
        this.importTour(tour);
      }
    },
    methods: {
      deleteDay(day) { //删除指定天
        this.$store.commit('deleteDay', day);
      },
      handleCancel() { //判断地图对话框取消时是否撤销新的一天
        if (this.adding == true) {
          this.$store.commit('deleteDay', this.nowDay);
        }
        this.chooseDay = false; //关闭对话框
      },
      checkDetail(day) {
        this.detailDay = day;
        this.detailShow = true;
      },
      starFunc() {
        let that = this;
        if (!this.star) {
          //收藏plan到服务器
          axios
            .get("https://ly.inftime.cn/weapp/collections", {
              params: {
                action: 1,
                user_id: localStorage.getItem('user_id'),
                type: 2, //1:route 2:plan 3:hotel
                content: JSON.stringify(this.$store.getters.exportData),
                fromcity: null,
                tocity: this.$store.state.city,
              }
            })
            .then(function(response) {
              that.plan_id = response.data;
              that.$notify({
                title: "收藏成功",
                message: "可在“综合”页面查看",
                type: "success",
                position: "top-right",
                offset: 80
              });
              that.star = !that.star;
            })
            .catch(function(error) {});
        } else {
          //从服务器中删除收藏
          axios
            .get("https://ly.inftime.cn/weapp/collections", {
              params: {
                action: 2,
                id: that.plan_id,
                type: 2, //1:route 2:plan 3:hotel
              }
            })
            .then(function(response) {
              that.star = !that.star;
            })
            .catch(function(error) {});
        }
      },
      addDay() { //添加新的一天
        this.chooseDay = true;
        this.adding = true;
        this.$store.commit('addNewDay');
        console.log(this.$store.state.totalDays)
        console.log(this.$store.state.nowDay)
        console.log(this.nowDay)
        this.$store.commit('switchDay', this.$store.state.totalDays - 1);
      },
      showDay(day) { //显示指定天行程
        this.adding = false;
        this.$store.commit('switchDay', day);
        this.chooseDay = true;
      },
      searchTour(destination) {
        let that = this;
        that.tours = [];
        axios
          .get("https://ly.inftime.cn/weapp/route", {
            params: {
              city: destination
            }
          })
          .then(function(response) {
            if (response.data.routes.length > 0) {
              that.tours = response.data.routes;
            } else {
              console.log("No classic routes.");
            }
          })
          .catch(function(error) {
            console.log(error);
          });
      },
      searchHotel() {
        this.firstRecommend = false;
        if (
          !this.lastSearch ||
          this.lastSearch.getTime() - new Date().getTime() <= -5000
        ) {
          this.lastSearch = new Date();
          let center = [0,0] 
          if(this.$store.state.points.length>0 && this.$store.state.points[0].length>0 && this.$store.state.points[0][0].detail){
            center[0] = this.$store.state.points[0][0].detail.location.O
            center[1] = this.$store.state.points[0][0].detail.location.P
          }
          else{
            center[0] = this.$store.state.cityCenter.O
            center[1] = this.$store.state.cityCenter.P
          }
          let placeSearch = new AMap.PlaceSearch({
            type: "住宿服务", // 高德API兴趣点类别
            pageSize: 30,
            pageIndex: Math.ceil(Math.random() * 20)
          });
          let that = this;
          placeSearch.searchNearBy("", center, 5000, function(status, result) {
            if (status == "complete" && result.poiList.count > 0) {
              console.log(result);
              let temp = [0, 1, 2, 4, 7, 12, 18, 24];
              that.hotels = [];
              for (let j = 0; j < 8; j++) {
                let i = temp[j] + Math.ceil(Math.random() * 5);
                let curPoint = {
                  id: null,
                  amap_id: result.poiList.pois[i].id,
                  name: result.poiList.pois[i].name,
                  address: result.poiList.pois[i].address,
                  distance: result.poiList.pois[i].distance,
                  location: result.poiList.pois[i].location,
                  added: false,
                  confirmed: false,
                  total: result.poiList.pois[i].name,
                  photo: "" //基本上都没照片
                };
                let distanceText = "";
                if (curPoint.distance <= 200) {
                  distanceText = "距离很近";
                } else if (curPoint.distance <= 500) {
                  distanceText = "距离较近";
                } else if (curPoint.distance <= 1500) {
                  distanceText = "距离中等";
                } else if (curPoint.distance <= 2500) {
                  distanceText = "距离较远";
                } else {
                  distanceText = "距离很远";
                }
                curPoint.detail =
                  distanceText + " / " + result.poiList.pois[i].address; //暂时
                that.hotels.push(curPoint);
              }
            } else {
              console.log(result);
            }
          });
        } else {
          this.$notify({
            title: "提示",
            message: "查询频率过快，请稍后再试",
            type: "warning",
            position: "top-right",
            offset: 80
          });
        }
      },
      addHotel(hotel) {
        /* 2019/08/02 v1.2 hotel存储由Vuex转移至数据库
        if (hotel.added == true) {
          this.$store.commit("deleteHotel", hotel);
        } else {
          this.$store.state.accommodation.push(hotel);
        }
        */
        if (hotel.added == true) {
          //从数据库中删除hotel
          axios
            .get("https://ly.inftime.cn/weapp/collections", {
              params: {
                action: 2,
                id: hotel.id,
                type: 3, //1:route 2:plan 3:hotel
              }
            })
            .then(function(response) {
              hotel.added = !hotel.added;
            })
            .catch(function(error) {
              console.log(error);
            });
        } else {
          //插入hotel到数据库
          axios
            .get("https://ly.inftime.cn/weapp/collections", {
              params: {
                action: 1,
                user_id: localStorage.getItem('user_id'),
                type: 3, //1:route 2:plan 3:hotel
                content: JSON.stringify(hotel),
                fromcity: null,
                tocity: this.$store.state.city,
              }
            })
            .then(function(response) {
              hotel.added = !hotel.added;
              hotel.id = response.data;
              this.$notify({
                title: '收藏成功',
                message: '可在“综合”页面查看',
                type: 'success',
                position: 'top-right',
                offset: 80
              });
            })
            .catch(function(error) {});
        }
      },
      searchSight() {
        //搜索景点
        let center = [
          this.$store.state.cityCenter.O,
          this.$store.state.cityCenter.P
        ];
        let placeSearch = new AMap.PlaceSearch({
          type: "风景名胜", // 高德API兴趣点类别
          pageSize: 35
        });
        let that = this;
        placeSearch.searchNearBy("", center, 5000, function(status, result) {
          if (status == "complete" && result.poiList.count > 0) {
            let temp = [1, 2, 3, 5, 8, 13, 21, 34];
            for (let j = 0; j < 10; j++) {
              let i = temp[j];
              let curPoint = {
                name: result.poiList.pois[i].name,
                address: result.poiList.pois[i].address,
                distance: result.poiList.pois[i].distance,
                location: result.poiList.pois[i].location,
                type: "info"
              };
              that.sights.push(curPoint);
            }
          } else {
            console.log(result);
          }
        });
      },
      importTour(tour) {
        let that = this;
        that.loading = true;
        if (that.tourView == null)
          that.chooseDay = true;
        that.$store.state.points = [];
        let data = JSON.parse(tour);
        this.$store.state.storge = data;
        this.$store.state.city = data.city;
        this.$store.state.AMap_Bus.city = data.city;
        this.$store.state.nowDay = 0;
        this.$store.state.totalDays = data.totalDays;
        for (let i = 0; i < this.$store.state.totalDays; i++)
          this.$store.state.points.push([]);
        let searchConfig = this.$store.state.AMap_PlaceSearch.config;
        searchConfig.city = data.city;
        setTimeout(function() {
          that.$store.state.mapContainer.$emit("setNewCity", data.city);
          that.$store.state.mapContainer.$emit("importData");
        }, 1000);
        setTimeout(function() {
          that.chooseDay = false;
          that.loading = false;
        }, 2000);
      },
      showPointDetail(index) {
        let curDetail = this.choices[index].detail;
        this.dialogTitle = curDetail.name;
        this.dialogWidth = "30%";
        this.dialogScore = 0.0;
        this.dialogText =
          '<p style="text-align:left;margin-bottom: 10px; line-height: 1.75em;">';
        //按类别显示详情
        if (curDetail.deep_type) {
          switch (curDetail.deep_type) {
            case "SCENIC":
              {
                this.dialogWidth = "50%";
                this.dialogText += curDetail.scenic.intro + "<br><br>";
                if (curDetail.scenic.opentime)
                  this.dialogText +=
                  "开放时间：" + curDetail.scenic.opentime + "<br>";
                if (curDetail.scenic.rating) {
                  this.dialogScore = curDetail.scenic.rating;
                  //this.dialogText+='景点评分：'+curDetail.scenic.rating+'<br>';
                }
                if (parseFloat(curDetail.scenic.price) >= 0) {
                  this.dialogText +=
                    "门票价格：" + curDetail.scenic.price + "元<br>";
                } else {
                  this.dialogText += "门票价格：" + curDetail.scenic.price + "<br>";
                }
                break;
              }
            case "DINING":
              {
                this.dialogWidth = "50%";
                this.dialogText += curDetail.dining.intro + "<br><br>";
                this.dialogText +=
                "开业时间：" + curDetail.dining.opentime + "<br>";
                this.dialogScore = curDetail.dining.cp_rating;
                //this.dialogText+='酒店评分：'+curDetail.dining.cp_rating+'<br>';
                this.dialogText += "人均消费：" + curDetail.dining.cost + "元<br>";
                break;
              }
            case "HOTEL":
              {
                this.dialogWidth = "50%";
                this.dialogText += curDetail.hotel.intro + "<br><br>";
                if (curDetail.hotel.star != 0) {
                  this.dialogText += "星级：" + curDetail.hotel.star + "<br>";
                }
                this.dialogScore = curDetail.hotel.rating;
                this.dialogText +=
                "最低房价：" + curDetail.hotel.lowest_price + "元<br>";
                break;
              }
          }
        }
        this.dialogText += "地址：" + curDetail.address + "</p>";
        this.dialogVisible = true;
      },
      setCenter(index) {
        this.$store.state.mapContainer.$emit("setCenter", index);
      },
      deletePoint(index) {
        if (index == 0) {
          this.$store.commit("updateTransferPlan_Special", index);
        } else if (
          index <
          this.$store.state.points[this.$store.state.nowDay].length - 1
        ) {
          this.$store.state.mapContainer.$emit(
            "updateTransferPlanWhenDeleteCard",
            index,
            this.$store.state.travelType
          );
        } else {
          this.$store.commit("updateTransferPlan_Special", index);
        }
      },
      getPriceData(point) { //0交通费用描述 1交通费 2其他费用描述 3景点门票/餐饮人均消费/酒店
        let priceData = ['', '', 0, ''];
        if (!isNullOrUndefined(point.transfer)) {
          switch (point.transfer.type) {
            case 'bus':
              {
                priceData[0] = '票价';
                priceData[1] = point.transfer.plan.plans[0].cost;
                break;
              }
            case 'driving':
              {
                priceData[0] = '路费';
                priceData[1] = point.transfer.plan.routes[0].tolls;
                break;
              }
          }
        }
        if (!isNullOrUndefined(point.detail.deep_type)) {
          switch (point.detail.deep_type) {
            case 'SCENIC':
              {
                priceData[2] = '门票价格';
                if (parseFloat(point.detail.scenic.price) >= 0) {
                  priceData[3] = point.detail.scenic.price + '元';
                } else {
                  priceData[3] = point.detail.scenic.price;
                }
                break;
              }
            case 'DINING':
              {
                priceData[2] = '人均消费';
                priceData[3] = point.detail.dining.cost + " 元";
                break;
              }
            case 'HOTEL':
              {
                priceData[2] = '最低房价';
                priceData[3] = point.detail.hotel.lowest_price + " 元";
                break;
              }
          }
        } else {
          priceData[2] = 0;
        }
        return priceData;
      },
    }
  };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .demonstration {
    margin-right: 20px;
    margin-left: 20px;
  }

  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }



  .image {
    width: 100%;
    display: block;
  }

  .router-link-active {
    text-decoration: none !important;
  }

  a {
    text-decoration: none;
  }

      .flex-obver-xs{
    display: flex;
  }


  @media screen and (max-width: 768px) {
      .day-text{
      display: none;
    }
    .margin-left-xs{
      margin-left: 10px!important;
    }
        .margin-right-xs{
      margin-right: 10px;
    }
        .flex-obver-xs{
      display: block;
    }

    .star-xs{
      margin-top: 5px;
      margin-right: 0px!important;
    }

   }
</style>
