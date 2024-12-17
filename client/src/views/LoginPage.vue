<template>
    <div class="container">
      <h1>Авторизация</h1>
      <form @submit.prevent="login">
        <div>
          <label for="username">Имя пользователя</label>
          <input id="username" v-model="username" type="text" required />
        </div>
        <div>
          <label for="password">Пароль</label>
          <input id="password" v-model="password" type="password" required />
        </div>
        <button type="submit">Войти</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import Cookies from "js-cookie";
  
  export default {
    data() {
      return {
        username: "",
        password: "",
      };
    },
    methods: {
      async login() {
        try {
          const formData = new URLSearchParams();
          formData.append("username", this.username);
          formData.append("password", this.password);
  
          const csrfToken = Cookies.get("csrftoken"); // Получаем CSRF токен
  
          const response = await axios.post(
            "/admin/login/?next=/admin/",
            formData,
            {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken, // Передаем CSRF токен
              },
              withCredentials: true,
            }
          );
  
          if (response.status === 200 && !response.data.includes("Please correct the errors below")) {
            alert("Вы успешно вошли!");
            this.$router.push("/"); // Перенаправляем на главную страницу
          } else {
            alert("Ошибка авторизации. Проверьте данные.");
          }
        } catch (error) {
          console.error("Ошибка авторизации:", error.response?.data || error);
          alert("Ошибка авторизации. Проверьте данные.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 400px;
    margin: 0 auto;
  }
  </style>
  