<template>
  <div class="login-container">
    <div class="card">
      <div class="card-body">
        <h3 class="card-title text-center mb-4">Вход в систему</h3>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Имя пользователя</label>
            <input
              type="text"
              class="form-control"
              id="username"
              v-model="username"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Пароль</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="password"
              required
            />
          </div>
          <div v-if="userStore.error" class="alert alert-danger">
            {{ userStore.error }}
          </div>
          <button
            type="submit"
            class="btn btn-primary w-100"
            :disabled="userStore.isLoading"
          >
            {{ userStore.isLoading ? 'Загрузка...' : 'Войти' }}
          </button>
        </form>
        <div class="text-center mt-3">
          <a href="/admin" class="text-decoration-none">Войти через админ-панель</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const userStore = useUserStore();
const router = useRouter();
const username = ref('');
const password = ref('');

const handleLogin = async () => {
  const success = await userStore.login(username.value, password.value);
  if (success) {
    router.push('/');
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 40px auto;
}

.card {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style> 