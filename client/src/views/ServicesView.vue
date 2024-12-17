<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { inject } from 'vue';
import { useToast } from "vue-toastification";
import ServiceMap from '@/components/ServiceMap.vue';

const serviceToAdd = ref({});
const serviceToEdit = ref({});
const services = ref([]);
const loading = ref(false);
const stats = ref({ total_services: 0 });
const otpVerified = inject('otpVerified');
const toast = useToast();
const filters = ref({ name: '', location: '' });

const fetchServices = async () => {
  loading.value = true;
  try {
    const params = { ...filters.value };
    const response = await axios.get('/api/services/', { params });
    services.value = response.data;
  } catch (error) {
    console.error("Error fetching services:", error);
    toast.error("Ошибка при загрузке сервисов! ❌");
  } finally {
    loading.value = false;
  }
};

const onServiceAdd = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.post('/api/services/', serviceToAdd.value);
    await fetchServices();
    toast.success("Сервис успешно добавлен! ✨");
    serviceToAdd.value = {};
  } catch (error) {
    console.error('Error adding service:', error);
    toast.error("Ошибка при добавлении сервиса! ❌");
  }
};

const onServiceEditClick = (service) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  serviceToEdit.value = { ...service };
};

const onUpdateService = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.put(`/api/services/${serviceToEdit.value.id}/`, serviceToEdit.value);
    await fetchServices();
    toast.success("Сервис успешно обновлен! 🔄");
  } catch (error) {
    console.error("Error updating service:", error);
    toast.error("Ошибка при обновлении сервиса! ❌");
  }
};

const onRemoveClick = async (service) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  
  try {
    await axios.delete(`/api/services/${service.id}/`);
    await fetchServices();
    toast.success("Сервис успешно удален! 🗑️");
  } catch (error) {
    console.error(error);
    toast.error("Ошибка при удалении сервиса! ❌");
  }
};

const fetchStats = async () => {
  try {
    const response = await axios.get('/api/services/stats/');
    stats.value = response.data;
  } catch (error) {
    console.error("Error fetching stats:", error);
    toast.error("Ошибка при загрузке статистики! ❌");
  }
};

onBeforeMount(async () => {
  await fetchServices();
  await fetchStats();
});
</script>

<template>
  <div class="container-fluid">
    <ServiceMap />
    <div class="stats-section p-3 mb-3 border rounded">
      <h5 class="text-primary">Статистика сервисов</h5>
      <div class="row">
        <div class="col">
          <p><strong>Всего сервисов:</strong> {{ stats.total_services }}</p>
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="filters-section p-3 mb-3 border rounded">
      <h5 class="text-primary">Фильтры</h5>
      <div class="row">
        <div class="col">
          <input
            type="text"
            class="form-control"
            placeholder="Название сервиса"
            v-model="filters.name"
            @input="fetchServices"
          />
        </div>
        <div class="col">
          <input
            type="text"
            class="form-control"
            placeholder="Местоположение"
            v-model="filters.location"
            @input="fetchServices"
          />
        </div>
      </div>
    </div>
    
    <div class="p-2">
      <form @submit.prevent.stop="onServiceAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="serviceToAdd.name" required />
              <label for="floatingInput">Название сервиса</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="serviceToAdd.location" required />
              <label for="floatingInput">Местоположение</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div class="row pt-4">
        <div class="col-5"><strong>Сервис</strong></div>
        <div class="col"><strong>Местоположение</strong></div>
      </div>

      <div class="pt-2">
        <div v-for="service in services" :key="service.id" class="service-item">
          <div>{{ service.name }}</div>
          <div>{{ service.location }}</div>
          <div class="service-item-buttons">
            <button class="btn btn-secondary" @click="onServiceEditClick(service)" :data-bs-toggle="otpVerified ? 'modal' : null" data-bs-target="#editServiceModal"><i class="bi bi-pencil-fill"></i></button>
            <button class="btn btn-danger" @click="onRemoveClick(service)"><i class="bi bi-x"></i></button>
          </div>
        </div>
      </div>

      <!-- Модальное окно редактирования сервиса -->
      <div class="modal fade" id="editServiceModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Редактировать сервис</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="form-floating">
                <input class="form-control" type="text" v-model="serviceToEdit.name" />
                <label for="floatingInput">Название сервиса</label>
              </div>
              <div class="form-floating">
                <input class="form-control" type="text" v-model="serviceToEdit.location" />
                <label for="floatingInput">Местоположение</label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" @click="onUpdateService" data-bs-dismiss="modal">Сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.service-item {
  padding: 0.5rem;
  padding-left: 10px;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 4px;
  display: grid;
  grid-template-columns: 1fr 1fr auto auto;
  align-content: center;
  align-items: center;
  justify-content: space-between;
}

.service-item-buttons{
  display: flex;
  gap: 0.2rem;
}

.form-control{
  margin-top: 0.5rem;
}

.form-select{
  margin-top: 0.5rem;
}
</style>
