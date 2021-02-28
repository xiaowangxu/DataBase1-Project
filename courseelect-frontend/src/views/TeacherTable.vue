<template>
	<div id="teachertable">
		<div
			style="width: 100%; display: flex; flex-direction: row; margin-bottom: 10px; align-items: center; box-sizing: border-box;">
			<el-select value="/teachertable" placeholder="请选择" @change="switch_Page($event)">
				<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<div style="flex:1"></div>
			<el-button size="medium" icon="el-icon-refresh-left" circle @click="refresh_TeacherList()"></el-button>
			<el-button type="success" size="medium" icon="el-icon-plus" round @click="addDialog = true">添加</el-button>
			<div style="flex:1"></div>
			<el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button>
		</div>
		<el-row>
			<el-card>
				<el-table height="500" :data=" list" style="width: 100%">
					<el-table-column prop="tid" label="教师号">
					</el-table-column>
					<el-table-column prop="name" label="姓名">
					</el-table-column>
					<el-table-column prop="depart" label="学院">
					</el-table-column>
					<el-table-column label="操作" width="140">
						<template slot-scope="scope">
							<el-button v-show="!scope.row.isadmin" @click="open_modify_Teacher(scope.row)"
								type="primary" size="small" icon="el-icon-edit" circle></el-button>
							<el-button v-show="!scope.row.isadmin" @click="delete_Teacher(scope.row)" type="danger"
								size="small" icon="el-icon-delete" circle></el-button>
							<el-button v-show="!scope.row.isadmin" @click="reset_Teacher(scope.row)" type="warning"
								size="small" icon="el-icon-unlock" circle></el-button>
						</template>
					</el-table-column>
				</el-table>
			</el-card>
		</el-row>

		<el-dialog :visible.sync="addDialog" width="400px">
			<el-form :model="teacherForm" ref="ruleForm" class="demo-ruleForm">
				<el-form-item label="工号" prop="tid">
					<el-input v-model="teacherForm.tid"></el-input>
				</el-form-item>
				<el-form-item label="姓名" prop="name">
					<el-input v-model="teacherForm.name"></el-input>
				</el-form-item>
				<el-form-item label="学院" require prop="depart">
					<el-select v-model="teacherForm.depart" placeholder="请选择" style="width: 100%;">
						<el-option v-for="item in depart" :key="item.value" :label="item.label" :value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="addDialog = false" round>取 消</el-button>
				<el-button type="primary" @click="add_Teacher()" round>确 定</el-button>
			</div>
		</el-dialog>
		<el-dialog :visible.sync="modifyDialog" width="400px">
			<el-form :model="teacherModifyForm" ref="ruleForm" class="demo-ruleForm">
				<el-form-item label="工号" prop="tid">
					<el-input v-model="teacherModifyForm.tid"></el-input>
				</el-form-item>
				<el-form-item label="姓名" prop="name">
					<el-input v-model="teacherModifyForm.name"></el-input>
				</el-form-item>
				<el-form-item label="学院" require prop="depart">
					<el-select v-model="teacherModifyForm.depart" placeholder="请选择" style="width: 100%;">
						<el-option v-for="item in depart" :key="item.value" :label="item.label" :value="item.value">
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="modifyDialog = false" round>取 消</el-button>
				<el-button type="primary" @click="modify_Teacher()" round>确 定</el-button>
			</div>
		</el-dialog>
	</div>

</template>

<script>
	export default {
		name: 'teachertable',
		components: {
		},
		data() {
			return {
				list: [],
				options: [{ label: '学生', value: '/studenttable' }, { label: '教师', value: '/teachertable' }, { label: '课程', value: '/coursetable' }],
				depart: [{ label: '计算机科学', value: '计算机科学' }, { label: '智能科学', value: '智能科学' }],
				addDialog: false,
				modifyDialog: false,
				teacherForm: {
					tid: '',
					name: '',
					depart: ''
				},
				teacherModifyForm: {
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
			refresh_TeacherList() {
				fetch('http://127.0.0.1:8000/teacher/')
					.then(res => res.json())
					.then(json => {
						this.list = json.list
					})
			},
			add_Teacher() {
				let data = this.teacherForm
				this.$axios.post("http://127.0.0.1:8000/teacher/", data)
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
						this.refresh_TeacherList()
					})
				this.addDialog = false
			},
			delete_Teacher(row) {
				this.$axios.post("http://127.0.0.1:8000/teacher/delete/", { id: row.id })
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
						this.refresh_TeacherList()
					})
			},
			open_modify_Teacher(row) {
				this.teacherModifyForm = {
					id: row.id,
					tid: row.tid,
					name: row.name,
					depart: row.depart
				}
				this.modifyDialog = true
			},
			modify_Teacher() {
				let data = this.teacherModifyForm
				this.$axios.post("http://127.0.0.1:8000/teacher/modify/", data)
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
						this.refresh_TeacherList()
					})
				this.modifyDialog = false
			},
			reset_Teacher(row) {
				this.$axios.post("http://127.0.0.1:8000/teacher/resetPassword/", { id: row.id })
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
			this.refresh_TeacherList()
		}
	}
</script>

<style>
</style>