<template>
    <h2>Recommended stories</h2>
    <div>
        <input type="button" value="Refresh Recommendations" @click="forceResetCategories" />

        <div class="loadingScreen" v-if="loading"><i class="bi bi-hourglass-split"></i>Loading your recommendations; please wait...</div>

        <div v-if="!loading" class="storiesWrapper">
            <div v-for="c in categories">
                <div class="storiesList">
                    <div v-for="s in c.stories.slice(0,1) " class="storyCard">
                        <a :href="s.url" target="_blank" class="clickableCard">
                            <span class="storyTitle"> {{ s.title }} </span>
                            <span class="subTitle"> {{ s.feed_source_name }} | {{ s.time }} </span>
                            <span class="summary"> {{ s.summary }} </span>
                        </a>
                    </div>
                    <div v-for="s in c.stories.slice(1) " class="smallerStory">
                        <div class="smallerStoryLink"> <a :href="s.url" target="_blank"> {{ s.title }} </a> </div>
                        <div> {{ s.feed_source_name }} | {{ s.time }} </div>
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
.storiesWrapper {
    margin-top: 10px;
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
    display: block;
    color: rgba(0,0,0,0.5);
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
</style>