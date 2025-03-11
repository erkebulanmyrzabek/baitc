<template>
    <div class="profile-page">
        <div class="profile-header-wrapper">
            <div class="profile-header">
                <div class="profile-avatar-wrapper">
                    <div class="profile-avatar">
                        <img :src="user?.photo_url || '/default-avatar.png'" alt="Profile photo">
                    </div>
                    <div class="online-status"></div>
                </div>
                <div class="profile-info">
                    <h1>{{ user?.first_name }} {{ user?.last_name }}</h1>
                    <p class="username">@{{ user?.username }}</p>
                    <div class="profile-stats">
                        <div class="stat">
                            <span class="stat-value">{{ userProfile.hackathons_count || 0 }}</span>
                            <span class="stat-label">Хакатонов</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">{{ userProfile.achievements?.length || 0 }}</span>
                            <span class="stat-label">Достижений</span>
                        </div>
                        <div class="stat">
                            <span class="stat-value">{{ userProfile.tech_stack?.length || 0 }}</span>
                            <span class="stat-label">Технологий</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="content-wrapper">
            <div class="section hackathons-section">
                <h2>Участие в хакатонах</h2>
                <div class="hackathons-grid">
                    <div v-for="hackathon in userProfile.hackathons" :key="hackathon.id" class="hackathon-card">
                        <div class="hackathon-card-header">
                            <span class="hackathon-date">{{ formatDate(hackathon.date) }}</span>
                            <span :class="['status-badge', hackathon.status]">{{ hackathon.status }}</span>
                        </div>
                        <h3>{{ hackathon.name }}</h3>
                        <p class="hackathon-role">{{ hackathon.role || 'Участник' }}</p>
                        <div class="team-members" v-if="hackathon.team_members">
                            <div class="team-avatars">
                                <img v-for="member in hackathon.team_members.slice(0, 3)" :key="member.id" :src="member.photo_url || '/default-avatar.png'" :alt="member.name">
                                <div v-if="hackathon.team_members.length > 3" class="more-members">
                                    +{{ hackathon.team_members.length - 3 }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section achievements-section">
                <h2>Достижения</h2>
                <div class="achievements-grid">
                    <div v-for="achievement in userProfile.achievements" :key="achievement.id" class="achievement-card" :class="{ 'achievement-locked': !achievement.unlocked }">
                        <div class="achievement-icon">
                            <img :src="achievement.icon" :alt="achievement.name">
                        </div>
                        <div class="achievement-info">
                            <h3>{{ achievement.name }}</h3>
                            <p>{{ achievement.description }}</p>
                            <span v-if="achievement.unlocked" class="unlock-date">
                                Получено {{ formatDate(achievement.unlocked_date) }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section tech-stack-section">
                <h2>Технический стек</h2>
                <div class="tech-stack-grid">
                    <div v-for="tech in userProfile.tech_stack" :key="tech.name" class="tech-card">
                        <div class="tech-icon">
                            <img :src="tech.icon" :alt="tech.name">
                        </div>
                        <div class="tech-info">
                            <h3>{{ tech.name }}</h3>
                            <div class="progress-bar">
                                <div class="progress" :style="{ width: tech.level + '%' }"></div>
                            </div>
                            <span class="level-text">Уровень {{ tech.level }}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>  
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
    name: 'ProfileView',
    setup() {
        const user = ref(window.Telegram.WebApp.initDataUnsafe.user);
        const userProfile = ref({
            hackathons: [],
            achievements: [],
            tech_stack: [],
            hackathons_count: 0
        });

        const fetchUserProfile = async () => {
            try {
                const response = await axios.get(`/api/users/${user.value.id}/profile`);
                userProfile.value = response.data;
            } catch (error) {
                console.error('Error fetching user profile:', error);
            }
        };

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('ru-RU', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            }).format(date);
        };

        onMounted(() => {
            fetchUserProfile();
        });

        return {
            user,
            userProfile,
            formatDate
        };
    }
};
</script>

<style scoped>
.profile-page {
    min-height: 100vh;
    background: #f8f9fa;
    padding-bottom: 80px;
}

.profile-header-wrapper {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    padding: 40px 20px;
    color: white;
    margin-bottom: 30px;
}

.profile-header {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 30px;
}

.profile-avatar-wrapper {
    position: relative;
}

.profile-avatar {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 4px solid rgba(255, 255, 255, 0.2);
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.online-status {
    position: absolute;
    bottom: 10px;
    right: 10px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #22c55e;
    border: 3px solid white;
}

.profile-info {
    flex: 1;
}

.profile-info h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.username {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 5px 0 15px;
}

.profile-stats {
    display: flex;
    gap: 30px;
}

.stat {
    text-align: center;
}

.stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

.content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.section {
    margin-bottom: 40px;
}

.section h2 {
    font-size: 1.5rem;
    color: #1f2937;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.hackathons-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.hackathon-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.hackathon-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.hackathon-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.hackathon-date {
    color: #6b7280;
    font-size: 0.9rem;
}

.status-badge {
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
}

.status-badge.active {
    background: #dcfce7;
    color: #166534;
}

.status-badge.completed {
    background: #dbeafe;
    color: #1e40af;
}

.hackathon-role {
    color: #6b7280;
    font-size: 0.9rem;
    margin: 5px 0;
}

.team-members {
    margin-top: 15px;
}

.team-avatars {
    display: flex;
    align-items: center;
}

.team-avatars img {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 2px solid white;
    margin-left: -8px;
}

.team-avatars img:first-child {
    margin-left: 0;
}

.more-members {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #e5e7eb;
    color: #4b5563;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: -8px;
}

.achievements-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.achievement-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: flex-start;
    gap: 15px;
    transition: transform 0.2s;
}

.achievement-card:hover {
    transform: translateY(-2px);
}

.achievement-locked {
    opacity: 0.6;
    filter: grayscale(1);
}

.achievement-icon {
    width: 50px;
    height: 50px;
    flex-shrink: 0;
}

.achievement-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.achievement-info h3 {
    margin: 0 0 5px;
    font-size: 1.1rem;
    color: #1f2937;
}

.achievement-info p {
    margin: 0;
    font-size: 0.9rem;
    color: #6b7280;
}

.unlock-date {
    display: block;
    margin-top: 8px;
    font-size: 0.8rem;
    color: #059669;
}

.tech-stack-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
}

.tech-card {
    background: white;
    border-radius: 12px;
    padding: 15px;
    display: flex;
    align-items: center;
    gap: 15px;
}

.tech-icon {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
}

.tech-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.tech-info {
    flex: 1;
}

.tech-info h3 {
    margin: 0 0 8px;
    font-size: 1rem;
    color: #1f2937;
}

.progress-bar {
    height: 6px;
    background: #e5e7eb;
    border-radius: 3px;
    overflow: hidden;
}

.progress {
    height: 100%;
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 3px;
    transition: width 0.3s ease;
}

.level-text {
    display: block;
    margin-top: 5px;
    font-size: 0.8rem;
    color: #6b7280;
}

@media (max-width: 768px) {
    .profile-header {
        flex-direction: column;
        text-align: center;
    }

    .profile-stats {
        justify-content: center;
    }

    .profile-avatar {
        width: 120px;
        height: 120px;
    }

    .profile-info h1 {
        font-size: 2rem;
    }

    .hackathons-grid,
    .achievements-grid,
    .tech-stack-grid {
        grid-template-columns: 1fr;
    }
}
</style>