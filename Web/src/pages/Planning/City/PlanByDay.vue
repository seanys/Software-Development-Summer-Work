<template>
  <div>
    <div v-if="mode==1" style="height:40px">
      <span style="font-weight:bold;font-size: 24px;float:left;margin-left:10px;">第{{nowday+1}}天：{{city[nowday]}}</span>
      <el-button-group style="float:right;margin-right: 15px;">
        <el-button type="primary" :disabled="$store.state.nowDay==0" @click="$store.commit('switchDay', $store.state.nowDay-1)"
          icon="el-icon-arrow-left" round><span class="day-text">上一天</span></el-button>
        <el-button type="primary" :disabled="$store.state.nowDay==$store.state.totalDays-1" @click="$store.commit('switchDay', $store.state.nowDay+1)"
          round><span class="day-text">下一天</span><i class="el-icon-arrow-right el-icon--right"></i></el-button>
      </el-button-group>
    </div>
    <div class="map-box">
      <MapContainer style="margin-top:10px;" />
    </div>
  </div>
</template>

<script>
  import MapContainer from "../City/MapContainer";
  export default {
    name: "PlanByDay",
    components: {
      MapContainer,
    },
    data() {
      return {};
    },
    props: ['mode'],
    computed: {
      city: function() {
        let cityarray = [];
        let citydisplay = [];
        for (let i = 0; i < this.$store.state.totalDays; i++) {
          cityarray.push([]);
          citydisplay.push([]);
          //若还未添加景点就返回初始值
          if (this.$store.state.points[i].length == 0) {
            cityarray[i] = [this.$store.state.city];
          } else {
            for (let j = 0; j < this.$store.state.points[i].length; j++) {
              let cityexists = false;
              for (let k = 0; k < cityarray[i].length; k++) {
                if (this.$store.state.points[i][j].detail.cityname == cityarray[i][k]) {
                  cityexists = true;
                  break;
                }
              }
              if (!cityexists)
                cityarray[i].push(this.$store.state.points[i][j].detail.cityname);
            }
          }
        }
        for (let i = 0; i < cityarray.length; i++) {
          for (let j = 0; j < cityarray[i].length - 1; j++) {
            citydisplay[i] += cityarray[i][j] + '，';
          }
          citydisplay[i] += cityarray[i][cityarray[i].length - 1];
        }
        return citydisplay;
      },
      nowday: function() {
        return this.$store.state.nowDay;
      }
    },
  };
</script>

<style scoped>
  #MapContainer {
    width: 100%;
    height: 400px;
  }

  .map-box{
    max-height:420px;margin:20px 10px;
  }


  @media screen and (max-width: 768px) {

    .day-text {
      display: none;
    }
    .map-box{
      max-height:420px;margin:20px 0px;
    }
  }
</style>
