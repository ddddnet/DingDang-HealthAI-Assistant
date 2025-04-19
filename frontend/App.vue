<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
	/************************************************************
  ** 请将全局样式拷贝到项目的全局 CSS 文件或者当前页面的顶部 **
  ** 否则页面将无法正常显示                                  **
  ************************************************************/

	html {
		font-size: 16px;
	}

	body {
		margin: 0;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans',
			'Droid Sans', 'Helvetica Neue', 'Microsoft Yahei', sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
	}

	view,
	image,
	text {
		box-sizing: border-box;
		flex-shrink: 0;
	}

	#app {
		width: 100vw;
		height: 100vh;
	}
	
	.text-center {
		align-items: center;
	}
	.mbox-1{
		margin-top: 10rpx;
		margin-bottom: 20rpx;
		margin-left: 20rpx;
		margin-right: 20rpx;
	}
	.mbox-2{
		margin-top: 20rpx;
		margin-bottom: 20rpx;
		margin-left: 20rpx;
		margin-right: 20rpx;
		background-color: white;
	}
	.mbox-3 {
	    margin-top: 30rpx;
	    margin-bottom: 30rpx;
	    margin-left: 30rpx;
	    margin-right: 30rpx;
	}
	.mbox-4 {
	    margin-top: 40rpx;
	    margin-bottom: 40rpx;
	    margin-left: 40rpx;
	    margin-right: 40rpx;
	}
	.mbox-5 {
	    margin-top: 50rpx;
	    margin-bottom: 50rpx;
	    margin-left: 50rpx;
	    margin-right: 50rpx;
	}
	.mbox-6 {
	    margin-top: 60rpx;
	    margin-bottom: 60rpx;
	    margin-left: 60rpx;
	    margin-right: 60rpx;
	}
	.mbox-7 {
	    margin-top: 70rpx;
	    margin-bottom: 70rpx;
	    margin-left: 70rpx;
	    margin-right: 70rpx;
	}
	.mbox-8 {
	    margin-top: 80rpx;
	    margin-bottom: 80rpx;
	    margin-left: 80rpx;
	    margin-right: 80rpx;
	}
	.mbox-9 {
	    margin-top: 90rpx;
	    margin-bottom: 90rpx;
	    margin-left: 90rpx;
	    margin-right: 90rpx;
	}
	.mbox-10 {
	    margin-top: 100rpx;
	    margin-bottom: 100rpx;
	    margin-left: 100rpx;
	    margin-right: 100rpx;
	}
	.mbox-11 {
	    margin-top: 110rpx;
	    margin-bottom: 110rpx;
	    margin-left: 110rpx;
	    margin-right: 110rpx;
	}
	.mbox-12 {
	    margin-top: 120rpx;
	    margin-bottom: 120rpx;
	    margin-left: 120rpx;
	    margin-right: 120rpx;
	}
	.mbox-13 {
	    margin-top: 130rpx;
	    margin-bottom: 130rpx;
	    margin-left: 130rpx;
	    margin-right: 130rpx;
	}
	.mbox-14 {
	    margin-top: 140rpx;
	    margin-bottom: 140rpx;
	    margin-left: 140rpx;
	    margin-right: 140rpx;
	}
	.mbox-15 {
	    margin-top: 150rpx;
	    margin-bottom: 150rpx;
	    margin-left: 150rpx;
	    margin-right: 150rpx;
	}
	.mbox-16 {
	    margin-top: 160rpx;
	    margin-bottom: 160rpx;
	    margin-left: 160rpx;
	    margin-right: 160rpx;
	}
	.mbox-17 {
	    margin-top: 170rpx;
	    margin-bottom: 170rpx;
	    margin-left: 170rpx;
	    margin-right: 170rpx;
	}
	.mbox-18 {
	    margin-top: 180rpx;
	    margin-bottom: 180rpx;
	    margin-left: 180rpx;
	    margin-right: 180rpx;
	}
	.mbox-19 {
	    margin-top: 190rpx;
	    margin-bottom: 190rpx;
	    margin-left: 190rpx;
	    margin-right: 190rpx;
	}
	.mbox-20 {
	    margin-top: 200rpx;
	    margin-bottom: 200rpx;
	    margin-left: 200rpx;
	    margin-right: 200rpx;
	}
	.mt-1 {
	    margin-top: 10rpx;
	}
	.mt-2 {
	    margin-top: 20rpx;
	}
	.mt-3 {
	    margin-top: 30rpx;
	}
	.mt-4 {
	    margin-top: 40rpx;
	}
	.mt-5 {
	    margin-top: 50rpx;
	}
	.mt-6 {
	    margin-top: 60rpx;
	}
	.mt-7 {
	    margin-top: 70rpx;
	}
	.mt-8 {
	    margin-top: 80rpx;
	}
	.mt-9 {
	    margin-top: 90rpx;
	}
	.mt-10 {
	    margin-top: 100rpx;
	}
	.mt-11 {
	    margin-top: 110rpx;
	}
	.mt-12 {
	    margin-top: 120rpx;
	}
	.mt-13 {
	    margin-top: 130rpx;
	}
	.mt-14 {
	    margin-top: 140rpx;
	}
	.mt-15 {
	    margin-top: 150rpx;
	}
	.mt-16 {
	    margin-top: 160rpx;
	}
	.mt-17 {
	    margin-top: 170rpx;
	}
	.mt-18 {
	    margin-top: 180rpx;
	}
	.mt-19 {
	    margin-top: 190rpx;
	}
	.mt-20 {
	    margin-top: 200rpx;
	}
	
	.mr-1 {
	    margin-right: 10rpx;
	}
	.mr-2 {
	    margin-right: 20rpx;
	}
	.mr-3 {
	    margin-right: 30rpx;
	}
	.mr-4 {
	    margin-right: 40rpx;
	}
	.mr-5 {
	    margin-right: 50rpx;
	}
	.mr-6 {
	    margin-right: 60rpx;
	}
	.mr-7 {
	    margin-right: 70rpx;
	}
	.mr-8 {
	    margin-right: 80rpx;
	}
	.mr-9 {
	    margin-right: 90rpx;
	}
	.mr-10 {
	    margin-right: 100rpx;
	}
	.mr-11 {
	    margin-right: 110rpx;
	}
	.mr-12 {
	    margin-right: 120rpx;
	}
	.mr-13 {
	    margin-right: 130rpx;
	}
	.mr-14 {
	    margin-right: 140rpx;
	}
	.mr-15 {
	    margin-right: 150rpx;
	}
	.mr-16 {
	    margin-right: 160rpx;
	}
	.mr-17 {
	    margin-right: 170rpx;
	}
	.mr-18 {
	    margin-right: 180rpx;
	}
	.mr-19 {
	    margin-right: 190rpx;
	}
	.mr-20 {
	    margin-right: 200rpx;
	}
	
	.mb-1 {
	    margin-bottom: 10rpx;
	}
	.mb-2 {
	    margin-bottom: 20rpx;
	}
	.mb-3 {
	    margin-bottom: 30rpx;
	}
	.mb-4 {
	    margin-bottom: 40rpx;
	}
	.mb-5 {
	    margin-bottom: 50rpx;
	}
	.mb-6 {
	    margin-bottom: 60rpx;
	}
	.mb-7 {
	    margin-bottom: 70rpx;
	}
	.mb-8 {
	    margin-bottom: 80rpx;
	}
	.mb-9 {
	    margin-bottom: 90rpx;
	}
	.mb-10 {
	    margin-bottom: 100rpx;
	}
	.mb-11 {
	    margin-bottom: 110rpx;
	}
	.mb-12 {
	    margin-bottom: 120rpx;
	}
	.mb-13 {
	    margin-bottom: 130rpx;
	}
	.mb-14 {
	    margin-bottom: 140rpx;
	}
	.mb-15 {
	    margin-bottom: 150rpx;
	}
	.mb-16 {
	    margin-bottom: 160rpx;
	}
	.mb-17 {
	    margin-bottom: 170rpx;
	}
	.mb-18 {
	    margin-bottom: 180rpx;
	}
	.mb-19 {
	    margin-bottom: 190rpx;
	}
	.mb-20 {
	    margin-bottom: 200rpx;
	}
	
	.mf-1 {
	    margin-left: 10rpx;
	}
	.mf-2 {
	    margin-left: 20rpx;
	}
	.mf-3 {
	    margin-left: 30rpx;
	}
	.mf-4 {
	    margin-left: 40rpx;
	}
	.mf-5 {
	    margin-left: 50rpx;
	}
	.mf-6 {
	    margin-left: 60rpx;
	}
	.mf-7 {
	    margin-left: 70rpx;
	}
	.mf-8 {
	    margin-left: 80rpx;
	}
	.mf-9 {
	    margin-left: 90rpx;
	}
	.mf-10 {
	    margin-left: 100rpx;
	}
	.mf-11 {
	    margin-left: 110rpx;
	}
	.mf-12 {
	    margin-left: 120rpx;
	}
	.mf-13 {
	    margin-left: 130rpx;
	}
	.mf-14 {
	    margin-left: 140rpx;
	}
	.mf-15 {
	    margin-left: 150rpx;
	}
	.mf-16 {
	    margin-left: 160rpx;
	}
	.mf-17 {
	    margin-left: 170rpx;
	}
	.mf-18 {
	    margin-left: 180rpx;
	}
	.mf-19 {
	    margin-left: 190rpx;
	}
	.mf-20 {
	    margin-left: 200rpx;
	}


	.codefun-flex-row {
		display: flex;
		flex-direction: row;
	}

	.codefun-flex-col {
		display: flex;
		flex-direction: column;
	}

	.codefun-justify-start {
		justify-content: flex-start;
	}

	.codefun-justify-end {
		justify-content: flex-end;
	}

	.codefun-justify-center {
		justify-content: center;
	}

	.codefun-justify-between {
		justify-content: space-between;
	}

	.codefun-justify-around {
		justify-content: space-around;
	}

	.codefun-justify-evenly {
		justify-content: space-evenly;
	}

	.codefun-items-start {
		align-items: flex-start;
	}

	.codefun-items-end {
		align-items: flex-end;
	}

	.codefun-items-center {
		align-items: center;
	}

	.codefun-items-baseline {
		align-items: baseline;
	}

	.codefun-items-stretch {
		align-items: stretch;
	}

	.codefun-self-start {
		align-self: flex-start;
	}

	.codefun-self-end {
		align-self: flex-end;
	}

	.codefun-self-center {
		align-self: center;
	}

	.codefun-self-baseline {
		align-self: baseline;
	}

	.codefun-self-stretch {
		align-self: stretch;
	}

	.codefun-flex-1 {
		flex: 1 1 0%;
	}

	.codefun-flex-auto {
		flex: 1 1 auto;
	}

	.codefun-grow {
		flex-grow: 1;
	}

	.codefun-grow-0 {
		flex-grow: 0;
	}

	.codefun-shrink {
		flex-shrink: 1;
	}

	.codefun-shrink-0 {
		flex-shrink: 0;
	}

	.codefun-relative {
		position: relative;
	}

	.codefun-ml-2 {
		margin-left: 4rpx;
	}

	.codefun-mt-2 {
		margin-top: 4rpx;
	}

	.codefun-ml-4 {
		margin-left: 8rpx;
	}

	.codefun-mt-4 {
		margin-top: 8rpx;
	}

	.codefun-ml-6 {
		margin-left: 12rpx;
	}

	.codefun-mt-6 {
		margin-top: 12rpx;
	}

	.codefun-ml-8 {
		margin-left: 16rpx;
	}

	.codefun-mt-8 {
		margin-top: 16rpx;
	}

	.codefun-ml-10 {
		margin-left: 20rpx;
	}

	.codefun-mt-10 {
		margin-top: 20rpx;
	}

	.codefun-ml-12 {
		margin-left: 24rpx;
	}

	.codefun-mt-12 {
		margin-top: 24rpx;
	}

	.codefun-ml-14 {
		margin-left: 28rpx;
	}

	.codefun-mt-14 {
		margin-top: 28rpx;
	}

	.codefun-ml-16 {
		margin-left: 32rpx;
	}

	.codefun-mt-16 {
		margin-top: 32rpx;
	}

	.codefun-ml-18 {
		margin-left: 36rpx;
	}

	.codefun-mt-18 {
		margin-top: 36rpx;
	}

	.codefun-ml-20 {
		margin-left: 40rpx;
	}

	.codefun-mt-20 {
		margin-top: 40rpx;
	}

	.codefun-ml-22 {
		margin-left: 44rpx;
	}

	.codefun-mt-22 {
		margin-top: 44rpx;
	}

	.codefun-ml-24 {
		margin-left: 48rpx;
	}

	.codefun-mt-24 {
		margin-top: 48rpx;
	}

	.codefun-ml-26 {
		margin-left: 52rpx;
	}

	.codefun-mt-26 {
		margin-top: 52rpx;
	}

	.codefun-ml-28 {
		margin-left: 56rpx;
	}

	.codefun-mt-28 {
		margin-top: 56rpx;
	}

	.codefun-ml-30 {
		margin-left: 60rpx;
	}

	.codefun-mt-30 {
		margin-top: 60rpx;
	}

	.codefun-ml-32 {
		margin-left: 64rpx;
	}

	.codefun-mt-32 {
		margin-top: 64rpx;
	}

	.codefun-ml-34 {
		margin-left: 68rpx;
	}

	.codefun-mt-34 {
		margin-top: 68rpx;
	}

	.codefun-ml-36 {
		margin-left: 72rpx;
	}

	.codefun-mt-36 {
		margin-top: 72rpx;
	}

	.codefun-ml-38 {
		margin-left: 76rpx;
	}

	.codefun-mt-38 {
		margin-top: 76rpx;
	}

	.codefun-ml-40 {
		margin-left: 80rpx;
	}

	.codefun-mt-40 {
		margin-top: 80rpx;
	}

	.codefun-ml-42 {
		margin-left: 84rpx;
	}

	.codefun-mt-42 {
		margin-top: 84rpx;
	}

	.codefun-ml-44 {
		margin-left: 88rpx;
	}

	.codefun-mt-44 {
		margin-top: 88rpx;
	}

	.codefun-ml-46 {
		margin-left: 92rpx;
	}

	.codefun-mt-46 {
		margin-top: 92rpx;
	}

	.codefun-ml-48 {
		margin-left: 96rpx;
	}

	.codefun-mt-48 {
		margin-top: 96rpx;
	}

	.codefun-ml-50 {
		margin-left: 100rpx;
	}

	.codefun-mt-50 {
		margin-top: 100rpx;
	}

	.codefun-ml-52 {
		margin-left: 104rpx;
	}

	.codefun-mt-52 {
		margin-top: 104rpx;
	}

	.codefun-ml-54 {
		margin-left: 108rpx;
	}

	.codefun-mt-54 {
		margin-top: 108rpx;
	}

	.codefun-ml-56 {
		margin-left: 112rpx;
	}

	.codefun-mt-56 {
		margin-top: 112rpx;
	}

	.codefun-ml-58 {
		margin-left: 116rpx;
	}

	.codefun-mt-58 {
		margin-top: 116rpx;
	}

	.codefun-ml-60 {
		margin-left: 120rpx;
	}

	.codefun-mt-60 {
		margin-top: 120rpx;
	}

	.codefun-ml-62 {
		margin-left: 124rpx;
	}

	.codefun-mt-62 {
		margin-top: 124rpx;
	}

	.codefun-ml-64 {
		margin-left: 128rpx;
	}

	.codefun-mt-64 {
		margin-top: 128rpx;
	}

	.codefun-ml-66 {
		margin-left: 132rpx;
	}

	.codefun-mt-66 {
		margin-top: 132rpx;
	}

	.codefun-ml-68 {
		margin-left: 136rpx;
	}

	.codefun-mt-68 {
		margin-top: 136rpx;
	}

	.codefun-ml-70 {
		margin-left: 140rpx;
	}

	.codefun-mt-70 {
		margin-top: 140rpx;
	}

	.codefun-ml-72 {
		margin-left: 144rpx;
	}

	.codefun-mt-72 {
		margin-top: 144rpx;
	}

	.codefun-ml-74 {
		margin-left: 148rpx;
	}

	.codefun-mt-74 {
		margin-top: 148rpx;
	}

	.codefun-ml-76 {
		margin-left: 152rpx;
	}

	.codefun-mt-76 {
		margin-top: 152rpx;
	}

	.codefun-ml-78 {
		margin-left: 156rpx;
	}

	.codefun-mt-78 {
		margin-top: 156rpx;
	}

	.codefun-ml-80 {
		margin-left: 160rpx;
	}

	.codefun-mt-80 {
		margin-top: 160rpx;
	}

	.codefun-ml-82 {
		margin-left: 164rpx;
	}

	.codefun-mt-82 {
		margin-top: 164rpx;
	}

	.codefun-ml-84 {
		margin-left: 168rpx;
	}

	.codefun-mt-84 {
		margin-top: 168rpx;
	}

	.codefun-ml-86 {
		margin-left: 172rpx;
	}

	.codefun-mt-86 {
		margin-top: 172rpx;
	}

	.codefun-ml-88 {
		margin-left: 176rpx;
	}

	.codefun-mt-88 {
		margin-top: 176rpx;
	}

	.codefun-ml-90 {
		margin-left: 180rpx;
	}

	.codefun-mt-90 {
		margin-top: 180rpx;
	}

	.codefun-ml-92 {
		margin-left: 184rpx;
	}

	.codefun-mt-92 {
		margin-top: 184rpx;
	}

	.codefun-ml-94 {
		margin-left: 188rpx;
	}

	.codefun-mt-94 {
		margin-top: 188rpx;
	}

	.codefun-ml-96 {
		margin-left: 192rpx;
	}

	.codefun-mt-96 {
		margin-top: 192rpx;
	}

	.codefun-ml-98 {
		margin-left: 196rpx;
	}

	.codefun-mt-98 {
		margin-top: 196rpx;
	}

	.codefun-ml-100 {
		margin-left: 200rpx;
	}

	.codefun-mt-100 {
		margin-top: 200rpx;
	}
</style>