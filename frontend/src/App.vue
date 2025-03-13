<template>
    <div class="app">
        <div v-if="loading" class="loading-screen">
            <div class="loader"></div>
            <p>Загрузка...</p>
        </div>
        
        <div v-else-if="error" class="error-screen">
            <p>{{ error }}</p>
            <button @click="retryAuth" class="retry-button">Повторить</button>
        </div>

        <router-view v-else />
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAuth } from './composables/useAuth';
import { useRouter } from 'vue-router';
import AuthService from './services/authService'

const { loading, error, initializeAuth } = useAuth();
const router = useRouter();

const authService = new AuthService()

const retryAuth = () => {
    initializeAuth();
};

onMounted(async () => {
    try {
        const isAuthenticated = await authService.authenticate()
        if (!isAuthenticated) {
            console.error('Authentication failed')
        }
    } catch (error) {
        console.error('Error during authentication:', error)
    }
});
</script>

<style>
.app {
    min-height: 100vh;
}

.loading-screen,
.error-screen {
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 20px;
}

.loader {
    width: 48px;
    height: 48px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #6366f1;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}

.error-screen {
    color: #ef4444;
}

.retry-button {
    margin-top: 20px;
    padding: 10px 20px;
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
}

.retry-button:hover {
    background: #4f46e5;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
