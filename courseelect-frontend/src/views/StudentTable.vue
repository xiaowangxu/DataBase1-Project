<template>
	<div id="app">
		<div
			style="width: 100%; display: flex; flex-direction: row; margin-bottom: 10px; align-items: center; box-sizing: border-box;">
			<el-select value="/studenttable" placeholder="请选择" @change="switch_Page($event)">
				<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<div style="flex:1"></div>
			<el-button size="medium" icon="el-icon-refresh-left" circle @click="refresh_StudentList()"></el-button>
			<el-button type="success" size="medium" icon="el-icon-plus" round @click="addDialog = true">添加</el-button>
			<div style="flex:1"></div>
			<el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button>
		</div>
		<el-row>
			<el-card>
				<el-table height="500" :data=" list" style="width: 100%">
					<el-table-column prop="sid" label="学号">
					</el-table-column>
					<el-table-column prop="name" label="姓名">
					</el-table-column>
					<el-table-column prop="sex" label="性别">
					</el-table-column>
					<el-table-column prop="birth" label="出生日期">
					</el-table-column>
					<el-table-column prop="depart" label="学院">
					</el-table-column>
					<el-table-column label="操作" width="140">
						<template slot-scope="scope">
							<el-button @click="open_modify_Student(scope.row)" type="primary" size="small"
								icon="el-icon-edit" circle></el-button>
							<el-button @click="delete_Student(scope.row)" type="danger" size="small"
								icon="el-icon-delete" circle></el-button>
							<el-button @click="reset_Student(scope.row)" type="warning" size="small"
								icon="el-icon-unlock" circle></el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-card>
		</el-row>

		<el-dialog :visible.sync="addDialog" width="400px">
			<el-form :model="studentForm" ref="ruleForm" class="demo-ruleForm">
				<el-form-item label="学号" prop="sid">
					<el-input v-model="studentForm.sid"></el-input>
				</el-form-item>
				<el-form-item label="姓名" prop="name">
					<el-input v-model="studentForm.name"></el-input>
				</el-form-item>
				<el-form-item label="出生日期" prop="birth" require>
					<el-date-picker type="date" placeholder="选择日期" v-model="studentForm.birth" style="width: 100%;">
					</el-date-picker>
				</el-form-item>
				<el-form-item label="性别" prop="sex">
					<el-radio-group v-model="studentForm.sex">
						<el-radio label="男"></el-radio>
						<el-radio label="女"></el-radio>
					</el-radio-group>
				</el-form-item>
				<el-form-item label="学院" require prop="depart">
					<el-select v-model="studentForm.depart" placeholder="请选择" style="width: 100%;">
						<el-option v-for="item in depart" :key="item.value" :label="item.label" :value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="addDialog = false" round>取 消</el-button>
				<el-button type="primary" @click="add_Student()" round>确 定</el-button>
			</div>
		</el-dialog>
		<el-dialog :visible.sync="modifyDialog" width="400px">
			<el-form :model="studentModifyForm" ref="ruleForm" class="demo-ruleForm">
				<el-form-item label="学号" prop="sid">
					<el-input v-model="studentModifyForm.sid"></el-input>
				</el-form-item>
				<el-form-item label="姓名" prop="name">
					<el-input v-model="studentModifyForm.name"></el-input>
				</el-form-item>
				<el-form-item label="出生日期" prop="birth" require>
					<el-date-picker type="date" placeholder="选择日期" v-model="studentModifyForm.birth"
						style="width: 100%;">
					</el-date-picker>
				</el-form-item>
				<el-form-item label="性别" prop="sex">
					<el-radio-group v-model="studentModifyForm.sex">
						<el-radio label="男"></el-radio>
						<el-radio label="女"></el-radio>
					</el-radio-group>
				</el-form-item>
				<el-form-item label="学院" require prop="depart">
					<el-select v-model="studentModifyForm.depart" placeholder="请选择" style="width: 100%;">
						<el-option v-for="item in depart" :key="item.value" :label="item.label" :value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="modifyDialog = false" round>取 消</el-button>
				<el-button type="primary" @click="modify_Student()" round>确 定</el-button>
			</div>
		</el-dialog>
	</div>

</template>

<script>
	export default {
		name: 'studenttable',
		components: {
		},
		data() {
			return {
				list: [],
				options: [{ label: '学生', value: '/studenttable' }, { label: '教师', value: '/teachertable' }, { label: '课程', value: '/coursetable' }],
				depart: [{ label: '计算机科学', value: '计算机科学' }, { label: '智能科学', value: '智能科学' }],
				addDialog: false,
				modifyDialog: false,
				studentForm: {
					sid: '',
					name: '',
					sex: '',
					birth: '',
					depart: ''
				},
				studentModifyForm: {
					sid: '',
					name: '',
					sex: '',
					birth: '',
					depart: ''
				}
			}
		},
		methods: {
			logout() {
				localStorage.login = JSON.stringify({})
				this.$router.go(-1)
			},
			refresh_StudentList() {
				fetch('http://127.0.0.1:8000/students/')
					.then(res => res.json())
					.then(json => {
						this.list = json.list
					})
			},
			add_Student() {
				let data = this.studentForm
				function formatDate(date) {
					var d = new Date(date),
						month = '' + (d.getMonth() + 1),
						day = '' + d.getDate(),
						year = d.getFullYear();

					if (month.length < 2)
						month = '0' + month;
					if (day.length < 2)
						day = '0' + day;

					return [year, month, day].join('-');
				}
				data.birth = formatDate(data.birth)
				this.$axios.post("http://127.0.0.1:8000/students/", data)
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
						this.refresh_StudentList()
					})
				this.addDialog = false
			},
			delete_Student(row) {
				this.$axios.post("http://127.0.0.1:8000/students/delete/", { id: row.id })
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
						this.refresh_StudentList()
					})
			},
			open_modify_Student(row) {
				this.studentModifyForm = {
					id: row.id,
					sid: row.sid,
					name: row.name,
					sex: row.sex,
					birth: row.birth,
					depart: row.depart
				}
				this.modifyDialog = true
			},
			modify_Student() {
				let data = this.studentModifyForm
				function formatDate(date) {
					var d = new Date(date),
						month = '' + (d.getMonth() + 1),
						day = '' + d.getDate(),
						year = d.getFullYear();

					if (month.length < 2)
						month = '0' + month;
					if (day.length < 2)
						day = '0' + day;

					return [year, month, day].join('-');
				}
				data.birth = formatDate(data.birth)
				this.$axios.post("http://127.0.0.1:8000/students/modify/", data)
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
						this.refresh_StudentList()
					})
				this.modifyDialog = false
			},
			reset_Student(row) {
				this.$axios.post("http://127.0.0.1:8000/students/resetPassword/", { id: row.id })
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
					})
			},
			switch_Page(page) {
				this.$router.replace(page)
			}
		},
		mounted() {
			this.refresh_StudentList()
		}
	}
</script>

<style>
</style>