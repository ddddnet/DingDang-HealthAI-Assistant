<template>
	<view class="codefun-flex-col page">
		<image class="image" src="../../static/image/codefun/25be226c485623fe87e11de9de7a0404.png" />
		<view class="codefun-flex-col section codefun-mt-46">
			<text class="codefun-self-center text">一键登录</text>
			<view class="codefun-flex-row codefun-items-center codefun-self-stretch section_2">
				<image class="image_2" src="../../static/image/codefun/6039fbbe2a8f7e8d52172560f867aa6b.png" />
				<input class="ml-19" placeholder="手机号码" @input="inputPhoneNumber" />
			</view>
			<view class="codefun-flex-col codefun-self-stretch group">
				<view class="codefun-flex-row codefun-justify-between codefun-self-stretch section_3">
					<view class="codefun-flex-row codefun-items-center">
						<image class="codefun-shrink-0 image_3"
							src="../../static/image/codefun/573ef06b1f3d412b797e59fc433bab74.png" />
						<input class="ml-21" placeholder="密码" :password="showPassword" @input="inputPassword" />
					</view>
					<text class="image_2" :class="[!showPassword ? 'uni-eye-active' : '']"
						@click="changePassword">👀</text>
				</view>
				<text class="codefun-self-end font_2 text_3 mt-19" @click="resetPassword()">忘记密码</text>
			</view>
			
			<view class="codefun-flex-col codefun-self-stretch group_2">
				<view @click="login()"
					class="codefun-flex-col codefun-justify-start codefun-items-center codefun-self-stretch view">
					<text class="text_4">一键登录</text>
				</view>
				<!-- #ifdef MP-TOUTIAO -->
				<view @click="Dylogin()"
					class="mt-5 codefun-flex-col codefun-justify-start codefun-items-center codefun-self-stretch view">
					<text class="text_4">抖音登录</text>
				</view>
				<!-- #endif -->
				<text @click="noLogin()" class="codefun-self-center font_2 text_5 mt-25">游客体验</text>
			</view>

			<view class="codefun-flex-row codefun-items-center codefun-self-stretch group_3">
				<wd-checkbox v-model="checkboxValue" shape="square" @change="handleCheckboxChange"></wd-checkbox>
				<view class="group_5 codefun-ml-8">
					<text class="font_2 text_6">我已阅读并同意</text>
					<text class="font_3" @click="goto_contra('user')">《用户协议》</text>
					<text class="font_2 text_7">和</text>
					<text class="font_3 text_8" @click="goto_contra('private')">《隐私政策》</text>
				</view>
			</view>
			
		</view>
	</view>
</template>

<script>
	export default {
		components: {},
		props: {},
		data() {
			return {
				showPassword: true,
				phoneNumber: '',
				password: '',
				checkboxValue: false,
				aggre:false,
				systemInfo: {}
			};
		},
		onLoad() {
			let logined = uni.getStorageSync("login_user")
			if (logined) {
				uni.reLaunch({
					url: "/pages/home/home"
				})
			}
			uni.getSystemInfo({
				success: (res) => {
					const data = {
						uniPlatform: res.uniPlatform,
						deviceId: res.deviceId,
						osName: res.osName,
					};
					const jsonData = JSON.stringify(data);
					this.systemInfo = jsonData
				},
				fail: (err) => {
				}
			})
		},
		methods: {
			goto_contra(type) {
				if (type == "user") {
					uni.navigateTo({
						url: "/pages/webview/webview?url=" + this.$host_api + "/contract/user"
					})
				} else if (type == "private") {
					uni.navigateTo({
						url: "/pages/webview/webview?url=" + this.$host_api + "/contract/private"
					})
				}
			},
			noLogin() {
				uni.reLaunch({
					url: "/pages/home/home"
				})
			},
			inputPhoneNumber: function(e) {
				this.phoneNumber = e.detail.value;
			},
			inputPassword: function(e) {
				this.password = e.detail.value;
			},
			changePassword: function() {
				this.showPassword = !this.showPassword;
			},
			handleCheckboxChange(e) {
				this.checkboxValue = e.detail.value;
			},
			resetPassword() {
				
				uni.showModal({
					title: '请联系工作人员',
					content: "微信：zxxxcoach",
					confirmText: "复制",
					success: (e) => {
						if (e.confirm) {
							uni.setClipboardData({
								data: "zxxxcoach",
								success: (e) => {
									uni.showToast({
										title: "已复制到剪切板",
										icon: "success",
									});
								},
								fail: (err) => {
									console.error("复制到剪切板失败:", err);
									uni.showToast({
										title: "复制失败，请稍后再试",
										icon: "none",
									});
								}
							})
						}
					}
				})
			},
			login_success(res) {

				if (res.msg == "注册成功") {
					try {
						let user = res.user
						uni.setStorageSync("login_user", user);
						uni.showToast({
							title: res.msg + '\n' + user
						})
						uni.reLaunch({
							url: "/pages/my/my-info-form"
						})
					} catch (error) {
						//TODO handle the exception
						uni.showToast({
							title: '程序错误' + error
						})
					}

				} else {
					try {
						let user = res.user
						let name = res.name
						uni.setStorageSync("login_user", user);
						uni.setStorageSync("login_user_name", name);
						uni.showToast({
							title: res.msg + '\n' + user
						})
						uni.reLaunch({
							url: "/pages/home/home?page_user=" + user
						})
					} catch (error) {
						//TODO handle the exception
						uni.showToast({
							title: '程序错误' + error
						})
					}
				}
			},
			login() {
				
				if (this.checkboxValue == false) {
					uni.showToast({
						title: "请阅读并同意\n《用户协议》\n《隐私政策》",
						icon: 'error'
					})
					return
				}
				
				if (this.phoneNumber == "") {
					uni.showToast({
						title: "请输入手机号码",
						icon: 'error'
					})
					return
				}
				if (this.password == "") {
					uni.showToast({
						title: "请输入密码",
						icon: 'error'
					})
					return
				}
				let system_data = JSON.stringify(this.systemInfo)
				uni.request({
					url: this.$host_api + "/login",
					method: 'POST',
					data: {
						"user": this.phoneNumber,
						"password": this.password,
						"systemInfo": system_data
					},
					success: (res) => {

						if (res.statusCode == 200) {
							if (res.data.code == 1) {
								//账户没问题
								this.login_success(res.data)
							} else if (res.data.code == 0) {
								uni.showToast({
									title: res.data.msg,
									icon: 'error'
								})
								return
							} else {
								uni.showToast({
									title: "服务器错误",
									icon: 'error'
								})
								return
							}
						} else {
							uni.showToast({
								title: "服务器或程序错误",
								icon: 'error'
							})
							return
						}

					},
					fail: (err) => {
						uni.showToast({
							title: "程序错误",
							icon: 'error'
						})
					}
				})
			},
			Dylogin() {
				
				
				if (this.phoneNumber == "") {
					uni.showToast({
						title: "请输入手机号码",
						icon: 'error'
					})
					return
				}
				if (this.password == "") {
					uni.showToast({
						title: "请输入密码",
						icon: 'error'
					})
					return
				}
				let system_data = JSON.stringify(this.systemInfo)
				uni.request({
					url: this.$host_api + "/login",
					method: 'POST',
					data: {
						"user": this.phoneNumber,
						"password": this.password,
						"systemInfo": system_data
					},
					success: (res) => {
			
						if (res.statusCode == 200) {
							if (res.data.code == 1) {
								//账户没问题
								this.login_success(res.data)
							} else if (res.data.code == 0) {
								uni.showToast({
									title: res.data.msg,
									icon: 'error'
								})
								return
							} else {
								uni.showToast({
									title: "服务器错误",
									icon: 'error'
								})
								return
							}
						} else {
							uni.showToast({
								title: "服务器或程序错误",
								icon: 'error'
							})
							return
						}
			
					},
					fail: (err) => {
						uni.showToast({
							title: "程序错误",
							icon: 'error'
						})
					}
				})
			}
		},
	};
