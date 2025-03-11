<template>
  <div class="rating-page">
    <div class="rating-header">
      <h1>Рейтинг участников</h1>
      <p class="rating-description">
        Рейтинг формируется на основе участия в хакатонах, кейс-чемпионатах и вебинарах. 
        За каждое участие начисляются баллы в зависимости от типа мероприятия и результата.
      </p>
    </div>

    <div class="filters-section">
      <div class="search-filter">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Поиск по имени..."
          @input="filterParticipants"
        >
      </div>

      <div class="period-filter">
        <select v-model="selectedPeriod" @change="filterParticipants">
          <option value="all">За все время</option>
          <option value="month">За месяц</option>
          <option value="year">За год</option>
        </select>
      </div>

      <div class="activity-filter">
        <select v-model="selectedActivity" @change="filterParticipants">
          <option value="all">Все активности</option>
          <option value="hackathons">Хакатоны</option>
          <option value="casecups">Кейс-чемпионаты</option>
          <option value="webinars">Вебинары</option>
        </select>
      </div>
    </div>

    <div class="rating-table-container">
      <table class="rating-table">
        <thead>
          <tr>
            <th>Место</th>
            <th>Участник</th>
            <th>Баллы</th>
            <th>Хакатоны</th>
            <th>Кейс-чемпионаты</th>
            <th>Вебинары</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(participant, index) in paginatedParticipants" 
              :key="participant.id"
              :class="{ 'current-user': participant.id === currentUserId }">
            <td class="rank">{{ (currentPage - 1) * itemsPerPage + index + 1 }}</td>
            <td class="participant-info">
              <img :src="participant.avatar" :alt="participant.name" class="avatar">
              <span class="name">{{ participant.name }}</span>
            </td>
            <td class="points">{{ participant.points }}</td>
            <td>{{ participant.hackathons_count }}</td>
            <td>{{ participant.casecups_count }}</td>
            <td>{{ participant.webinars_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <button 
        :disabled="currentPage === 1" 
        @click="changePage(currentPage - 1)"
        class="pagination-btn"
      >
        <i class="fas fa-chevron-left"></i>
      </button>

      <button 
        v-for="page in displayedPages" 
        :key="page"
        :class="['pagination-btn', { active: page === currentPage }]"
        @click="changePage(page)"
      >
        {{ page }}
      </button>

      <button 
        :disabled="currentPage === totalPages" 
        @click="changePage(currentPage + 1)"
        class="pagination-btn"
      >
        <i class="fas fa-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const participants = ref([])
const searchQuery = ref('')
const selectedPeriod = ref('all')
const selectedActivity = ref('all')
const currentPage = ref(1)
const itemsPerPage = 20
const currentUserId = ref(null) // Получаем из хранилища или API

// Фильтрация участников
const filteredParticipants = computed(() => {
  return participants.value.filter(participant => {
    const matchesSearch = participant.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesActivity = selectedActivity.value === 'all' || 
                          (selectedActivity.value === 'hackathons' && participant.hackathons_count > 0) ||
                          (selectedActivity.value === 'casecups' && participant.casecups_count > 0) ||
                          (selectedActivity.value === 'webinars' && participant.webinars_count > 0)
    return matchesSearch && matchesActivity
  })
})

// Пагинация
const totalPages = computed(() => {
  return Math.ceil(filteredParticipants.value.length / itemsPerPage)
})

const paginatedParticipants = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredParticipants.value.slice(start, end)
})

const displayedPages = computed(() => {
  const delta = 2
  const range = []
  const rangeWithDots = []
  let l

  for (let i = 1; i <= totalPages.value; i++) {
    if (i === 1 || i === totalPages.value || 
        (i >= currentPage.value - delta && i <= currentPage.value + delta)) {
      range.push(i)
    }
  }

  range.forEach(i => {
    if (l) {
      if (i - l === 2) {
        rangeWithDots.push(l + 1)
      } else if (i - l !== 1) {
        rangeWithDots.push('...')
      }
    }
    rangeWithDots.push(i)
    l = i
  })

  return rangeWithDots
})

// Методы
const filterParticipants = () => {
  currentPage.value = 1
}

const changePage = (page) => {
  currentPage.value = page
}

const fetchParticipants = async () => {
  try {
    const response = await axios.get('/api/rating', {
      params: {
        period: selectedPeriod.value
      }
    })
    participants.value = response.data
  } catch (error) {
    console.error('Error fetching participants:', error)
  }
}

onMounted(() => {
  fetchParticipants()
})
</script>

<style scoped>
.rating-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.rating-header {
  text-align: center;
  margin-bottom: 40px;
}

.rating-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 15px;
}

.rating-description {
  color: #6b7280;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.search-filter input,
.period-filter select,
.activity-filter select {
  padding: 10px 15px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #4b5563;
  background-color: white;
  transition: all 0.3s ease;
}

.search-filter input {
  width: 300px;
}

.search-filter input:focus,
.period-filter select:focus,
.activity-filter select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
}

.rating-table-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  overflow: hidden;
  margin-bottom: 30px;
}

.rating-table {
  width: 100%;
  border-collapse: collapse;
}

.rating-table th {
  background: #f9fafb;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  color: #4b5563;
  border-bottom: 1px solid #e5e7eb;
}

.rating-table td {
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
  color: #1f2937;
}

.rating-table tr:last-child td {
  border-bottom: none;
}

.participant-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.rank {
  font-weight: 600;
  color: #6366f1;
}

.points {
  font-weight: 600;
  color: #059669;
}

.current-user {
  background-color: #f3f4f6;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 30px;
}

.pagination-btn {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  background: white;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.pagination-btn.active {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .rating-header h1 {
    font-size: 2rem;
  }

  .filters-section {
    flex-direction: column;
  }

  .search-filter input {
    width: 100%;
  }

  .rating-table {
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .rating-table th,
  .rating-table td {
    white-space: nowrap;
  }
}
</style>