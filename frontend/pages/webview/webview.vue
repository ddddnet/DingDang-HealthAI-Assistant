<template>
	<view>
		<web-view :src="url"></web-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				url:""
			}
		},
		onLoad(option) {
			if(option){
				try {
					this.url = option.url
				}catch (e) {
					this.url = this.$host_api
				}
				
			}else{
				this.url = this.$host_api
			}
		},
		methods: {
			
		}
	}
</script>

<style>

</style>
