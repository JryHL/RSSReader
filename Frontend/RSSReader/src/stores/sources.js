import { defineStore } from 'pinia'

export const useSourcesStore = defineStore('sources', {
    state: () => (
        {
            sources: []
        }
    ),
    actions: {
        addSource(source) {
            this.sources += source;
        }
    }
})