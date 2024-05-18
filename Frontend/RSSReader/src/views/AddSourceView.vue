<template>
    <h1>Add a source</h1>
    <div class="sources-form">
        <form class="sources-form-contents">
            <input type="text" placeholder="Name of RSS feed (e.g. AP News)" v-model="sourceName"/>
            <input type="text" placeholder="RSS Feed URL" v-model="sourceURL"/>
            <input type="button" id="addSrcButton" :onclick="submitForm" value="Submit"/>
        </form>
    </div>
</template>
<script>
    import { createSource } from "../api/sourcesApi"
    import { useRouter } from 'vue-router'
   
    export default {
        data() {
            return {
                sourceName: "",
                sourceURL: ""
            }
        },

        methods: {
            async submitForm() {
                let res = await createSource(this.sourceName, this.sourceURL);
                if (res?.status !== 200) {
                    alert("Error occurred")
                } else {
                    this.$router.push('/')
                }
            }
        }
    }

</script>
<style scoped>
    .sources-form-contents {
        display: flex;
        flex-direction: column;
        width: 40vw;
    }

    #addSrcButton {
        width: 10vw;
        align-self:flex-end;
    }
</style>