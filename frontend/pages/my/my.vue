<template>
<view class="codefun-flex-col page">
  <view class="codefun-flex-col codefun-self-stretch">
    <view class="codefun-flex-col codefun-self-stretch group">
      <view class="codefun-flex-col codefun-justify-start codefun-items-center codefun-self-stretch image-wrapper">
        <image class="codefun-shrink-0 image" src="/static/image/codefun/5bcb25c6e661a3e69c50dd1d9607e2bb.png" />
      </view>
      <image
        class="codefun-shrink-0 codefun-self-center image_2"
        src="/static/p.png"
      />
    </view>
    <text class="codefun-self-center font text">{{login_user_name}}</text>
    <text class="codefun-self-center text_2">id@{{login_user}}</text>
    <view class="codefun-flex-col codefun-self-stretch group_2">
      <view @click="gotoUserInfo()" class="codefun-flex-row codefun-justify-between codefun-items-center section">
        <view class="codefun-flex-row codefun-items-center">
          <image class="codefun-shrink-0 image_3" src="/static/image/codefun/14bdb29833c87169b417dd0c1910c059.png" />
          <text class="font ml-45">个人信息</text>
        </view>
        <image class="image_4" src="/static/image/codefun/77374c92022051cbecba4ecfd9b5c8f8.png" />
      </view>
      <view @click="deving()" class="codefun-flex-row codefun-justify-between codefun-items-center section_2 mt-9">
        <view class="codefun-flex-row codefun-items-center">
          <image class="codefun-shrink-0 image_5" src="/static/image/codefun/f050d18a3e6f27c25fb4316aee17f5d8.png" />
          <text class="codefun-ml-48 font text_3">账号设置</text>
        </view>
        <image class="image_4" src="/static/image/codefun/77374c92022051cbecba4ecfd9b5c8f8.png" />
      </view>
      <view @click="deving()" class="codefun-flex-row codefun-justify-between codefun-items-center section_3 mt-9">
        <view class="codefun-flex-row codefun-items-center">
          <image class="codefun-shrink-0 image_6" src="/static/image/codefun/7e218622a2e0a1d5374c579a3a387e05.png" />
          <text class="font text_4 ml-45">消息提醒</text>
        </view>
        <image class="image_4" src="/static/image/codefun/77374c92022051cbecba4ecfd9b5c8f8.png" />
      </view>
      <view @click="deving()" class="codefun-flex-row codefun-justify-between codefun-items-center section_3 mt-9">
        <view class="codefun-flex-row codefun-items-center">
          <image class="codefun-shrink-0 image_6" src="/static/image/codefun/7abf95300b3873eff62e7330faf8585e.png" />
          <text class="font text_5 ml-45">软件与帮助</text>
        </view>
        <image class="image_4" src="/static/image/codefun/77374c92022051cbecba4ecfd9b5c8f8.png" />
      </view>
      <view v-if="login_status" @click="logout()" class="codefun-flex-row codefun-justify-center codefun-items-center group_3 mt-9">
        <image class="image_6" src="/static/image/codefun/dcabc8a95ae886061b338d95cfcb48d5.png" />
        <text class="codefun-ml-22 font text_6">注销</text>
      </view>
	  <view v-if="!login_status" class="group_3 mt-9">
		  <navigator url="/pages/login/login">
			  <button type="default">去登录</button>
		  </navigator>
	  </view>
	  
    </view>
  </view>
  <text class="codefun-self-center text_7 mt-103">叮当网络@ddddnet.top</text>
</view>
</template>

