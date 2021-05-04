<template>
	<div style="width: 100%; height: 100%; display: flex; flex-direction: column;justify-content: center;
    align-items: center;">
		<el-card style="width: 300px; ">
			<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
				<el-radio-group v-model="type">
					<el-radio-button label="学生"></el-radio-button>
					<el-radio-button label="职员"></el-radio-button>
				</el-radio-group>
			</div>
			<el-form :model="login">
				<el-form-item label="账号" prop="id">
					<el-input v-model="login.id"></el-input>
				</el-form-item>
				<el-form-item label="密码" prop="password">
					<el-input v-model="login.password"></el-input>
				</el-form-item>
			</el-form>
			<el-row style="margin-bottom: 0px;">
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center;">
					<el-button type="primary" @click="login_in()" round>登 录</el-button>
				</div>
			</el-row>
		</el-card>
	</div>
</template>

<script>
	export default {
		name: 'loginin',
		components: {
		},
		data() {
			return {
				type: '学生',
				login: {
					id: '',
					password: ''
				}
			}
		},
		methods: {
			login_in() {
				if (this.type === '职员') {
					this.$axios.post("http://127.0.0.1:8000/teacher/login/", this.login)
						.then(res => {
							if (res.data.state === 'failed') {
								this.$message.error({
									message: res.data.data,
									showClose: true
								});
							}
							else {
								this.$message.success({
									message: "登录成功",
									showClose: true
								});
								localStorage.login = JSON.stringify({
									type: 'teacher',
									id: res.data.id,
									name: res.data.name,
									tid: res.data.tid
								})
								if (res.data.isadmin) {
									this.$router.push('/controlhub')
								}
								else {
									this.$router.push('/teacherhub')
								}
							}
						})
				}
				else {
					this.$axios.post("http://127.0.0.1:8000/students/login/", this.login)
						.then(res => {
							if (res.data.state === 'failed') {
								this.$message.error({
									message: res.data.data,
									showClose: true
								});
							}
							else {
								this.$message.success({
									message: "登录成功",
									showClose: true
								});
								localStorage.login = JSON.stringify({
									type: 'student',
									id: res.data.id,
									name: res.data.name,
									sid: res.data.sid
								})
								this.$router.push('/studenthub')
							}
						})
				}
			}
		},
		mounted() {
		}
	}
</script>

<style>
</style>