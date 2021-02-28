<template>
	<div>
		<div
			style="width: 100%; display: flex; flex-direction: row; margin-bottom: 10px; align-items: center; box-sizing: border-box;">
			<h1 style="margin: 0px; color: white;"><span style="font-size: 20px;">欢迎 </span>{{info.sid}}, {{info.name}}
			</h1>
			<div style="flex:1"></div>
			<el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button>
		</div>
		<el-card>
			<el-tabs tabPosition="left" @tab-click="on_Tab_changed($event.label)">
				<el-tab-pane label="我的课程">
					<div
						style="margin-bottom: 20px; display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px; align-items: center;">
						<el-radio-group v-model="courseType">
							<el-radio-button label="未结束"></el-radio-button>
							<el-radio-button label="已完成"></el-radio-button>
						</el-radio-group>
					</div>
					<div v-show="courseType === '已完成'"
						style="display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px;">
						<div class="container" style="justify-content: flex-end; flex: unset;">
							<a
								style="margin-right: 10px; margin-top: 8px; font-size: 30px; font-style: italic; text-align: right;box-sizing: border-box;">{{get_Remarks.avg}}</a>
							<a
								style="margin-right: 10px;margin-right: 20px;  font-size: 60px; font-style: italic;">{{get_Remarks.avgcredit}}</a>
						</div>
						<template v-for="item in get_FinishedCourse">
							<div :key="item.cid"
								style="border-radius: 6px; box-shadow: #00000026 0px 5px 7px 0px; display: flex; flex-direction: column; padding: 10px 15px;"
								:style="{'background-color': color[item.id % color.length]}">
								<div class="container">
									<div class="vcontainer">

										<a
											style="margin-bottom: 10px; color: white; font-size: 24px; font-weight: bolder;">{{item.cname}}
											<span style="font-weight: lighter;">{{item.cid}}</span></a>
										<div class="container">
											<div class="vcontainer">
												<a style="color: white; font-size: 16px; font-weight: bolder;">{{item.tname}}
													<span style="font-weight: lighter;">{{item.tid}}</span></a>
												<a style="color: white; font-size: 16px; font-weight: lighter;">{{item.credit}}
													<span style="font-weight: bolder;">学分</span></a>
											</div>
										</div>
									</div>
									<div class="container" style="flex: unset;">
										<a
											style="margin-right: 10px; margin-top: 8px; color: white; font-size: 30px; font-style: italic;">{{item.grade}}</a>
										<a
											style="margin-right: 10px; color: white; font-size: 60px; font-style: italic;">{{get_GPA_Str(item.grade)}}</a>
									</div>
								</div>
							</div>
						</template>
					</div>
					<div v-show="courseType === '未结束'"
						style="display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px;">
						<template v-for="item in get_UnfinishedCourse">
							<div :key="item.cid"
								style="border-radius: 6px; box-shadow: #00000026 0px 5px 7px 0px; display: flex; flex-direction: column; padding: 10px 15px;"
								:style="{'background-color': color[item.id % color.length]}">
								<div class="vcontainer">

									<a style="margin-bottom: 10px; color: white; font-size: 24px; font-weight: bolder;">{{item.cname}}
										<span style="font-weight: lighter;">{{item.cid}}</span></a>
									<div class="container">
										<div class="vcontainer">
											<a style="color: white; font-size: 16px; font-weight: bolder;">{{item.tname}}
												<span style="font-weight: lighter;">{{item.tid}}</span></a>
											<a style="color: white; font-size: 16px; font-weight: lighter;">{{item.credit}}
												<span style="font-weight: bolder;">学分</span></a>
										</div>
									</div>
								</div>
							</div>
						</template>
					</div>
				</el-tab-pane>
				<el-tab-pane label="成绩单">
					<div
						style="margin-top: 10px; margin-bottom: 20px; display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px; align-items: center;">
						<canvas id="chart"></canvas>
					</div>
				</el-tab-pane>
				<el-tab-pane label="选课">
					<div
						style="display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px; align-items: center;">
						<el-transfer v-model="elect" :button-texts="['退课', '选课']" :titles="['可选', '已选']"
							:data="options">
							<div slot="right-footer"
								style="width: 100%; height: 100%;display: flex; align-items: center; justify-content: center;">

								<a
									style="text-align: center; font-size: 16px; color: #303133; font-weight: 400;">已选学分：{{get_SumCredit}}</a>

							</div>
						</el-transfer>
					</div>
					<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
						<el-button type="primary" @click="elect_Confirm()" round :disabled="!can_Elect">选</el-button>
					</div>
				</el-tab-pane>
				<el-tab-pane label="账户管理">
					<div style="padding: 0px 200px 0px 210px;">
						<el-form :model="passwordForm">
							<el-form-item prop="old" label="旧密码">
								<el-input v-model="passwordForm.old"></el-input>
							</el-form-item>
							<el-form-item prop="new" label="新密码">
								<el-input v-model="passwordForm.new"></el-input>
							</el-form-item>
						</el-form>
						<div
							style="display: flex; margin-top: 20px; flex-direction: row; align-items: center; justify-content: center;">
							<el-button type="primary" @click="set_Password()" round>重 置 密 码</el-button>
						</div>
					</div>
				</el-tab-pane>
			</el-tabs>
		</el-card>
	</div>
