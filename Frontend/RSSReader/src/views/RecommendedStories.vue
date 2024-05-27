<template>
    <div class="topBar">
        <h1 class="roboto">Your Briefing</h1>
        <button class="text-button" @click="forceResetCategories" :disabled="loading"><i v-if="!loading"
                class="bi bi-arrow-clockwise"></i> {{ btnText }}</button>
    </div>
    <div>
        <div class="roboto-condensed notificationScreen" v-if="loading"><i class="bi bi-hourglass-split"></i>Loading
            your recommendations; please wait...</div>
        <div v-if="!loading" class="storiesWrapper">
            <div v-if="!fullyUpdated" class="roboto-condensed notFullyUpdatedNotification">
                <i class="bi bi-info-square"></i>&nbsp;
                Some feeds are taking a bit long to respond, so some stories may be older. Try refreshing in a few
                minutes. We are fetching them in the background.
            </div>
            <div v-for="c in categories" :key="c.id">
                <div class="storiesList">
                    <div class="keyword"> {{ c.keyword.toUpperCase() }} </div>
                    <div v-for="s in c.stories.slice(0, 1) " class="mainStory" :key="s.id">

                        <div>
                            <a :href="s.url" target="_blank" class="clickableCard">
                                <span class="storyTitle"> {{ s.title }} </span>
                                <span class="block subTitle"> {{ s.feed_source_name }} | {{ s.time }}
                                    <span v-if="s.neg_sentiment > 0.2">🔥</span>
                                    <span v-if="s.pos_sentiment > 0.2">📈</span>
                                </span>
                                <span class="block summary"> {{ s.summary }} </span>
                            </a>
                        </div>
                        <a :href="`https://archive.today/newest/${s.url}`" target="_blank" class="roboto archiveLink">
                            <i class="bi bi-archive"></i> Archive
                        </a>
                    </div>

                    <hr>

                    <div v-for="s in c.stories.slice(1) " class="smallerStory" :key="s.id">

                        <div>
                            <a class="clickableCard" :href="s.url" target="_blank">
                                <span class="block smallerTitle"> {{ s.title }}</span>
                                <span class="block subTitle"> {{ s.feed_source_name }} | {{ s.time }}

                                    <span v-if="s.neg_sentiment > 0.2">🔥</span>
                                    <span v-if="s.pos_sentiment > 0.2">📈</span>
                                </span>
                            </a>
                        </div>
                        <a :href="`https://archive.today/newest/${s.url}`" target="_blank"
                            class="roboto archiveLink">
                            <i class="bi bi-archive"></i> Archive
                        </a>
                    </div>

                </div>
            </div>
            <div v-if="storiesEmpty" class="roboto-condensed notificationScreen">
                <p><i class="bi bi-rss"></i></p>
                <p>No stories found. <Router-Link :to="{ name: 'sourcelist' }">Add RSS feeds</Router-Link> or check that
                    they are correct.</p>
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
            loading: true,
            fullyUpdated: true
        }
    },
    computed: {
        storiesEmpty() {
            if (this.categories && this.categories.length) {
                return false;
            }
            return true;
        },
        btnText() {
            if (this.loading) return "LOADING...";
            return "REFRESH"
        }
    },
    methods: {
        async getStories() {
            this.loading = true;
            const fetched = await getRecommendedStories();
            this.categories = fetched.categories;
            this.fullyUpdated = fetched.fullyUpdated;
            setTimeout(() => {
                this.loading = false;
            }, LOADING_SCREEN_TIME);

        },
        async forceResetCategories() {
            this.loading = true;
            const fetched = await getRefreshedStoryCategories();
            console.log(fetched);
            this.categories = fetched.categories;
            this.fullyUpdated = fetched.fullyUpdated;
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
    margin-top: -5px;
}

.storyTitle {
    font-size: 30px;
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
    font-size: 20px;
}

.smallerStory {
    margin-top: 10px;
}

.storiesList {
    padding: 15px;
    border-style: solid;
    border-width: 1px;
    border-radius: 10px;
    border-color: rgba(0, 0, 0, 0.3);
    margin-bottom: 10px;
    box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.3);
}

.subTitle {
    color: rgba(0, 0, 0, 0.5);
    font-family: 'Noto Sans', sans-serif;
    font-size: 15px;
}

.clickableCard {
    text-decoration: none;
    color: black;
    transition: 0.3s;
}

.clickableCard:hover {
    text-decoration: underline;

    .storyTitle {
        color: rgba(0, 0, 0, 0.8);
    }
}

.block {
    display: block;
}

.summary {
    font-family: 'Noto Serif', serif;
    color: rgba(0, 0, 0, 0.9);
    margin-top: 7px;
    font-size: 20px;
    overflow: hidden;
    text-overflow: ellipsis;
    text-wrap: nowrap;
}

.keyword {
    font-family: Roboto, sans-serif;
    color: rgba(200, 100, 20, 1);
    font-weight: 700;
    font-size: 20px;
}

.notificationScreen {
    text-align: center;
    color: rgba(0, 0, 0, 0.7);
    margin-top: 100px;
    font-size: 30px;
}

.topBar {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
}

.notFullyUpdatedNotification {
    background-color: rgba(20, 120, 200, 1);
    color: white;
    padding: 10px;
    font-size: 20px;
    margin-bottom: 7px;
    box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.3);
}

.archiveLink {
    text-decoration: none;
    color: rgba(0, 0, 0, 0.5);
    transition: 0.2s;
}

.archiveLink:hover {
    text-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
}
</style>