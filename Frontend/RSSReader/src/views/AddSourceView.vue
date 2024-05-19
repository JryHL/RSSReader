<template>
    <div class="source-add-wrap">
        <h1 class="roboto">Add a source</h1>
        <div class="sources-form">
            <form class="sources-form-contents">
                <input type="text" class="text-input" placeholder="Name of RSS feed (e.g. AP News)" v-model="sourceName"/>
                <input type="text" class="text-input" placeholder="RSS Feed URL" v-model="sourceURL"/>
                <input type="button" class="text-button" id="addSrcButton" :onclick="submitForm" :value="buttonValue" :disabled="buttonDisabled"/>
            </form>
        </div>
    </div>
</template>
<script>
    import { createSource } from "../api/sourcesApi"
    import { useRouter } from 'vue-router'
   
    export default {
        data() {
            return {
                sourceName: "",
                sourceURL: "",
                buttonDisabled: false,
                buttonValue: "SUBMIT"
            }
        },

        methods: {
            async submitForm() {
                this.buttonDisabled = true;
                this.buttonValue = "SUBMITTING..."
                let res = await createSource(this.sourceName, this.sourceURL);
                if (res?.status !== 200) {
                    alert("An error occurred")
                    this.$router.push({name: "sourcelist"})
                } else {
                    this.$router.push({name: "sourcelist"})
                }
            }
        }
    }

</script>
<style scoped>
    .sources-form-contents {
        display: flex;
        flex-direction: column;
        width: 50%;
        gap: 10px;
    }

    #addSrcButton {
        align-self:flex-end;
    }
    .source-add-wrap {
        margin-top: 50px;
    }
</style>