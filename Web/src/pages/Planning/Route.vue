<template>
  <div>
    <el-card style="margin-top:20px;padding-top:10px;padding-bottom:20px;padding-left:17px;" shadow="never">
      <div style="line-height:40px;margin-bottom:20px;text-align: left;">
        <span class="demonstration" style="margin-right:60px;margin-left:20px;">线路</span>
        <SearchCascader style="width:150px;" mode='1'/>
        <span class="demonstration" style="color:#909399;font-size:14px;">前往</span>
        <SearchCascader style="width:150px;" mode='2'/>
        <!-- <span class="demonstration">游玩天数</span> -->
        <span class="demonstration" style="color:#909399;font-size:14px;">共</span>
        <!--el-input v-model="daysOption" placeholder="1" style="width:50px;"></el-input-->
        <el-input-number
          v-model="daysOption"
          controls-position="right"
          size="medium"
          :min="1"
          :max="30"
          style="width:100px;"
        ></el-input-number>
        <span class="demonstration" style="color:#909399;font-size:14px;">天</span>
        <!-- <el-switch v-model="timeDuration" active-text="选择出发日期" style="margin-left:20px;"></el-switch> -->
      </div>
      <div style="margin-top:20px;text-align:left;">
        <span class="demonstration" style="margin-right:30px;margin-left:20px;">单程预算</span>
        <el-input v-model="priceRange[0]" placeholder="1" style="width:80px"></el-input>
        <span class="demonstration" style="color:#909399;font-size:14px;">至</span>
        <el-input v-model="priceRange[1]" placeholder="1" style="width:80px"></el-input>
        <span class="demonstration" style="color:#909399;font-size:14px;">元</span>
      </div>
      <div style="margin-top:20px;text-align:left;">
        <span class="demonstration" style="margin-right:30px;">考虑因素</span>
        <el-tag v-for="tag in tags" :disable-transitions="false" @close="handleClose(tag)" :key="tag.name" style="margin-right:10px;">{{tag}}</el-tag>
        <el-tag v-for="tag in pre_tags" :disable-transitions="false" @close="handleClose(tag)" :key="tag.name" type="info" tyle="margin-right:10px;">{{tag}}</el-tag>
      </div>
      <div style="margin-top:20px;text-align:left;">
        <span class="demonstration" style="margin-right:30px;">日期范围</span>
        <el-date-picker v-model="startTime" type="daterange" :clearable="false" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd"></el-date-picker>
      </div>
    </el-card>
    <el-card style="margin-top:40px;" shadow="never">
      <div style="font-size:24px;text-align:left;font-weight:bold;margin-left:30px;display:flex">
        <div style="flex:1;">交通规划</div>
        <el-button type="primary" style="float:right;margin-right:30px;" @click="getRoutes()">规划方案</el-button>
      </div>
      <div style="overflow:auto;margin-top:10px;">
        <p style="color:#909399;font-size:15px;margin-top:30px;" v-if="routes.length==0">快开始规划你的行程吧！</p>
        <el-row :gutter="40" style="margin:10px;">
          <el-col :span="12" v-for="route in routes" :key="route">
            <el-tooltip class="item" effect="dark" :content="route.description" placement="top">
            <el-card style="margin-bottom: 20px;height:160px;">
              <div slot="header" class="clearfix text">
                <img v-show="route.type=='train'" src="/static/train.png" style="float:left;margin-top:-5px;"/>
                <img v-show="route.type=='flight'" src="/static/flight.png" style="float:left;margin-top:-5px;"/>
                <span style="font-weight:bold;">{{route.total}}</span>
                <el-button
                  v-if="!route.added"
                  style="float: right; padding: 3px 0;"
                  @click="addPlan(route)"
                  type="text"
                >收藏</el-button>
                <el-button
                  v-if="route.added"
                  style="float: right; padding: 3px 0;color:#F56C6C"
                  type="text"
                  @click="addPlan(route)"
                >取消</el-button>
              </div>
              <!-- 暂时不考虑中途路线 -->
              <div class="text item" style="line-height:24px;font-size:14px;color:#606266;">{{route.go[0]}}</div>
              <div class="text item" style="line-height:24px;font-size:14px;color:#606266;">{{route.back[0]}}</div>
            </el-card>
            </el-tooltip>

          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import SearchCascader from "./SearchCascader";
