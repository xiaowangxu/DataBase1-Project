<template>
	<div style="display: flex; flex-direction: column; height: 100%;">

		<div style=" width: 100%; display: flex; flex-direction: row; margin-bottom: 10px; align-items: center; box-sizing:
				border-box;">
			<h1 style="margin: 0px; color: white;">{{info.tid}},
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

			<transition name="slide-fade2">
				<div v-if="page==='main'"
					style="margin: 12px; position: absolute; top: 0; right: 0; bottom: 0; left: 0; flex: 1; overflow: hidden;"
					tabPosition="left" @tab-click="on_Tab_changed($event.label)">

					<div v-if="currentTab === 'courses'"
						style="display: flex; flex-direction: column; gap: 12px; overflow: visible; height: 100%;">
						<el-select style="align-self: flex-end; margin: 10px 10px 0px 0px;" v-model="selectedTerm"
							placeholder="请选择" @change="switch_Term($event)">
							<el-option v-for="item in termList" :key="item.term" :label="item.term" :value="item.term">
							</el-option>
						</el-select>
						<div
							style="display: flex; flex-direction: row; gap: 20px; box-sizing: content-box; ; flex-wrap: wrap; overflow: auto; overflow: auto; padding: 10px; flex: 1; align-content:flex-start;">
							<template v-for="item in courseList">
								<div class="coursecard" :key="item.cid"
									style="flex:1; display: flex; flex-direction: column; padding: 10px 15px"
									:style="{'background': `linear-gradient(45deg, ${color[item.id**3 % color.length]}, ${color[(item.id**3+1) % color.length]})`}">

									<div class="container"
										style="display: flex; flex-direction: row; justify-content: space-between; flex: 1; gap: 20px;">
										<div class="vcontainer">

											<a
												style="color: white; font-size: 24px; font-weight: bolder; word-break: keep-all;">{{item.name}}
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
											style="justify-content: center; flex: unset; flex-direction: column; gap: 13px; align-items: flex-end; padding-top: 5px; justify-content: space-between;">
											<div
												style="width:min-content; background-color: white; padding: 5px 12px 5px 11px; border-radius: 5px; height: min-content;">
												<a style="font-weight: bolder; font-family: consolas;"
													:style="{'font-size': '30px', 'font-style': 'italic', 'color': color[(item.id**3+1) % color.length]}">{{Math.round(item.avg*100)/100}}</a>
											</div>
											<div style="display: flex; flex-direction: row; gap: 10px;">
												<el-button v-if="item.term !== currentTerm" size="small"
													icon="el-icon-more" circle
													style="margin: none;align-self: flex-end;"
													@click="gradeinput(item)">
												</el-button>
												<el-button v-else style="align-self: flex-end;" type="success"
													size="small" icon="el-icon-plus" round @click="gradeinput(item)">
													成绩填报
												</el-button>

											</div>

										</div>
									</div>
								</div>
							</template>
						</div>
						<!-- <div
								style="flex: 1; display: flex; flex-direction: column; align-items: center;justify-content: center;">
								<canvas sty id="chart"></canvas>
							</div> -->
					</div>

					<div v-if="currentTab === 'apply'"
						style="display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px; align-items: center;">
						<el-button style="margin: 10px 10px 0px 0px; align-self: flex-end;" type="success" size="medium"
							icon="el-icon-plus" round @click="applyDialog = true">
							新建申请
						</el-button>
						<div style="flex:1;width: 100%;">
							<el-table :data="applyCourseList" style="flex:1;width: 100%">
								<el-table-column prop="cid" label="课号">
								</el-table-column>
								<el-table-column prop="name" label="课名">
								</el-table-column>
								<el-table-column prop="term" label="学期">
								</el-table-column>
								<el-table-column prop="credit" label="学分">
								</el-table-column>
								<el-table-column label="操作" width="70">
									<template slot-scope="scope">
										<el-button @click="delete_Application(scope.row)" type="danger" size="small"
											icon="el-icon-delete" circle></el-button>
									</template>
								</el-table-column>
							</el-table>
						</div>
					</div>

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
				</div>

				<!-- </el-card> -->
			</transition>
			<transition name="slide-fade">
				<teacher v-if="page==='gradeinput'"
					style="margin: 22px; position: relative; top: 0px; flex: 1; position: absolute;  top: 0; right: 0; bottom: 0; left: 0;"
					:colors="{color1: gradeinput_course.color1, color2: gradeinput_course.color2}"
					:id="gradeinput_course.id" :courseinfo="gradeinput_course.info"
					:readonly="gradeinput_course.readonly" @back="page = 'main'">
				</teacher>
			</transition>
		</div>

		<div
			style="position: fixed; left: 180px; width: 80px; top: 150px; display: flex; flex-direction: column; gap: 10px;">
			<div class="tabs" :class="{'selected': currentTab==='courses'}" @click="currentTab ='courses'">
				<a style="margin: auto; line-height: 12px;">课程</a>
			</div>
			<div class="tabs" :class="{'selected': currentTab==='apply'}" @click="currentTab ='apply'">
				<a style="margin: auto; line-height: 12px;">开课</a>
			</div>
			<div class="tabs" :class="{'selected': currentTab==='profile'}" @click="currentTab ='profile'">
				<a style="margin: auto; line-height: 12px;">账户</a>
			</div>
		</div>

		<el-dialog :visible.sync="applyDialog" width="400px">
			<el-form :model=" courseForm" :rules="applyDialogRules" ref="applyForm" class="demo-ruleForm">
				<el-form-item label="课号" prop="cid">
					<el-input v-model="courseForm.cid"></el-input>
				</el-form-item>
				<el-form-item label="课名" prop="name">
					<el-input v-model="courseForm.name"></el-input>
				</el-form-item>
				<el-form-item label="学分" prop="credit">
					<el-input-number v-model="courseForm.credit" :min="0" :max="10"></el-input-number>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="applyDialog = false" round>取 消</el-button>
				<el-button type="primary" @click="apply_Course()" round>确 定</el-button>
			</div>
		</el-dialog>
	</div>
