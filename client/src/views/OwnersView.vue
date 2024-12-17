<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { inject } from 'vue';
import { useToast } from "vue-toastification";

const ownerToAdd = ref({});
const ownerToEdit = ref({});
const owners = ref([]);
const loading = ref(false);
const stats = ref({ total_owners: 0 });
const otpVerified = inject('otpVerified');
const toast = useToast();
const filters = ref({ name: '', car: '' });
const cars = ref([]);

const fetchCars = async () => {
  try {
    const response = await axios.get('/api/cars/');
    cars.value = response.data;
  } catch (error) {
    console.error('Error fetching cars:', error);
    toast.error("Ошибка при загрузке списка автомобилей! ❌");
  }
};

const fetchOwners = async () => {
  loading.value = true;
  try {
    const params = { ...filters.value };
    const response = await axios.get('/api/owners/', { params });
    owners.value = response.data;
  } catch (error) {
    console.error("Error fetching owners:", error);
    toast.error("Ошибка при загрузке владельцев! ❌");
  } finally {
    loading.value = false;
  }
};

const onOwnerAdd = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.post('/api/owners/', ownerToAdd.value);
    await fetchOwners();
    toast.success("Владелец успешно добавлен! ✨");
    ownerToAdd.value = {};
  } catch (error) {
    console.error('Error adding owner:', error);
    toast.error("Ошибка при добавлении владельца! ❌");
  }
};

const onOwnerEditClick = (owner) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  ownerToEdit.value = {
    id: owner.id,
    name: owner.name,
    car: owner.car.id
  };
};

const onUpdateOwner = async () => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }

  try {
    await axios.put(`/api/owners/${ownerToEdit.value.id}/`, ownerToEdit.value);
    await fetchOwners();
    toast.success("Данные владельца успешно обновлены! 🔄");
  } catch (error) {
    console.error("Error updating owner:", error);
    toast.error("Ошибка при обновлении данных владельца! ❌");
  }
};

const onRemoveClick = async (owner) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  
  try {
    await axios.delete(`/api/owners/${owner.id}/`);
    await fetchOwners();
    toast.success("Владелец успешно удален! 🗑️");
  } catch (error) {
    console.error(error);
    toast.error("Ошибка при удалении владельца! ❌");
  }
};

const fetchStats = async () => {
  try {
    const response = await axios.get('/api/owners/stats/');
    stats.value = response.data;
  } catch (error) {
    console.error("Error fetching stats:", error);
    toast.error("Ошибка при загрузке статистики! ❌");
  }
};

onBeforeMount(async () => {
  await fetchOwners();
  await fetchStats();
  await fetchCars();
});
</script>

<template>
  <div class="container-fluid">
    <div class="stats-section p-3 mb-3 border rounded">
      <h5 class="text-primary">Статистика владельцев</h5>
      <div class="row">
        <div class="col">
          <p><strong>Всего владельцев:</strong> {{ stats.total_owners }}</p>
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
            placeholder="Имя владельца"
            v-model="filters.name"
            @input="fetchOwners"
          />
        </div>
        <div class="col">
          <select class="form-select" v-model="filters.car" @change="fetchOwners">
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
      </div>
    </div>

    <div class="p-2">
      <form @submit.prevent.stop="onOwnerAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="ownerToAdd.name" required />
              <label for="floatingInput">Имя владельца</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating">
              <select class="form-select" v-model="ownerToAdd.car" required>
                <option :value="car.id" v-for="car in cars" :key="car.id">
                  {{ car.brand.name }} {{ car.name }}
                </option>
              </select>
              <label for="floatingInput">Автомобиль</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div class="row pt-4">
        <div class="col"><strong>Владелец</strong></div>
        <div class="col"><strong>Автомобиль</strong></div>
        <div class="col-5"><strong>Фото автомобиля</strong></div>
      </div>

      <div class="pt-2">
        <div v-for="owner in owners" :key="owner.id" class="owner-item">
          <div>{{ owner.name }}</div>
          <div>{{ owner.car.brand.name }} {{ owner.car.name }} {{ owner.car.year }} {{ owner.car.color }}</div>
          <div>
            <img
              v-if="owner.car.picture"
              :src="owner.car.picture"
              alt="Фото"
              style="max-width: 60px; max-height: 60px; cursor: pointer;"
              @click="currentImage = owner.car.picture"
              data-bs-toggle="modal"
              data-bs-target="#imageModal"
            />
            <span v-else>Нет фото</span>
          </div>
          <div class = "owner-item-buttons">
            <button class="btn btn-secondary" @click="onOwnerEditClick(owner)" :data-bs-toggle="otpVerified ? 'modal' : null" data-bs-target="#editOwnerModal">
              <i class="bi bi-pencil-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(owner)">
              <i class="bi bi-x"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Модальное окно просмотра изображения -->

      <div class="modal fade" id="imageModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Просмотр изображения</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
            </div>
            <div class="modal-body text-center">
              <img v-if="currentImage" :src="currentImage" alt="Изображение" class="img-fluid" />
            </div>
          </div>
        </div>
      </div>


      <!-- Модальное окно редактирования владельца -->
      <div class="modal fade" id="editOwnerModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Редактировать владельца</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="form-floating">
                <input class = "form-control" type="text" v-model="ownerToEdit.name" />
                <label for="floatingInput">Имя владельца</label>
              </div>
              <div class="form-floating">
                <select class = "form-select" v-model="ownerToEdit.car">
                  <option :value="car.id" v-for="car in cars" :key="car.id">
                    {{ car.brand.name }} {{ car.name }} {{ car.year }}, {{ car.color }}
                  </option>
                </select>
                <label for="floatingInput">Автомобиль</label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" @click="onUpdateOwner" data-bs-dismiss="modal">Сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>





<style lang="scss" scoped>
.owner-item {
  padding: 0.5rem;
  padding-left: 10px;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 4px;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto auto;
  align-content: center;
  align-items: center;
  justify-content: space-between;
}

.owner-item-buttons{
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
