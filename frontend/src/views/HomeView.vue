<script setup>
import Navbar from '../components/Navbar.vue'
import { ref, onMounted } from 'vue'
import { useMiniApp } from 'vue-tg'
import { RouterLink } from 'vue-router'
import axiosInstance from '../services/axiosConfig'

const loading = ref({
  hackathons: false
})
const error = ref({
  hackathons: null
})
const hackathons = ref([])

const refreshHackathons = async () => {
  loading.value.hackathons = true
  error.value.hackathons = null
  
  try {
    const response = await axiosInstance.get('/hackathons/')
    hackathons.value = response.data
  } catch (err) {
    console.error('Error fetching hackathons:', err)
    error.value.hackathons = 'Ошибка при загрузке хакатонов'
  } finally {
    loading.value.hackathons = false
  }
}

const registerForHackathon = async (hackathonId) => {
  try {
    await axiosInstance.post(`/hackathons/${hackathonId}/register/`)
    await refreshHackathons()
  } catch (err) {
    console.error('Error registering for hackathon:', err)
  }
}

const unregisterFromHackathon = async (hackathonId) => {
  try {
    await axiosInstance.post(`/hackathons/${hackathonId}/unregister/`)
    await refreshHackathons()
  } catch (err) {
    console.error('Error unregistering from hackathon:', err)
  }
}

const getRegistrationStatus = (hackathon) => {
  if (hackathon.is_finished) return 'Хакатон завершен'
  if (hackathon.participants_count >= hackathon.max_participants) return 'Нет мест'
  if (!hackathon.registration_open) return 'Регистрация закрыта'
  return 'Регистрация открыта'
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  refreshHackathons()
})
</script>

<template>
  <div class="home">
    <section class="hero-section">
      <div class="hero-content">
        <h1>Добро пожаловать в мир хакатонов</h1>
        <p>Участвуйте в соревнованиях, развивайте навыки и побеждайте вместе с нами</p>
        <RouterLink to="/hackathons" class="cta-button">Найти хакатон</RouterLink>
      </div>
    </section>

    <section class="upcoming-section">
      <div class="section-header">
        <h2>Ближайшие хакатоны</h2>
        <RouterLink to="/hackathons" class="see-all">Смотреть все</RouterLink>
      </div>
      <div v-if="loading.hackathons" class="loading-state">
        Загрузка хакатонов...
      </div>
      <div v-else-if="error.hackathons" class="error-state">
        {{ error.hackathons }}
        <button @click="refreshHackathons" class="retry-button">Повторить</button>
      </div>
      <div v-else-if="hackathons.length === 0" class="no-data">
        Нет доступных хакатонов
      </div>
      <div v-else class="hackathons-grid">
        <div v-for="hackathon in hackathons" :key="hackathon?.id || index" class="hackathon-card">
          <!-- <div class="hackathon-image">
            <img :src="hackathon.image || '/default-hackathon.jpg'" :alt="hackathon.name">
            <span class="hackathon-date">{{ formatDate(hackathon.start_date) }}</span>
          </div> -->
          <div class="hackathon-content">
            <h3>{{ hackathon.name }}</h3>
            <p>{{ hackathon.short_description }}</p>
            <div class="hackathon-info">
              <div class="info-item">
                <i class="fas fa-users"></i>
                <span>{{ hackathon.participants_count || 0 }}/{{ hackathon.max_participants }}</span>
              </div>
              <div class="info-item">
                <i class="fas fa-map-marker-alt"></i>
                <span>{{ hackathon.is_online ? 'Онлайн' : (hackathon.location || 'Не указано') }}</span>
              </div>
            </div>
            <div class="hackathon-footer">
              <div class="tags">
                <span v-for="tag in (hackathon.tags || [])" :key="tag.id" class="tag">{{ tag.name }}</span>
              </div>
              <button 
                v-if="hackathon.is_registered" 
                @click="unregisterFromHackathon(hackathon.id)"
                class="unregister-button"
              >
                Отменить участие
              </button>
              <button 
                v-else-if="hackathon.can_register" 
                @click="registerForHackathon(hackathon.id)"
                class="join-button"
              >
                Участвовать
              </button>
              <span v-else class="registration-closed">
                {{ getRegistrationStatus(hackathon) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>

  <div>
    <button @click="requestPhoneNumber">Предоставить номер телефона</button>
  </div>



</template>

<script>

</script>

<style scoped>
.home {
  padding-bottom: 80px;
}

.hero-section {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
  margin-bottom: 40px;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 20px;
}

.hero-content p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 30px;
}

.cta-button {
  display: inline-block;
  background: white;
  color: #6366f1;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 20px;
}

.section-header h2 {
  font-size: 1.5rem;
  color: #1f2937;
}

.see-all {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
}

.hackathons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 0 20px;
}

