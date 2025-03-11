<script setup>
import Navbar from '../components/Navbar.vue'
import { ref, onMounted } from 'vue'
import { useMiniApp } from 'vue-tg'

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
    hackathonsTimestamp: 'cached_hackathons_timestamp'
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

onMounted(async () => {
    // Получаем данные пользователя из Telegram Mini App
    if (MiniApp.initDataUnsafe?.user?.username) {
        username.value = MiniApp.initDataUnsafe.user.username
    }

    await fetchHackathons()
})

const isCacheValid = (timestampKey) => {
    const timestamp = localStorage.getItem(timestampKey)
    if (!timestamp) return false
    return Date.now() - parseInt(timestamp) < CACHE_DURATION
}

const fetchHackathons = async () => {
    // Проверяем кэш
    if (isCacheValid(CACHE_KEYS.hackathonsTimestamp)) {
        const cachedData = localStorage.getItem(CACHE_KEYS.hackathons)
        if (cachedData) {
            try {
                hackathons.value = JSON.parse(cachedData)
                return
            } catch (e) {
                console.error('Ошибка при чтении кэша:', e)
                // Если ошибка при чтении кэша, продолжаем загрузку с сервера
            }
        }
    }

    loading.value.hackathons = true
    error.value.hackathons = null

    try {
        console.log('Fetching from:', `${API_URL}/api/hackathons/`)
        const response = await fetch(`${API_URL}/api/hackathons/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        })
        
        if (!response.ok) {
            const errorText = await response.text()
            console.error('API Error Response:', errorText)
            throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const contentType = response.headers.get('content-type')
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Received non-JSON response from server')
        }

        const data = await response.json()
        console.log('Received data:', data)
        
        // Проверяем, является ли data массивом
        if (!Array.isArray(data)) {
            throw new Error('API должен возвращать массив хакатонов')
        }

        // Сохраняем массив хакатонов
        hackathons.value = data

        // Сохраняем в кэш
        localStorage.setItem(CACHE_KEYS.hackathons, JSON.stringify(data))
        localStorage.setItem(CACHE_KEYS.hackathonsTimestamp, Date.now().toString())
    } catch (e) {
        console.error('Ошибка при получении хакатонов:', e)
        error.value.hackathons = `Не удалось загрузить список хакатонов: ${e.message}`
    } finally {
        loading.value.hackathons = false
    }
}

// Функция для обновления данных
const refreshHackathons = async () => {
    // Очищаем кэш
    localStorage.removeItem(CACHE_KEYS.hackathons)
    localStorage.removeItem(CACHE_KEYS.hackathonsTimestamp)
    await fetchHackathons()
}

// Заглушки для будущих API функций
const fetchNews = async () => {
    try {
        // const response = await fetch('API_URL/news')
        // news.value = await response.json()
    } catch (error) {
        console.error('Error fetching news:', error)
    }
}
</script>

<template>
    <main>
        <div class="home-view">
            <div class="user-info">
                <h2 class="username">@{{ username }}</h2>
            </div>
            
            <div class="content-section">
                <div class="section news">
                    <h2>Последние новости</h2>
                    <div class="cards-container">
                        <!-- Здесь будут карточки новостей -->
                        <div class="placeholder-card">
                            <div class="placeholder-image"></div>
                            <div class="placeholder-text"></div>
                        </div>
                        <div class="placeholder-card">
                            <div class="placeholder-image"></div>
                            <div class="placeholder-text"></div>
                        </div>
                    </div>
                </div>

                <div class="section hackathons">
                    <div class="section-header">
                        <h2>Хакатоны</h2>
                        <button @click="refreshHackathons" class="refresh-button">
                            Обновить
                        </button>
                    </div>
                    
                    <div v-if="loading.hackathons" class="loading">
                        Загрузка...
                    </div>
                    
                    <div v-else-if="error.hackathons" class="error">
                        {{ error.hackathons }}
                        <button @click="fetchHackathons" class="retry-button">
                            Попробовать снова
                        </button>
                    </div>
                    
                    <div v-else class="cards-container">
                        <div v-for="hackathon in hackathons" 
                             :key="hackathon.id" 
                             class="hackathon-card">
                            <h3>{{ hackathon.name }}</h3>
                            <p>{{ hackathon.description }}</p>
                            <div class="dates">
                                <span>{{ new Date(hackathon.start_date).toLocaleDateString() }}</span>
                                -
                                <span>{{ new Date(hackathon.end_date).toLocaleDateString() }}</span>
                            </div>
                        </div>
                        
                        <div v-if="hackathons.length === 0" class="empty-state">
                            Нет активных хакатонов
                        </div>
                    </div>
                </div>

                <div class="section webinars">
                    <h2>Вебинары</h2>
                    <div class="cards-container">
                        <!-- Здесь будут карточки вебинаров -->
                        <div class="placeholder-card">
                            <div class="placeholder-image"></div>
                            <div class="placeholder-text"></div>
                        </div>
                    </div>
                </div>

                <div class="section case-cups">
                    <h2>Кейс-капы</h2>
                    <div class="cards-container">
                        <!-- Здесь будут карточки кейс-капов -->
                        <div class="placeholder-card">
                            <div class="placeholder-image"></div>
                            <div class="placeholder-text"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
.home-view {
    padding: 20px;
    padding-bottom: 100px; /* Для навбара */
    max-width: 100vw;
    box-sizing: border-box;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
}

.user-info {
    margin-bottom: 24px;
    position: sticky;
    top: 0;
    z-index: 10;
    padding: 10px 0;
    background: linear-gradient(to bottom, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0) 100%);
}

.username {
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: clamp(18px, 5vw, 24px);
    font-weight: 700;
    color: #1a1a1a;
    margin: 0;
    padding: 8px 16px;
    background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.4));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px;
    display: inline-block;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 90%;
}

.content-section {
    display: flex;
    flex-direction: column;
    gap: 32px;
    width: 100%;
    max-width: 100%;
}

.section {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.05);
    width: 100%;
    box-sizing: border-box;
}

.section h2 {
    font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: clamp(16px, 4vw, 20px);
    font-weight: 600;
    margin: 0 0 16px 0;
    color: #1a1a1a;
}

.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
    width: 100%;
}

.placeholder-card {
    background: rgba(255,255,255,0.5);
    border-radius: 16px;
    padding: 16px;
    height: 200px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.placeholder-image {
    width: 100%;
    height: 120px;
    background: rgba(0,0,0,0.05);
    border-radius: 12px;
}

.placeholder-text {
    width: 70%;
    height: 20px;
    background: rgba(0,0,0,0.05);
    border-radius: 6px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.refresh-button, .retry-button {
    padding: 8px 16px;
    border-radius: 8px;
    border: none;
    background: rgba(255, 255, 255, 0.8);
    color: #1a1a1a;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.refresh-button:hover, .retry-button:hover {
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-1px);
}

.loading {
    text-align: center;
    padding: 20px;
    color: #666;
}

.error {
    text-align: center;
    padding: 20px;
    color: #ff4444;
}

.hackathon-card {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.hackathon-card h3 {
    margin: 0;
    font-size: 18px;
    color: #1a1a1a;
}

.hackathon-card p {
    margin: 0;
    color: #666;
    font-size: 14px;
}

.dates {
    font-size: 14px;
    color: #888;
}

.empty-state {
    text-align: center;
    padding: 40px;
    color: #666;
    font-style: italic;
}

@media screen and (max-width: 600px) {
    .home-view {
        padding: 12px;
        padding-bottom: 80px;
    }

    .section {
        padding: 16px;
        border-radius: 20px;
    }

    .cards-container {
        grid-template-columns: 1fr;
    }

    .username {
        font-size: 18px;
        padding: 6px 12px;
    }

    .hackathon-card {
        padding: 16px;
    }
}

@media screen and (max-width: 360px) {
    .home-view {
        padding: 8px;
        padding-bottom: 70px;
    }

    .section {
        padding: 12px;
        border-radius: 16px;
    }

    .username {
        font-size: 16px;
        padding: 4px 10px;
    }
}
</style>
