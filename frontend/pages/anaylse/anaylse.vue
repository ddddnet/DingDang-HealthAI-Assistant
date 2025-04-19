<template>
	<view class="page-container">
		<wd-notify />
		<!-- 判断登录 -->
		<view v-if="login_status">
			<!-- 判断加载完成 -->
			<view v-if="data_done">
				<!-- 数据为空 -->
				<view v-if="data_empty" class="">
					<wd-status-tip image="content" tip="今日暂无记录" />
					<wd-textarea v-model="emptytisp" readonly></wd-textarea>
				</view>
				<!-- 数据不为空 -->
				<view v-if="data_empty == false" class="">
					<view class="grid-box">
						<uni-section class="tite" title="基础数据 " type="line"></uni-section>
						<wd-row>
							<wd-col :span="12">
								<uni-card title="🚀基础代谢" sub-title="" extra="" >
									<wd-count-to prefix="" :startVal="0" :decimals="0"
										:endVal="health_data.daily.daily_TDEE" :fontSize="32" suffix="cal"
										color="#ff5722"></wd-count-to>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🏅体重" sub-title="" extra="" >
									<wd-count-to prefix="" :startVal="0" :decimals="2"
										:endVal="health_data.daily.daily_weight" :fontSize="32" suffix="kg"
										color="#ffb800"></wd-count-to>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🔎是否超标(AI)" sub-title="" extra="" >
									<button v-if="health_data.daily.daily_over === 0" type="default">否</button>
									<button v-if="health_data.daily.daily_over === 1" type="warn">是</button>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🤖AI分析" sub-title="" extra="" @click="openAIreport(health_data.daily.daily_id)">
									<button type="default">查看</button>
								</uni-card>
							</wd-col>
						</wd-row>
					</view>
					<view>
						<uni-section class="tite" title="健康数据 " type="line"></uni-section>
						<wd-row>
							<wd-col :span="12">
								<uni-card title="🥣顿数" sub-title="" extra="" >
									<wd-count-to prefix="" :startVal="0" :decimals="0"
										:endVal="health_data.daily.daily_count" :fontSize="32" suffix="顿"
										color="#1e9fff"></wd-count-to>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🔥卡路里" sub-title="" extra="">
									<wd-count-to prefix="" :startVal="0" :decimals="0"
										:endVal="health_data.daily.daily_cal" :fontSize="32" suffix="cal"
										color="#1e9fff"></wd-count-to>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🍚碳水" sub-title="" extra="" >
									<wd-count-to prefix="" :startVal="0" :decimals="0"
										:endVal="health_data.daily.daily_carbon" :fontSize="32" suffix="g"
										color="#1e9fff"></wd-count-to>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🥚蛋白质" sub-title="" extra="" >
									<wd-count-to prefix="" :startVal="0" :decimals="0"
										:endVal="health_data.daily.daily_protein" :fontSize="32" suffix="g"
										color="#1e9fff"></wd-count-to>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🥩脂肪" sub-title="" extra="" >
									<wd-count-to prefix="" :startVal="0" :decimals="0"
										:endVal="health_data.daily.daily_fat" :fontSize="32" suffix="g"
										color="#1e9fff"></wd-count-to>
								</uni-card>
							</wd-col>
							<wd-col :span="12">
								<uni-card title="🥗膳食纤维" sub-title="" extra="" >
									<wd-count-to prefix="" :startVal="0" :decimals="0"
										:endVal="health_data.daily.daily_df" :fontSize="32" suffix="g"
										color="#1e9fff"></wd-count-to>
								</uni-card>
							</wd-col>
						</wd-row>
					</view>


					<view class="record-box">
						<uni-section class="tite" title="健康记录" type="line"></uni-section>
						<wd-tabs v-model="activeTab" sticky>
							<wd-tab title="今日">
								<view class="tab-content">
									<!-- 列表 -->
									<uni-list >
										<uni-list-item v-for="(item,index) in health_data.records" :key="index"
											@click="openList(health_data.records[index].record_type,health_data.records[index].record_id)"
											link
											:title="health_data.records[index].record_title"
											:note="health_data.records[index].record_time_de " showArrow
											:thumb="health_data.records[index].record_url" thumb-size="lg" rightText=""
											/>
									</uni-list>
									<uni-list>
										<uni-list-item title="对数据有疑问?" note="咨询专业教练" showArrow thumb="/static/p.png"
											thumb-size="lg" rightText="点击咨询" />
									</uni-list>
								</view>
							</wd-tab>
							<wd-tab title="历史">
								<view class="tab-content">
									<wd-status-tip image="content" tip="开发中..." />
								</view>
							</wd-tab>
						</wd-tabs>
					</view>
				</view>

			</view>

			<!-- 未加载完成 -->
			<view v-else class="">
				<!-- 骨架屏 -->
				<wd-skeleton v-for="index in 9" theme="paragraph" />
			</view>
		</view>

		<!-- 未登录 -->
		<view v-if="login_status == false">
			<view class="grid-box">
				<uni-section class="tite" title="基础数据 " type="line"></uni-section>
				<wd-row>
					<wd-col :span="12">
						<uni-card title="🚀基础代谢" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="0" :endVal="1560" :fontSize="32"
								suffix="cal" color="#ff5722"></wd-count-to>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🏅体重" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="2" :endVal="50.3" :fontSize="32" suffix="kg"
								color="#ffb800"></wd-count-to>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🔎是否超标" sub-title="" extra="" @click="onClick">
							<button type="warn">是</button>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🤖AI分析" sub-title="" extra="" @click="onClick">
							<button type="default">查看</button>
						</uni-card>
					</wd-col>
				</wd-row>
			</view>
			<view>
				<uni-section class="tite" title="健康数据 " type="line"></uni-section>
				<wd-row>
					<wd-col :span="12">
						<uni-card title="🥣顿数" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="0" :endVal="3" :fontSize="32" suffix="顿"
								color="#1e9fff"></wd-count-to>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🔥卡路里" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="0" :endVal="1560" :fontSize="32"
								suffix="cal" color="#1e9fff"></wd-count-to>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🍚碳水" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="0" :endVal="1560" :fontSize="32" suffix="g"
								color="#1e9fff"></wd-count-to>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🥚蛋白质" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="0" :endVal="1560" :fontSize="32" suffix="g"
								color="#1e9fff"></wd-count-to>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🥩脂肪" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="0" :endVal="1560" :fontSize="32" suffix="g"
								color="#1e9fff"></wd-count-to>
						</uni-card>
					</wd-col>
					<wd-col :span="12">
						<uni-card title="🥗膳食纤维" sub-title="" extra="" @click="onClick">
							<wd-count-to prefix="" :startVal="0" :decimals="0" :endVal="1560" :fontSize="32" suffix="g"
								color="#1e9fff"></wd-count-to>
						</uni-card>
					</wd-col>
				</wd-row>
			</view>


			<view class="record-box">
				<uni-section class="tite" title="健康记录" type="line"></uni-section>
				<wd-tabs v-model="activeTab" sticky>
					<wd-tab title="今日">
						<view class="tab-content">
							<wd-status-tip image="search" tip="请登录" />
						</view>
					</wd-tab>
					<wd-tab title="历史">
						<view class="tab-content">
							<wd-status-tip image="search" tip="请登录" />
						</view>
					</wd-tab>
				</wd-tabs>
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
				login_status: false,  // 登录状态
				login_user: "",      // 登录用户ID
				login_user_name: "", // 登录用户名
				systemInfo: {},      // 系统信息
				data_done: false,    // 数据加载完成状态
				data_empty: null,    // 数据是否为空(null:未加载, true:空, false:有数据)
				isLoading: false,    // 加载中状态
				emptytisp: "提示：刚刚上传完照片需要等待数分钟才能看到报表\n下拉屏幕可以刷新",
				daily_data: {
					food_count: 0,
				},
				health_data: {}

			}
		},
		onShow() {
			// 获取手机信息
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
			
			this.login_user = uni.getStorageSync("login_user")
			
			if (this.login_user) {
				this.login_status = true
				this.login_user_name = uni.getStorageSync("login_user_name")
				this.getRecord()
			}
			// 强制更新视图
			this.$forceUpdate()
			
		},
		onPullDownRefresh() {
			this.getRecord()
		},
		methods: {
			openAIreport(id){
<<<<<<< HEAD
=======
				console.log("打开ai分析",id)
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac
				uni.navigateTo({
					url:"/pages/webview/webview?url=" + this.$host_api + "/get_daily_detail/"+id
				})
			},
			openList(type,id){
<<<<<<< HEAD
=======
				console.log(type,id)
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac
				if(type == "food"){
					uni.navigateTo({
						url:"/pages/webview/webview?url=" + this.$host_api + "/get_food_detail/"+id
					})
				}else{
					uni.showToast({
						icon:"none",
						title:"点击食物可以查看详情分析"
					})
				}
				
			},
			onClick(e) {
				this.showNotify({
					type: "danger",
					message: "请登录"
				})
			},

			getRecord() {
				let that = this
				this.data_done = false
				// 创建一个新的 Date 对象，表示当前日期和时间
				let today = new Date();
				// 获取年份，使用 padStart 方法确保是 4 位数字
				let year = today.getFullYear().toString();
				// 获取月份，月份从 0 开始，所以需要加 1，使用 padStart 方法确保是 2 位数字
				let month = (today.getMonth() + 1).toString().padStart(2, '0');
				// 获取日期，使用 padStart 方法确保是 2 位数字
				let day = today.getDate().toString().padStart(2, '0');
				// 拼接成所需的格式
				let formattedDate = year + month + day;
				console.log(formattedDate)
				uni.request({
					url: this.$host_api + "/getDailyEvent",
					method: "POST",
					data: {
						user: that.login_user,
						date: formattedDate,
						systemInfo: that.systemInfo
					},
					success: (res) => {
						console.log(res)
						if (res.data.code == 1) {
							//获取成功
<<<<<<< HEAD
							that.health_data = res.data.data
							that.data_empty = false  // 明确设置data_empty为false
=======
							this.health_data = res.data.data
							this.data_empty = false  // 明确设置data_empty为false
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac
						} else {
							//今日没有数据
							that.data_empty = true
							this.showNotify({
								type: "primary",
								message: "🤖今日没有记录，快去打卡吧~"
							})
						}
<<<<<<< HEAD
						that.data_done = true
						// 强制更新视图
						that.$forceUpdate()
=======
						this.data_done = true
						// 强制更新视图
						this.$forceUpdate()
>>>>>>> 5eb6e8feae16940a32ab49097e8523c6d864fbac

					},
					fail: (err) => {
						that.showNotify({
							type: "danger",
							message: "🤖加载失败下拉重试~"
						})
					},
					complete() {
						uni.stopPullDownRefresh();
					}
				})
			},


		}
	}
</script>

<style>

</style>