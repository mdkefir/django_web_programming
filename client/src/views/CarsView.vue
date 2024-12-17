<script setup>
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import { inject } from 'vue';
import { useToast } from "vue-toastification";

const carToAdd = ref({});
const carToEdit = ref({});
const cars = ref([]);
const loading = ref(false);
const carsPictureRef = ref(null);
const carsPictureUpdateRef = ref(null);
const carAddImageUrl = ref(null);
const currentImage = ref(null);
const stats = ref({ total_cars: 0, avg_year: 0, max_year: 0, min_year: 0 }); 
const brands = ref([]);
const otpVerified = inject('otpVerified');
const checkOtpStatus = inject('checkOtpStatus');
const filters = ref({ name: '', brand: '', year: '', color: '' });
const isExporting = ref(false);
const toast = useToast();



const fetchCars = async () => {
  loading.value = true;

  const params = { ...filters.value };
  const response = await axios.get('/api/cars/', { params });

  cars.value = response.data;
  loading.value = false;
};

const fetchBrands = async () => {
  try {
    const response = await axios.get('/api/brands/');
    brands.value = response.data;
  } catch (error) {
    console.error("Error fetching brands:", error);
  }
};

const fetchStats = async () => {
  try {
    const response = await axios.get('/api/cars/stats/');
    stats.value = response.data;
  } catch (error) {
    console.error("Error fetching stats:", error);
  }
};

