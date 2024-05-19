<template>
    <div class="storiesList">
        <h1 class="roboto"> {{ sourceName }} </h1>
        <div v-for="s in stories" class="storyCard">
            <a :href="s.url" target="_blank" class="clickableCard">
                <span class="storyTitle"> {{ s.title }} </span>
                <span class="block subTitle"> {{ s.time }} </span>
                <span class="block summary"> {{ s.summary }} </span>
            </a>
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
        computed: {
            sourceName() {
                return this.$route.params.source_name;
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
<style scoped>
    .storiesList {
        margin-top: 50px;
    }
    .storyTitle {
        font-size:25px;
        display: block;
        overflow: hidden;
        text-wrap: nowrap;
        text-overflow: ellipsis;
        font-family: 'Roboto Condensed', sans-serif;
        font-weight: bold;
        transition: 0.3s;
    }
    .subTitle{
        color: rgba(0,0,0,0.5);
        font-family: 'Noto Sans', sans-serif;
        font-size: 12px;
    }
    .clickableCard {
        text-decoration: none;
        color: black;
        transition: 0.3s;
    }
    .clickableCard:hover {
        text-decoration: underline;
        .storyTitle {
            color: rgba(0,0,0,0.8);
        }
    }
    .block {
        display:block;
    }
    .summary {
        font-family: 'Noto Serif', serif;
        color: rgba(0,0,0,0.9);
        margin-top: 7px;
        font-size: 15px;
        overflow: hidden;
        text-overflow: ellipsis;
        text-wrap: nowrap;
    }
    .storyCard {
        padding: 15px;
        border-style: solid;
        border-width: 1px;
        border-radius: 10px;
        border-color: rgba(0,0,0,0.3);
        margin-bottom: 10px;
        box-shadow: 0px 3px 3px rgba(0,0,0,0.3);
    }
</style>