.hackathon-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.hackathon-card:hover {
  transform: translateY(-2px);
}

.hackathon-image {
  position: relative;
  height: 160px;
}

.hackathon-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hackathon-date {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.hackathon-content {
  padding: 20px;
}

.hackathon-content h3 {
  margin: 0 0 10px;
  font-size: 1.2rem;
  color: #1f2937;
}

.hackathon-content p {
  color: #6b7280;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.hackathon-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tags {
  display: flex;
  gap: 8px;
}

.tag {
  background: #f3f4f6;
  color: #4b5563;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.join-button {
  background: #6366f1;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.join-button:hover {
  background: #4f46e5;
}

.user-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.user-rank {
  font-size: 1.2rem;
  font-weight: 700;
  color: #6366f1;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-info h3 {
  margin: 0;
  font-size: 1rem;
  color: #1f2937;
}

.user-info p {
  margin: 4px 0 0;
  font-size: 0.9rem;
  color: #6b7280;
}

.user-achievements {
  display: flex;
  gap: 4px;
}

.user-achievements img {
  width: 24px;
  height: 24px;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  padding: 0 20px;
}

.shop-item {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.item-image {
  height: 160px;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-content {
  padding: 15px;
  text-align: center;
}

.item-content h3 {
  margin: 0 0 8px;
  font-size: 1rem;
  color: #1f2937;
}

.item-price {
  color: #6366f1;
  font-weight: 600;
  margin-bottom: 12px;
}

.buy-button {
  background: #6366f1;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  width: 100%;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.buy-button:hover {
  background: #4f46e5;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 0 20px;
}

.news-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.news-card:hover {
  transform: translateY(-2px);
}

.news-image {
  position: relative;
  height: 160px;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-date {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.news-content {
  padding: 20px;
}

.news-content h3 {
  margin: 0 0 10px;
  font-size: 1.2rem;
  color: #1f2937;
}

.news-content p {
  color: #6b7280;
  margin-bottom: 15px;
  font-size: 0.9rem;
  line-height: 1.5;
}

.read-more {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
}

.webinars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 0 20px;
}

.webinar-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.webinar-card:hover {
  transform: translateY(-2px);
}

.webinar-image {
  position: relative;
  height: 160px;
}

.webinar-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.webinar-date {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.webinar-content {
  padding: 20px;
}

.webinar-content h3 {
  margin: 0 0 10px;
  font-size: 1.2rem;
  color: #1f2937;
}

.webinar-content p {
  color: #6b7280;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.webinar-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.webinar-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.speaker {
  font-weight: 500;
  color: #4b5563;
  font-size: 0.9rem;
}

.duration {
  color: #6b7280;
  font-size: 0.8rem;
}

.register-button {
  background: #6366f1;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.register-button:hover {
  background: #4f46e5;
}

.case-cups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 0 20px;
}

.case-cup-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.case-cup-card:hover {
  transform: translateY(-2px);
}

.case-cup-image {
  position: relative;
  height: 160px;
}

.case-cup-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.case-cup-date {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.case-cup-content {
  padding: 20px;
}

.case-cup-content h3 {
  margin: 0 0 10px;
  font-size: 1.2rem;
  color: #1f2937;
}

.case-cup-content p {
  color: #6b7280;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.case-cup-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.participate-button {
  background: #6366f1;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.participate-button:hover {
  background: #4f46e5;
}

.loading-state {
  text-align: center;
  padding: 20px;
  color: #6b7280;
}

.error-state {
  text-align: center;
  padding: 20px;
  color: #ef4444;
}

.retry-button {
  background: #6366f1;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  margin-top: 10px;
  cursor: pointer;
}

.hackathon-info {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #6b7280;
  font-size: 0.9rem;
}

.unregister-button {
  background: #ef4444;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.unregister-button:hover {
  background: #dc2626;
}

.registration-closed {
  color: #6b7280;
  font-size: 0.9rem;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #6b7280;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 20px;
  }

  .hero-content h1 {
    font-size: 2rem;
  }

  .hero-content p {
    font-size: 1rem;
  }

  .hackathons-grid,
  .leaderboard-grid,
  .items-grid,
  .news-grid,
  .webinars-grid,
  .case-cups-grid {
    grid-template-columns: 1fr;
  }
}
</style>