const onCarAdd = async () => {
  if (!otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }

  const formData = new FormData();
  try {
    formData.append('name', carToAdd.value.name);
    formData.append('brand', carToAdd.value.brand);
    if (carsPictureRef.value?.files[0]) {
      formData.append('picture', carsPictureRef.value.files[0]);
    }
    formData.append('year', carToAdd.value.year);
    formData.append('color', carToAdd.value.color);

    await axios.post('/api/cars/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchCars();
  } catch (error) {
    console.error('Error adding car:', error.response.data);
  }
  carToAdd.value = {}; // Сбрасываем данные автомобиля
  carsPictureRef.value.value = ""; // Сбрасываем input для файла
  carAddImageUrl.value = {};
};

const onUpdateCar = async () => {
  if (!otpVerified.value) {
    alert("Доступ запрещён. Выполните двойную аутентификацию.");
    return;
  }

  const formData = new FormData();
  try {
    formData.append('name', carToEdit.value.name);
    formData.append('brand', carToEdit.value.brand); // Передаем ID бренда
    if (carsPictureUpdateRef.value?.files[0]) {
      formData.append('picture', carsPictureUpdateRef.value.files[0]); // Обновляем изображение, если оно выбрано
    }
    formData.append('year', carToEdit.value.year);
    formData.append('color', carToEdit.value.color);

    await axios.put(`/api/cars/${carToEdit.value.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await fetchCars();

    // Очистка после успешного обновления
    carsPictureUpdateRef.value.value = ""; // Сбрасываем input для файла
  } catch (error) {
    console.error("Error updating car:", error.response.data);
  }
};

const onCarEditClick = (car) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  carToEdit.value = { ...car, brand: car.brand.id, year: car.year, color: car.color};
};


const onRemoveClick = async (car) => {
  if (!otpVerified.value) {
    toast.warning("Требуется двойная аутентификация! 🔐", {
      timeout: 4000,
      icon: "🔒"
    });
    return;
  }
  
  try {
    await axios.delete(`/api/cars/${car.id}/`);
    await fetchCars();
    toast.success("Автомобиль успешно удален! 🗑️");
  } catch (error) {
    console.error(error);
    toast.error("Ошибка при удалении автомобиля! ❌");
  }
};

async function carsAddPictureChange(){
  carAddImageUrl.value = URL.createObjectURL(carsPictureRef.value.files[0])
}

const exportToExcel = async () => {
  try {
    isExporting.value = true;
    const response = await axios.get('/api/cars/export_excel/', {
      responseType: 'blob'
    });
    
    // Создаем ссылку для скачивания
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    
    // Имя файла из заголовка Content-Disposition или дефолтное
    const contentDisposition = response.headers['content-disposition'];
    let filename = 'cars.xlsx';
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename=(.+)/);
      if (filenameMatch.length === 2) filename = filenameMatch[1];
    }
    
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    toast.success("Файл успешно экспортирован! 📊");
  } catch (error) {
    console.error('Ошибка при экспорте:', error);
    toast.error("Ошибка при экспорте данных! ❌");
  } finally {
    isExporting.value = false;
  }
};

onBeforeMount(async () => {
  await fetchCars();
  await fetchBrands();
  await fetchStats();
  await checkOtpStatus();
});

</script>

<template>
  <div class="container-fluid">
    <div class="stats-section p-3 mb-3 border rounded">
      <h5 class="text-primary">Статистика автомобилей</h5>
      <div class="row">
        <div class="col">
          <p><strong>Всего автомобилей:</strong> {{ stats.total_cars }}</p>
          <p><strong>Средний год выпуска:</strong> {{ Math.round(stats.avg_year) }}</p>
        </div>
        <div class="col">
          <p><strong>Самый ранний год выпуска:</strong> {{ stats.min_year }}</p>
          <p><strong>Самый поздний год выпуска:</strong> {{ stats.max_year }}</p>
        </div>
      </div>
      <div class="text-end">
        <button 
          class="btn btn-success" 
          @click="exportToExcel"
          :disabled="isExporting"
        >
          <i class="bi bi-file-earmark-excel me-2"></i>
          {{ isExporting ? 'Экспорт...' : 'Экспорт в Excel' }}
        </button>
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
            placeholder="Название"
            v-model="filters.name"
            @input="fetchCars"
          />
        </div>
        <div class="col">
          <select class="form-select" v-model="filters.brand" @change="fetchCars">
            <option value="">Все бренды</option>
            <option v-for="brand in brands" :key="brand.id" :value="brand.id">
              {{ brand.name }}
            </option>
          </select>
        </div>
        <div class="col">
          <input
            type="number"
            class="form-control"
            placeholder="Год"
            v-model="filters.year"
            @input="fetchCars"
          />
        </div>
        <div class="col">
          <input
            type="text"
            class="form-control"
            placeholder="Цвет"
            v-model="filters.color"
            @input="fetchCars"
          />
        </div>
      </div>
    </div>

    <div class="p-2">
      <form @submit.prevent.stop="onCarAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <!-- ТУТ ПОДКЛЮЧИЛ carToAdd.name -->
              <input
                type="text"
                class="form-control"
                v-model="carToAdd.name"
                required
              />
              <label for="floatingInput">Название автомобиля</label>
            </div>
          </div>
          
          <div class="col-auto">
              <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
            <div class="form-floating">
              <select class="form-select" v-model="carToAdd.brand" required>
                <option :value="b.id" v-for="b in brands" :key="b.id">{{ b.name }}</option>
              </select>
              <label for="floatingInput">Бренд</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="carToAdd.year"
                placeholder="Год выпуска"
              />
              <label>Год выпуска</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="carToAdd.color"
                placeholder="Цвет"
              />
              <label>Цвет</label>
            </div>
          </div>
          <div class="col-auto">
            <input
              type="file"
              class="form-control"
              ref="carsPictureRef"
              @change="carsAddPictureChange"
            />
          </div>
          <div class="col-auto">
            <img :src="carAddImageUrl" style="max-height:60px;" alt="">
          </div>
          
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>

      <div class="container-fluid">
        <div class="row pt-4">
          <div class="col"><strong>Автомобиль</strong></div>
          <div class="col"><strong>Фото автомобиля</strong></div>
        </div>

        <div class="pt-2">
          <div v-for="item in cars" :key="item.id" class="car-item">
            <!-- Информация об автомобиле -->
            <div class="car-info">
              <div>{{ item.brand.name }} {{ item.name }} {{ item.year }}, {{ item.color }}</div>
            </div>

            <!-- Фото автомобиля -->
            <div class="car-photo">
              <img 
                v-if="item.picture" 
                :src="item.picture" 
                class="car-image"
                style="max-width: 60px; max-height: 60px; cursor: pointer;"
                @click="currentImage = item.picture" 
                data-bs-toggle="modal"
                data-bs-target="#imageModal" 
                alt="Изображение автомобиля"
              />
              <span v-else>Нет фото</span>
            </div>

            <!-- Действия -->
            <div class="car-actions">
              <button class="btn btn-secondary" @click="onCarEditClick(item)" :data-bs-toggle="otpVerified ? 'modal' : null"  data-bs-target="#editCarModal">
                <i class="bi bi-pencil-fill"></i>
              </button>
              <button class="btn btn-danger" @click="onRemoveClick(item)">
                <i class="bi bi-x"></i>
              </button>
            </div>
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

      <!-- Модальное окно редактирования автомобиля -->
      <div class="modal fade" id="editCarModal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Редактировать автомобиль</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="carToEdit.name"
                    placeholder="Название автомобиля"
                  />
                  <label>Название автомобиля</label>
                </div>
              </div>
              <div class="form-floating">
                <select class="form-select" v-model="carToEdit.brand">
                  <option :value="b.id" v-for="b in brands" :key="b.id">{{ b.name }}</option>
                </select>
                <label for="floatingInput">Бренд</label>
              </div>

              
              <div class="col">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    v-model="carToEdit.year"
                    placeholder="Год выпуска"
                  />
                  <label>Год выпуска</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="carToEdit.color"
                    placeholder="Цвет"
                  />
                  <label>Цвет</label>
                </div>
              </div>

              <div class="mt-3">
                <label>Текущая фотография:</label>
                <img v-if="carToEdit.picture" :src="carToEdit.picture" style="max-height: 60px;" alt="Текущая фотография" />
              </div>
              <div class="mt-3">
                <label>Загрузить новое изображение:</label>
                <input class="form-control" type="file" ref="carsPictureUpdateRef" />
              </div>
          </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-primary" @click="onUpdateCar" data-bs-dismiss="modal">Сохранить</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.car-item {
  display: grid;
  grid-template-columns: 1fr 3fr auto;
  align-items: center;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 4px;
}


.car-info {
  text-align: left;
}

.car-photo {
  text-align: center;
}

.car-actions {
  display: flex;
  gap: 0.2rem;
  text-align: right;
}

.form-control{
  margin-top: 0.5rem;
}

.form-select{
  margin-top: 0.5rem;
}

/* Добавь стили по необходимости */
</style>
