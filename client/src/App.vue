{% csrf_token %}

<script setup>
import { ref, provide } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { useUserStore } from './stores/user';
import { onMounted } from "vue";
import { useToast } from "vue-toastification";

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
// Состояние двойной аутентификации
const otpKey = ref('');
const otpVerified = ref(false);
const otpLoading = ref(false);
const userStore = useUserStore();
const qrCodeUrl = ref(null);
const toast = useToast();

onMounted(() => {
  userStore.checkAuth(); // Проверка авторизации при загрузке
});

const fetchQrCode = async () => {
  try {
    const response = await axios.get('/api/auth/otp-qr-code/', {
      responseType: 'blob'
    });
    qrCodeUrl.value = URL.createObjectURL(response.data);
  } catch (error) {
    console.error('Ошибка загрузки QR-кода:', error);
    alert('Не удалось загрузить QR-код. Пожалуйста, попробуйте позже.');
  }
};

// Проверить статус OTP
const checkOtpStatus = async () => {
  try {
    const response = await axios.get('/api/auth/otp-status/');
    otpVerified.value = response.data.otp_good;
  } catch (error) {
    console.error('Ошибка проверки OTP:', error);
    otpVerified.value = false;
  }
};

// Отправить OTP-код
const submitOtp = async () => {
  try {
    const response = await axios.post('/api/auth/otp-login/', { key: otpKey.value });
    otpVerified.value = response.data.success;
    if (!otpVerified.value) {
      toast.error("Неверный OTP-код! Попробуйте снова. 🔄", {
        timeout: 4000,
        icon: "❌"
      });
    } else {
      toast.success("Двойная аутентификация успешно выполнена! 🔓", {
        timeout: 4000,
        icon: "✅"
      });
    }
  } catch (error) {
    console.error("Ошибка отправки OTP:", error);
    toast.error("Ошибка при проверке OTP-кода! ⚠️");
  }
};

// Предоставляем OTP состояние и функции другим компонентам
provide('otpVerified', otpVerified);
provide('submitOtp', submitOtp);
provide('checkOtpStatus', checkOtpStatus);
</script>

<template>
  <div>

    <!-- Модальное окно -->
    <div class="modal fade" id="qrModal" tabindex="-1" aria-labelledby="qrModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="qrModalLabel">QR-код для OTP</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
          </div>
          <div class="modal-body text-center">
            <img v-if="qrCodeUrl" :src="qrCodeUrl" alt="QR-код для OTP" class="img-fluid" />
            <p v-else>QR-код загружается...</p>
            <p class="mt-3">
              Отсканируйте этот QR-код с помощью приложения Google Authenticator 
              для настройки двухфакторной аутентификации
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">АвтоИнфо</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Автомобили</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/brands">Бренды</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/owners">Владельцы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/services">Сервисы</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/servicerecords">Записи об обслуживании</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li v-if="userStore.isAuthenticated" class="nav-item">
              <span class="nav-link">
                {{ userStore.user.username }} ({{ userStore.user.is_staff ? 'Администратор' : 'Пользователь' }})
              </span>
            </li>
            <li v-if="userStore.isAuthenticated" class="nav-item">
              <button 
                class="btn btn-outline-primary me-2" 
                data-bs-toggle="modal" 
                data-bs-target="#qrModal"
                @click="fetchQrCode"
              >
                <i class="bi bi-qr-code me-1"></i>
                Настроить 2FA
              </button>
            </li>
            <li v-if="userStore.isAuthenticated" class="nav-item">
              <button class="btn btn-danger" @click="userStore.logout">Выйти</button>
            </li>
            <li v-else class="nav-item">
              <router-link class="btn btn-primary nav-link" to="/login">Войти</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <div class="container">
    <div v-if="!otpVerified" class="otp-auth-section p-3 mb-3 border rounded">
      <h5 class="text-primary">Двойная аутентификация</h5>
      <div class="row">
        <div class="col">
          <input
            type="text"
            class="form-control"
            v-model="otpKey"
            placeholder="Введите OTP-код"
          />
        </div>
        <div class="col-auto">
          <button class="btn btn-success" @click="submitOtp" :disabled="otpLoading">
            {{ otpLoading ? 'Загрузка...' : 'Подтвердить OTP' }}
          </button>
        </div>
      </div>
      <p class="text-danger mt-2">Для доступа к защищённым операциям выполните двойную аутентификацию.</p>
    </div>

    <router-view />
  </div>
</template>

<style>
.otp-auth-section {
  background-color: #f8f9fa;
}

.modal-dialog {
  max-width: 400px;
}

.modal img {
  max-width: 100%;
  height: auto;
}
</style>
