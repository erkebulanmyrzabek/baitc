<template>
  <div class="space-y-6">
    <!-- Хлебные крошки -->
    <nav class="flex" aria-label="Breadcrumb">
      <ol class="inline-flex items-center space-x-1 md:space-x-3">
        <li class="inline-flex items-center">
          <RouterLink to="/hackathons" 
                      class="inline-flex items-center text-sm font-medium text-gray-700 hover:text-blue-600">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
            </svg>
            Хакатоны
          </RouterLink>
        </li>
        <li aria-current="page">
          <div class="flex items-center">
            <svg class="w-6 h-6 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            </svg>
            <span class="ml-1 text-sm font-medium text-gray-500 md:ml-2">{{ hackathon.name }}</span>
          </div>
        </li>
      </ol>
    </nav>

    <!-- Основная информация -->
    <div class="bg-white rounded-xl shadow-sm overflow-hidden">
      <!-- Изображение хакатона -->
      <div class="aspect-video w-full">
        <img v-if="hackathon.image" 
             :src="hackathon.image" 
             :alt="hackathon.name" 
             class="w-full h-full object-cover">
        <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center">
          <svg class="w-24 h-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
      </div>

      <!-- Контент -->
      <div class="p-6">
        <!-- Заголовок и статус -->
        <div class="flex items-start justify-between mb-4">
          <h1 class="text-2xl font-bold text-gray-900">{{ hackathon.name }}</h1>
          <div>
            <span v-if="hackathon.is_registration_open" class="px-3 py-1 text-sm bg-green-500 text-white rounded-full">
              Регистрация открыта
            </span>
            <span v-else-if="hackathon.is_active" class="px-3 py-1 text-sm bg-blue-500 text-white rounded-full">
              Проходит
            </span>
            <span v-else-if="hackathon.is_finished" class="px-3 py-1 text-sm bg-gray-500 text-white rounded-full">
              Завершен
            </span>
            <span v-else class="px-3 py-1 text-sm bg-yellow-500 text-white rounded-full">
              Скоро
            </span>
          </div>
        </div>

        <!-- Основная информация -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div class="space-y-4">
            <div>
              <h3 class="text-sm font-medium text-gray-500">📅 Регистрация</h3>
              <p class="mt-1 text-sm text-gray-900">
                {{ formatDate(hackathon.start_registration) }} - {{ formatDate(hackathon.end_registration) }}
              </p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">🎯 Проведение</h3>
              <p class="mt-1 text-sm text-gray-900">
                {{ formatDate(hackathon.start_hackathon) }} - {{ formatDate(hackathon.end_hackathon) }}
              </p>
            </div>
            <div v-if="hackathon.prize_pool">
              <h3 class="text-sm font-medium text-gray-500">💰 Призовой фонд</h3>
              <p class="mt-1 text-xl font-bold text-gray-900">{{ hackathon.prize_pool }} ₸</p>
              
              <!-- Призовые места -->
              <div class="mt-3 space-y-2">
                <div v-for="prize in hackathon.prize_places" 
                     :key="prize.place"
                     class="flex items-center justify-between bg-gray-50 rounded-lg p-2">
                  <div class="flex items-center">
                    <span v-if="prize.place === 1" class="text-2xl mr-2">🥇</span>
                    <span v-else-if="prize.place === 2" class="text-2xl mr-2">🥈</span>
                    <span v-else-if="prize.place === 3" class="text-2xl mr-2">🥉</span>
                    <span v-else class="text-2xl mr-2">🏅</span>
                    <span class="text-sm font-medium">{{ prize.place }} место</span>
                  </div>
                  <span class="text-sm font-bold text-gray-900">{{ prize.prize_amount }} ₸</span>
                </div>
              </div>
            </div>
          </div>
          <div class="space-y-4">
            <div>
              <h3 class="text-sm font-medium text-gray-500">👥 Участники</h3>
              <p class="mt-1 text-sm text-gray-900">{{ hackathon.participants_count }} человек</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">🏆 Количество победителей</h3>
              <p class="mt-1 text-sm text-gray-900">{{ hackathon.number_of_winners }}</p>
            </div>
            <div>
              <h3 class="text-sm font-medium text-gray-500">🌐 Формат проведения</h3>
              <p class="mt-1 text-sm text-gray-900">
                {{ getFormatLabel(hackathon.type) }}
              </p>
            </div>
            <div v-if="hackathon.tags?.length">
              <h3 class="text-sm font-medium text-gray-500">🏷️ Теги</h3>
              <div class="mt-1 flex flex-wrap gap-2">
                <span v-for="tag in hackathon.tags" 
                      :key="tag.id"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ tag.name }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Описание -->
        <div class="prose max-w-none">
          <h3 class="text-sm font-medium text-gray-500 mb-2">📝 Описание</h3>
          <div v-html="formattedDescription"></div>
        </div>

        <!-- Кнопки действий -->
        <div class="mt-6 flex flex-col sm:flex-row gap-4">
          <button v-if="hackathon.is_registration_open" 
                  @click="register"
                  class="btn-primary flex-1">
            Зарегистрироваться
          </button>
          <RouterLink to="/hackathons" 
                      class="btn-secondary flex-1 text-center">
            Вернуться к списку
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Результаты -->
    <div v-if="hackathon.is_active || hackathon.is_finished" 
         class="bg-white rounded-xl shadow-sm p-6">
      <h2 class="text-lg font-semibold text-gray-900 mb-4">Результаты</h2>
      <div v-if="hackathon.winners?.length" class="space-y-4">
        <div v-for="winner in hackathon.winners" 
             :key="winner.id"
             class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <span v-if="winner.place === 1" class="text-2xl">🥇</span>
              <span v-else-if="winner.place === 2" class="text-2xl">🥈</span>
              <span v-else-if="winner.place === 3" class="text-2xl">🥉</span>
            </div>
            <div class="ml-4">
              <div class="text-sm font-medium text-gray-900">{{ winner.team_name }}</div>
              <div class="text-sm text-gray-500">{{ winner.project_name }}</div>
            </div>
          </div>
          <div class="text-sm text-gray-500">
            {{ winner.prize }}
          </div>
        </div>
      </div>
      <p v-else class="text-gray-500">Результаты пока не объявлены</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const hackathon = ref({})

const formattedDescription = computed(() => {
  return hackathon.value.description?.replace(/\n/g, '<br>') || ''
})

const getFormatLabel = (type) => {
  const labels = {
    online: 'Онлайн',
    offline: 'Офлайн',
    hybrid: 'Гибридный'
  }
  return labels[type] || type
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric'
  }).format(date)
}

const register = async () => {
  try {
    await axios.post(`/api/hackathons/${hackathon.value.id}/register/`)
    // Обработка успешной регистрации
  } catch (error) {
    console.error('Error registering for hackathon:', error)
  }
}

const fetchHackathon = async () => {
  try {
    const response = await axios.get(`/api/hackathons/${route.params.id}/`)
    hackathon.value = response.data
  } catch (error) {
    console.error('Error fetching hackathon:', error)
  }
}

onMounted(() => {
  fetchHackathon()
})
</script>

<style scoped>
.btn-primary {
  @apply px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-500 transform hover:scale-105 text-center;
}

.btn-secondary {
  @apply px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all duration-500 transform hover:scale-105;
}

.prose {
  @apply text-gray-600 text-sm leading-relaxed;
}
</style> 