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
			style="background-color: white; flex:1; position: fixed; top: 140px; left: 300px; right: 200px; bottom: 80px; border-radius: 10px; box-shadow: rgb(0 0 0 / 7%) 0px 5px 9px 9px; overflow: hidden; display: flex; flex-direction: row;">

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
									:style="{'background': `linear-gradient(45deg, ${Color[(item.id) % Color.length][0]}, ${Color[(item.id) % Color.length][1]})`}">

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
												style="background-color: white; padding: 5px 12px 5px 11px; border-radius: 5px; height: min-content;">
												<a style="font-weight: bolder; font-family: consolas;"
													:style="{'font-size': '30px', 'font-style': 'italic', 'color': Color[(item.id) % Color.length][1]}">{{Math.round(item.avg*100)/100}}</a>
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
						<div style="flex:1;width: 100%; margin-right: 10px;">
							<el-table :data="applyCourseList"
								style="flex:1;width: 100%; font-weight: bolder; font-size: 16px;">
								<el-table-column prop="cid" label="课号">
								</el-table-column>
								<el-table-column label="课名" width='180'>
									<template slot-scope="scope">
										<div
											style="display: flex; flex-direction: row; justify-content: flex-start; gap: 10px; align-items: center;">
											<!-- <div class="courseinfo"
										:style="{'background': `linear-gradient(45deg, ${Color[(scope.row.id) % Color.length][0]}, ${Color[(scope.row.id) % Color.length][1]})`}"
										@click="course_Info(scope.row)">
									</div> -->
											<el-popover placement="right" :title="scope.row.name" width="200"
												trigger="hover">
												<span>课号：{{scope.row.id}} </span><br>
												<span>教师：{{scope.row.tname}} </span><br>
												<span>教师号：{{scope.row.tid}} </span><br>
												<span>学分：{{scope.row.credit}} </span><br><br>
												<span>{{scope.row.description}} </span>
												<div slot="reference" class="courseinfo"
													:style="{'background': `linear-gradient(45deg, ${Color[(scope.row.id) % Color.length][0]}, ${Color[(scope.row.id) % Color.length][1]})`}">
												</div>
											</el-popover>
											{{scope.row.name}}
										</div>
									</template>
								</el-table-column>
								<el-table-column prop="term" label="学期">
								</el-table-column>
								<el-table-column prop="credit" label="学分">
								</el-table-column>
								<el-table-column label="状态">
									<template slot-scope="scope">
										<div style="font-size:14px; color: white; font-weight:bolder; border-radius: 16px; height: 32px;width: 100px;display: flex; flex-direction: column; align-items: center; justify-content: center;"
											:style="{'background': (scope.row.accept === false ? 'linear-gradient(45deg, rgb(221, 7, 25), rgb(233, 116, 20))':
												(scope.row.accept === true? 
												'linear-gradient(45deg, rgb(23, 230, 131), rgb(10, 175, 60))' :
												'linear-gradient(45deg, rgb(238, 181, 23), rgb(255, 139, 6))' 
													)
												), 'width': scope.row.accept === null? '32px': '100px'}">
											<i v-if="scope.row.accept === false" class="el-icon-close" sty>未通过</i>
											<i v-if="scope.row.accept === true" class="el-icon-check">审核通过</i>
											<i v-if="scope.row.accept === null" class="el-icon-loading"></i>
										</div>
									</template>
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

					<div v-if="currentTab === 'profile'" style="height: 100%; overflow: auto;">
						<div
							style="width: 100%; flex: 1; display: flex; flex-direction: row; flex-wrap: wrap; overflow: auto; gap: 10px; padding: 30px; box-sizing: border-box; align-items: flex-start;align-content: flex-start;">
							<div class="card"
								style="width: 200px; background-color: white; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; gap: 10px;">
								<h2 style="margin: 0px;">🚦 修改密码</h2>
								<el-form :model="passwordForm">
									<el-form-item prop="old" label="旧密码">
										<el-input v-model="passwordForm.old"></el-input>
									</el-form-item>
									<el-form-item prop="new" label="新密码">
										<el-input v-model="passwordForm.new"></el-input>
									</el-form-item>
								</el-form>
								<div
									style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
									<el-button type="primary" @click="set_Password()" round>重置密码</el-button>
								</div>
							</div>

						</div>
					</div>
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
			style="position: fixed; left: 180px; width: 100px; top: 150px; display: flex; flex-direction: column; gap: 10px;">
			<div class="tabs" :class="{'selected': currentTab==='courses'}" @click="currentTab ='courses'">
				<a style="margin: auto; line-height: 12px;">🏢 课程</a>
			</div>
			<div class="tabs" :class="{'selected': currentTab==='apply'}" @click="currentTab ='apply'">
				<a style="margin: auto; line-height: 12px;">🎯 开课</a>
			</div>
			<!-- <div class="tabs" :class="{'selected': currentTab==='query'}" @click="currentTab ='query'">
				<a style="margin: auto; line-height: 12px;">查询</a>
			</div> -->
			<div class="tabs" :class="{'selected': currentTab==='profile'}" @click="currentTab ='profile'">
				<a style="margin: auto; line-height: 12px;">👓 账户</a>
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
				<el-form-item label="介绍" prop="description">
					<el-input type="textarea" v-model="courseForm.description"></el-input>
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
					credit: 1,
					description: '无描述'
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
					color1: this.Color[(item.id) % this.Color.length][0],
					color2: this.Color[(item.id) % this.Color.length][1],
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
					tid: this.info.id,
					description: this.courseForm.description
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
							this.load_Applications()
						}
					})

			},
			reset_Form(formName) {
				this.$refs[formName].resetFields();
			},
			course_Info(row) {
				this.$router.push({ name: "CourseInfo", params: row })
			}
		},
		mounted() {
			this.info = JSON.parse(localStorage.login)
			this.load_Courses();
		}
	}
</script>

<style scoped>
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
		padding: 14px 0px;
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

	.card {
		border-radius: 10px;
		box-shadow: #00000026 0px 2px 7px 0px;
		transform: scale(1) translateY(0px);
		transition: all .2s ease-out;
	}

	.card:hover {
		border-radius: 10px;
		box-shadow: #00000041 0px 4px 12px 0px;
		transform: scale(1.01) translateY(-2px);
		transition: all .2s ease-out;
	}

	.courseinfo:hover {
		opacity: 0.8;
		transition: 0.1s;
	}

	.courseinfo {
		min-width: 32px;
		min-height: 32px;
		text-align: center;
		padding: 4px;
		border-radius: 50%;
		color: white;
		opacity: 1;
		transition: 0.1s;
		/* user-select: none; */
		/* cursor: zoom-in; */
	}
</style>