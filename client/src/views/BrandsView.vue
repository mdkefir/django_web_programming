<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { inject } from 'vue';
import { useToast } from "vue-toastification";

const brandToAdd = ref({});
const brandToEdit = ref({});
const brands = ref([]);
const loading = ref(false);
const stats = ref({ total_brands: 0 });
const otpVerified = inject('otpVerified');
const toast = useToast();
const filters = ref({ name: '' });

const fetchBrands = async () => {
  loading.value = true;
  try {
    const params = { ...filters.value };
    const response = await axios.get('/api/brands/', { params });
    brands.value = response.data;
  } catch (error) {
    console.error("Error fetching brands:", error);
    toast.error("Ошибка при загрузке брендов! ❌");
  } finally {
    loading.value = false;
  }
};

const onBrandAdd = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.post('/api/brands/', brandToAdd.value);
    await fetchBrands();
    toast.success("Бренд успешно добавлен! ✨");
    brandToAdd.value = {};
  } catch (error) {
    console.error('Error adding brand:', error);
    toast.error("Ошибка при добавлении бренда! ❌");
  }
};

const onBrandEditClick = (brand) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  brandToEdit.value = { ...brand };
};

const onUpdateBrand = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.put(`/api/brands/${brandToEdit.value.id}/`, brandToEdit.value);
    await fetchBrands();
    toast.success("Бренд успешно обновлен! 🔄");
  } catch (error) {
    console.error("Error updating brand:", error);
    toast.error("Ошибка при обновлении бренда! ❌");
  }
};

const onRemoveClick = async (brand) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  
  try {
    await axios.delete(`/api/brands/${brand.id}/`);
    await fetchBrands();
    toast.success("Бренд успешно удален! 🗑️");
  } catch (error) {
    console.error(error);
    toast.error("Ошибка при удалении бренда! ❌");
  }
};

const fetchStats = async () => {
  try {
    const response = await axios.get('/api/brands/stats/');
    stats.value = response.data;
  } catch (error) {
    console.error("Error fetching stats:", error);
    toast.error("Ошибка при загрузке статистики! ❌");
  }
};

onBeforeMount(async () => {
  await fetchBrands();
  await fetchStats();
});
</script>

<template>
  <div class="container-fluid">
    <div class="stats-section p-3 mb-3 border rounded">
      <h5 class="text-primary">Статистика брендов</h5>
      <div class="row">
        <div class="col">
          <p><strong>Всего брендов:</strong> {{ stats.total_brands }}</p>
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
            placeholder="Название бренда"
            v-model="filters.name"
            @input="fetchBrands"
          />
        </div>
      </div>
    </div>

    <div class="p-2">
      <form @submit.prevent.stop="onBrandAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="brandToAdd.name" required />
              <label for="floatingInput">Название бренда</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div class="pt-2">
        <div v-for="brand in brands" :key="brand.id" class="brand-item">
          <div>{{ brand.name }}</div>
          <div class = "brand-item-buttons">
              <button class="btn btn-secondary" @click="onBrandEditClick(brand)" :data-bs-toggle="otpVerified ? 'modal' : null" data-bs-target="#editBrandModal"><i class="bi bi-pencil-fill"></i></button>
              <button class="btn btn-danger" @click="onRemoveClick(brand)"><i class="bi bi-x"></i></button>
          </div>
        </div>
      </div>

      <!-- Модальное окно редактирования бренда -->
      <div class="modal fade" id="editBrandModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Редактировать бренд</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="form-floating">
                <input class="form-control" type="text" v-model="brandToEdit.name" />
                <label for="floatingInput">Название бренда</label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" @click="onUpdateBrand" data-bs-dismiss="modal">Сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.modal-footer{
  margin-left:0.5rem;
  padding:0.5rem;
}

.brand-item {
  padding: 0.5rem;
  padding-left: 10px;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 4px;
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-content: center;
  align-items: center;
  justify-content: space-between;
}

.brand-item-buttons{
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
