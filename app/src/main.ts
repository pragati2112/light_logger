import {createApp} from 'vue'
import App from './App.vue'
import {router} from './router'
// @ts-ignore
import WaveUI from 'wave-ui'
import {createPinia} from "pinia";
import 'wave-ui/dist/wave-ui.css'

const app = createApp(App)

new WaveUI(app,{
  colors: {
    primary: '#9ac332',
    secondary: '#5d9a26'
  }
})


app.use(router)
    .use(createPinia())
    .mount('#app')