<template>
	<div id="app">
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
		padding: 60px 100px;
	}

	.el-row {
		margin-bottom: 10px;
	}

	.el-dialog {
		border-radius: 10px;
	}
</style>