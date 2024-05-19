<template>
    <div class="source-entry-list">
        <div v-if="!sources || !sources.length" class="roboto-condensed notificationScreen">
            <p><i class="bi bi-newspaper"></i></p>
            <p>No sources found. Try adding some!</p>
        </div>
        <div class="source-entry" v-for="s in sources">
            <div>
                <div class="roboto-condensed source-name">
                    {{ s.name }}
                </div>
                <div class="noto-serif small-text">
                    {{ s.url }}
                </div>
            </div>
            <div>
            <i class="bi bi-trash viewbutton" @click="onDeleteSource(s.id)"></i>
            <i class="bi bi-chevron-double-right viewbutton" @click="goToStories(s.id)"></i>
            </div>
        </div>
    </div>
</template>
<script>
    import { mapState } from 'pinia'
    import { useSourcesStore } from '../stores/sources'
    import { fetchSources, deleteSource } from '../api/sourcesApi.js'
    export default {
        
        data() {
            return {

            }  
        },
        computed: {
            ...mapState(useSourcesStore, ['sources'])
        },
        async created() {
            this.updateSources()
        },
        methods: {
            async updateSources(){
                const store = useSourcesStore();
                store.$patch({sources: await fetchSources()})
            },
            goToStories(id) {
                this.$router.push({name: 'stories', params: {id: id}})
            },
            async onDeleteSource(id) {
                await deleteSource(id);
                this.updateSources();
            }
        }
    }
</script>
<style scoped>
    .source-entry {
        border-color: rgba(0,0,0,0.5);
        border-width: 1px;
        border-style: solid;
        border-radius: 10px;
        padding: 0.6em;
        font-size: 1.2em;
        box-shadow: 0px 3px 3px rgba(0,0,0,0.3);
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    .source-entry-list {
        display: flex;
        flex-direction: column;
        gap:7px;
        margin-top: 10px;
    }
    .viewbutton {
        font-size: 2em;
        transition: 0.2s;
    }
    .viewbutton:hover {
        color: rgba(220, 110, 22, 1);
    }
    .notificationScreen {
        text-align:center;
        color: rgba(0,0,0,0.7);
        margin-top: 100px;
        font-size: 20px;
    }
    .source-name {
        font-size: 20px;
        font-weight: bold;
    }
    .small-text {
        font-size: 14px;
        color: rgba(0,0,0,0.7);
    }
</style>