<template>
	<div style="width: 100%; height: 100%; display: flex; flex-direction: column; gap: 10px;">
		<div style="width: 100%; display: flex; flex-direction: row; align-items: center; box-sizing: border-box;">
			<el-select value="/coursetable" placeholder="请选择" @change="switch_Page($event)">
				<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<div style="flex:1"></div>
			<el-button size="medium" icon="el-icon-refresh-left" circle @click="refresh_CourseList()"></el-button>
			<el-button type="success" size="medium" icon="el-icon-plus" round @click="addDialog = true">添加</el-button>
			<div style="flex:1"></div>
			<el-button size="medium" round disabled>当前学期：{{currentTerm}}
			</el-button>
			<!-- <el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button> -->
		</div>
		<div style="flex: 1; display: flex; flex-direction: row; box-sizing: border-box;">
			<div
				style="width: 60%; height: 100%; display: flex; flex-direction: column; gap: 10px; margin-right: 20px;">
				<div
					style="background-color: white; flex: 1; padding: 14px 20px 20px 20px; border-radius: 10px; box-shadow: rgb(0 0 0 / 7%) 0px 5px 9px 9px; box-sizing: border-box;">
					<el-table :data=" list" style="width: 100%; height: 100%; font-size: 16px;">
						<el-table-column prop="cid" label="课号">
						</el-table-column>
						<el-table-column prop="term" label="学期">
						</el-table-column>
						<!-- <el-table-column prop="name" label="课名">
						</el-table-column> -->
						<el-table-column label="课名" width='180'>
							<template slot-scope="scope">

								<div
									style="display: flex; flex-direction: row; justify-content: flex-start; gap: 10px; align-items: center;">
									<!-- <div class="courseinfo"
										:style="{'background': `linear-gradient(45deg, ${Color[(scope.row.id) % Color.length][0]}, ${Color[(scope.row.id) % Color.length][1]})`}"
										@click="course_Info(scope.row)">
									</div> -->
									<el-popover placement="right" :title="scope.row.name" width="200" trigger="hover">
										<span>课号：{{scope.row.id}} </span><br>
										<span>教师：{{scope.row.tname}} </span><br>
										<span>教师号：{{scope.row.tid}} </span><br>
										<span>学分：{{scope.row.credit}} </span><br>
										<span>容量：{{scope.row.currentcount}}/{{scope.row.capacity}} </span><br><br>
										<span>{{scope.row.description}} </span>
										<div slot="reference" class="courseinfo"
											:style="{'background': `linear-gradient(45deg, ${Color[(scope.row.id) % Color.length][0]}, ${Color[(scope.row.id) % Color.length][1]})`}">
										</div>
									</el-popover>
									{{scope.row.name}}
								</div>
							</template>
						</el-table-column>
						<el-table-column prop="credit" label="学分">
						</el-table-column>
						<el-table-column prop="tid" label="工号">
						</el-table-column>
						<el-table-column prop="tname" label="教师">
						</el-table-column>
						<el-table-column prop="depart" label="学院">
						</el-table-column>
						<el-table-column label="操作" width="140">
							<template slot-scope="scope">
								<el-button @click="open_modify_Course(scope.row)" type="primary" size="small"
									icon="el-icon-edit" circle></el-button>
								<el-button @click="delete_Course(scope.row)" type="danger" size="small"
									icon="el-icon-delete" circle></el-button>
								<el-button @click="get_Student(scope.row)" type="warning" size="small"
									icon="el-icon-more" circle></el-button>
							</template>
						</el-table-column>
					</el-table>

				</div>
				<div
					style="width: 100%; background-color: white; border-radius: 10px; padding: 10px 10px; box-sizing: border-box; display: flex; flex-direction: row; justify-content: center; box-shadow: rgb(0 0 0 / 7%) 0px 5px 9px 9px;">
					<el-pagination background layout="prev, pager, next" :page-count="pagescount"
						:current-page="currentpage" @current-change="change_Page">
					</el-pagination>
				</div>
			</div>
			<div style="flex: 1; width: 10px; display: flex; flex-direction: column; gap: 20px;">
				<h1 style="margin: 20px 0px 0px 0px; color: white; align-self: flex-end; min-height: 43px;">
					{{currentCourse}}</h1>
				<div
					style="background-color: white; flex: 1; padding: 14px 20px 20px 20px; border-radius: 10px; box-shadow: rgb(0 0 0 / 7%) 0px 5px 9px 9px; box-sizing: border-box;">
					<el-table :data="studentslist" style="width: 100%; height: 100%; font-size: 16px;">
						<el-table-column prop="sid" label="学号">
						</el-table-column>
						<el-table-column prop="name" label="姓名">
						</el-table-column>
						<el-table-column prop="grade" label="成绩">
						</el-table-column>
						<el-table-column label="操作" width="70">
							<template slot-scope="scope">
								<el-button @click="delete_Election(scope.row)" type="danger" size="small"
									icon="el-icon-delete" circle></el-button>
							</template>
						</el-table-column>
					</el-table>
				</div>
			</div>
		</div>

		<el-dialog :visible.sync="addDialog" width="400px">
			<el-form :model="courseForm" ref="ruleForm" class="demo-ruleForm">
				<el-form-item label="课号" prop="cid">
					<el-input v-model="courseForm.cid"></el-input>
				</el-form-item>
				<el-form-item label="课名" prop="name">
					<el-input v-model="courseForm.name"></el-input>
				</el-form-item>
				<el-form-item label="学分" prop="credit">
					<el-input-number v-model="courseForm.credit" :min="0" :max="10"></el-input-number>
				</el-form-item>
				<el-form-item label="容量" prop="capacity">
					<el-input-number v-model="courseForm.capacity" :min="0" :max="1000"></el-input-number>
				</el-form-item>
				<el-form-item label="学院" require prop="depart">
					<el-select v-model="courseForm.depart" placeholder="请选择" style="width: 100%;"
						@change="on_addCourse_Depart_changed($event)">
						<el-option v-for="item in depart" :key="item.value" :label="item.label" :value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="教师" require prop="tuid">
					<el-select v-model="courseForm.tuid" placeholder="请选择" style="width: 100%;">
						<el-option v-for="item in teacherList" :key="item.value" :label="item.label"
							:value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="介绍" prop="description">
					<el-input type="textarea" v-model="courseForm.description"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="addDialog = false" round>取 消</el-button>
				<el-button type="primary" @click="add_Course()" round>确 定</el-button>
			</div>
		</el-dialog>
		<el-dialog :visible.sync="modifyDialog" width="400px">
			<el-form :model="courseModifyForm" ref="ruleForm" class="demo-ruleForm">
				<el-form-item label="课号" prop="cid">
					<el-input v-model="courseModifyForm.cid"></el-input>
				</el-form-item>
				<el-form-item label="课名" prop="name">
					<el-input v-model="courseModifyForm.name"></el-input>
				</el-form-item>
				<el-form-item label="学分" prop="credit">
					<el-input-number v-model="courseModifyForm.credit" :min="0" :max="10"></el-input-number>
				</el-form-item>
				<el-form-item label="容量" prop="capacity">
					<el-input-number v-model="courseModifyForm.capacity" :min="0" :max="1000"></el-input-number>
				</el-form-item>
				<el-form-item label="学院" require prop="depart">
					<el-select v-model="courseModifyForm.depart" placeholder="请选择" style="width: 100%;"
						@change="on_modifyCourse_Depart_changed($event)">
						<el-option v-for="item in depart" :key="item.value" :label="item.label" :value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="教师" require prop="tuid">
					<el-select v-model="courseModifyForm.tuid" placeholder="请选择" style="width: 100%;">
						<el-option v-for="item in modifyteacherList" :key="item.value" :label="item.label"
							:value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
				<el-form-item label="介绍" prop="description">
					<el-input type="textarea" v-model="courseModifyForm.description"></el-input>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="modifyDialog = false" round>取 消</el-button>
				<el-button type="primary" @click="modify_Course()" round>确 定</el-button>
			</div>
		</el-dialog>
	</div>
