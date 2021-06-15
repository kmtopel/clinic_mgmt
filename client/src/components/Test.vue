<template>
    <h1 class="header_text"> {{ msg }}</h1>
</template>
<script>

export default ({
    name: 'Test',
    data: () => ({
        msg: String,
        
    })
})
</script>
<style scoped>
.header_text {
    color: red;
}
</style>
