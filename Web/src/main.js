// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from "vuex";
import App from './App'
import router from './router'
import Element from 'element-ui'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)
Vue.use(Element)
Vue.use(Vuex)

Vue.config.productionTip = false
axios.defaults.headers.post['Content-Type'] =
    'application / x - www - form - urlencoded '

const store = new Vuex.Store({
    state: {
        data: [],
        city: '',
        cityCenter: { 'O': '117.28304200000002', 'P': '31.86119' },
        departure: '',
        totalDays: 0,
        nowDay: 0,
        points: [], //按天规划中的地点
        transport: [], //交通方案
        accommodation: [], //住宿方案
        mapContainer: null,
        travelType: 'bus',
        storge: '',
        //地点搜索
        AMap_PlaceSearch: {
            config: {
                city: '全国',
                extensions: 'all'
            },
            search: {}
        },
        //驾车规划
        AMap_Driving: {
            policy: AMap.DrivingPolicy.LEAST_TIME,
            hideMarkers: true,
            autoFitView: false,
            showTraffic: false
        },
        //公交规划
        AMap_Bus: {
            city: '全国',
            hideMarkers: true,
            autoFitView: false
        },
        AMap_Walk: {
            hideMarkers: true,
            autoFitView: false
        },
    },
    mutations: {
        //添加新的一天
        addNewDay(state) {
            state.totalDays++;
            //state.nowDay=state.totalDays-1;
            state.points.push([]);
        },
        setdata(state, data) {
            state.data = data
        },
        //设置PlaceSearch插件 target:插件对象
        setPlaceSearch(state, target) {
            state.AMap_PlaceSearch.config = target.config;
            state.AMap_PlaceSearch.search = target.search;
        },
        //切换天数到第D天（数组编号）
        switchDay(state, d) {
            if (d < state.totalDays && d >= 0) {
                let nowP = state.points[state.nowDay];
                for (var i = 0; i < nowP.length; i++) {
                    nowP[i].marker.hide(); //hide marker
                    if (nowP[i].transfer) {
                        for (let z = 0; z < nowP[i].transfer.routes.length; z++) {
                            nowP[i].transfer.routes[z].hide(); //hide path
                        }
                    }
                }
                let newP = state.points[d];
                for (var j = 0; j < newP.length; j++) {
                    newP[j].marker.show(); //show marker
                    if (newP[j].transfer) {
                        for (let z = 0; z < newP[j].transfer.routes.length; z++) {
                            newP[j].transfer.routes[z].show(); //show path
                        }
                    }
                }
                state.nowDay = d;
            }

        },
        //删除第D天（数组编号）待测试
        deleteDay(state, d) {
            if (d < state.totalDays && d >= 0) {
                for (let t = 0; t < state.points[d].length; t++) {
                    state.points[d][t].marker.hide(); //hide markers
                    if (state.points[d][t].transfer)
                        for (let z = 0; z < state.points[d][t].transfer.routes.length; z++) {
                            state.points[d][t].transfer.routes[z].hide(); //hide path
                        }
                }
                state.points.splice(d, 1);
                state.totalDays--;
            }
            if (state.nowDay >= d) {
                if (state.nowDay > 0) state.nowDay--;
            }
        },
        /**
         * @description 添加景点到数据集
         * @param {object} payload
         * @param {object} payload.data 数据
         * @param {number} payload.dayTo 可选，添加到的天
         */
        addPointFromMap(state, payload) {
            if (!payload.dayTo) {
                state.points[state.nowDay].push(payload.data);
            } else state.points[payload.dayTo].push(payload.data); 
        },
        /**
         * @description 更新出行方案，替换整个transfer对象
         * @param {object} payload
         * @param {number} payload.index point当日索引
         * @param {object} payload.newTransfer point新transfer
         */
        updateTransferPlan: function(state, payload) {
            if (state.points[state.nowDay][payload.index].transfer) {
                let route = state.points[state.nowDay][payload.index].transfer.routes;
                for (let i = 0; i < route.length; i++) {
                    route[i].hide();
                }
            }
            state.points[state.nowDay][payload.index].transfer = payload.newTransfer;
        },
        //删除卡片并更新方案
        updateTransferPlanWhenDeleteCard: function(state, payload) {
            if (state.points[state.nowDay][payload.index].transfer) {
                let route = state.points[state.nowDay][payload.index].transfer.routes;
                for (let i = 0; i < route.length; i++) {
                    route[i].hide();
                }
                route = state.points[state.nowDay][payload.index - 1].transfer.routes;
                for (let i = 0; i < route.length; i++) {
                    route[i].hide();
                }
            }
            state.points[state.nowDay][payload.index].transfer = payload.newTransfer;
            //删除卡片
            state.points[state.nowDay][payload.index - 1].marker.hide();
            state.points[state.nowDay].splice(payload.index - 1, 1);
        },
        //删除头尾卡片并更新方案
        updateTransferPlan_Special: function(state, index) {
            if (index == state.points[state.nowDay].length - 1) {
                if (state.points[state.nowDay][index].transfer) {
                    let route = state.points[state.nowDay][index].transfer.routes;
                    for (let i = 0; i < route.length; i++) {
                        route[i].hide();
                    }
                }
            } else {
                if (state.points[state.nowDay][index + 1].transfer) {
                    let route = state.points[state.nowDay][index + 1].transfer.routes;
                    for (let i = 0; i < route.length; i++) {
                        route[i].hide();
                    }
                }
            }
            //删除卡片
            state.points[state.nowDay][index].marker.hide();
            state.points[state.nowDay].splice(index, 1);
        },
        /**
         * @description 更新出行方案索引
         * @param {object} payload
         * @param {number} payload.index point当日索引
         * @param {object} payload.newRoutes point新的transfer.routes
         * @param {number} payload.transferIndex point出行方案索引
         */
        updateTransferIndex: function(state, payload) {
            if (state.points[state.nowDay][payload.index].transfer) {
                let route = state.points[state.nowDay][payload.index].transfer.routes;
                for (let i = 0; i < route.length; i++) {
                    route[i].hide();
                }
            }
            let item = state.points[state.nowDay][payload.index];
            state.points[state.nowDay][payload.index].transfer.routes = payload.newRoutes;
            state.points[state.nowDay][payload.index].transfer.index = payload.transferIndex;
        },
        /**
         * @description 当天内移动节点顺序 待测试
         * @param {object} payload
         * @param {number} payload.oldIndex 节点旧索引
         * @param {number} payload.newIndex 节点新索引
         */
        sortItem: function(state, payload) {
            let nowDay = state.points[state.nowDay];
            nowDay.splice(payload.newIndex, 0, nowDay.splice(payload.oldIndex, 1)[0]);
        },
        deletePlan: function(state, plan) {
            for (let i = 0; i < state.transport.length; i++) {
                if (state.transport[i] == plan) {
                    state.transport.splice(i, 1);
                }
            }
        },
        deleteHotel: function(state, hotel) {
            for (let i = 0; i < state.accommodation.length; i++) {
                if (state.accommodation[i] == hotel) {
                    state.accommodation.splice(i, 1);
                }
            }
        }
    },
    actions: {
        addPointFromMap(context, payload) {
            return new Promise(function(resolve, reject) {
                if (!payload.data.detail) { //no detail
                    context.state.AMap_PlaceSearch.search.getDetails(payload.data.id, function(
                        status,
                        result
                    ) {
                        if (status == "complete") {
                            console.log(result);
                            payload.data.detail = result.poiList.pois[0];
                            context.commit("addPointFromMap", payload);
                        } else {
                            console.log(result);
                            context.commit("addPointFromMap", payload);
                        }
                        resolve();
                    });
                } else { //already exist data
                    context.commit("addPointFromMap", payload);
                    resolve();
                }
            });
        },
    },
    getters: {
        exportData: state => {
            let data = {};
            data.city = state.city;
            data.totalDays = state.totalDays;
            data.points = state.points;
            let ar = [];
            for (let i = 0; i < state.totalDays; i++) {
                ar.push([]);
                for (let j = 0; j < state.points[i].length; j++) {
                    let poi = state.points[i][j];
                    ar[i].push({
                        id: poi.detail.id,
                        transfer: poi.transfer ? {
                            type: poi.transfer.type,
                            index: poi.transfer.index
                        } : null
                    });
                }
            }
            data.points = ar;
            return data;
        }
    }
});

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    components: { App },
    template: '<App/>'
});