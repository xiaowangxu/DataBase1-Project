<template>
	<div style="display: flex; flex-direction: column; height: 100%;">

		<div style=" width: 100%; display: flex; flex-direction: row; margin-bottom: 10px; align-items: center; box-sizing:
				border-box;">
			<h1 style="margin: 0px; color: white;">{{info.sid}},
				{{info.name}}
			</h1>
			<div style="flex:1"></div>
			<el-button size="medium" round disabled>当前学期：{{currentTerm}}
			</el-button>
			<el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出
			</el-button>
		</div>

		<div
			style="background-color: white; flex:1; position: fixed; top: 140px; left: 280px; right: 200px; bottom: 80px; border-radius: 10px; box-shadow: rgb(0 0 0 / 7%) 0px 5px 9px 9px; overflow: hidden; display: flex; flex-direction: row;">
			<div style="margin: 12px; position: absolute; top: 0; right: 0; bottom: 0; left: 0; flex: 1; overflow: hidden;"
				tabPosition="left" @tab-click="on_Tab_changed($event.label)">

				<div v-if="currentTab === 'courses'"
					style="display: flex; flex-direction: column; gap: 12px; overflow: visible; height: 100%;">
					<div style="display: flex; flex-direction: row; justify-content: flex-end; gap: 20px;">
						<div v-if="selectedTerm !== currentTerm"
							style="padding: 10px 12px 0px 12px ; display: flex; flex-direction: row; gap: 30px;">
							<a style="font-weight: bolder; font-family: consolas; font-size: 30px; font-style: italic;">
								<a
									style="font-style: normal; font-size: 20px; margin-right: 2px;">平均成绩</a>{{get_Remarks.avg}}</a>
							<a style="font-weight: bolder; font-family: consolas; font-size: 30px; font-style: italic;">
								<a
									style="font-style: normal; font-size: 20px; margin-right: 2px;">绩点</a>{{get_Remarks.sumcredit}}</a>
							<a style="font-weight: bolder; font-family: consolas; font-size: 30px; font-style: italic;">
								<a
									style="font-style: normal; font-size: 20px; margin-right: 2px;">均绩</a>{{get_Remarks.avgcredit}}</a>
						</div>
						<el-select style="align-self: flex-end; margin: 10px 10px 0px 0px; justify-self: flex-end;"
							v-model="selectedTerm" placeholder="请选择" @change="switch_Term($event)">
							<el-option v-for="item in termList" :key="item.term" :label="item.term" :value="item.term">
							</el-option>
						</el-select>
					</div>
					<div
						style="display: flex; flex-direction: row; gap: 20px; box-sizing: content-box; ; flex-wrap: wrap; overflow: auto; overflow: auto; padding: 10px; flex: 1; align-content:flex-start;">
						<template v-for="item in courseList">
							<div class="coursecard" :key="item.cid"
								style="flex:1; display: flex; flex-direction: column; padding: 10px 15px"
								:style="{'background': `linear-gradient(45deg, ${Color[(item.id) % Color.length][0]}, ${Color[(item.id) % Color.length][1]})`}">

								<div class="container"
									style="display: flex; flex-direction: row; justify-content: space-between; flex: 1; gap: 20px;">
									<div class="vcontainer">

										<a
											style="color: white; font-size: 24px; font-weight: bolder; word-break: keep-all;">{{item.cname}}
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
									<div class="container"
										style="justify-content: center; flex: unset; flex-direction: column; gap: 13px; align-items: flex-end; padding: 5px 0px; justify-content: flex-start;">
										<div v-if="item.term
											=== currentTerm" style="background-color: white; padding: 5px 12px 5px 11px; border-radius: 5px; height: min-content;">
											<a style="font-weight: bolder; font-family: consolas;"
												:style="{'font-size': '30px', 'color': Color[(item.id) % Color.length][1]}">{{'进行中'}}</a>

											<!-- <a v-else style="font-weight: bolder; font-family: consolas;"
												:style="{'font-size': '30px', 'font-style': 'italic', 'color': Color[(item.id) % Color.length][1]}">{{get_GPA_Str(item.grade)}}</a> -->
										</div>
										<template v-else>
											<div
												style="background-color: white; padding: 5px 12px 5px 11px; border-radius: 5px; height: min-content; align-self: flex-end;">
												<a style="font-weight: bolder; font-family: consolas;"
													:style="{'font-size': '30px', 'font-style': 'italic', 'color': Color[(item.id) % Color.length][1]}">
													<a
														style="font-style: normal; font-size: 20px; margin-right: 2px;">成绩</a>{{item.grade}}</a>
											</div>
											<div
												style="background-color: white; padding: 5px 12px 5px 11px; border-radius: 5px; height: min-content; align-self: center;">
												<a style="font-weight: bolder; font-family: consolas;"
													:style="{'font-size': '30px', 'font-style': 'italic', 'color': Color[(item.id) % Color.length][1]}">
													<a
														style="font-style: normal; font-size: 20px; margin-right: 2px;">绩点</a>{{get_GPA_Str(item.grade)}}</a>
											</div>
										</template>

										<!-- <div style="display: flex; flex-direction: row; gap: 10px;">
											<el-button v-if="item.term !== currentTerm" size="small" icon="el-icon-more"
												circle style="margin: none;align-self: flex-end;"
												@click="gradeinput(item)">
											</el-button>
											<el-button v-else style="align-self: flex-end;" type="success" size="small"
												icon="el-icon-plus" round @click="gradeinput(item)">
												成绩填报
											</el-button>

										</div> -->

									</div>
								</div>
							</div>
						</template>
					</div>
				</div>

				<div v-show="currentTab === 'grade'"
					style="display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 10px 0px 10px; align-items: center; height: 100%; justify-content: space-between;">
					<div style="padding: 10px 12px 0px 12px ; display: flex; flex-direction: row; gap: 30px;">
						<a style="font-weight: bolder; font-family: consolas; font-size: 30px; font-style: italic;">
							<a style="font-style: normal; font-size: 20px; margin-right: 2px;">平均成绩</a>{{grade.avg}}</a>
						<a style="font-weight: bolder; font-family: consolas; font-size: 30px; font-style: italic;">
							<a style="font-style: normal; font-size: 20px; margin-right: 2px;">平均绩点</a>{{grade.gpa}}</a>
						<!-- <a style="font-weight: bolder; font-family: consolas; font-size: 30px; font-style: italic;">
							<a
								style="font-style: normal; font-size: 20px; margin-right: 2px;">均绩</a>{{get_Remarks.avgcredit}}</a> -->
					</div>
					<div style="height: 100%; width: 100%;"><canvas ref="courseChart1"></canvas></div>


				</div>

				<div v-if="currentTab === 'profile'" style="padding: 10px;">
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
						<el-button type="primary" @click="set_Password()" round>重置密码</el-button>
					</div>
				</div>
			</div>
		</div>

		<div
			style="position: fixed; left: 180px; width: 80px; top: 150px; display: flex; flex-direction: column; gap: 10px;">
			<div class="tabs" :class="{'selected': currentTab==='courses'}" @click="currentTab ='courses'">
				<a style="margin: auto; line-height: 12px;">课程</a>
			</div>
			<div class="tabs" :class="{'selected': currentTab==='grade'}" @click="currentTab ='grade'">
				<a style="margin: auto; line-height: 12px;">成绩</a>
			</div>
			<div class="tabs" :class="{'selected': currentTab==='profile'}" @click="currentTab ='profile'">
				<a style="margin: auto; line-height: 12px;">账户</a>
			</div>
		</div>

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
				currentTab: 'courses',
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
				currentTerm: undefined,
				selectedTerm: undefined,
				termList: [],

				grade: {
					avg: 0,
					gpa: 0
				},

				courseType: '未结束',
				courseList: [],
				remarks: {
					avg: 0,
					sumcredit: 0,
					avgcredit: 0
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
				],
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
				let totalcredit = 0
				let sumcredit = 0
				let sumt = 0
				this.courseList.filter((i) => {
					if (i.grade !== null) {
						sum += i.grade
						count++
						sumt += i.credit
						sumcredit += this.get_GPA(i.grade) * i.credit
						totalcredit += i.credit
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
					sumcredit: sumt,
					avgcredit: Math.round(sumcredit / totalcredit * 100) / 100
				}
			},
			get_UnfinishedCourse: function () {
				return this.courseList.filter((i) => {
					return i.grade === null
				})
			}
		},
		methods: {
			load_Courses() {
				this.$axios.post("http://127.0.0.1:8000/students/getCourseTerm/", { id: this.info.id })
					.then(res => {
						console.log(res.data)
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
							return false
						}
						else {
							this.termList = res.data.list
							this.currentTerm = res.data.current
							return true
						}
					}).then((res) => {
						console.log(res)
						if (res) {
							if (!this.termList.map(t => t.term).includes(this.selectedTerm)) {
								this.selectedTerm = this.termList[0].term
							}
							this.get_Course(this.info.id, this.selectedTerm)
						}
					})
			},
			load_Grades() {
				this.$axios.post("http://127.0.0.1:8000/students/getGPAs/", { id: this.info.id })
					.then(res => {
						console.log(res.data)
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
						}
						else {
							let list = res.data.list
							if (list.length === 0) return
							this.grade.avg = Math.round(list.reduce((a, i) => { return a + i.avg }, 0) / list.length * 100) / 100
							this.grade.gpa = Math.round(list.reduce((a, i) => { return a + i.gpa }, 0) / list.length * 100) / 100
							this.chart2 = new Chart(this.$refs.courseChart1, {
								type: 'line',
								data: {
									labels: list.map(i => i.term),
									datasets: [{
										label: 'GPA',
										data: list.map(i => i.gpa),
										fill: false,
										borderColor: 'rgb(75, 192, 192)',
										tension: 0.1
									}]
								},
								options: {
									scales: {
										y: {
											beginAtZero: true
										}
									}
								}
							})
						}
					})
			},
			get_Course(id, term) {
				let param = { id: id, term: term }
				return this.$axios.post("http://127.0.0.1:8000/students/getCourse/", param)
					.then(res => {
						console.log(res.data)
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
						}
						else {
							this.courseList = res.data.list
						}
					})
			},
			switch_Term() {
				console.log(this.selectedTerm)
				this.get_Course(this.info.id, this.selectedTerm)
			},
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
				else if (tab === '我的课程' || tab === '成绩单') {
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
			get_GPA(i) {
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
			get_GPA_Str(i) {
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
			this.load_Courses()
			this.load_Grades()
		}
	}
</script>

<style>
	.slide-fade-enter-active {
		transition: all .2s ease-out;
	}

	.slide-fade-leave-active {
		transition: all .2s ease-out;
	}

	.slide-fade-enter {
		transform: translateX(100%);
		opacity: 0.5;
	}

	.slide-fade-leave-to {
		transform: translateX(100%);
		opacity: 0.5;
	}

	.slide-fade2-enter-active {
		transition: all .2s ease-out;
	}

	.slide-fade2-leave-active {
		transition: all .2s ease-out;
	}

	.slide-fade2-enter {
		transform: translateX(-100%);
		opacity: 0.5;
	}

	.slide-fade2-leave-to {
		transform: translateX(-100%);
		opacity: 0.5;
	}

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

	.tabs {
		padding: 12px 0px;
		border-radius: 6px;
		display: flex;
		user-select: none;
		flex-direction: column;
		align-content: center;
		color: rgb(5, 47, 182);
		box-shadow: rgba(63, 106, 226, 0.26) 0px 5px 7px 0px;
		background: linear-gradient(45deg, rgb(255, 255, 255), rgb(255, 255, 255));
		transform: scale(1) translateX(0px);
		transition: all .2s ease-out;
	}

	.tabs.selected {
		background: linear-gradient(45deg, rgb(36, 111, 250), rgb(5, 47, 182));
		box-shadow: #406a8654 0px 5px 7px 0px;
		color: white;
		transform: scale(1) translateY(0px);
		transition: all .2s ease-out;
	}

	.tabs.selected:hover {
		background: linear-gradient(45deg, rgb(36, 111, 250), rgb(5, 47, 182));
		box-shadow: #24567754 0px 3px 3px 0px;
		color: white;
		transform: scale(0.96) translateY(1px);
		transition: all .1s ease-out;
	}

	.tabs.selected:active {
		background: linear-gradient(45deg, rgb(36, 111, 250), rgb(5, 47, 182));
		box-shadow: #406a8654 0px 1px 2px 0px;
		color: white;
		transform: scale(0.94) translateY(2px);
		transition: all .2s ease-out;
	}

	.tabs:hover {
		box-shadow: #00000041 0px 10px 12px 0px;
		transform: scale(1.01) translateY(-1px);
		transition: all .2s ease-out;
	}

	.tabs:active {
		box-shadow: #0c269b54 0px 2px 6px 0px;
		transform: scale(0.95) translateY(1px);
		transition: all .1s ease-out;
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