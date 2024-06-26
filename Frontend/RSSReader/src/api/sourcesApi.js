import axios from 'axios';
const api = axios.create({
    baseURL: 'http://localhost:5000/'
});
export async function fetchSources() {
    let res = await api.get('/getSources');
    console.log(res);
    let parsed = res?.data?.feeds || [];
    return parsed;
}

export async function createSource(name, url) {
    let res = await api.post('/createSource', {"name": name, "url": url})
    return res;
}

export async function deleteSource(id) {
    let res = await api.delete('/deleteSource', {params: {"id": id}})
    return res;
}

export async function fetchStories(id) {
    let res = await api.get('/fetchStoriesFromSource', {params: {"id": id}});
    return res?.data?.stories || [];
}

export async function getRecommendedStories() {
    let res = await api.get('/getStoryCategories');
    return {
        categories: res?.data?.categories || [],
        fullyUpdated: res?.data?.fullyUpdated || false
    }
}

export async function getRefreshedStoryCategories() {
    let res = await api.get('/getRefreshedStoryCategories');
    return {
        categories: res?.data?.categories || [],
        fullyUpdated: res?.data?.fullyUpdated || false
    }
}

