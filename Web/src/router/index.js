import Vue from 'vue'
import Router from 'vue-router'
import User from '@/pages/User'
import Community from '@/pages/Community'
import Travel from '@/pages/Travel'
import Planning from '@/pages/Planning'
import Recommend from '@/pages/Recommend'
import Article from '@/pages/Article'
import History from '@/pages/User/History'
import Star from '@/pages/User/Star'
import Setting from '@/pages/User/Setting'
import City from '@/pages/Planning/City'
import PlanByDay from '@/pages/Planning/City/PlanByDay'
import Route from '@/pages/Planning/Route'
import Comprehensive from '@/pages/Planning/Comprehensive'
import PlanView from '@/pages/PlanView'
import Login from '@/pages/Login'
import Register from '@/pages/Register'
import Publish from '@/pages/Publish'

Vue.use(Router)
export default new Router({
    routes: [{
            path: '/',
            name: 'Travel',
            component: Travel
        },
        {
            path: '/travel',
            name: 'Travel',
            component: Travel
        },
        {
            path: '/planning',
            name: 'Planning',
            component: Planning,
            children: [{
                    path: '/',
                    component: Route
                },
                {
                    path: 'route',
                    component: Route
                },
                {
                    path: 'city',
                    component: City,
                    children: [{
                        path: '/',
                        component: PlanByDay,
                        meta: {
                            keepAlive: true
                        }
                    }]
                },
                {
                    path: 'comprehensive',
                    component: Comprehensive
                },
            ]
        },
        {
            path: '/user',
            name: 'User',
            component: User,
            children: [{
                    path: '/',
                    component: Star
                },
                {
                    path: 'star',
                    component: Star
                },
                {
                    path: 'setting',
                    component: Setting
                },
                {
                    path: 'history',
                    component: History
                }
            ]
        },
        {
            path: '/article',
            name: 'Article',
            component: Article
        },
        {
            path: '/community',
            name: 'Community',
            component: Community
        },
        {
            path: '/publish',
            name: 'Publish',
            component: Publish
        },
        {
            path: '/recommend',
            name: 'Recommend',
            component: Recommend
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
        },
        {
            path: '/register',
            name: 'Register',
            component: Register,
        },
        {
            path: '/planview',
            component: PlanView
        },
        {
            path: '/test',
            redirect: '/' //test为所放置的文件夹名称，不修改的话可能会无法显示页面
        }
    ],
})