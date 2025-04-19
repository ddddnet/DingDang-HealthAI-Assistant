<template>
	<view>
		<view class="mbox-5" v-if="login_status">
		    <uni-forms :modelValue="formData" :rules="rules" ref="form">
		        <uni-forms-item label="名字" name="name">
		            <uni-easyinput type="text" v-model="formData.name" placeholder="请输入名字" />
		        </uni-forms-item>
		        <uni-forms-item label="性别" name="gender">
		            <uni-data-checkbox v-model="formData.gender" :localdata="genderOptions" />
		        </uni-forms-item>
		        <uni-forms-item label="年龄" name="age">
		            <uni-easyinput type="number" v-model="formData.age" placeholder="请输入年龄" />
		        </uni-forms-item>
		        <uni-forms-item label="身高（cm）" name="height">
		            <uni-easyinput type="number" v-model="formData.height" placeholder="请输入身高" />
		        </uni-forms-item>
		        <uni-forms-item label="体重（kg）" name="weight">
		            <uni-easyinput type="number" v-model="formData.weight" placeholder="请输入体重" />
		        </uni-forms-item>
		        <uni-forms-item label="活动频率" name="activityLevel">
		            <uni-data-checkbox v-model="formData.activityLevel" :localdata="activityLevelOptions" />
		        </uni-forms-item>
		    </uni-forms>
			<wd-button block size="large" @click="submitForm">提交</wd-button>
		</view>
		<view class="mbox-5" v-else>
			<wd-status-tip image="network" tip="请先登录" />
			<navigator url="/pages/login/login">
				<button type="default" class="mt-5" >去登录</button>
			</navigator>
		</view>
	</view>
    
</template>

<script>
    export default {
        data() {
            return {
				login_status:false,
				systemInfo: {},
                formData: {
                    name: '',
                    gender: [],
                    age: '',
                    height: '',
                    weight: '',
                    activityLevel: []
                },
                rules: {
                    name: {
                        rules: [
                            { required: true, errorMessage: '请填写名字' }
                        ]
                    },
                    gender: {
                        rules: [
                            { required: true, errorMessage: '请选择性别' }
                        ]
                    },
                    age: {
                        rules: [
                            { required: true, errorMessage: '请填写年龄' },
                            { type: 'number', min: 0, errorMessage: '年龄必须为非负整数' }
                        ]
                    },
                    height: {
                        rules: [
                            { required: true, errorMessage: '请填写身高' },
                            { type: 'number', min: 0, errorMessage: '身高必须为非负整数' }
                        ]
                    },
                    weight: {
                        rules: [
                            { required: true, errorMessage: '请填写体重' },
                            { type: 'number', min: 0, errorMessage: '体重必须为非负整数' }
                        ]
                    },
                    activityLevel: {
                        rules: [
                            { required: true, errorMessage: '请选择活动频率' }
                        ]
                    }
                },
                genderOptions: [
                    { value: '男', text: '男' },
                    { value: '女', text: '女' }
                ],
                activityLevelOptions: [
                    { value: 0, text: '久坐\n无规律运动习惯，日常活动量很少' },
                    { value: 1, text: '轻度活动,每周进行轻微运动1-3天\n如散步、轻松的骑自行车等' },
                    { value: 2, text: '中度活动,每周进行中等强度运动3-5天\n如慢跑、游泳、有氧运动等' },
                    { value: 3, text: '高度活动,每周进行高强度运动6-7天\n或日常活动量较大的工作\n如建筑工人、农民等' }
                ]
            };
        },
		onLoad() {
			try{
				this.login_user = uni.getStorageSync("login_user")
				if (this.login_user) {
					this.login_status = true
				}
			}
			catch(err){
				uni.showToast({
					title:err
				})
				uni.navigateBack()
			}
			
		},
        methods: {
			
            submitForm() {
				const _this = this
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
				
                this.$refs.form.validate().then(res => {
					res.user = this.login_user
					res.systemInfo = this.systemInfo
					const setName = res.name
					uni.request({
						url:this.$host_api + "/setUserInfo",
						method:"POST",
						data:res,
						success: (res) => {
							if (res.data.code == 1) {
								uni.showToast({
									title: res.data.msg,
									icon: 'success'
								})
								
								try{
									uni.setStorageSync("login_user_name",setName)
								}catch(error){
									uni.showToast({
										title:error,
										icon:'fail'
									})
								}
								
								uni.reLaunch({
									url:"/pages/my/my"
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
					
                }).catch(err => {
                });
            }
        }
    };
</script>