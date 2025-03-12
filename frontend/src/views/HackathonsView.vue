<template>
  <div class="hackathons-page">
    <div class="header">
      <h1>Хакатоны</h1>
      <div class="filters">
        <input type="text" v-model="searchQuery" placeholder="Поиск хакатонов..." class="search-input">
        <select v-model="sortBy" class="sort-select">
          <option value="date">По дате</option>
          <option value="name">По названию</option>
        </select>
      </div>
    </div>

    <div class="hackathons-grid">
      <div v-for="hackathon in filteredHackathons" :key="hackathon.id" class="hackathon-card">
        <div class="hackathon-image">
          <img :src="hackathon.image_url || '/default-hackathon.jpg'" :alt="hackathon.name">
          <div class="date-badge">
            {{ formatDate(hackathon.start_date) }}
          </div>
        </div>
        <div class="hackathon-content">
          <h3>{{ hackathon.name }}</h3>
          <p class="description">{{ hackathon.description }}</p>
          <div class="hackathon-details">
            <div class="detail">
              <span class="label">Дедлайн регистрации:</span>
              <span class="value">{{ formatDate(hackathon.registration_deadline) }}</span>
            </div>
            <div class="detail">
              <span class="label">Период проведения:</span>
              <span class="value">{{ formatDate(hackathon.start_date) }} - {{ formatDate(hackathon.end_date) }}</span>
            </div>
          </div>
          <button class="register-button">Зарегистрироваться</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const hackathons = ref([])
    const searchQuery = ref('')
    const sortBy = ref('date')
    const loading = ref(false)
    const error = ref(null)

    const API_URL = import.meta.env.VITE_API_URL

    const fetchHackathons = async () => {
      loading.value = true
      try {
        const response = await axios.get(`${API_URL}/api/hackathons/`)
        hackathons.value = response.data
      } catch (err) {
        error.value = 'Ошибка при загрузке хакатонов'
        console.error(err)
      } finally {
        loading.value = false
      }
    }

    const filteredHackathons = computed(() => {
      let result = [...hackathons.value]
      
      
      if (searchQuery.value) {
        result = result.filter(h => 
          h.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          h.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
      }

      if (sortBy.value === 'date') {
        result.sort((a, b) => new Date(a.start_date) - new Date(b.start_date))
      } else if (sortBy.value === 'name') {
        result.sort((a, b) => a.name.localeCompare(b.name))
      }

      return result
    })

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU')
    }

    onMounted(fetchHackathons)

    return {
      hackathons,
      searchQuery,
      sortBy,
      loading,
      error,
      filteredHackathons,
      formatDate
    }
  }
}
</script>

<style scoped>
.hackathons-page {
  padding: 20px;
}

.header {
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5em;
  margin-bottom: 20px;
  color: #2c3e50;
}

.filters {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.search-input, .sort-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

.search-input {
  flex: 1;
}

.hackathons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.hackathon-card {
  border: 1px solid #eee;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.hackathon-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.hackathon-image {
  position: relative;
  height: 200px;
}

.hackathon-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.date-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
}

.hackathon-content {
  padding: 20px;
}

.hackathon-content h3 {
  margin: 0 0 10px 0;
  font-size: 1.4em;
  color: #2c3e50;
}

.description {
  color: #666;
  margin-bottom: 15px;
  display: -webkit-box;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.hackathon-details {
  margin-bottom: 15px;
}

.detail {
  margin-bottom: 5px;
}

.label {
  color: #666;
  font-size: 0.9em;
}

.value {
  margin-left: 5px;
  color: #2c3e50;
  font-weight: 500;
}

.register-button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-button:hover {
  background-color: #3aa876;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .hackathons-grid {
    grid-template-columns: 1fr;
  }
}
</style>