</template>

<script>
	import Chart from 'chart.js'

	export default {
		name: 'studenthub',
		components: {
		},
		data() {
			return {
				passwordForm: {
					old: '',
					new: ''
				},
				info: { name: '', id: '' },
				elect: [],
				haselected: [],
				options: [],
				creditmap: {},
				myCourses: [],
				courseType: '未结束',
				courseList: [],
				remarks: {
					avg: 0,
					sumcredit: 0,
					avgcredit: 0
				},
				color: ['#D32F2F', '#7B1FA2', '#303F9F', '#1976D2', '#689F38', '#FBC02D', '#FFA000', '#F57C00', '#E64A19', '#5D4037', '#111d5e', '#2f2519', '#c70039', '#184d47', '#f37121', '#ffbd69', '#b83b5e', '#3ec1d3', '#6c5b7b', '#455d7a', '#8f8787'],
				canvas: null,
				chartdata: {
					labels: [],
					datasets: [{
						label: '成绩',
						data: [],
						backgroundColor: [
							'#D32F2F', '#7B1FA2', '#303F9F', '#1976D2', '#689F38', '#FBC02D', '#FFA000', '#F57C00', '#E64A19', '#5D4037', '#111d5e', '#2f2519', '#c70039', '#184d47', '#f37121', '#ffbd69', '#b83b5e', '#3ec1d3', '#6c5b7b', '#455d7a', '#8f8787'
						],
						borderColor: [
							'#D32F2F', '#7B1FA2', '#303F9F', '#1976D2', '#689F38', '#FBC02D', '#FFA000', '#F57C00', '#E64A19', '#5D4037', '#111d5e', '#2f2519', '#c70039', '#184d47', '#f37121', '#ffbd69', '#b83b5e', '#3ec1d3', '#6c5b7b', '#455d7a', '#8f8787'
						],
						borderWidth: 2
					}]
				}
			}
		},
		computed: {
			get_SumCredit: function () {
				let sum = 0
				this.elect.forEach((i) => {
					sum += this.creditmap[i]
				})
				return sum
			},
			can_Elect: function () {
				let a = new Set(this.elect)
				let b = new Set(this.haselected)
				let difference1 = new Set([...a].filter(x => !b.has(x)))
				let difference2 = new Set([...b].filter(x => !a.has(x)))
				return !(difference1.size === 0 && difference2.size === 0)
			},
			get_FinishedCourse: function () {
				let list = this.courseList.filter((i) => {
					if (i.grade !== null) {
						return true
					}
					return false
				})
				return list
			},
			get_Remarks: function () {
				let sum = 0
				let count = 0
				let sumcredit = 0
				this.courseList.filter((i) => {
					if (i.grade !== null) {
						sum += i.grade
						count++
						sumcredit += this.get_GPA(i.grade)
						return true
					}
					return false
				})
				return count === 0 ? {
					avg: 0,
					sumcredit: 0,
					avgcredit: 0
				} : {
						avg: Math.round(sum * 100 / count) / 100,
						sumcredit: sumcredit,
						avgcredit: Math.round(sumcredit * 100 / count) / 100
					}
			},
			get_UnfinishedCourse: function () {
				return this.courseList.filter((i) => {
					return i.grade === null
				})
			}
		},
		methods: {
			logout() {
				localStorage.login = JSON.stringify({})
				this.$router.go(-1)
			},
			elect_Confirm() {
				let a = new Set(this.elect)
				let b = new Set(this.haselected)
				let remove = new Set([...b].filter(x => !a.has(x)))
				let add = new Set([...a].filter(x => !b.has(x)))
				this.$axios.post("http://127.0.0.1:8000/course/elect/", { remove: Array.from(remove), add: Array.from(add), id: this.info.id })
					.then(res => {
						// console.log(res.data)
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
						}
						else {
							if (res.data.data.length > 0) {
								res.data.data.forEach((i) => {
									this.$message.success({
										message: i,
										showClose: true
									})
								})
							}
							else {
								this.$message.success({
									message: '选课成功',
									showClose: true
								})
							}
						}
						this.on_Tab_changed('选课')
					})
			},
			set_Password() {
				this.$axios.post("http://127.0.0.1:8000/students/setPassword/", { id: this.info.id, old: this.passwordForm.old, new: this.passwordForm.new })
					.then(res => {
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
						}
						else {
							this.$message.success({
								message: res.data.data,
								showClose: true
							});
							this.logout()
						}
					})
			},
			on_Tab_changed(tab) {
				if (tab === '选课') {
					this.$axios.post("http://127.0.0.1:8000/course/getStudent/", { id: this.info.id })
						.then(res => {
							// console.log(res.data)
							if (res.data.state === 'failed') {
								this.$message.error({
									message: res.data.data,
									showClose: true
								});
							}
							else {
								this.creditmap = {}
								this.options = res.data.list.map((i) => {
									this.creditmap[i.id] = i.credit
									return { label: `${i.cid} ${i.name} 教师：${i.tid} ${i.tname} 学分：${i.credit}`, key: i.id, credit: i.credit }
								})
								this.elect = res.data.elected.map((i) => {
									return i.cid_id
								})
								this.haselected = res.data.elected.map((i) => {
									return i.cid_id
								})
							}
						})
				}
				else if (tab === '我的课程') {
					this.$axios.post("http://127.0.0.1:8000/students/getCourse/", { id: this.info.id })
						.then(res => {
							// console.log(res.data)
							if (res.data.state === 'failed') {
								this.$message.error({
									message: res.data.data,
									showClose: true
								});
							}
							else {
								this.courseList = res.data.list
								let label = []
								let data = []
								let color = []
								this.courseList.filter(i => i.grade !== null).forEach(i => {
									label.push(i.cname)
									data.push(i.grade)
									color.push(this.color[i.id % this.color.length])
								})
								this.chartdata.labels = label
								this.chartdata.datasets[0].data = data
								this.chartdata.datasets[0].borderColor = color
								this.chartdata.datasets[0].backgroundColor = color
								this.canvas.update()
							}
						})
				}
			},
			get_GPA: function (i) {
				if (i < 60) return 0
				if (i < 63) return 1.0
				if (i < 67) return 1.7
				if (i < 71) return 2.0
				if (i < 74) return 2.3
				if (i < 77) return 2.7
				if (i < 81) return 3.0
				if (i < 84) return 3.3
				if (i < 89) return 3.7
				return 4.0
			},
			get_GPA_Str: function (i) {
				if (i < 60) return '0.0'
				if (i < 63) return '1.0'
				if (i < 67) return '1.7'
				if (i < 71) return '2.0'
				if (i < 74) return '2.3'
				if (i < 77) return '2.7'
				if (i < 81) return '3.0'
				if (i < 84) return '3.3'
				if (i < 89) return '3.7'
				return '4.0'
			}
		},
		mounted() {
			this.info = JSON.parse(localStorage.login)
			this.on_Tab_changed('我的课程')
			let ctx = document.getElementById('chart')
			this.canvas = new Chart(ctx, {
				type: 'bar',
				data: this.chartdata,
				options: {
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true
							}
						}]
					}
				}
			})
		}
	}
</script>

<style>
	.el-transfer-panel {
		width: 350px;
		height: 350px;
		margin-bottom: 20px;
	}

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
</style>