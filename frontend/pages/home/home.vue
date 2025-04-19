<template>
	<view class="page">
		<wd-notify />
		<!-- 用户信息卡片 -->
		<view class="user-card">
			<view class="user-info">
				<image class="avatar" src="/static/p.png"></image>
				<view class="user-detail">
					<text class="username">{{login_user_name || '未登录'}}</text>
					<text class="location">id@{{login_user}}</text>
				</view>
			</view>
		</view>

		<!-- 可进食状态 -->
		<view :class="['clock-times', !login_status ? 'cannot-eat' : isOver8Hours ? 'cannot-eat' : 'can-eat']" @click="handleStatusClick">
			<text class="status-text">{{ !login_status ? '未登录' : timeRangeText }}</text>
		</view>

		<!-- 中间大圆形打卡按钮 -->
		<view class="clock-container">
			<view class="clock-circle" @click="FchooseImage">
				<view class="circle-content">
					<text class="clock-text">打卡</text>
				</view>
			</view>
			<view class="support-text">
				<text>支持食物照片、运动截图、体重图片 \n 上传时间为打卡时间</text>
				<!-- #ifdef MP-TOUTIAO -->
				<text>\n推荐在微信使用小程序，体验更完善</text>
				<!-- #endif -->
			</view>
		</view>

	</view>
</template>

