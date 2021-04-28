<template>
	<div style="display: flex; flex-direction: column; gap: 10px; max-height: 100%; box-sizing: border-box;">
		<div
			style="width: 100%; display: flex; flex-direction: row; align-items: center; box-sizing: border-box; gap: 20px;">
			<el-button style="align-self: flex-start;" size="medium" icon="el-icon-top-left" round
				@click="$emit('back')">返回
			</el-button>


			<div style="flex: 1; border-radius: 10px; box-shadow: #00000026 0px 5px 7px 0px; display: flex; flex-direction: column; padding: 10px 15px"
				:style="{'background': `linear-gradient(45deg, ${colors.color1}, ${colors.color2})`}">
				<div class="container"
					style="display: flex; flex-direction: row; justify-content: space-between; flex: 1; gap: 20px;">
					<div class="vcontainer">

						<a style="color: white; font-size: 24px; font-weight: bolder; word-break: keep-all;">{{courseinfo.name}}
							<span style="font-weight: lighter;">{{courseinfo.cid}}</span></a>
						<div class="container">
							<div class="container" style="gap: 10px;">
								<a style="color: white; font-size: 16px; font-weight: lighter;">{{courseinfo.credit}}
									<span style="font-weight: bolder;">学分</span></a>
							</div>

						</div>

					</div>
					<div class="container"
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
					</div>
				</div>

			</div>

		</div>
		<div v-if="readonly"
			style="flex: 1; width: 100%; display: flex; flex-direction: row; gap: 20px; max-height: 100%; height: 100px;">

			<el-table :data="studentList"
				style="width: 100%; flex:1; overflow-y: auto; font-weight: bolder; font-size: 16px;"
				:default-sort="{prop:'sid', order:'ascending'}">
				<el-table-column prop="sid" label="学号" sortable>
				</el-table-column>
				<el-table-column prop="name" label="姓名" sortable>
				</el-table-column>
				<el-table-column prop="grade" label="成绩" sortable>
				</el-table-column>
			</el-table>
			<div style="width: 50%; display: flex; flex-direction: column; overflow-y: auto; overflow-x: hidden;">
				<canvas ref="courseChart1"></canvas>
				<canvas ref="courseChart2"></canvas>
			</div>
		</div>
		<el-table v-else :data="studentList"
			style="width: 100%; flex:1; overflow-y: auto; font-weight: bolder; font-size: 16px;"
			:default-sort="{prop:'sid', order:'ascending'}">
			<el-table-column prop="sid" label="学号" sortable>
			</el-table-column>
			<el-table-column prop="name" label="姓名" sortable>
			</el-table-column>
			<el-table-column v-if="!readonly" prop="grade" label="成绩" width="140" sortable
				:filters="[{text: '已填写', value: true}, {text: '未填写', value: false}]" :filter-method="filter_Grade">
				<template slot-scope="scope">
					<el-input type="number" min="0" max="100" step="1" v-model.number="scope.row.grade">
					</el-input>
				</template>
			</el-table-column>
		</el-table>

		<el-button v-if="!readonly" style="align-self: flex-end; margin-top: 10px;" type="primary"
			@click="update_Grade()" round>上 传
		</el-button>
	</div>
</template>

