<template>
	<view>
		<view v-if="login_status">
			<uni-section v-if="infoDone" class="mbox-2" title="个人信息" type="line">
				<uni-list>
					<uni-list-item title="名字" :rightText="userInfo.name" />
					<uni-list-item title="性别" :rightText="userInfo.gender" />
					<uni-list-item title="年龄" :rightText="userInfo.age.toString()" />
					<uni-list-item title="身高" :rightText="userInfo.height.toString()" note="cm" />
					<uni-list-item title="体重" :rightText="userInfo.weight.toString()" note="kg" />
					<uni-list-item title="活动频率" :rightText="getActivityLevelText(userInfo.activity_level)" />
					<uni-list-item title="BMR" :rightText="userInfo.bmr.toString()" note="基础代谢率" />
					<uni-list-item title="PAL" :rightText="userInfo.pal.toString()" note="身体活动水平" />
					<uni-list-item title="TDEE" :rightText="userInfo.tdee.toString()" note="总能量消耗" />
					<uni-list-item title="信息记录时间" :rightText="userInfo.time" />
				</uni-list>
			</uni-section>

			<wd-skeleton v-else class="mbox-2" theme="paragraph" />

			<view class="mbox-2">
				<navigator url="/pages/my/my-info-form">
					<wd-button block size="large" >修改个人信息</wd-button>
				</navigator>
			</view>
			<!-- <view class="mbox-2">
				<wd-button @click="logout()" block plain size="large" type="info" >注销账户</wd-button>
			</view> -->
		</view>
		<!-- 未登录 -->
		<view v-else class="mbox-2">
			<wd-status-tip image="content" tip="尚未登录" />
			<navigator url="/pages/login/login">
				<button type="default" class="mt-5" >去登录</button>
			</navigator>
		</view>

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
				deviceId: ""
			}
		},
		onLoad(option) {
			this.login_user = uni.getStorageSync("login_user")
			if (this.login_user) {
				this.login_status = true
				this.getUserInfo()
			}

		},
		methods: {
			
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
							uni.setNavigationBarTitle({
								title:res.data.data.name + "的个人信息"
							})
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

<style>

</style>