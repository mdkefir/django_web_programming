import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import "bootstrap/dist/css/bootstrap.min.css"; // Стиль
import "bootstrap/dist/js/bootstrap.bundle.min.js"; // JS-функциональность
import 'bootstrap-icons/font/bootstrap-icons.css'; // Иконки
import axios from 'axios';

import App from './App.vue'
import router from './router'

const app = createApp(App)

const toastOptions = {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: "button",
    icon: true,
    rtl: false
}

app.use(createPinia())
app.use(router)
app.use(Toast, toastOptions)

axios.defaults.baseURL = 'http://localhost:8000';  // URL вашего бэкенда
axios.defaults.withCredentials = true;  // Важно для работы с куками

app.mount('#app')
