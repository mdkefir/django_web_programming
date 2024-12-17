<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { inject } from 'vue';
import { useToast } from "vue-toastification";

const recordToAdd = ref({});
const recordToEdit = ref({});
const records = ref([]);
const cars = ref([]);
const services = ref([]);
const loading = ref(false);
const stats = ref({
  total_records: 0,
  total_services: 0,
  avg_records_per_service: 0,
  top_service_name: '',
  top_service_count: 0
});
const otpVerified = inject('otpVerified');
const toast = useToast();
const filters = ref({ car: '', service: '', date: '' });

const fetchCars = async () => {
  try {
    const response = await axios.get('/api/cars/');
    cars.value = response.data;
  } catch (error) {
    console.error('Error fetching cars:', error);
    toast.error("Ошибка при загрузке списка автомобилей! ❌");
  }
};

const fetchServices = async () => {
  try {
    const response = await axios.get('/api/services/');
    services.value = response.data;
  } catch (error) {
    console.error('Error fetching services:', error);
    toast.error("Ошибка при загрузке списка сервисов! ❌");
  }
};

const fetchRecords = async () => {
  loading.value = true;
  try {
    const params = { ...filters.value };
    const response = await axios.get('/api/service-records/', { params });
    records.value = response.data;
  } catch (error) {
    console.error("Error fetching records:", error);
    toast.error("Ошибка при загрузке записей! ❌");
  } finally {
    loading.value = false;
  }
};

const onRecordAdd = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.post('/api/service-records/', recordToAdd.value);
    await fetchRecords();
    toast.success("Запись успешно добавлена! ✨");
    recordToAdd.value = {};
  } catch (error) {
    console.error('Error adding record:', error);
    toast.error("Ошибка при добавлении записи! ❌");
  }
};

const onRecordEditClick = (record) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  recordToEdit.value = {
    id: record.id,
    car: record.car.id,
    service: record.service.id,
    date: record.date,
    details: record.details
  };
};

const onUpdateRecord = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.put(`/api/service-records/${recordToEdit.value.id}/`, recordToEdit.value);
    await fetchRecords();
    toast.success("Запись успешно обновлена! 🔄");
  } catch (error) {
    console.error("Error updating record:", error);
    toast.error("Ошибка при обновлении записи! ❌");
  }
};

const onRemoveClick = async (record) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  
  try {
    await axios.delete(`/api/service-records/${record.id}/`);
    await fetchRecords();
    toast.success("Запись успешно удалена! 🗑️");
  } catch (error) {
    console.error(error);
    toast.error("Ошибка при удалении записи! ❌");
  }
};

const fetchStats = async () => {
  try {
    const response = await axios.get('/api/service-records/stats/');
    stats.value = response.data;
  } catch (error) {
    console.error("Error fetching stats:", error);
    toast.error("Ошибка при загрузке статистики! ❌");
  }
};

onBeforeMount(async () => {
  await fetchRecords();
  await fetchStats();
  await fetchCars();
  await fetchServices();
});
</script>

