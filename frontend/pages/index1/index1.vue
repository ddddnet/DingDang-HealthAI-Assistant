<template>
  <view class="codefun-flex-col page">
    <view class="codefun-flex-col codefun-items-center">
      <image class="image" src="../../static/image/codefun/c75b01aa2fa2a13b3464917d05e4fd2f.png" />
      <image class="image_2 mt-49" src="../../static/image/codefun/b96c73010d19905056c89bc244b26e1e.png" />
    </view>
    <view class="codefun-flex-row equal-division mt-83">
		<!-- 跳过 -->
      <image @click="gotoLogin()"
        class="image_3 equal-division-item"
        src="../../static/image/codefun/b7f4a6fc25bc7aa51e7d5531eaedfe15.png"
      />
	  <!-- 下一步 -->
      <image @click="gotoIndex2()"
        class="image_3 equal-division-item ml-31"
        src="../../static/image/codefun/35f09a2874af72de961d83a87b9beebd.png"
      />
    </view>
  </view>
</template>

<script>
  export default {
    components: {},
    props: {},
    data() {
      return {};
    },

    methods: {
		gotoLogin(){
			uni.reLaunch({
				url: '/pages/login/login',
			})
		},
		gotoIndex2() {
			uni.redirectTo({
				url: '/pages/index2/index2',
			})
		},
	},
  };
</script>

<style scoped lang="css">
  .mt-49 {
    margin-top: 98rpx;
  }
  .mt-83 {
    margin-top: 166rpx;
  }
  .ml-31 {
    margin-left: 62rpx;
  }
  .page {
    padding: 194rpx 0 44rpx;
    background-color: #ffffff;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    height: 100%;
  }
  .image {
    width: 618rpx;
    height: 618rpx;
  }
  .image_2 {
    width: 100vw;
    height: 51.2vw;
  }
  .equal-division {
    margin: 0 30rpx;
  }
  .image_3 {
    flex: 1 1 314rpx;
  }
  .equal-division-item {
    height: 120rpx;
  }
</style>