<script>
	import whtMd5 from '@/uni_modules/wht-md5/js_sdk/wht-md5.js'
	export default {
		data() {
			return {
				login_user: "",
				login_status: false,
				infoDone: false,
				userInfo: {},
				systemInfo: {},
				deviceId: "",
				login_user_name: ""
			}
		},
		onLoad(option) {
			this.login_user = uni.getStorageSync("login_user")
			if (this.login_user) {
				this.login_status = true
				this.login_user_name = uni.getStorageSync("login_user_name")
				uni.setNavigationBarTitle({
					title:"@" + this.login_user_name
				})
				this.getUserInfo()
			}

		},
		methods: {
			deving(){
				uni.showToast({
					title:"开发中",
					icon:"none"
				})
			},
			
			logout() {
				try {
					uni.removeStorageSync("login_user")
					uni.reLaunch({
						url: "/pages/index/index"
					})
				} catch (e) {
					uni.showToast({
						title:"操作失败",
						icon:'fail'
					})
				}
			},
			
			gotoUserInfo(){
				uni.navigateTo({
					url:"/pages/my/my-info"
				})
			},
			
			getUserInfo() {

				uni.getSystemInfo({
					success: (res) => {
						const data = {
							uniPlatform: res.uniPlatform,
							deviceId: res.deviceId,
							osName: res.osName,
						};
						const jsonData = JSON.stringify(data);
						this.systemInfo = jsonData
						this.deviceId = res.deviceId
					},
					fail: (err) => {
					}
				})

				// let request_code = whtMd5( this.deviceId + this.login_user )
				let request_code = whtMd5("hello")

				uni.request({
					url: this.$host_api + "/getUserInfo",
					method: 'POST',
					data: {
						user: this.login_user,
						systemInfo: this.systemInfo,
						code: request_code
					},
					success: (res) => {
						if (res.data.code == 1) {
							this.userInfo = res.data.data;
							this.infoDone = true
						} else {
							uni.showToast({
								title: res.data.msg,
								icon: 'none'
							})
						}
					},
					fail: (err) => {
					}
				})
			},

			getActivityLevelText(level) {
				const activityLevelMap = [{
						value: 0,
						text: '久坐'
					},
					{
						value: 1,
						text: '轻度活动,每周进行轻微运动1-3天'
					},
					{
						value: 2,
						text: '中度活动,每周进行中等强度运动3-5天'
					},
					{
						value: 3,
						text: '高度活动,每周进行高强度运动6-7天'
					}
				];
				const matched = activityLevelMap.find(item => item.value === level);
				return matched ? matched.text : level.toString();
			}
		}
	}
</script>

<style scoped lang="css">
.mt-9 {
  margin-top: 15.77rpx;
}
.ml-45 {
  margin-left: 78.86rpx;
}
.mt-103 {
  margin-top: 180.49rpx;
}
.page {
  padding: 43.81rpx 42.06rpx 56.07rpx;
  background-color: #ffffff;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden;
  height: 100%;
}
.group {
  padding: 0 17.52rpx;
  height: 492.41rpx;
}
.image-wrapper {
  margin-right: 12.27rpx;
  border-radius: 29.79rpx;
  overflow: hidden;
  background-color: #ffc7de;
}
.image {
  opacity: 0.2;
  mix-blend-mode: LUMINOSITY;
  width: 616.82rpx;
  height: 411.8rpx;
}
.image_2 {
  margin-top: -122.66rpx;
  border-radius: 50.82rpx;
  width: 199.77rpx;
  height: 199.77rpx;
}
.text_2 {
  margin-top: 10.51rpx;
  color: #000000;
  font-size: 21.03rpx;
  font-family: Nunito;
  line-height: 18.15rpx;
}
.group_2 {
  margin-top: 45.56rpx;
  border-radius: 68.34rpx;
}
.section {
  margin-right: 35.05rpx;
  padding: 28.04rpx 17.52rpx;
  background-color: #ffffff;
  border-radius: 12.27rpx;
}
.image_3 {
  width: 38.55rpx;
  height: 35.05rpx;
}
.image_4 {
  width: 12.27rpx;
  height: 24.53rpx;
}
.section_2 {
  margin-right: 35.05rpx;
  padding: 28.04rpx 17.52rpx 28.04rpx 24.53rpx;
  background-color: #ffffff;
  border-radius: 12.27rpx;
}
.image_5 {
  width: 29.79rpx;
  height: 35.05rpx;
}
.section_3 {
  margin-right: 35.05rpx;
  padding: 24.53rpx 17.52rpx;
  background-color: #ffffff;
  border-radius: 12.27rpx;
}
.image_6 {
  width: 42.06rpx;
  height: 42.06rpx;
}
.group_3 {
  padding: 21.03rpx 0;
  border-radius: 12.27rpx;
  border-left: solid 1.75rpx #ffffff;
  border-right: solid 1.75rpx #ffffff;
  border-top: solid 1.75rpx #ffffff;
  border-bottom: solid 1.75rpx #ffffff;
}
.font {
  font-size: 24.53rpx;
  font-family: Nunito;
  line-height: 23.36rpx;
  font-weight: 700;
  color: #000000;
}
.text_5 {
  line-height: 23.25rpx;
}
.text_4 {
  line-height: 23.25rpx;
}
.text_3 {
  line-height: 22.25rpx;
}
.text {
  margin-top: 21.00rpx;
  font-size: 26.30rpx;
  line-height: 25.00rpx;
}
.text_6 {
  color: #89969f;
  line-height: 23.13rpx;
}
.text_7 {
  color: #000000;
  font-size: 21.03rpx;
  font-family: SourceHanSansCN;
  line-height: 22.75rpx;
}
</style>