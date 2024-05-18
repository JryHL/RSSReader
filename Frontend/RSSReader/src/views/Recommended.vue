<template>
    <h2>Recommended stories</h2>
    <div>
        <input type="button" value="Refresh Recommendations" @click="forceResetCategories" />

        <div class="loadingScreen" v-if="loading"><i class="bi bi-hourglass-split"></i>Loading your recommendations; please wait...</div>

        <div v-if="!loading">
            <div v-for="c in categories">
                <h3> {{ c.keyword.charAt(0).toUpperCase() + c.keyword.slice(1) }} </h3>
                <div class="storiesList">
                    <div v-for="s in c.stories" class="storyCard">
                        <div> <a :href="s.url" target="_blank"> {{ s.title }} </a> </div>
                        <div> {{ s.time }} </div>
                        <div> {{ s.feed_source_name }} </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import { getRecommendedStories, getRefreshedStoryCategories } from '../api/sourcesApi.js';
import { LOADING_SCREEN_TIME } from '@/common/constants.js';
export default {
    data() {
        return {
            categories: [],
            loading: true
        }
    },
    methods: {
        async getStories() {
            this.loading = true;
            const fetched = await getRecommendedStories();
            this.categories = fetched;
            setTimeout(() => {
                this.loading = false;
            }, LOADING_SCREEN_TIME);

        },
        async forceResetCategories() {
            this.loading = true;
            const fetched = await getRefreshedStoryCategories();
            console.log(fetched);
            this.categories = fetched;
            setTimeout(() => {
                this.loading = false;
            }, LOADING_SCREEN_TIME);
        }
    },
    async created() {
        this.getStories();
    }
}
</script>
<style scoped>
.loadingScreen {
    width: 100%;
    height: 100%;
    text-align: center;
    font-family: sans-serif;
    font-size: 2em;
    color: rgba(0, 0, 0, 0.5);
}
.storiesList {
    display: flex;
    overflow:auto;
    gap: 5px;

}
.storyCard {
    border-style: solid;
    border-width: 1px;
    border-color: rgba(0,0,0,0.5);
    border-radius: 5px;
    box-shadow: 0px 3px 3px rgba(0,0,0,0.5);
    padding: 5px;
    min-width: 300px;
    width: 300px;
    height: 200px;
}
</style>