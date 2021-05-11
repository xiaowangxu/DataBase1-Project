<template>
	<div style="width: 100%; height: 100%; display: flex; flex-direction: column; gap: 10px;">
		<div style="width: 100%; display: flex; flex-direction: row; align-items: center; box-sizing: border-box;">
			<el-select value="/application" placeholder="请选择" @change="switch_Page($event)">
				<el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
				</el-option>
			</el-select>
			<div style="flex:1"></div>
			<el-button size="medium" icon="el-icon-refresh-left" circle @click="refresh_ApplicationList()"></el-button>
			<div style="flex:1"></div>
			<el-button size="medium" round disabled>当前学期：{{currentTerm}}
			</el-button>
			<!-- <el-button type="danger" size="medium" icon="el-icon-top-left" round @click="logout()">登出</el-button> -->
		</div>
		<div
			style="background-color: white; flex: 1; padding: 14px 20px 20px 20px; border-radius: 10px; box-shadow: rgb(0 0 0 / 7%) 0px 5px 9px 9px;">
			<el-table :data=" list" style="width: 100%; height: 100%; font-size: 16px;">
				<el-table-column prop="cid" label="课号">
				</el-table-column>
				<el-table-column prop="term" label="学期">
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
						<el-button @click="reject(scope.row)" type="danger" size="small" icon="el-icon-close" circle>
						</el-button>
						<el-button @click="allow(scope.row)" type="success" size="small" icon="el-icon-check" circle>
						</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>

		<div
			style="width: 100%; background-color: white; border-radius: 10px; padding: 10px 10px; box-sizing: border-box; display: flex; flex-direction: row; justify-content: center; box-shadow: rgb(0 0 0 / 7%) 0px 5px 9px 9px;">
			<el-pagination background layout="prev, pager, next" :page-count="pagescount" :current-page="currentpage"
				@current-change="change_Page">
			</el-pagination>
		</div>
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
				currentTerm: '',
				pagescount: 0,
				currentpage: 0,
				options: [/*{ label: '控制台', value: '/controlhub' },*/ { label: '学生', value: '/studenttable' }, { label: '教师', value: '/teachertable' }, { label: '课程', value: '/coursetable' }, { label: '开课申请', value: '/application' }]
			}
		},
		methods: {
			logout() {
				localStorage.login = JSON.stringify({})
				this.$router.go(-1)
			},
			change_Page(pageidx) {
				this.refresh_ApplicationList(pageidx)
			},
			refresh_ApplicationList(page = 1) {
				this.$axios.post("http://127.0.0.1:8000/course/application/paged/", { page: page })
					.then(res => {
						// console.log('res=>', res);
						this.currentpage = res.data.current
						this.pagescount = res.data.pages
						this.list = res.data.list
					})
			},
			switch_Page(page) {
				this.$router.replace(page)
			},
			reject(row) {
				this.$axios.post("http://127.0.0.1:8000/course/application/modify/", { id: row.id, accept: false })
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
							this.refresh_ApplicationList()
						}
					})
			},
			allow(row) {
				this.$axios.post("http://127.0.0.1:8000/course/application/modify/", { id: row.id, accept: true })
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
							this.refresh_ApplicationList()
						}
					})
			}
		},
		mounted() {
			this.refresh_ApplicationList()
			this.$axios.post("http://127.0.0.1:8000/term/current/", {})
				.then(res => {
					this.currentTerm = res.data.current
				})
		}
	}
</script>

<style>
</style>