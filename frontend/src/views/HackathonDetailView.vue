<template>
  <div class="hackathon-detail">
    <div v-if="loading" class="loading">
      Загрузка информации о хакатоне...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
      <button @click="fetchHackathon" class="retry-button">Попробовать снова</button>
    </div>

    <div v-else-if="hackathon" class="hackathon-content">
      <div class="header">
        <button @click="router.back()" class="back-button">
          ← Назад
        </button>
        <h1>{{ hackathon.name }}</h1>
      </div>

      <div class="main-info">
        <div class="image-container">
          <img 
            :src="hackathon.image || 'https://via.placeholder.com/800x400?text=Hackathon'" 
            :alt="hackathon.name"
            @error="handleImageError"
          >
        </div>

        <div class="info-panel">
          <div class="status-card">
            <div class="status-item">
              <span class="label">Статус регистрации:</span>
              <span :class="['value', { 'closed': !hackathon.can_register }]">
                {{ hackathon.can_register ? 'Открыта' : 'Закрыта' }}
              </span>
            </div>
            <div class="status-item">
              <span class="label">Участники:</span>
              <span class="value">{{ hackathon.participants_count }}/{{ hackathon.max_participants }}</span>
            </div>
            <div class="status-item">
              <span class="label">Дедлайн регистрации:</span>
              <span class="value">{{ formatDate(hackathon.registration_deadline) }}</span>
            </div>
            <div class="status-item">
              <span class="label">Период проведения:</span>
              <span class="value">{{ formatDate(hackathon.start_date) }} - {{ formatDate(hackathon.end_date) }}</span>
            </div>
            <div class="status-item">
              <span class="label">Призовой фонд:</span>
              <span class="value">{{ hackathon.prize_pool }}</span>
            </div>
            <div class="status-item">
              <span class="label">Формат:</span>
              <span class="value">{{ hackathon.is_online ? 'Онлайн' : 'Офлайн' }}</span>
            </div>
            <div v-if="!hackathon.is_online" class="status-item">
              <span class="label">Место проведения:</span>
              <span class="value">{{ hackathon.location }}</span>
            </div>
          </div>

          <button 
            @click="handleRegistration" 
            :class="['register-button', { 'registered': hackathon.is_registered }]"
            :disabled="!hackathon.can_register && !hackathon.is_registered"
          >
            {{ getButtonText() }}
          </button>
        </div>
      </div>

      <div class="description-section">
        <h2>Описание</h2>
        <div class="description" v-html="formatDescription(hackathon.full_description)"></div>
      </div>

      <div class="requirements-section">
        <h2>Требования к участникам</h2>
        <div class="requirements" v-html="formatDescription(hackathon.requirements)"></div>
      </div>

      <div class="tags-section" v-if="hackathon.tags && hackathon.tags.length">
        <h2>Теги</h2>
        <div class="tags">
          <span v-for="tag in hackathon.tags" :key="tag.id" class="tag">
            {{ tag.name }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { hackathonService } from '@/services/hackathonService'
import { useAuth } from '@/composables/useAuth'

export default {
  setup() {
    const route = useRoute()
    const router = useRouter()
    const { isAuthenticated } = useAuth()
    
    const hackathon = ref(null)
    const loading = ref(true)
    const error = ref(null)

    const fetchHackathon = async () => {
      loading.value = true
      error.value = null
      try {
        const data = await hackathonService.getHackathon(route.params.id)
        hackathon.value = data
      } catch (err) {
        error.value = 'Ошибка при загрузке информации о хакатоне'
        console.error('Ошибка при загрузке хакатона:', err)
      } finally {
        loading.value = false
      }
    }

    const handleRegistration = async () => {
      if (!isAuthenticated.value) {
        error.value = 'Необходимо авторизоваться для регистрации'
        return
      }

      try {
        if (hackathon.value.is_registered) {
          await hackathonService.unregisterFromHackathon(hackathon.value.id)
          hackathon.value.is_registered = false
          hackathon.value.participants_count--
        } else {
          await hackathonService.registerForHackathon(hackathon.value.id)
          hackathon.value.is_registered = true
          hackathon.value.participants_count++
        }
      } catch (err) {
        error.value = err.response?.data?.error || 'Ошибка при регистрации'
        console.error('Ошибка при регистрации:', err)
      }
    }

    const getButtonText = () => {
      if (!hackathon.value) return ''
      if (hackathon.value.is_registered) {
        return 'Отменить регистрацию'
      }
      if (!hackathon.value.can_register) {
        return 'Регистрация закрыта'
      }
      return 'Зарегистрироваться'
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const formatDescription = (text) => {
      if (!text) return ''
      return text.replace(/\n/g, '<br>')
    }

    const handleImageError = (event) => {
      event.target.src = 'https://via.placeholder.com/800x400?text=Hackathon'
    }

    onMounted(fetchHackathon)

    return {
      hackathon,
      loading,
      error,
      router,
      handleRegistration,
      getButtonText,
      formatDate,
      formatDescription,
      handleImageError
    }
  }
}
</script>

<style scoped>
.hackathon-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 1.2em;
  color: #666;
}

.error {
  color: #dc3545;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
}

.back-button {
  padding: 10px 20px;
  background: none;
  border: 1px solid #2c3e50;
  border-radius: 8px;
  color: #2c3e50;
  cursor: pointer;
  transition: all 0.2s;
}

.back-button:hover {
  background: #2c3e50;
  color: white;
}

h1 {
  margin: 0;
  font-size: 2.5em;
  color: #2c3e50;
}

.main-info {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}

.image-container {
  border-radius: 12px;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.info-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.status-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.status-item {
  margin-bottom: 15px;
}

.status-item:last-child {
  margin-bottom: 0;
}

.label {
  display: block;
  color: #666;
  font-size: 0.9em;
  margin-bottom: 5px;
}

.value {
  font-weight: 500;
  color: #2c3e50;
}

.value.closed {
  color: #dc3545;
}

.register-button {
  padding: 15px;
  border: none;
  border-radius: 8px;
  background-color: #42b983;
  color: white;
  font-size: 1.1em;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-button:hover:not(:disabled) {
  background-color: #3aa876;
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

.description-section,
.requirements-section,
.tags-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h2 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.8em;
}

.description,
.requirements {
  line-height: 1.6;
  color: #2c3e50;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  padding: 5px 15px;
  background-color: #e9ecef;
  border-radius: 20px;
  color: #2c3e50;
  font-size: 0.9em;
}

@media (max-width: 768px) {
  .main-info {
    grid-template-columns: 1fr;
  }

  .image-container img {
    height: 300px;
  }
}
</style> 