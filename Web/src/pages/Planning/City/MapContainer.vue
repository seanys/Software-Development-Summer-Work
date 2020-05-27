<template>
  <div id="MapContainer">
    <div id="map"></div>
    <Searchbar @searchChecked="createInfoWindow"/>
  </div>
</template>

<script>
import Searchbar from "./SearchBar.vue";
export default {
  name: "MapContainer",
  components: {
    Searchbar
  },
  data() {
    return {
      /*地图对象*/
      map: {},
    };
  },
  created: function() {
    let that = this.$store.state.mapContainer=this;
    //更新指定节点的出行方案类型 itemIndex 指定节点的索引 type 出行类型
    this.$on("updateTransferPlan", function(itemIndex, type) {
      let m_From =
        that.$store.state.points[that.$store.state.nowDay][itemIndex - 1].detail
          .location;
      let m_To =
        that.$store.state.points[that.$store.state.nowDay][itemIndex].detail
          .location;
      that.createTransferObj(m_From, m_To, type).then(newTransfer => {
        that.$store.commit({
          type: "updateTransferPlan",
          newTransfer: newTransfer,
          index: itemIndex,
        });
      });
    });

    //删除卡片并更新出行方案
    this.$on("updateTransferPlanWhenDeleteCard", function(itemIndex, type) {
      let m_From =
        that.$store.state.points[that.$store.state.nowDay][itemIndex - 1].detail
          .location;
      let m_To =
        that.$store.state.points[that.$store.state.nowDay][itemIndex + 1].detail
          .location;
      that.createTransferObj(m_From, m_To, type).then(newTransfer => {
        that.$store.commit({
          type: "updateTransferPlanWhenDeleteCard",
          newTransfer: newTransfer,
          index: itemIndex+1,
        });
      });
    });

    //修改出行计划索引
    this.$on("updateTransferIndex", function(itemIndex, transferIndex) {
      that.updateTransferIndex(itemIndex, transferIndex);
    });
    //移动地图到指定点
    this.$on("setCenter", function(index) {
      let position = that.$store.state.points[that.$store.state.nowDay][
        index
      ].marker.getPosition();
      that.map.panTo(position);
    });
    //导入景点
    this.$on("importData", function() {
      that.$store.commit("switchDay", 0);
      that.importData();
    });
    //更新城市
    this.$on("setNewCity", function(city) {
      that.setNewCity(city);
    });
  },
  mounted: function() {
    //创建地图
    let map = new AMap.Map("map", {
      resizeEnable: true,
      zoom: 12,
      mapStyle: "amap://styles/fe7d1f157e05c97d6930995928e4f39d"
    });
    this.$store.state.mapContainer=this;
    this.map = map;
    this.setNewCity(this.$store.state.city);
    console.log('Map created.',map.getContainer());
    //初始化地点搜索插件
    let searchConfig = this.$store.state.AMap_PlaceSearch.config;
    let search = new AMap.PlaceSearch(searchConfig);
    this.$store.commit("setPlaceSearch", {
      config: searchConfig,
      search: search
    });

    //绑定热点单击事件
    let that = this;
    map.on("hotspotclick", function(event) {
      that.createInfoWindow(event);
    });
  },
  methods: {
    //设置城市
    setNewCity:function(city){
      this.map.setCity(city);
    },
    //导入景点
    importData:function(){
    let that = this;
    if (this.$store.state.storge) {
      let src = this.$store.state.storge;
      let searchTool = new AMap.PlaceSearch({
        city: src.city,
        extensions: 'all'
      });
      function importNode(local_node, pre_node, search_tool) {
        return new Promise((resolve, reject) => {
          let node = {};
          node.id = local_node.id;
          search_tool.getDetails(local_node.id, function(status, result) {
            node.detail = result.poiList.pois[0];
            /*create Marker */
            let marker = new AMap.Marker({
              map: that.map,
              position: node.detail.location,
              animation: "AMAP_ANIMATION_DROP",
              title: node.detail.name
            });
            marker.show();
            node.marker = marker;
            /*create transfer */
            if (local_node.transfer && pre_node) {
              let poiFrom = pre_node.detail.location;
              that
                .createTransferObj(
                  poiFrom,
                  node.detail.location,
                  local_node.transfer.type
                )
                .then(result => {
                  node.transfer = result;
                  resolve(node);
                });
            } else {
              node.transfer = null;
              resolve(node);
            }
          });
        });
      }

      (async function() {
        for (let i = 0; i < src.points.length; i++) {
          for (let j = 0; j < src.points[i].length; j++) {
            let poi_node = await importNode(
              src.points[i][j],
              j == 0 ? null : that.$store.state.points[i][j - 1],
              searchTool
            );
            //console.log(poi_node);
            await that.$store.dispatch({
              type: "addPointFromMap",
              data: poi_node,
              dayTo: i
            });
            if (src.points[i][j].transfer && src.points[i][j].transfer.index != 0) {
              let idx = src.points[i][j].transfer.index;
              that.updateTransferIndex(j, idx);
            }
          }
          if (i != src.points.length - 1) that.$store.commit("switchDay", i + 1);
        }
        that.$store.commit("switchDay", 0);
      })();
    }
    /*end 导入 */
    },
    //创建点击热点信息窗体 event:点击地图触发的事件对象
    createInfoWindow: function(event) {
      let infoDiv = document.createElement("div");
      let InfoWindowDemo =
        '<div id="infoWindow">\
        <span class="infoName">' +
        event.name +
        '</span>\
        <span id="infoAction">\
          <i class="el-icon-plus"></i>\
        </span>\
      </div>\
      <div id="infoWindowArrow">\
        <div></div>\
      </div>';

      infoDiv.innerHTML += InfoWindowDemo;
      //绑定点击加号的事件
      let that = this;
      infoDiv.querySelector("#infoAction").onclick = function(e) {
        that.addPointToData(event);
      };

      let infoWindow = new AMap.InfoWindow({
        isCustom: true, //使用自定义窗体
        content: infoDiv,
        offset: new AMap.Pixel(0, -10),
        closeWhenClickMap: true,
        autoMove: true
      });
      infoWindow.open(this.map, event.lnglat);
    },
    /**
     * @description 根据type将result的路径画出
     * @param {object} result 搜索结果
     * @param {string} type 搜索类型
     * @param {number} index 方案索引
     * @return {array} routes 绘制了路线的数组
     */
    drawResultOnMap(result, index, type) {
      let that = this;
      let routes = [];
      if (type === "driving") {
        //driving plan
        let routesPoints = [];
        for (let t = 0; t < result.routes[index].steps.length; t++) {
          //遍历子路段
          for (let i = 0; i < result.routes[index].steps[t].path.length; i++) {
            //遍历路段坐标
            routesPoints.push(result.routes[index].steps[t].path[i]);
          }
        }
        let _route = new AMap.Polyline({
          map: that.map,
          isOutline: true,
          outlineColor: "#FFFFFF",
          strokeWeight: 5,
          strokeColor: "#4682B4",//钢蓝
          showDir: true,
          lineJoin: "round",
          path: routesPoints
        });
        routes.push(_route);
        return routes;
      } else if (type === "bus") {
        //bus plan
        let plan = result.plans[index];
        for (let i = 0; i < plan.segments.length; i++) {
          let seg_type = plan.segments[i].transit_mode;
          let _route = new AMap.Polyline({
            map: that.map,
            isOutline: true,
            outlineColor: "#FFFFFF",
            strokeWeight: 5,
            strokeColor:
              seg_type == "BUS"
                ? "#21a265"
                : seg_type == "SUBWAY" ? "#9370DB" : "#fed71a",
            showDir: true,
            lineJoin: "round",
            path: plan.segments[i].transit.path
          });
          routes.push(_route);
        }
        return routes;
      } else if (type === "ride") {
        let plan = result.routes[index];
        let routesPoints = [];
        for (let i = 0; i < plan.rides.length; i++) {
          for (let j = 0; j < plan.rides[i].path.length; j++) {
            routesPoints.push(plan.rides[i].path[j]);
          }
        }
        let _route = new AMap.Polyline({
          map: that.map,
          isOutline: true,
          outlineColor: "#FFFFFF",
          strokeWeight: 5,
          strokeColor: "#21a265",
          showDir: true,
          lineJoin: "round",
          path: routesPoints
        });
        routes.push(_route);
        return routes;
      } else if (type === "walk") {
        let plan = result.routes[index];
        let routesPoints = [];
        for (let i = 0; i < plan.steps.length; i++) {
          for (let j = 0; j < plan.steps[i].path.length; j++) {
            routesPoints.push(plan.steps[i].path[j]);
          }
        }
        let _route = new AMap.Polyline({
          map: that.map,
          isOutline: true,
          outlineColor: "#FFFFFF",
          strokeWeight: 5,
          strokeColor: "#fed71a",
          showDir: true,
          lineJoin: "round",
          path: routesPoints
        });
        routes.push(_route);
        return routes;
      }
    },
    /**
     * @description 生成路径规划结果
     * @param {object} poiFrom 高德lnglat对象
     * @param {object} poiTo 高德lnglat对象
     * @param {string} type 路径规划类别
     * @return {object} transfer对象
     */
    createTransferObj: function(poiFrom, poiTo, type) {
      let that = this;
      return new Promise(function(resolve, reject) {
        let transfer = {
          type: "",
          index: 0,
          kit: {},
          plan: {},
          routes: {}
        };
        if (type === "driving") {
          //Driving plan
          transfer.type = "driving";
          let kit = new AMap.Driving(that.$store.state.AMap_Driving);
          transfer.kit = kit;
          kit.search(poiFrom, poiTo, function(statue, result) {
            if (statue == "complete") {
              transfer.plan = result;
              transfer.routes = that.drawResultOnMap(result, 0, "driving"); //draw result
              resolve(transfer); //resolve result
            } else {
              console.log(result);
              reject();
            }
          });
        } else if (type === "bus") {
          //bus plan
          transfer.type = "bus";
          let kit = new AMap.Transfer(that.$store.state.AMap_Bus);
          transfer.kit = kit;
          kit.search(poiFrom, poiTo, function(statue, result) {
            //console.log(result);
            //console.log(statue);
            if (statue == "complete" && result.info!='NO_DATA') {
              transfer.plan = result;
              transfer.routes = that.drawResultOnMap(result, 0, "bus");
              resolve(transfer);
            } else {
              //reject(result);
              //若无公交线路则转入自驾规划
              //Driving plan
              transfer.type = "driving";
              let kit = new AMap.Driving(that.$store.state.AMap_Driving);
              transfer.kit = kit;
              kit.search(poiFrom, poiTo, function(statue, result) {
                if (statue == "complete" && result.info!='NO_DATA') {
                  transfer.plan = result;
                  transfer.routes = that.drawResultOnMap(result, 0, "driving"); //draw result
                  resolve(transfer); //resolve result
                } else {
                  //reject(result);
                  //若既无公交也无自驾（比如距离太近）则转入步行
                  transfer.type = "walk";
                  let kit = new AMap.Walking(that.$store.state.AMap_Walk);
                  transfer.kit = kit;
                  kit.search(poiFrom, poiTo, function(statue, result) {
                    if (statue == "complete") {
                      transfer.plan = result;
                      transfer.routes = that.drawResultOnMap(result, 0, "walk");
                      resolve(transfer);
                    } else reject(result);
                  });
                }
              });
            }
          });
        } else if (type === "ride") {
          transfer.type = "ride";
          let kit = new AMap.Riding(that.$store.state.AMap_Ride);
          transfer.kit = kit;
          kit.search(poiFrom, poiTo, function(statue, result) {
            if (statue == "complete") {
              transfer.plan = result;
              transfer.routes = that.drawResultOnMap(result, 0, "ride");
              resolve(transfer);
            } else {
              reject(result);
            }
          });
        } else if (type === "walk") {
          transfer.type = "walk";
          let kit = new AMap.Walking(that.$store.state.AMap_Walk);
          transfer.kit = kit;
          kit.search(poiFrom, poiTo, function(statue, result) {
            if (statue == "complete") {
              transfer.plan = result;
              transfer.routes = that.drawResultOnMap(result, 0, "walk");
              resolve(transfer);
            } else reject(result);
          });
        } else {
        }
      });
    },
    /**
     * @description 增加景点到总列表
     * @param {object} event 事件obj
     */
    addPointToData: function(event) {
      //20190716更新：检测景点是否当天已存在
      let pois = this.$store.state.points[this.$store.state.nowDay];
      for (let i = 0; i < pois.length; i++) {
          if (pois[i].id == event.id) return; //存在
      }

      let that = this;
      //生成标记
      let marker = new AMap.Marker({
        map: that.map,
        position: event.lnglat,
        animation: "AMAP_ANIMATION_DROP",
        title: event.name
      });
      marker.show();

      //生成路线
      let curPoints = this.$store.state.points[this.$store.state.nowDay];//当天景点列表
      let payload = {
        id: event.id,
        marker: marker,
        transfer: null
      };
      if (curPoints.length > 0) {
        //若存在之前节点，计算路径
        //trsts:前一节点到当前节点的规划对象
        this.createTransferObj(
          curPoints[curPoints.length - 1].detail.location,
          event.lnglat,
          that.$store.state.travelType
        )
          .then(result => {
            console.log(result);
            payload.transfer = result;
            that.$store.dispatch({
              type: "addPointFromMap",
              data: payload
            });
          })
          .catch(error => {
            console.log(error);
          });
      } else {
        //提交至Vuex
        that.$store.dispatch({
          type: "addPointFromMap",
          data: payload
        });
      }
    },
    updateTransferIndex:function(itemIndex, transferIndex){
      let that = this;
      let result =
        that.$store.state.points[that.$store.state.nowDay][itemIndex].transfer;
      let newRoutes = that.drawResultOnMap(
        result.plan,
        transferIndex,
        result.type
      );
      that.$store.commit({
        type: "updateTransferIndex",
        newRoutes: newRoutes,
        index: itemIndex,
        transferIndex: transferIndex
      });
    }
  },
  computed: {
    destination:function(){
      return this.$store.state.destination;
    }
  },
  watch: {
    destination:function(newCity){
      this.setNewCity(newCity);
    }
  }
};
</script>

<style>
#Mapcontainer {
  position: relative;
}
#map {
  height: 100%;
  width: 100%;
}

#infoWindow {
  height: 1rem;
  padding: 0.5rem;
  padding-right: 0;
  border-radius: 5px;
  border: #1a6840 2px solid;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.25);
  background-color: white;
  display: flex;
  align-items: center;
}
.infoName {
  padding: 0 1rem;
  text-align: center;
}
#infoAction {
  height: 2rem;
  width: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #1a6840;
  transition: all 0.2s ease;
}
#infoAction:hover {
  background-color: #1a6840;
}
#infoAction > i {
  color: white;
}
#infoWindowArrow > div {
  width: 0;
  height: 0;
  margin: 0 auto;
  border-top: 5px solid #207f4c;
  border-right: 40px solid transparent;
  border-left: 40px solid transparent;
}

#Searchbar {
  position: absolute;
  left: 20px;
  top: 20px;
  z-index: 1000;
}
</style>
