<template>
	<div>
		<div
			style="width: 100%; display: flex; flex-direction: row; margin-bottom: 10px; align-items: center; box-sizing: border-box;">
			<h1 style="margin: 0px; color: white;"><span style="font-size: 20px;">欢迎 </span>{{info.tid}}, {{info.name}}
			</h1>
			<div style="flex:1"></div>
			<el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button>
		</div>
		<el-card>
			<el-tabs tabPosition="left" @tab-click="on_Tab_changed($event.label)">
				<el-tab-pane label="我的课程">
					<div
						style="display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px;">
						<template v-for="item in courseList">
							<div :key="item.cid"
								style="border-radius: 6px; box-shadow: #00000026 0px 5px 7px 0px; display: flex; flex-direction: column; padding: 10px 15px;"
								:style="{'background-color': color[item.id % color.length]}">
								<div class="container">
									<div class="vcontainer">

										<a
											style="margin-bottom: 10px; color: white; font-size: 24px; font-weight: bolder;">{{item.name}}
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
									<a
										style="margin-right: 10px; color: white; font-size: 60px; font-style: italic;">{{item.grade}}</a>
								</div>
							</div>
						</template>
					</div>
				</el-tab-pane>
				<el-tab-pane label="成绩填报">
					<div
						style="display: flex; flex-direction: column; gap: 20px; overflow: visible; padding: 0px 0px 0px 10px; align-items: center;">
						<el-select v-model="selectedCourse" placeholder="请选择" @change="switch_Course($event)">
							<el-option v-for="item in get_CourseOptions" :key="item.value" :label="item.label"
								:value="item.value">
							</el-option>
						</el-select>
						<div style="height: 600px; width: 100%;">
							<el-table height="600" :data="studentList" style="width: 100%">
								<el-table-column prop="sid" label="学号">
								</el-table-column>
								<el-table-column prop="name" label="姓名">
								</el-table-column>
								<el-table-column label="成绩" width="140">
									<template slot-scope="scope">
										<el-input type="number" min="0" max="100" step="1"
											v-model.number="scope.row.grade">
										</el-input>
									</template>
								</el-table-column>
							</el-table>
						</div>
						<div
							style="display: flex; margin-top: 20px; flex-direction: row; align-items: center; justify-content: center;">
							<el-button type="primary" @click="update_Grade()" round>上 传</el-button>
						</div>
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
	export default {
		name: 'teacherhub',
		components: {
		},
		data() {
			return {
				passwordForm: {
					old: '',
					new: ''
				},
				info: { name: '', id: '' },
				selectedCourse: undefined,
				courseList: [],
				studentList: [],
				studentListOld: [],
				color: ['#D32F2F', '#7B1FA2', '#303F9F', '#1976D2', '#689F38', '#FBC02D', '#FFA000', '#F57C00', '#E64A19', '#5D4037', '#111d5e', '#2f2519', '#c70039', '#184d47', '#f37121', '#ffbd69', '#b83b5e', '#3ec1d3', '#6c5b7b', '#455d7a', '#8f8787'],
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
					this.$axios.post("http://127.0.0.1:8000/teacher/getCourse/", { id: this.info.id })
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
						}
					})
			},
			update_Grade() {
				let list = this.studentList.filter((i, idx) => {
					return i.grade !== this.studentListOld[idx]
				}).map((i) => {
					return { id: i.euid, grade: i.grade }
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
			}
		},
		mounted() {
			this.info = JSON.parse(localStorage.login)
			this.on_Tab_changed('我的课程')
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