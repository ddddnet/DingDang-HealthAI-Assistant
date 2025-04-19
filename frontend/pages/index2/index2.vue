<template>
  <view class="codefun-flex-col page">
    <image
      class="codefun-shrink-0 codefun-self-center image"
      src="../../static/image/codefun/b204b091b5d913255168e6816c300fbd.png"
    />
    <image
      class="codefun-shrink-0 codefun-self-center image_2"
      src="../../static/image/codefun/3d6c51012ab2d6dc265d4402ab7d7182.png"
    />
	<!-- 下一步 -->
    <image @click="gotoLogin()"
      class="codefun-shrink-0 codefun-self-start image_4"
      src="../../static/image/codefun/dca89cadbe3449015a3ab79e56e36c09.png"
    />
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
	},
  };
</script>

<style scoped lang="css">
  .page {
    padding-top: 152rpx;
    background-color: #ffffff;
    height: 100%;
    width: 100%;
    overflow-y: auto;
    overflow-x: hidden;
  }
  .image {
    width: 618rpx;
    height: 758rpx;
  }
  .image_2 {
    width: 100vw;
    height: 68.2667vw;
  }
  .image_4 {
    margin-top: -14rpx;
    width: 101.0667vw;
    height: 28.8vw;
  }
</style>