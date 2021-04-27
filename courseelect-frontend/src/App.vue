<template>
	<div id="app" style="height: 100%;">
		<!-- <div id="nav">
			<router-link to="/">Home</router-link> |
			<router-link to="/about">About</router-link>
		</div> -->
		<router-view />
	</div>
</template>

<style>
	#app {
		font-family: 'Avenir', Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		color: #2c3e50;
	}

	body {
		background-color: rgb(93, 167, 252);
		position: fixed;
		padding: 80px 200px;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
		box-sizing: content-box;
		margin: 0px;
	}

	.el-row {
		margin-bottom: 10px;
	}

	.el-dialog {
		border-radius: 10px;
	}
</style>