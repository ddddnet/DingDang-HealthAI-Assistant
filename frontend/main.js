import App from './App'

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
	...App
})
app.$mount()
// #endif

// #ifdef VUE3
import {
	createSSRApp
} from 'vue'
export function createApp() {
	const app = createSSRApp(App)
	app.config.globalProperties.$host_api = 'https://ddddnet.xxxx.com';
	// 后端地址 后面不可以带斜杠 正确示范：https://baidu.com
	
	return {
		app
	}
}
// #endif