import { createRouter, createWebHashHistory } from "vue-router";
const routes = [
    { path: '/', name: 'welcome', component: () => import('/@src/components/HelloWorld.vue') },
]
export const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
})