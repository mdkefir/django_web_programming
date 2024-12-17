import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null
  }),
  actions: {
    async checkAuth() {
      try {
        const response = await axios.get("/api/auth/user/");
        this.user = response.data;
        this.isAuthenticated = true;
        this.error = null;
      } catch (error) {
        this.user = null;
        this.isAuthenticated = false;
        this.error = "Пользователь не авторизован";
      }
    },
    async login(username, password) {
      this.isLoading = true;
      try {
        await axios.get('/api/auth/csrf/');
        
        const response = await axios.post('/api/auth/login/', {
          username,
          password,
        });
        
        this.user = response.data;
        this.isAuthenticated = true;
        this.error = null;
        return true;
      } catch (error) {
        this.error = error.response?.data?.error || "Ошибка авторизации";
        return false;
      } finally {
        this.isLoading = false;
      }
    },
    async logout() {
      try {
        await axios.post("/api/auth/logout/");
        this.user = null;
        this.isAuthenticated = false;
      } catch (error) {
        console.error("Ошибка при выходе:", error);
      }
    }
  }
});
