<template>
	<div style="width: 100%; height: 100%; display: flex; flex-direction: column; gap: 10px; overflow: auto;">
		<div style="width: 100%; display: flex; flex-direction: row; align-items: center; box-sizing: border-box;">
			<!-- <el-select value="/controlhub" placeholder="请选择" @change="switch_Page($event)">
				<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<div style="flex:1"></div>
			<el-button size="medium" icon="el-icon-refresh-left" circle @click="refresh_StudentList()"></el-button>
			<el-button type="success" size="medium" icon="el-icon-plus" round @click="addDialog = true">添加</el-button> -->
			<div style="flex:1"></div>

			<el-button size="medium" round disabled>当前学期：{{currentTerm}}
			</el-button>
			<el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button>
		</div>
		<div
			style="width: 100%; flex: 1; display: flex; flex-direction: row; flex-wrap: wrap; overflow: auto; gap: 10px; padding: 30px; box-sizing: border-box; align-items: flex-start;align-content: flex-start; justify-content: center;">
			<div class="card"
				style="width: 200px; background-color: white; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; gap: 20px;">
				<h2 style="margin: 0px;">🛴 项目管理</h2>
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
					<el-button type="primary" @click="$router.push('/studenttable')" round style="width: 100%;">🧑 学生
					</el-button>
				</div>
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
					<el-button type="primary" @click="$router.push('/teachertable')" round style="width: 100%;">🧔 教师
					</el-button>
				</div>
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
					<el-button type="primary" @click="$router.push('/coursetable')" round style="width: 100%;">🏢 课程
					</el-button>
				</div>
				<el-badge :value="has_Application? 'new':''" style="width: 100%;">
					<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
						<el-button type="primary" @click="$router.push('/application')" round style="width: 100%;">🏁
							申请</el-button>
					</div>
				</el-badge>
			</div>
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
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
					<el-button type="primary" @click="set_Password()" round>重置密码</el-button>
				</div>
			</div>
			<div class="card"
				style="width: 200px; background-color: white; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; gap: 10px;">
				<h2 style="margin: 0px;">🎉 新学期</h2>
				<el-form :model="termForm">
					<el-form-item label="学期">
						<el-input v-model="termForm.term"></el-input>
					</el-form-item>
				</el-form>
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
					<el-button type="primary" @click="next_Term()" round>开始新学期</el-button>
				</div>
			</div>

		</div>

	</div>

</template>

<script>
	export default {
		name: 'studenttable',
		components: {
		},
		data() {
			return {
				info: { name: '', id: '' },
				currentTerm: '',
				has_Application: false,
				options: [{ label: '控制台', value: '/controlhub' }, { label: '学生', value: '/studenttable' }, { label: '教师', value: '/teachertable' }, { label: '课程', value: '/coursetable' }, { label: '开课申请', value: '/application' }],
				passwordForm: {
					old: '',
					new: ''
				},
				termForm: {
					term: ''
				}
			}
		},
		methods: {
			logout() {
				localStorage.login = JSON.stringify({})
				this.$router.go(-1)
			},
			switch_Page(page) {
				this.$router.replace(page)
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
			next_Term() {
				if (this.termForm.term === '') return
				this.$axios.post("http://127.0.0.1:8000/term/next/", { term: this.termForm.term })
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
							this.$axios.post("http://127.0.0.1:8000/course/application/has/", {})
								.then(res => {
									this.has_Application = res.data.has
								})
						}
					})
			}
		},
		mounted() {
			this.info = JSON.parse(localStorage.login)
			this.$axios.post("http://127.0.0.1:8000/course/application/has/", {})
				.then(res => {
					this.has_Application = res.data.has
				})
			this.$axios.post("http://127.0.0.1:8000/term/current/", {})
				.then(res => {
					this.currentTerm = res.data.current
				})
		}
	}
</script>

<style scoped>
	.card {
		border-radius: 10px;
		box-shadow: #00000026 0px 5px 7px 0px;
		transform: scale(1) translateY(0px);
		transition: all .2s ease-out;
	}

	.card:hover {
		border-radius: 10px;
		box-shadow: #00000041 0px 10px 12px 0px;
		transform: scale(1.01) translateY(-2px);
		transition: all .2s ease-out;
	}
</style>