<template>
    <div class="topBar">
        <h1 class="roboto">Your Sources</h1>
        <button class="text-button" @click="goToAddSource">
            <i class="bi bi-plus-lg"></i>
            ADD AN RSS FEED
        </button>
    </div>


    <Sources/>
</template>
<script>
    import Sources from '../components/Sources.vue';
    export default {
        components: {
            Sources
        },
        methods: {
            goToAddSource() {
                this.$router.push({name: 'add'});
            }
        }
    }
</script>
<style scoped>
    .topBar {
        display: flex;
        flex-direction: row;
        gap: 10px;
        align-items: center;
    }
</style>