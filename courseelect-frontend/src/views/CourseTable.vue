<template>
	<div id="coursetable">
		<div
			style="width: 100%; display: flex; flex-direction: row; margin-bottom: 10px; align-items: center; box-sizing: border-box;">
			<el-select value="/coursetable" placeholder="请选择" @change="switch_Page($event)">
				<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<div style="flex:1"></div>
			<el-button size="medium" icon="el-icon-refresh-left" circle @click="refresh_CourseList()"></el-button>
			<el-button type="success" size="medium" icon="el-icon-plus" round @click="addDialog = true">添加</el-button>
			<div style="flex:1"></div>
			<el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button>
		</div>
		<div style="display: flex; flex-direction: row; gap: 20px">

			<el-card style="flex: 2;">
				<el-table height="500" :data=" list" style="width: 100%">
					<el-table-column prop="cid" label="课号">
					</el-table-column>
					<el-table-column prop="name" label="课名">
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
							<el-button @click="get_Student(scope.row)" type="warning" size="small" icon="el-icon-more"
								circle></el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-card>
			<div style="flex: 1; display: flex; flex-direction: column; gap: 20px;">
				<h1 style="margin: 0px; color: white;">{{currentCourse}}</h1>
				<el-card>
					<el-table height="500" :data="studentslist" style="width: 100%">
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
				</el-card>
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
				options: [{ label: '学生', value: '/studenttable' }, { label: '教师', value: '/teachertable' }, { label: '课程', value: '/coursetable' }],
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
					depart: ''
				},
				courseModifyForm: {
					id: -1,
					cid: '',
					name: '',
					tuid: '',
					credit: 1,
					depart: ''
				},
				currentCourse: '无选中课程',
				studentslist: []
			}
		},
		methods: {
			logout() {
				localStorage.login = JSON.stringify({})
				this.$router.go(-1)
			},
			refresh_CourseList() {
				fetch('http://127.0.0.1:8000/course/')
					.then(res => res.json())
					.then(json => {
						this.list = json.list
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
				console.log(row)
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
						this.get_Student({ id: row.cid, name: this.currentCourse })
					})
			},
			get_Student(row) {
				this.currentCourse = row.cid + " " + row.name
				this.$axios.post("http://127.0.0.1:8000/students/getByCourse/", { id: row.id })
					.then(res => {
						// console.log('res=>', res);
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
						this.refresh_CourseList()
					})
			},
			open_modify_Course(row) {
				this.courseModifyForm = {
					cid: row.cid,
					id: row.id,
					name: row.name,
					tuid: row.tuid,
					credit: row.credit,
					depart: row.depart
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
		}
	}
</script>

<style>
</style>