</template>

<script>
	export default {
		name: 'coursetable',
		components: {
		},
		data() {
			return {
				list: [],
				currentTerm: '',
				currentpage: -1,
				pagescount: 0,
				options: [/*{ label: '控制台', value: '/controlhub' },*/ { label: '学生', value: '/studenttable' }, { label: '教师', value: '/teachertable' }, { label: '课程', value: '/coursetable' }, { label: '开课申请', value: '/application' }],
				depart: [{ label: '计算机科学', value: '计算机科学' }, { label: '智能科学', value: '智能科学' }],
				addDialog: false,
				modifyDialog: false,
				teacherList: [],
				modifyteacherList: [],
				courseForm: {
					cid: '',
					name: '',
					tuid: '',
					credit: 1,
					depart: '',
					description: '无描述',
					capacity: 50
				},
				courseModifyForm: {
					id: -1,
					cid: '',
					name: '',
					tuid: '',
					credit: 1,
					depart: '',
					description: '',
					capacity: 0
				},
				currentC: undefined,
				currentCourse: '无选中课程',
				studentslist: [],
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
		methods: {
			logout() {
				localStorage.login = JSON.stringify({})
				this.$router.go(-1)
			},
			change_Page(pageidx) {
				this.refresh_CourseList(pageidx)
			},
			refresh_CourseList(page = 1) {
				this.$axios.post("http://127.0.0.1:8000/course/paged/", { page: page })
					.then(res => {
						console.log('res=>', res);
						this.currentpage = res.data.current
						this.pagescount = res.data.pages
						this.list = res.data.list
					}).then(() => {
						// this.refresh_StudentList()
					})
			},
			add_Course() {
				let data = this.courseForm
				this.$axios.post("http://127.0.0.1:8000/course/", data)
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
						}
					}).then(() => {
						this.refresh_CourseList()
					})
				this.addDialog = false
			},
			delete_Course(row) {
				this.$axios.post("http://127.0.0.1:8000/course/delete/", { id: row.id })
					.then(res => {
						console.log('res=>', res);
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
						}
					}).then(() => {
						this.refresh_CourseList()
					})
			},
			delete_Election(row) {
				this.$axios.post("http://127.0.0.1:8000/course/deleteElect/", { id: row.eid })
					.then(res => {
						console.log('res=>', res);
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
						}
					}).then(() => {
						this.get_Student()
					})
			},
			course_Info(row) {
				this.$router.push({ name: "CourseInfo", params: row })
			},
			get_Student(row) {
				row = row === undefined ? this.currentC : row
				this.currentC = row

				this.currentCourse = row.cid + " " + row.name
				this.$axios.post("http://127.0.0.1:8000/students/getByCourse/", { id: row.id })
					.then(res => {
						console.log('res=>', res);
						if (res.data.state === 'failed') {
							this.$message.error({
								message: res.data.data,
								showClose: true
							});
						}
						else {
							this.studentslist = res.data.list
						}
					}).then(() => {
						// this.refresh_CourseList()
					})
			},
			open_modify_Course(row) {
				this.courseModifyForm = {
					cid: row.cid,
					id: row.id,
					name: row.name,
					tuid: row.tuid,
					credit: row.credit,
					depart: row.depart,
					description: row.description,
					capacity: row.capacity
				}
				this.$axios.post("http://127.0.0.1:8000/teacher/getDepart/", { depart: this.courseModifyForm.depart })
					.then(res => {
						this.modifyteacherList = res.data.list.map((i) => {
							return { label: `${i.tid} ${i.name}`, value: i.id }
						})
					})
				this.modifyDialog = true
			},
			modify_Course() {
				let data = this.courseModifyForm
				this.$axios.post("http://127.0.0.1:8000/course/modify/", data)
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
						}
					}).then(() => {
						this.refresh_CourseList()
					})
				this.modifyDialog = false
			},
			on_addCourse_Depart_changed(depart) {
				this.courseForm.tuid = ''
				this.$axios.post("http://127.0.0.1:8000/teacher/getDepart/", { depart: depart })
					.then(res => {
						console.log(res)
						this.teacherList = res.data.list.map((i) => {
							return { label: `${i.tid} ${i.name}`, value: i.id }
						})
					})
			},
			on_modifyCourse_Depart_changed(depart) {
				this.courseModifyForm.tuid = ''
				this.$axios.post("http://127.0.0.1:8000/teacher/getDepart/", { depart: depart })
					.then(res => {
						this.modifyteacherList = res.data.list.map((i) => {
							return { label: `${i.tid} ${i.name}`, value: i.id }
						})
					})
			},
			switch_Page(page) {
				this.$router.replace(page)
			}
		},
		mounted() {
			this.refresh_CourseList()
			this.$axios.post("http://127.0.0.1:8000/term/current/", {})
				.then(res => {
					this.currentTerm = res.data.current
				})
		}
	}
</script>

<style scoped>
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