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
    <Navbar />
</template>

<script setup>
import { onMounted } from 'vue';
import { provideAuth } from './composables/useAuth';
import { useRouter } from 'vue-router';
import AuthService from './services/authService';
import { setupInterceptors } from './services/setupInterceptors';
import Navbar from './components/Navbar.vue';

const { loading, error, setLoading, setError, setUser } = provideAuth();
const router = useRouter();
const authService = new AuthService();

// Настраиваем интерцепторы
setupInterceptors(authService);

const retryAuth = async () => {
    setError(null);
    setLoading(true);
    
    try {
        const isAuthenticated = await authService.authenticate();
        if (!isAuthenticated) {
            setError('Ошибка аутентификации. Пожалуйста, попробуйте снова.');
        } else {
            const user = authService.getUser();
            setUser(user);
        }
    } catch (error) {
        console.error('Error during authentication:', error);
        if (error.message === 'Приложение должно быть запущено в Telegram') {
            setError('Это приложение должно быть открыто через Telegram.');
        } else {
            setError('Произошла ошибка при аутентификации. Пожалуйста, попробуйте снова.');
        }
    } finally {
        setLoading(false);
    }
};

onMounted(async () => {
    await retryAuth();
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
