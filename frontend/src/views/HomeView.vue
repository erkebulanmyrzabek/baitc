<script setup>
import Navbar from '../components/Navbar.vue'
import { ref, onMounted } from 'vue'
import { useMiniApp } from 'vue-tg'
import { RouterLink } from 'vue-router'

const MiniApp = useMiniApp()
const username = ref('')
const news = ref([])
const hackathons = ref([])
const webinars = ref([])
const caseCups = ref([])
const loading = ref({
    hackathons: false,
    news: false,
    webinars: false,
    caseCups: false
})
const error = ref({
    hackathons: null,
    news: null,
    webinars: null,
    caseCups: null
})

// Константы для кэширования
const CACHE_DURATION = 15 * 60 * 1000 // 15 минут в миллисекундах
const CACHE_KEYS = {
    hackathons: 'cached_hackathons',
    hackathonsTimestamp: 'cached_hackathons_timestamp',
    news: 'cached_news',
    newsTimestamp: 'cached_news_timestamp',
    webinars: 'cached_webinars',
    webinarsTimestamp: 'cached_webinars_timestamp',
    caseCups: 'cached_casecups',
    caseCupsTimestamp: 'cached_casecups_timestamp'
}

const API_URL = import.meta.env.VITE_API_URL 

onMounted(async () => {
    if (MiniApp.initDataUnsafe?.user?.username) {
        username.value = MiniApp.initDataUnsafe.user.username
    }

    await Promise.all([
        fetchHackathons(),
        fetchNews(),
        fetchWebinars(),
        fetchCaseCups()
    ])
})

// Общая функция для проверки кэша
const isCacheValid = (timestampKey) => {
    const timestamp = localStorage.getItem(timestampKey)
    if (!timestamp) return false
    return Date.now() - parseInt(timestamp) < CACHE_DURATION
}

// Общая функция для получения данных с API
const fetchData = async (endpoint, cacheKey, timestampKey, loadingKey, errorKey, ref) => {
    if (isCacheValid(timestampKey)) {
        const cachedData = localStorage.getItem(cacheKey)
        if (cachedData) {
            try {
                ref.value = JSON.parse(cachedData)
                return
            } catch (e) {
                console.error(`Ошибка при чтении кэша для ${endpoint}:`, e)
            }
        }
    }

    loading.value[loadingKey] = true
    error.value[errorKey] = null

    try {
        const apiUrl = `${API_URL}/api/${endpoint}`
        console.log(`Fetching from: ${apiUrl}`)
        
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        })
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        ref.value = data

        // Сохраняем в кэш
        localStorage.setItem(cacheKey, JSON.stringify(data))
        localStorage.setItem(timestampKey, Date.now().toString())
    } catch (e) {
        console.error(`Ошибка при получении ${endpoint}:`, e)
        error.value[errorKey] = `Не удалось загрузить данные: ${e.message}`
    } finally {
        loading.value[loadingKey] = false
    }
}

const fetchHackathons = () => fetchData(
    'hackathons/', 
    CACHE_KEYS.hackathons,
    CACHE_KEYS.hackathonsTimestamp,
    'hackathons',
    'hackathons',
    hackathons
)

const fetchNews = () => fetchData(
    'news/',
    CACHE_KEYS.news,
    CACHE_KEYS.newsTimestamp,
    'news',
    'news',
    news
)

const fetchWebinars = () => fetchData(
    'webinars/',
    CACHE_KEYS.webinars,
    CACHE_KEYS.webinarsTimestamp,
    'webinars',
    'webinars',
    webinars
)

const fetchCaseCups = () => fetchData(
    'case-cups/',
    CACHE_KEYS.caseCups,
    CACHE_KEYS.caseCupsTimestamp,
    'caseCups',
    'caseCups',
    caseCups
)

// Функции обновления данных
const refreshData = async (fetchFunction, cacheKey, timestampKey) => {
    localStorage.removeItem(cacheKey)
    localStorage.removeItem(timestampKey)
    await fetchFunction()
}

const refreshHackathons = () => refreshData(
    fetchHackathons,
    CACHE_KEYS.hackathons,
    CACHE_KEYS.hackathonsTimestamp
)

const refreshNews = () => refreshData(
    fetchNews,
    CACHE_KEYS.news,
    CACHE_KEYS.newsTimestamp
)

const refreshWebinars = () => refreshData(
    fetchWebinars,
    CACHE_KEYS.webinars,
    CACHE_KEYS.webinarsTimestamp
)

const refreshCaseCups = () => refreshData(
    fetchCaseCups,
    CACHE_KEYS.caseCups,
    CACHE_KEYS.caseCupsTimestamp
)

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
      <div class="hackathons-grid">
        <div v-for="hackathon in hackathons" :key="hackathon.id" class="hackathon-card">
          <div class="hackathon-image">
            <img :src="hackathon.image" :alt="hackathon.name">
            <span class="hackathon-date">{{ hackathon.start_date }}</span>
          </div>
          <div class="hackathon-content">
            <h3>{{ hackathon.name }}</h3>
            <p>{{ hackathon.description }}</p>
            <div class="hackathon-footer">
              <div class="tags">
                <span v-for="tag in hackathon.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <button class="join-button">Участвовать</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="news-section">
      <div class="section-header">
        <h2>Последние новости</h2>
        <RouterLink to="/news" class="see-all">Смотреть все</RouterLink>
      </div>
      <div class="news-grid">
        <div v-for="item in news" :key="item.id" class="news-card">
          <div class="news-image">
            <img :src="item.image" :alt="item.title">
            <span class="news-date">{{ item.date }}</span>
          </div>
          <div class="news-content">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
            <RouterLink :to="'/news/' + item.id" class="read-more">Читать далее</RouterLink>
          </div>
        </div>
      </div>
    </section>

    <section class="webinars-section">
      <div class="section-header">
        <h2>Предстоящие вебинары</h2>
        <RouterLink to="/webinars" class="see-all">Смотреть все</RouterLink>
      </div>
      <div class="webinars-grid">
        <div v-for="webinar in webinars" :key="webinar.id" class="webinar-card">
          <div class="webinar-image">
            <img :src="webinar.image" :alt="webinar.title">
            <span class="webinar-date">{{ webinar.date }}</span>
          </div>
          <div class="webinar-content">
            <h3>{{ webinar.title }}</h3>
            <p>{{ webinar.description }}</p>
            <div class="webinar-footer">
              <div class="webinar-info">
                <span class="speaker">{{ webinar.speaker }}</span>
                <span class="duration">{{ webinar.duration }}</span>
              </div>
              <button class="register-button">Зарегистрироваться</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="case-cups-section">
      <div class="section-header">
        <h2>Кейс-чемпионаты</h2>
        <RouterLink to="/case-cups" class="see-all">Смотреть все</RouterLink>
      </div>
      <div class="case-cups-grid">
        <div v-for="caseCup in caseCups" :key="caseCup.id" class="case-cup-card">
          <div class="case-cup-image">
            <img :src="caseCup.image" :alt="caseCup.title">
            <span class="case-cup-date">{{ caseCup.date }}</span>
          </div>
          <div class="case-cup-content">
            <h3>{{ caseCup.title }}</h3>
            <p>{{ caseCup.description }}</p>
            <div class="case-cup-footer">
              <div class="tags">
                <span v-for="tag in caseCup.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <button class="participate-button">Участвовать</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

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
