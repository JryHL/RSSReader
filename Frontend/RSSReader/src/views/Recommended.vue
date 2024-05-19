<template>
    <div class="topBar">
        <h1 class="roboto">Your Briefing</h1>
        <button class="text-button" @click="forceResetCategories"><i class="bi bi-arrow-clockwise"></i> REFRESH</button>
    </div>
    <div>


        <div class="roboto-condensed notificationScreen" v-if="loading"><i class="bi bi-hourglass-split"></i>Loading your recommendations; please wait...</div>

        <div v-if="!loading" class="storiesWrapper">
            <div v-for="c in categories">
                <div class="storiesList">
                    <div class="keyword"> {{ c.keyword.toUpperCase() }} </div>
                    <div v-for="s in c.stories.slice(0,1) " class="storyCard">
                        <a :href="s.url" target="_blank" class="clickableCard">
                            <span class="storyTitle"> {{ s.title }} </span>
                            <span class="block subTitle"> {{ s.feed_source_name }} | {{ s.time }} </span>
                            <span class="block summary"> {{ s.summary }} </span>
                        </a>
                    </div>
                    <ul>
                    <li v-for="s in c.stories.slice(1) " class="smallerStory">
                        <a class="clickableCard" :href="s.url" target="_blank"> 
                            <span class="block smallerTitle"> {{ s.title }}</span>
                            <span class="block subTitle"> {{ s.feed_source_name }} | {{ s.time }} </span>
                        </a>
                        
                    </li>
                    </ul>
                </div>
            </div>
            <div v-if="storiesEmpty" class="roboto-condensed notificationScreen">
                <p><i class="bi bi-rss"></i></p>
                <p>No stories found. <Router-Link :to="{name: 'sourcelist'}">Add RSS feeds</Router-Link> or check that they are correct.</p>
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
    computed: {
        storiesEmpty() {
            if (this.categories && this.categories.length) {
                return false;
            }
            return true;
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

.smallerTitle {
    overflow: hidden;
    text-wrap: nowrap;
    text-overflow: ellipsis;
    font-family: 'Roboto Condensed', sans-serif;
}

.storiesList {
    padding: 15px;
    border-style: solid;
    border-width: 1px;
    border-radius: 10px;
    border-color: rgba(0,0,0,0.3);
    margin-bottom: 10px;
    box-shadow: 0px 3px 3px rgba(0,0,0,0.3);
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
.keyword {
    font-family: Roboto, sans-serif;
    color: rgba(200, 100, 20, 1);
    font-weight: 700;
}

.notificationScreen {
    text-align:center;
    color: rgba(0,0,0,0.7);
    margin-top: 100px;
    font-size: 20px;
}

.topBar {
    display: flex;
    flex-direction: row;
    align-items:center;
    gap: 10px;
}
</style>