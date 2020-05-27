<template>
  <div style="display:inline-flex;">
    <el-cascader style="width:100%" v-if="mode==1" :options="option" size="medium" filterable :props="{ expandTrigger: 'hover' }"
      :placeholder="this.$store.state.departure==''?'选择出发地':this.$store.state.departure" v-model="departure"
      :show-all-levels="false">
    </el-cascader>
    <el-cascader style="width:100%" v-if="mode==2" :options="option" size="medium" filterable :props="{ expandTrigger: 'hover' }"
      :placeholder="this.$store.state.city==''?'选择目的地':this.$store.state.city" v-model="destination" :show-all-levels="false">
      <!--hover:浮动出现下级菜单-->
    </el-cascader>
  </div>
</template>

<script>
  export default {
    name: "SearchCascader",
    data() {
      return {
        destination: [],
        departure: [],
        option: [],
      };
    },
    props: ['mode'],
    mounted: function() {
      let that = this;
      //请求行政区信息
      if (this.$store.state.district == null) {
        AMap.service("AMap.DistrictSearch", function() {
          let districtSearch = new AMap.DistrictSearch({
            level: "country",
            subdistrict: 2
          });
          districtSearch.search('中国', function(status, result) { //参照高德API
            that.formatArray(result.districtList[0].districtList);
            that.option = that.$store.state.district = result.districtList[0].districtList;
          });
        });
      } else {
        let list = that.$store.state.district;
        that.formatArray(list);
        that.option = list;
      }

      //定位出发地
      AMap.plugin('AMap.CitySearch', function() {
        var citySearch = new AMap.CitySearch()
        citySearch.getLocalCity(function(status, result) {
          if (status === 'complete' && result.info === 'OK') {
            console.log("location:", result.city);
            that.$store.state.departure = result.city;
          }
        })
      })
    },
    methods: {
      formatArray: function(target) { //格式化行政区查询结果
        let that = this;
        target.forEach(element => {
          if (
            element.districtList &&
            element.districtList.length != 0 &&
            element.districtList[0].level != "district"
          ) {
            that.formatArray(element.districtList);
          } else {
            element.districtList = null;
          }
          element.label = element.name;
          element.value = [element.name, element.center];
          element.children = element.districtList;
        });
      },
    },
    watch: {
      destination: function() {
        let city = this.destination[this.destination.length - 1];
        this.$store.state.city = city[0];
        this.$store.state.cityCenter = city[1];
        console.log('newDestination:', this.$store.state.city);
      },
      departure: function() {
        this.$store.state.departure = this.departure[this.departure.length - 1][0];
        console.log('newDeparture:', this.$store.state.departure);
      }
    },
  };
</script>