<script>
	import Chart from 'chart.js'

	export default {
		name: 'teacherhub2',
		components: {
		},
		props: {
			readonly: {
				type: Boolean,
				default: true
			},
			id: {
				type: Number,
				default: -2
			},
			colors: {
				type: Object,
				default: () => {
					return {
						color1: 'black',
						color2: 'black'
					}
				}
			},
			courseinfo: {
				type: Object,
				default: () => {
					return {
						avg: -1,
						cid: "unknown",
						credit: -1,
						depart: "unknown",
						id: -1,
						name: "unknown",
						tid: "unknown",
						tname: "unknown",
						tuid: -1
					}
				}
			}
		},
		data() {
			return {
				applyDialog: false,
				courseForm: {
					cid: '',
					name: '',
					credit: 1
				},
				applyDialogRules: {
					cid: [
						{ required: true, message: '请输入课号', trigger: 'blur' },
						{ min: 1, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
					],
					name: [
						{ required: true, message: '请输入课名', trigger: 'blur' },
						{ min: 1, max: 50, message: '长度在 3 到 50 个字符', trigger: 'blur' }
					]
				},
				passwordForm: {
					old: '',
					new: ''
				},
				info: { name: '', id: '' },
				selectedCourse: undefined,
				selectedTerm: undefined,
				courseList: [],
				termList: [],
				studentList: [],
				applyCourseList: [],
				studentListOld: [],
				// color: ['#D32F2F', '#7B1FA2', '#303F9F', '#1976D2', '#689F38', '#FBC02D', '#FFA000', '#F57C00', '#E64A19', '#5D4037', '#111d5e', '#2f2519', '#c70039', '#184d47', '#f37121', '#ffbd69', '#b83b5e', '#3ec1d3', '#6c5b7b', '#455d7a', '#8f8787'],
				color: ['#9b1645', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#00bcd4', '#009688', '#59662c', '#9fa328', '#ffdd00', '#ff9800', '#ff5722'],
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
			get_Avg: function () {
				if (this.studentList.length === 0) return "NaN"
				else {
					let sum = this.studentList.reduce((sum, i) => {
						return sum + i.grade
					}, 0)
					return Math.round((sum / this.studentList.length) * 100) / 100
				}
			}
		},
		methods: {
			get_Course(id, term) {
				let param = { id: id, term: term }
				return this.$axios.post("http://127.0.0.1:8000/teacher/getCourse/", param)
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
							// console.log(res.data)
							let label = []
							let data = []
							let color = []
							this.courseList.forEach(i => {
								label.push(i.name)
								data.push(i.avg)
								color.push(this.color[i.id % this.color.length])
							})
							this.chartdata.labels = label
							this.chartdata.datasets[0].data = data
							this.chartdata.datasets[0].borderColor = color
							this.chartdata.datasets[0].backgroundColor = color
							this.canvas.update()
						}
					})
			},
			logout() {
				localStorage.login = JSON.stringify({})
				this.$router.go(-1)
			},
			set_Password() {
				this.$axios.post("http://127.0.0.1:8000/teacher/setPassword/", { id: this.info.id, old: this.passwordForm.old, new: this.passwordForm.new })
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
				if (tab === '我的课程') {
					this.$axios.post("http://127.0.0.1:8000/teacher/getCourseTerm/", { id: this.info.id })
						.then(res => {
							// console.log(res.data)
							if (res.data.state === 'failed') {
								this.$message.error({
									message: res.data.data,
									showClose: true
								});
								return false
							}
							else {
								this.termList = res.data.list
								return true
							}
						}).then((res) => {
							if (res) {
								if (this.selectedTerm === undefined) {
									this.selectedTerm = this.termList[0].term
								}
								this.get_Course(this.info.id, this.selectedTerm)
							}
						})


				}
				else if (tab === '成绩填报' && this.selectedCourse !== undefined) {
					this.switch_Course(this.selectedCourse)
				}
				else if (tab === '课程申请') {
					this.$axios.post("http://127.0.0.1:8000/teacher/getApplyCourse/", { id: this.info.id })
						.then(res => {
							// console.log(res.data)
							if (res.data.state === 'failed') {
								this.$message.error({
									message: res.data.data,
									showClose: true
								});
							}
							else {
								this.applyCourseList = res.data.list
							}
						})
				}
			},
			switch_Course(id) {
				this.$axios.post("http://127.0.0.1:8000/teacher/getCourseGrade/", { id: id })
					.then(res => {
						// console.log(res.data)
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
						}
						else {
							this.studentList = res.data.list
							this.studentListOld = res.data.list.map((i) => { return i.grade })
							if (this.readonly) {
								let data = Array(100).fill(0)
								this.studentList.forEach((i) => {
									data[Math.round(i.grade) - 1]++;
								})
								console.log(data)
								this.chart1 = new Chart(this.$refs.courseChart1, {
									type: 'bar',
									data: {
										labels: data.map((i, idx) => idx + 1),
										datasets: [{
											label: "人数",
											data: data,
											backgroundColor: data.map(() => this.colors.color2),
											borderWidth: 1
										}]
									},
									options: {
										scales: {
											y: {
												beginAtZero: false
											}
										}
									}
								})
							}
						}
					})
			},
			switch_Term() {
				this.get_Course(this.info.id, this.selectedTerm)
			},
			update_Grade() {
				let list = this.studentList.filter((i, idx) => {
					return i.grade !== this.studentListOld[idx]
				}).map((i) => {
					return { id: i.euid, grade: i.grade === '' ? '' : Math.max(Math.min(100, i.grade)) }
				})
				console.log(list)
				if (list.length <= 0) return
				this.$axios.post("http://127.0.0.1:8000/teacher/updateGrade/", { cuid: this.selectedCourse, list: list })
					.then(res => {
						// console.log(res.data)
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
						}
						else {
							this.$message.success({
								message: '更新成功',
								showClose: true
							});
						}
					})
			},
			apply_Course() {
				let data = {
					cid: this.courseForm.cid,
					name: this.courseForm.name,
					credit: this.courseForm.credit,
					tid: this.info.id
				}
				this.$refs.applyForm.validate((valid) => {
					if (valid) {
						this.$axios.post("http://127.0.0.1:8000/teacher/applyCourse/", data)
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
									this.reset_Form("applyForm")
									this.applyDialog = false;
									this.on_Tab_changed('课程申请')
								}
							})
					} else {
						this.$message.error({
							message: "表单部分内容有误",
							showClose: true
						})
					}
				});
			},
			delete_Application(row) {
				this.$axios.post("http://127.0.0.1:8000/teacher/deletApplyCourse/", { id: row.id })
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
							this.on_Tab_changed('课程申请')
						}
					})

			},
			reset_Form(formName) {
				this.$refs[formName].resetFields();
			},
			filter_Grade(value, row) {
				if (value) {
					return row.grade !== ''
				}
				else {
					return row.grade === ''
				}

			}
		},
		mounted() {
			this.info = JSON.parse(localStorage.login)
			// this.chart2 = new Chart(this.$refs.courseChart2, {
			// 	type: 'line',
			// 	data: {
			// 		labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
			// 		datasets: [{
			// 			label: '# of Votes',
			// 			data: [12, 19, 3, 5, 2, 3],
			// 			backgroundColor: [
			// 				this.colors.color2,
			// 				this.colors.color2,
			// 				this.colors.color2,
			// 				'rgba(75, 192, 192, 0.2)',
			// 				'rgba(153, 102, 255, 0.2)',
			// 				'rgba(255, 159, 64, 0.2)'
			// 			],
			// 			borderColor: [
			// 				this.colors.color1,
			// 				'rgba(54, 162, 235, 1)',
			// 				'rgba(255, 206, 86, 1)',
			// 				'rgba(75, 192, 192, 1)',
			// 				'rgba(153, 102, 255, 1)',
			// 				'rgba(255, 159, 64, 1)'
			// 			],
			// 			borderWidth: 1
			// 		}]
			// 	},
			// 	options: {
			// 		scales: {
			// 			y: {
			// 				beginAtZero: true
			// 			}
			// 		}
			// 	}
			// })
			this.switch_Course(this.id)
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