</script>

<style scoped lang="css">
	.ml-19 {
		margin-left: 36.54rpx;
	}

	.ml-21 {
		margin-left: 40.38rpx;
	}

	.mt-19 {
		margin-top: 36.54rpx;
	}

	.mt-25 {
		margin-top: 48.08rpx;
	}

	.page {
		padding-top: 151.92rpx;
		background-color: #5cbee8;
		width: 100%;
		overflow-y: auto;
		overflow-x: hidden;
		height: 100%;
	}

	.image {
		width: 100vw;
		height: 58.2051vw;
	}

	.section {
		padding: 53.27rpx 61.73rpx 120.19rpx 61.73rpx;
		background-color: #ffffff;
		border-radius: 69.23rpx 69.23rpx 0rpx 0rpx;
	}

	.text {
		color: #383838;
		font-size: 46.15rpx;
		font-family: HarmonyOSSansSC;
		line-height: 43.48rpx;
	}

	.section_2 {
		margin-top: 78.25rpx;
		padding: 25rpx 38.87rpx;
		background-color: #f2f2f2;
		border-radius: 115.38rpx;
	}

	.image_2 {
		opacity: 0.8;
		width: 50rpx;
		height: 42.31rpx;
	}

	.group {
		margin-top: 46.15rpx;
	}

	.section_3 {
		padding: 25rpx 43.38rpx;
		background-color: #f2f2f2;
		border-radius: 115.38rpx;
	}

	.image_3 {
		width: 41.25rpx;
		height: 38.79rpx;
	}

	.font_2 {
		font-size: 23.08rpx;
		font-family: HarmonyOSSansSC;
		line-height: 21.9rpx;
		color: #808080;
	}

	.text_3 {
		margin-right: 57.21rpx;
		color: #33333366;
		font-size: 25rpx;
		line-height: 23.08rpx;
	}

	.group_2 {
		margin-top: 98.08rpx;
	}

	.view {
		padding: 26.15rpx 0 31.04rpx;
		background-color: #30a0fc;
		border-radius: 115.38rpx;
	}

	.text_4 {
		color: #ffffff;
		font-size: 38.46rpx;
		font-family: HarmonyOSSansSC;
		line-height: 35.12rpx;
	}

	.text_5 {
		color: #30a0fc;
		line-height: 21.58rpx;
	}

	.group_3 {
		margin-top: 76.63rpx;
		padding: 0 3.62rpx;
	}

	.group_4 {
		border-radius: 1.92rpx;
		width: 23.08rpx;
		height: 23.08rpx;
		border: solid 1.92rpx #a6a6a6;
	}

	.group_5 {
		line-height: 21.9rpx;
		height: 21.9rpx;
	}

	.text_6 {
		line-height: 21.71rpx;
	}

	.font_3 {
		font-size: 23.08rpx;
		font-family: HarmonyOSSansSC;
		line-height: 21.9rpx;
		color: #2a82e4;
	}

	.text_7 {
		line-height: 20.65rpx;
	}

	.text_8 {
		line-height: 21.81rpx;
	}
</style>