<template>
  <div class="rating-page">
    <div class="header">
      <h1>Рейтинг участников</h1>
      <div class="filters">
        <input type="text" v-model="searchQuery" placeholder="Поиск участников..." class="search-input">
        <select v-model="sortBy" class="sort-select">
          <option value="rating">По рейтингу</option>
          <option value="name">По имени</option>
          <option value="hackathons">По количеству хакатонов</option>
        </select>
      </div>
    </div>

    <div class="leaderboard">
      <div v-for="(participant, index) in filteredParticipants" :key="participant.id" class="participant-card">
        <div class="rank">{{ index + 1 }}</div>
        <div class="participant-info">
          <div class="participant-image">
            <img :src="participant.avatar_url || '/default-avatar.jpg'" :alt="participant.name">
          </div>
          <div class="participant-details">
            <h3>{{ participant.name }}</h3>
            <p class="stats">
              <span class="stat">
                <span class="label">Рейтинг:</span>
                <span class="value">{{ participant.rating }}</span>
              </span>
              <span class="stat">
                <span class="label">Хакатонов пройдено:</span>
                <span class="value">{{ participant.hackathons_completed }}</span>
              </span>
              <span class="stat">
                <span class="label">Побед:</span>
                <span class="value">{{ participant.victories }}</span>
              </span>
            </p>
          </div>
          <div class="achievement-badges">
            <div v-for="badge in participant.badges" :key="badge.id" class="badge" :title="badge.name">
              🏆
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
  data() {
    return {
      participants: [],
      searchQuery: '',
      sortBy: 'rating'
    }
  },
  computed: {
    filteredParticipants() {
      return this.participants.filter(participant => 
        participant.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    }
  },
  methods: {
    async fetchParticipants() {
      try {
        const response = await axios.get(`${API_URL}/api/participants/`)
        this.participants = response.data
      } catch (err) {
        console.error('Ошибка при загрузке участников:', err)
      }
    }
  },
  mounted() {
    this.fetchParticipants()
  }
}
</script>

  <style scoped>
.rating-page {
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

.participants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.participant-card {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.participant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.participant-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.4em;
  color: #2c3e50;
}

.stats {
  margin: 15px 0;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #666;
}

.label {
  font-size: 0.9em;
}

.value {
  color: #2c3e50;
  font-weight: 500;
}

.achievement-badges {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.badge {
  font-size: 24px;
  cursor: help;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .participants-grid {
    grid-template-columns: 1fr;
  }
}
  </style>