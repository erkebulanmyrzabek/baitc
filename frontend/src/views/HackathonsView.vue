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

    <div v-if="loading" class="loading">
      Загрузка хакатонов...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
      <button @click="fetchHackathons" class="retry-button">Попробовать снова</button>
    </div>

    <div v-else class="hackathons-grid">
      <div v-for="hackathon in filteredHackathons" :key="hackathon.id" class="hackathon-card">
        <div class="hackathon-image">
          <img 
            :src="hackathon.image"
            :alt="hackathon.name"
            @error="handleImageError"
          >
          <div class="date-badge">
            {{ formatDate(hackathon.start_date) }}
          </div>
        </div>
        <div class="hackathon-content">
          <h3>{{ hackathon.name }}</h3>
          <p class="description">{{ hackathon.short_description }}</p>
          <div class="hackathon-details">
            <div class="detail">
              <span class="label">Дедлайн регистрации:</span>
              <span class="value">{{ formatDate(hackathon.registration_deadline) }}</span>
            </div>
            <div class="detail">
              <span class="label">Период проведения:</span>
              <span class="value">{{ formatDate(hackathon.start_date) }} - {{ formatDate(hackathon.end_date) }}</span>
            </div>
            <div class="detail">
              <span class="label">Участники:</span>
              <span class="value">{{ hackathon.participants_count }}/{{ hackathon.max_participants }}</span>
            </div>
          </div>
          <div class="button-group">
            <button 
              @click="handleRegistration(hackathon)" 
              :class="['register-button', { 'registered': hackathon.is_registered }]"
              :disabled="!hackathon.can_register && !hackathon.is_registered"
            >
              {{ getButtonText(hackathon) }}
            </button>
            <button 
              @click="router.push(`/hackathons/${hackathon.id}`)" 
              class="details-button"
            >
              Подробнее
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { hackathonService } from '@/services/hackathonService'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const hackathons = ref([])
    const searchQuery = ref('')
    const sortBy = ref('date')
    const loading = ref(false)
    const error = ref(null)
    const { isAuthenticated } = useAuth()
    const router = useRouter()

    const fetchHackathons = async () => {
      loading.value = true
      error.value = null
      try {
        const data = await hackathonService.getAllHackathons()
        hackathons.value = data.results || data // Поддержка пагинации
      } catch (err) {
        error.value = 'Ошибка при загрузке хакатонов'
        console.error('Ошибка при загрузке хакатонов:', err)
      } finally {
        loading.value = false
      }
    }

    const handleRegistration = async (hackathon) => {
      if (!isAuthenticated.value) {
        error.value = 'Необходимо авторизоваться для регистрации'
        return
      }

      try {
        if (hackathon.is_registered) {
          await hackathonService.unregisterFromHackathon(hackathon.id)
          hackathon.is_registered = false
          hackathon.participants_count--
        } else {
          await hackathonService.registerForHackathon(hackathon.id)
          hackathon.is_registered = true
          hackathon.participants_count++
        }
      } catch (err) {
        error.value = err.response?.data?.error || 'Ошибка при регистрации'
        console.error('Ошибка при регистрации:', err)
      }
    }

    const getButtonText = (hackathon) => {
      if (hackathon.is_registered) {
        return 'Отменить регистрацию'
      }
      if (!hackathon.can_register) {
        return 'Регистрация закрыта'
      }
      return 'Зарегистрироваться'
    }

    const filteredHackathons = computed(() => {
      let result = [...hackathons.value]
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        result = result.filter(h => 
          h.name.toLowerCase().includes(query) ||
          h.short_description.toLowerCase().includes(query)
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
      return new Date(dateString).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const handleImageError = (event) => {
      // Если изображение не загрузилось, заменяем его на изображение по умолчанию
      // TODO: Добавить изображение по умолчанию
    }

    onMounted(fetchHackathons)

    return {
      hackathons,
      searchQuery,
      sortBy,
      loading,
      error,
      filteredHackathons,
      formatDate,
      handleRegistration,
      getButtonText,
      handleImageError,
      router
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

.loading, .error {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
  color: #666;
}

.error {
  color: #dc3545;
}

.retry-button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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
  background: white;
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

.button-group {
  display: flex;
  gap: 10px;
}

.register-button, .details-button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.details-button {
  background-color: #2c3e50;
  color: white;
}

.details-button:hover {
  background-color: #34495e;
}

.register-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.register-button.registered {
  background-color: #dc3545;
}

.register-button.registered:hover {
  background-color: #c82333;
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