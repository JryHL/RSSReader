<template>
    <div>
        <div v-for="s in stories">
            <h2> <a :href="s.url">{{ s.title }}</a> </h2>
            <div> {{ s.time }} </div>
        </div>
    </div>
</template>

<script>
    import { fetchStories } from '../api/sourcesApi.js'
    export default {
        data() {
            return {
                stories: []
            }
        },
        methods: {
            async getStories() {
                const fetched = await fetchStories(this.$route.params.id)
                console.log(fetched)
                this.stories = fetched;
            }

        },
        async created() {
            this.getStories();
        }
    }
</script>