</template>

<script>
	// import Chart from 'chart.js'
	import T from './../components/TeacherHubGradeInput.vue'

	export default {
		name: 'teacherhub',
		components: {
			teacher: T
		},
		data() {
			return {
				page: 'main',
				currentTab: 'courses',
				gradeinput_course: {
					color1: "red",
					color2: "red",
					id: -1
				},

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
				currentTerm: undefined,
				selectedCourse: undefined,
				selectedTerm: undefined,
				courseList: [],
				termList: [],
				applyCourseList: [],
				color: ['#9b1645', '#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#00bcd4', '#009688', '#59662c', '#9fa328', '#ffdd00', '#ff9800', '#ff5722'],
			}
		},
		watch: {
			currentTab() {
				this.page = "main"
				switch (this.currentTab) {
					case 'courses': {
						this.load_Courses()
						return
					}
					case 'apply': {
						this.load_Applications()
						return
					}
				}
			},
			page() {
				switch (this.currentTab) {
					case 'courses': {
						this.load_Courses()
						return
					}
					case 'apply': {
						this.load_Applications()
						return
					}
				}
			}
		},
		computed: {
			get_CourseOptions: function () {
				return this.courseList.map((i) => {
					return { label: `${i.cid} ${i.name}`, value: i.id }
				})
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
			load_Courses() {
				this.$axios.post("http://127.0.0.1:8000/teacher/getCourseTerm/", { id: this.info.id })
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
						if (res) {
							if (!this.termList.map(t => t.term).includes(this.selectedTerm)) {
								this.selectedTerm = this.termList[0].term
							}
							this.get_Course(this.info.id, this.selectedTerm)
						}
					})
			},
			load_Applications() {
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
			},
			gradeinput(item) {
				// console.log(item)
				this.gradeinput_course = {
					color1: this.color[(item.id ** 3) % this.color.length],
					color2: this.color[(item.id ** 3 + 1) % this.color.length],
					id: item.id,
					readonly: item.term !== this.currentTerm,
					info: item
				}
				this.page = 'gradeinput'
			},
			switch_Term() {
				this.get_Course(this.info.id, this.selectedTerm)
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
									this.load_Applications()
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
							this.load_Courses()
						}
					})

			},
			reset_Form(formName) {
				this.$refs[formName].resetFields();
			}
		},
		mounted() {
			this.info = JSON.parse(localStorage.login)
			this.load_Courses();
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
		color: rgb(247, 38, 101);
		box-shadow: rgba(63, 106, 226, 0.26) 0px 5px 7px 0px;
		background: linear-gradient(45deg, rgb(255, 255, 255), rgb(255, 255, 255));
		transform: scale(1) translateX(0px);
		transition: all .2s ease-out;
	}

	.tabs.selected {
		background: linear-gradient(45deg, rgb(207, 43, 133), rgb(247, 139, 38));
		box-shadow: #9b510c54 0px 5px 7px 0px;
		color: white;
		transform: scale(1) translateY(0px);
		transition: all .2s ease-out;
	}

	.tabs.selected:hover {
		background: linear-gradient(45deg, rgb(207, 43, 133), rgb(247, 139, 38));
		box-shadow: #9b510c54 0px 5px 7px 0px;
		color: white;
		transform: scale(1) translateY(0px);
		transition: all .1s ease-out;
	}

	.tabs.selected:active {
		background: linear-gradient(45deg, rgb(207, 43, 133), rgb(247, 139, 38));
		box-shadow: #9b510c54 0px 5px 7px 0px;
		color: white;
		transform: scale(1) translateY(0px);
		transition: all .1s ease-out;
	}

	.tabs:hover {
		box-shadow: #00000041 0px 10px 12px 0px;
		transform: scale(1.01) translateY(-1px);
		transition: all .2s ease-out;
	}

	.tabs:active {
		box-shadow: #9b510c54 0px 2px 6px 0px;
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

	.el-tabs__header.is-left {
		position: sticky;
		top: 0;
	}
</style>