import axios from "axios";
export default {
  name: "Route",
  components: {
    SearchCascader
  },
  data() {
    return {
      logged: false,
      period: "不限天数",
      priceExpection: "不限价格",
      daysOption: 3,
      timeDuration: true,
      tags: ["只看直飞","尽量省钱"],
      pre_tags: ["不坐飞机"],
      routes: [],
      value: "",
      startTime: ["2019-07-30", "2019-08-30"],
      priceRange: [300, 3000], //价格区间
      sliderMarks: {
        //滑块标记
        500: "500元",
        2000: "2000元",
        5000: "5000元",
        8000: "8000元"
      }
    };
  },
  computed:{
    departure: function(){
      return this.$store.state.departure;
    },
    destination: function(){
      return this.$store.state.destination;
    },
  },
  methods: {
    addPlan(plan) {
      /* 2019/08/02 v1.2 route存储由Vuex转移至数据库
      if (plan.added == true) {
        this.$store.commit("deletePlan", plan);
      } else {
        this.$store.state.transport.push(plan);
        console.log(this.$store.state.transport);
      }
      plan.added = !plan.added;
      */
      if (plan.added == true) {
        //从数据库中删除route
      axios
        .get("https://ly.inftime.cn/weapp/collections", {
          params: {
           action:2,
           id:plan.id,
           type:1,//1:route 2:plan 3:hotel
          }
        })
        .then(function(response) {
          plan.added = !plan.added;
        })
        .catch(function(error) {
          console.log(error);
        });
      } else {
        //插入route到数据库
        axios
        .get("https://ly.inftime.cn/weapp/collections", {
          params: {
           action:1,
           user_id:localStorage.getItem('user_id'),
           type:1,//1:route 2:plan 3:hotel
           content:JSON.stringify(plan),
           fromcity:this.$store.state.departure,
           tocity:this.$store.state.city,
          }
        })
        .then(function(response) {
          plan.added = !plan.added;
          plan.id=response.data;
          this.$notify({
            title: '收藏成功',
            message: '可在“综合”页面查看',
            type: 'success',
            position: 'top-right',
            offset:80
          });
        })
        .catch(function(error) {
        });
      }
    },
    getRoutes() {
      this.routes = [];
      let that = this;
      //更新Vuex中totalDays和points
      /* 2019/08/02 v1.2 解除天数关联
      that.$store.state.totalDays = that.daysOption;
      that.$store.state.points = [];
      for (let i = 0; i < that.daysOption; i++) {
        that.$store.state.points.push([]);
      }
      */
      let routesAtoB = [];
      let routesBtoA = [];
      let done = 0; //两个GET有几个已经完成
      //查询去程路线（暂时只有航班）
      axios
        .get("https://ly.inftime.cn/weapp/flights", {
          params: {
            earlyTime: that.startTime[0],
            laterTime: that.startTime[1],
            from: "上海城区",
            to: "北京城区",
            minprice: that.priceRange[0],
            maxprice: that.priceRange[1]
          }
        })
        .then(function(response) {
          if (response.data.flights.length > 0) {
            routesAtoB = response.data.flights;
            done++;
          } else {
            that.$notify({
              title: "无匹配结果",
              message: "换个查询条件试试吧",
              type: "error",
              position: "top-right",
              offset: 80
            });
          }
          if (done == 2) {
            that.pushRoutes(routesAtoB, routesBtoA);
          }
        })
        .catch(function(error) {
          console.log(error);
        });
      //查询回程路线
      axios
        .get("https://ly.inftime.cn/weapp/flights", {
          params: {
            earlyTime: that.startTime[0],
            laterTime: that.startTime[1],
            from: "上海城区",
            to: "西安市",
            minprice: that.priceRange[0],
            maxprice: that.priceRange[1]
          }
        })
        .then(function(response) {
          if (response.data.flights.length > 0) {
            routesBtoA = response.data.flights;
            done++;
          } else {
            that.$notify({
              title: "无匹配结果",
              message: "换个查询条件试试吧",
              type: "error",
              position: "top-right",
              offset: 80
            });
          }
          if (done == 2) {
            that.pushRoutes(routesAtoB, routesBtoA);
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    let train1 = axios.get("https://ly.inftime.cn/weapp/train", {
          params: {
            from_city: that.$store.state.departure,
            to_city: that.$store.state.city,
            date: '2019-09-24'
          }
        })
    let train2 = axios.get("https://ly.inftime.cn/weapp/train", {
      params: {
        from_city: that.$store.state.city,
        to_city: that.$store.state.departure,
        date: '2019-09-24'
      }
    })
    Promise.all([train1, train2]).then(function (results) {
      console.log('12306 OK. ',results);
      that.push12306Routes(results[0].data,results[1].data)
      })
    },
    pushRoutes(rAB, rBA) {
      //往返数据
      for (let i = 0; i < Math.min(rAB.length, rBA.length, 6); i++) {
        let curRoute1 = rAB[i];
        console.log(curRoute1)
        let curRoute2 = rBA[i];
        let route = {
          id:null,
          type: 'flight',
          total: "",
          go: [],
          back: [],
          description: "",
          added: false,
          confirmed: false
        };
        route.go.push(
          //curRoute1.departureDate +
          //" " +
          curRoute1.flightNumber +
          " " +
          this.$store.state.departure +
          "->" +
          this.$store.state.city +
          " ￥" +
          curRoute1.price
        );
        route.back.push(
          //curRoute2.departureDate +
          //" " +
          curRoute2.flightNumber +
          " " +
          this.$store.state.city +
          "->" +
          this.$store.state.departure +
          " ￥" +
          curRoute2.price
        );
        route.total =
          "往返总价：" +
          (parseFloat(curRoute1.price) + parseFloat(curRoute2.price)
          ).toString() +
          "元";
        route.description =
          curRoute1.airlineName + " / " + curRoute2.airlineName;
        this.routes.push(route);
      }
    },
    push12306Routes(rAB, rBA) {
      //往返数据
      for (let i = 0; i < Math.min(rAB.length, rBA.length, 4); i++) {
        let curRoute1 = rAB[i];
        let curRoute2 = rBA[i];
        let route = {
          id:null,
          type: 'train',
          total: "",
          go: [],
          back: [],
          description: "",
          added: false,
          confirmed: false
        };
        route.go.push(
          curRoute1.station_train_code +
          " " +
          curRoute1.start_time +
          " " +
          curRoute1.from_station_name +
          "->" +
          curRoute1.to_station_name +
          " " +
          curRoute1.arrive_time
        );
        route.back.push(
          curRoute2.station_train_code +
          " " +
          curRoute2.start_time +
          " " +
          curRoute2.from_station_name +
          "->" +
          curRoute2.to_station_name +
          " " +
          curRoute2.arrive_time
        );
        route.total =
          "往返总价：" +
          (parseFloat(curRoute1.price.split('¥')[1]) + parseFloat(curRoute2.price.split('¥')[1])
          ).toString() +
          "元";
        route.description =
          curRoute1.type + " / " + curRoute2.type;
        this.routes.push(route);
      }
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.demonstration {
  margin-right: 20px;
  margin-left: 20px;
  font-weight: bold;
}
.el-row {
  margin-bottom: 20px;
}

@media screen and (max-width: 768px) {

}
</style>
