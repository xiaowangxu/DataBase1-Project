<template>
	<div style="display: flex; flex-direction: column; height: 100%; gap: 20px;">

		<div class="coursecard"
			style="border-radius: 10px; box-shadow: #00000026 0px 5px 7px 0px; display: flex; flex-direction: column; padding: 10px 15px"
			:style="{'background': `linear-gradient(45deg, ${colors.color1}, ${colors.color2})`}">
			<div class="container"
				style="display: flex; flex-direction: row; justify-content: space-between; flex: 1; gap: 20px;">
				<div class="vcontainer">

					<a style="color: white; font-size: 24px; font-weight: bolder; word-break: keep-all;">{{$route.params.name}}
						<span style="font-weight: lighter;">{{$route.params.cid}}</span></a>
					<div class="container">
						<div class="vcontainer">
							<a style="color: white; font-size: 16px; font-weight: bolder;">{{$route.params.tname}}
								<span style="font-weight: lighter;">{{$route.params.tid}}</span></a>
							<a style="color: white; font-size: 16px; font-weight: lighter;">{{$route.params.credit}}
								<span style="font-weight: bolder;">学分</span></a>
						</div>

					</div>

				</div>
				<!-- <div class="container"
					style="justify-content: center; flex: unset; flex-direction: row; gap: 13px; align-items: flex-end;  justify-content: space-between;">
					<div
						style="background-color: white; padding: 5px 12px 5px 11px; border-radius: 5px; height: min-content; align-self: center;">
						<a style="font-weight: bolder; font-family: consolas;"
							:style="{'font-size': '30px', 'font-style': 'italic', 'color': colors.color2}">
							<a
								style="font-style: normal; font-size: 20px; margin-right: 2px;">共</a>{{studentList.length}}<a
								style="font-style: normal; font-size: 20px; margin-left: 2px;">人</a></a>
					</div>
					<div
						style="background-color: white; padding: 5px 12px 5px 11px; border-radius: 5px; height: min-content; align-self: center;">
						<a style="font-weight: bolder; font-family: consolas;"
							:style="{'font-size': '30px', 'font-style': 'italic', 'color': colors.color2}">
							<a style="font-style: normal; font-size: 20px; margin-right: 2px;">均分</a>{{get_Avg}}</a>
					</div>
				</div> -->
			</div>
		</div>
		<div class="coursecard"
			style="border-radius: 10px; box-shadow: #00000026 0px 5px 7px 0px; display: flex; flex-direction: column; padding: 10px 15px; background: white; color: black;">
			<div class="container"
				style="display: flex; flex-direction: row; justify-content: space-between; flex: 1; gap: 20px;">
				<div class="vcontainer">
					<a style="color: black; font-size: 18px;">{{$route.params.description}}</a>

				</div>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'courseinfo',
		components: {
		},
		data() {
			return {
				colors: {
					color1: 'red',
					color2: 'blue'
				},
				Color: [
					['#9b1645', '#e91e63'],
					['#e91e63', '#9c27b0'],
					['#3f51b5', '#2196f3'],
					['#009688', '#59662c'],
					['#673ab7', '#3f51b5'],
					['#ffdd11', '#ff9800'],
					['#00bcd4', '#009688'],
					['#ff9800', '#ff5722'],
					['#9c27b0', '#673ab7'],
					['#59662c', '#9fa328'],
					['#2196f3', '#00bcd4'],
					['#9fa328', '#ffdd11'],
					['#a32866', '#f44336']
				]
			}
		},
		watch: {
		},
		computed: {
		},
		methods: {

		},
		mounted() {
			console.log(this.$route.params)
			this.colors.color1 = this.Color[(this.$route.params.id) % this.Color.length][0]
			this.colors.color2 = this.Color[(this.$route.params.id) % this.Color.length][1]
		}
	}
</script>

<style scoped>
	.container {
		display: flex;
		flex-direction: row;
		flex: 1;
	}

	.vcontainer {
		display: flex;
		flex-direction: column;
		flex: 1;
		gap: 4px;
	}

	.coursecard {
		border-radius: 10px;
		box-shadow: #00000026 0px 5px 7px 0px;
		transform: scale(1) translateY(0px);
		transition: all .2s ease-out;
	}

	.coursecard:hover {
		border-radius: 10px;
		box-shadow: #00000041 0px 10px 12px 0px;
		transform: scale(1.01) translateY(-2px);
		transition: all .2s ease-out;
	}
</style>