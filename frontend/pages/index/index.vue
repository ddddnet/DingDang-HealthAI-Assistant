<template>
	<view class="codefun-flex-col codefun-relative page">
		<view class="codefun-self-center group"></view>
		<view class="codefun-flex-col codefun-items-center codefun-self-stretch group_2">
			<!-- 按钮 -->
			<image class="image_2" @click="gotoIndex()"
				src="../../static/image/codefun/34764923e56a4ea450fbf1b9ffeeac4e.png" />
			<image class="image_3 mt-21" src="../../static/image/codefun/f1620910b16e51518956dbc759839e27.png" />
		</view>
		<image class="image pos" @click="test()" src="../../static/image/codefun/05fd939f1553cd6261ca49b0a90cd4a7.png" />
	</view>
</template>

<script>
	export default {
		components: {},
		props: {},
		data() {
			return {};
		},
		onLoad() {
			let logined = uni.getStorageSync("login_user")
			if(logined){
				uni.reLaunch({
					url:"/pages/home/home"
				})
			}
		},
		methods: {
			test(){
				
			},
			gotoIndex() {
				uni.redirectTo({
					url: '/pages/index1/index1',
				})
			},
		},
	};
</script>

<style scoped lang="css">
	.mt-21 {
		margin-top: 42rpx;
	}

	.page {
		padding: 546rpx 0 104rpx;
		background-color: #1947e5;
		width: 100%;
		overflow-y: auto;
		overflow-x: hidden;
		height: 100%;
	}

	.group {
		border-radius: 120rpx;
		overflow: hidden;
		width: 296rpx;
		height: 296rpx;
	}

	.group_2 {
		margin-top: 350rpx;
	}

	.image_2 {
		width: 314rpx;
		height: 138rpx;
	}

	.image_3 {
		width: 314rpx;
		height: 148rpx;
	}

	.image {
		border-radius: 120rpx;
		overflow: hidden;
		width: 296rpx;
		height: 294rpx;
	}

	.pos {
		position: absolute;
		left: 214rpx;
		top: 548rpx;
	}
</style>