<script>
	import {
		useNotify
	} from '@/uni_modules/wot-design-uni';
	export default {
		setup() {
			const {
				showNotify
			} = useNotify();

			return {
				showNotify
			};
		},
		data() {
			return {
				login_user: "",
				login_user_name: "",
				login_status: false,
				tabbar: 0,
				tempFilePaths: '',
				token: "",
				systemInfo: "",
				statusBarHeight: 0,
				firstMealTime: null
			}
		},
		computed: {
			timeRangeText() {
				if (!this.firstMealTime) return '今日没有进食记录，可以随时进食';
				
				// 确保firstMealTime是有效的日期字符串
				const firstMeal = new Date(this.firstMealTime);
				if (isNaN(firstMeal.getTime())) {
					return '时间格式错误';
				}

				const forbiddenStart = new Date(firstMeal);
				const forbiddenEnd = new Date(firstMeal.getTime() + 8 * 60 * 60 * 1000);

				const formatTime = (date) => {
					if (isNaN(date.getTime())) return '无效时间';
					return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', hour12: false });
				};

				if (this.isOver8Hours) {
					return `${formatTime(forbiddenEnd)} - ${formatTime(forbiddenStart)} 禁止进食`;
				} else {
					return `${formatTime(forbiddenStart)} - ${formatTime(forbiddenEnd)} 可以进食`;
				}
			},
			isOver8Hours() {
				// 如果没有第一顿时间，视为可以进食
				if (!this.firstMealTime) return false;
				const now = new Date();
				const firstMeal = new Date(this.firstMealTime);
				const diff = now - firstMeal;
				return diff > 8 * 60 * 60 * 1000;
			}
		},
		onLoad() {

			this.login_user = uni.getStorageSync("login_user")
			if (this.login_user) {
				this.login_status = true
				this.login_user_name = uni.getStorageSync("login_user_name")
				
			}

			// 获取手机信息
			uni.getSystemInfo({
				success: (res) => {
					this.statusBarHeight = res.statusBarHeight
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
		onShow(){
			this.login_user = uni.getStorageSync("login_user")
			if (this.login_user) {
				this.login_status = true
				this.login_user_name = uni.getStorageSync("login_user_name")
				
			}
		},
		onReady() {
			this.getFirstMealTime();
			this.getTopic();
		},
		methods: {
			getFirstMealTime() {
<<<<<<< HEAD
				if(this.login_status == false){
					return
				}
=======
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac
				uni.request({
					url: this.$host_api + "/getFirstMealTime",
					method: 'POST',
					data: {
						user: this.login_user,
						systemInfo: this.systemInfo
					},
					success: (res) => {
<<<<<<< HEAD
=======
						console.log("获取第一顿时间成功",res.data)
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac
						if (res.data.code === 1 && res.data.First) {
							// 将Unix时间戳（秒）转换为JavaScript时间戳（毫秒）
							this.firstMealTime = new Date(res.data.data.first_meal_time * 1000);
						} else if (res.data.code === 1 && !res.data.First) {
							this.firstMealTime = null;
							this.showNotify({ type: 'warning', duration: 3000, message: res.data.msg });
						} else {
							this.showNotify({ type: 'danger', duration: 3000, message: res.data.msg });
						}
					},
					fail: (err) => {
						this.showNotify({ type: 'danger', duration: 3000, message: '获取第一顿时间失败' });
					}
				});
			},
			getTopic(){
				let _this = this
				uni.request({
					url:this.$host_api + "/data",
					method:'GET',
					success(res) {
						let topic = res.data.topic
						_this.showNotify({ type: 'primary', duration: 3000 ,message: topic})
					},
					fail(err){
					}
				})
			},
			
			FchooseImage() {
				
				if(this.login_status == false){
					this.showNotify({ type: 'danger', duration: 1000 ,message: "❗请登录"})
					return
				}
				
				const api = this.$host_api
				const user = this.login_user
				const systeminfo = this.systemInfo
				const _this = this

				uni.chooseImage({
					count: 1, // 最多选择一张图片
					success: function(res) {
						const tempFilePaths = res.tempFilePaths;
						const filePath = tempFilePaths[0];
						// 调用后端接口获取上传凭证并上传图片

						// 获取上传凭证
						uni.request({
							url: api + '/getUploadSet', // 后端获取上传凭证的接口地址
							method: 'POST',
							data: {
								user: user,
								systemInfo: systeminfo
							},
							success: (res) => {

								if (res.data.code != 1) {
									uni.showToast({
										title: res.data.msg,
										icon: "error"
									})
									return
								}

								const uploadToken = res.data.token
								const uploadUrl = res.data.upload_url
								const uploadFileName = res.data.upload_file_name
								const uploadKey = res.data.key
								// 设置时间

								uni.uploadFile({
									url: uploadUrl, // 根据你的七牛云存储区域选择上传域名，这里假设是华东 - 浙江区域
									filePath: filePath,
									name: uploadFileName,
									formData: {
										'token': uploadToken,
										'key': uploadKey // 可选，指定上传到七牛云后的文件名，如果不指定七牛云会自动生成
									},
									success: function(ress) {
										_this.showNotify({ type: 'primary', duration: 2000 ,message: "🤖AI分析中..."})
										// 调用AI分析接口
										_this.ai_scarne(ress.data)
										// {"hash":"FpmQ9sBCtR0uLem3xepTHENGQ1MF","key":"food/food-13800138001-20250102223052"}
									},
									fail: function(err) {
										uni.showToast({
											title: "照片上传失败",
											icon: "error"
										})
									}
								});
							},
							fail: (err) => {
								
								uni.showToast({
									title: "连接服务器失败03",
									icon: "error"
								})
							}
						});
					},
					fail: (err) => {
						uni.showToast({
							title: "选择图片失败",
							icon: "error"
						})
					}
				});
			},

			ai_scarne(data) {
				const _this = this
				uni.request({
					url: this.$host_api + "/ai",
					method: 'POST',
					data: {
						user: this.login_user,
						systemInfo: this.systemInfo,
						data: data
					},
					success: (res) => {
						if (res.statusCode == 200) {
							if (res.data.code == 1) {
								//分析健康数据成功
<<<<<<< HEAD
=======
								console.log("获得健康数据", res.data)
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac
								
								_this.showNotify({ color: '#FFFFFF', background: '#61E4C5', duration: 2000 ,message:  res.data.type+ ':' + res.data.content})
								// 上传成功后重新获取第一顿时间事件
								setTimeout(() => {
									this.getFirstMealTime();
								}, 25000);
								return
							} else if (res.data.code == 0) {
								//分析健康数据失败
								
								_this.showNotify({ type: 'danger', duration: 2000 ,message: "❎" + res.data.msg})
								return
							} else {
								uni.showToast({
									title: "服务器错误01",
									icon: 'error'
								})
								//服务器返回格式错误
								return
							}
						} else {
							uni.showToast({
								title: "服务器错误02",
								icon: 'error'
							})
							return
						}
						
					},
					fail: (res) => {
<<<<<<< HEAD
=======
						console.log("AI分析失败", res)
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac
					}
				})
			},
			handleStatusClick() {
				if (!this.login_status) {
					uni.navigateTo({
						url: '/pages/login/login'
					});
				}
			}
		}
	}
			
</script>

<style>
	.page {
		background-color: #f5f7fa;
		min-height: 100vh;
		display: flex;

		flex-direction: column;
		overflow: hidden;
		position: fixed;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
		padding-top: 10px;
		/* 减小顶部内边距，与卡片之间的间距一致 */
	}

	.user-card {
		background-color: #fff;
		padding: 30rpx 40rpx;
		margin: 20rpx;
		border-radius: 12rpx;
		box-shadow: none;
	}
	/* #ifdef H5 */
	.user-card {
		background-color: #fff;
		padding: 30rpx 40rpx;
		margin: 20rpx;
		margin-top: 100rpx;
		border-radius: 12rpx;
		box-shadow: none;
	}
	/* #endif */

	.user-info {
		display: flex;
		align-items: center;
	}

	.avatar {
		width: 70rpx;
		height: 70rpx;
		border-radius: 50%;
		margin-right: 20rpx;
	}

	.user-detail {
		display: flex;
		flex-direction: column;
	}

	.username {
		font-size: 30rpx;
		font-weight: normal;
	}

	.location {
		font-size: 22rpx;
		color: #999;
		margin-top: 6rpx;
	}

	.clock-times {
		background-color: #fff;
		padding: 24rpx 40rpx;
		margin: 20rpx;
		border-radius: 12rpx;
		box-shadow: none;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.can-eat {
		background-color: #34d19d;
		/* WeUI 品牌绿色 */
		border: none;
	}

	.cannot-eat {
		background-color: #fa4350;
		/* WeUI 红色 */
		border: none;
	}

	.status-text {
		font-size: 32rpx;
		font-weight: bold;
		text-align: center;
		color: #FFFFFF;
	}

	.can-eat .status-text {
		color: #FFFFFF;
	}

	.cannot-eat .status-text {
		color: #FFFFFF;
	}

	.clock-container {
		margin: 20rpx;
		background-color: #fff;
		border-radius: 12rpx;
		box-shadow: none;
		flex: 1;
		min-height: 0;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	.clock-circle {
		width: 400rpx;
		height: 400rpx;
		border-radius: 50%;
		background-color: #FF89BB;
		/* WeUI 蓝色 */
		display: flex;
		justify-content: center;
		align-items: center;
		position: relative;
		z-index: 2;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		box-shadow: 0 3px 5px rgba(0, 0, 0, 0.2);
	}

	.clock-circle::before {
		content: '';
		position: absolute;
		width: 320rpx;
		height: 320rpx;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(255, 137, 187, 0.12) 0%, rgba(255, 137, 187, 0) 100%);
		/* WeUI 蓝色透明度 */
		z-index: 1;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	.clock-circle::after {
		content: '';
		position: absolute;
		width: 400rpx;
		height: 400rpx;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(255, 137, 187, 0.06) 0%, rgba(255, 137, 187, 0) 100%);
		/* WeUI 蓝色透明度 */
		z-index: 0;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	.clock-circle:active {
		transform: scale(0.95);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.18);
	}

	.circle-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		color: #ffffff;
		position: relative;
		z-index: 3;
	}

	.clock-text {
		font-size: 60rpx;
		font-weight: bold;
		color: #ffffff;
	}

	.clock-time {
		font-size: 26rpx;
		margin-top: 8rpx;
		color: #ffffff;
	}

	.check-in-btn {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.support-text {
		margin-top: 100rpx;
		text-align: center;
		color: #999;
		font-size: 20rpx;
	}
</style>