<template>
  <div class="service-map-container p-3 mb-3 border rounded">
    <h5 class="text-primary mb-3">Карта автосервисов</h5>
    <div class="map-wrapper">
      <div id="map" style="height: 400px;"></div>
    </div>
    <div class="service-list mt-3">
      <div v-for="service in services" :key="service.id" 
           class="service-item p-2" 
           :class="{ 'active': selectedService?.id === service.id }"
           @click="centerMapOn(service)">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ service.name }}</strong>
            <div class="text-muted">{{ service.location }}</div>
          </div>
          <button class="btn btn-sm btn-outline-primary" @click.stop="showRoute(service)">
            <i class="bi bi-map"></i> Маршрут
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const services = ref([]);
const map = ref(null);
const markers = ref([]);
const selectedService = ref(null);

// Функция для геокодирования адреса
const geocodeAddress = async (address) => {
  try {
    const response = await axios.get('/api/geocode/', {
      params: { address }
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка геокодирования:', error);
  }
  return null;
};

const initMap = () => {
  map.value = L.map('map').setView([55.7558, 37.6173], 10); // Москва по умолчанию
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map.value);
};

const centerMapOn = async (service) => {
  selectedService.value = service;
  const coords = await geocodeAddress(service.location);
  if (coords) {
    map.value.setView([coords.lat, coords.lon], 15);
    markers.value.forEach(marker => {
      if (marker.serviceId === service.id) {
        marker.openPopup();
      }
    });
  }
};

const showRoute = async (service) => {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const serviceCoords = await geocodeAddress(service.location);
      if (serviceCoords) {
        const url = `https://www.google.com/maps/dir/${position.coords.latitude},${position.coords.longitude}/${serviceCoords.lat},${serviceCoords.lon}`;
        window.open(url, '_blank');
      }
    });
  }
};

const loadServices = async () => {
  try {
    const response = await axios.get('/api/services/');
    services.value = response.data;
    
    // Добавляем маркеры для каждого сервиса
    for (const service of services.value) {
      const coords = await geocodeAddress(service.location);
      if (coords) {
        const marker = L.marker([coords.lat, coords.lon])
          .bindPopup(`
            <strong>${service.name}</strong><br>
            ${service.location}
          `)
          .addTo(map.value);
        marker.serviceId = service.id;
        markers.value.push(marker);
      }
    }
  } catch (error) {
    console.error('Ошибка загрузки сервисов:', error);
  }
};

onMounted(() => {
  initMap();
  loadServices();
});
</script>

<style scoped>
.service-map-container {
  background-color: #ffffff;
}

.map-wrapper {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.service-list {
  max-height: 200px;
  overflow-y: auto;
}

.service-item {
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.service-item:hover {
  background-color: #f8f9fa;
}

.service-item.active {
  background-color: #e9ecef;
}

/* Исправление иконок Leaflet */
:global(.leaflet-default-icon-path) {
  background-image: url("https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png");
}
</style> 