<template>
  <div class="container-fluid">
    <div class="stats-section p-3 mb-3 border rounded">
        <h5 class="text-primary">Статистика записей об обслуживании</h5>
        <div class="row">
          <div class="col">
            <p><strong>Всего записей:</strong> {{ stats.total_records || 0 }}</p>
            <p><strong>Всего сервисов:</strong> {{ stats.total_services || 0 }}</p>
          </div>
          <div class="col">
            <p><strong>Среднее количество записей на сервис:</strong> {{ stats.avg_records_per_service?.toFixed(2) || 0 }}</p>
            <p><strong>Самый популярный сервис:</strong> {{ stats.top_service_name || 'Не найден' }} ({{ stats.top_service_count || 0 }} записей)</p>
          </div>
        </div>
      </div>

      <!-- Фильтры -->
    <div class="filters-section p-3 mb-3 border rounded">
      <h5 class="text-primary">Фильтры</h5>
      <div class="row">
        <div class="col">
          <select class="form-select" v-model="filters.car" @change="fetchRecords">
            <option value="">Все автомобили</option>
            <option
              v-for="car in cars"
              :key="car.id"
              :value="car.id"
            >
              {{ car.brand.name }} {{ car.name }} {{ car.year }}, {{ car.color }}
            </option>
          </select>
        </div>
        <div class="col">
          <select class="form-select" v-model="filters.service" @change="fetchRecords">
            <option value="">Все сервисы</option>
            <option
              v-for="service in services"
              :key="service.id"
              :value="service.id"
            >
              {{ service.name }}
            </option>
          </select>
        </div>
        <div class="col">
          <input
            type="date"
            class="form-control"
            v-model="filters.date"
            @input="fetchRecords"
          />
        </div>
      </div>
    </div>
    
    <div class="p-2">
      <form @submit.prevent.stop="onRecordAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="recordToAdd.car" required>
                <option :value="car.id" v-for="car in cars">{{ car.brand.name }} {{ car.name }} {{ car.year }}, {{ car.color }}</option>
              </select>
              <label for="floatingInput">Автомобиль</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="recordToAdd.service" required>
                <option :value="service.id" v-for="service in services">{{ service.name }}</option>
              </select>
              <label for="floatingInput">Сервис</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input type="date" class="form-control" v-model="recordToAdd.date" required />
              <label for="floatingInput">Дата обслуживания</label>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <textarea class="form-control" v-model="recordToAdd.details" placeholder="Детали обслуживания (необязательно)"></textarea>
              <label for="floatingTextarea">Детали обслуживания</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary mt-3">Добавить</button>
          </div>
        </div>
      </form>

      <div class="row pt-4">
        <div class="col-3"><strong>Автомобиль</strong></div>
        <div class="col-2"><strong>Сервис</strong></div>
        <div class="col-3"><strong>Дата обслуживания</strong></div>
        <div class="col"><strong>Детали</strong></div>
      </div>

      <div class="pt-2">
        <div v-for="record in records" :key="record.id" class="record-item">
          <div>{{ record.car.brand.name }} {{ record.car.name }} {{ record.car.year }}, {{ record.car.color }}</div>
          <div>{{ record.service.name }}</div>
          <div>{{ record.date }}</div>
          <p v-if="record.details">{{ record.details }}</p>
          <div class = "record-item-buttons">
            <button class="btn btn-secondary" @click="onRecordEditClick(record)" :data-bs-toggle="otpVerified ? 'modal' : null" data-bs-target="#editRecordModal"><i class="bi bi-pencil-fill"></i></button>
            <button class="btn btn-danger" @click="onRemoveClick(record)"><i class="bi bi-x"></i></button>
          </div>
        </div>
      </div>

      <!-- Модальное окно редактирования записи об обслуживании -->
      <div class="modal fade" id="editRecordModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Редактировать запись</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="form-floating">
                <select class="form-select" v-model="recordToEdit.car">
                  <option :value="car.id" v-for="car in cars" :key="car.id">
                    {{ car.brand.name }} {{ car.name }} {{ car.year }}, {{ car.color }}
                  </option>
                </select>
                <label for="floatingInput">Автомобиль</label>
              </div>
              <div class="form-floating">
                <select class="form-select" v-model="recordToEdit.service">
                  <option :value="service.id" v-for="service in services" :key="service.id">
                    {{ service.name }}
                  </option>
                </select>
                <label for="floatingInput">Сервис</label>
              </div>
              <div class="form-floating">
                <input type="date" class="form-control" v-model="recordToEdit.date" required />
                <label for="floatingInput">Дата обслуживания</label>
              </div>
              <div class="form-floating">
                <textarea class="form-control" v-model="recordToEdit.details" placeholder="Детали обслуживания (необязательно)"></textarea>
                <label for="floatingInput">Детали обслуживания</label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" @click="onUpdateRecord" data-bs-dismiss="modal">Сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.record-item {
  padding: 0.5rem;
  padding-left: 10px;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 4px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto auto;
  align-content: center;
  align-items: center;
  justify-content: space-between;
}

.record-item-buttons{
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
