import { ref } from 'vue';
import authService from '../services/authService';

export function useAuth() {
    const isAuthenticated = ref(false);
    const userProfile = ref(null);
    const loading = ref(true);
    const error = ref(null);

    const initializeAuth = async () => {
        try {
            loading.value = true;
            error.value = null;

            // Получаем данные пользователя из Telegram WebApp
            const telegramUser = window.Telegram.WebApp.initDataUnsafe.user;
            
            if (!telegramUser) {
                throw new Error('Не удалось получить данные пользователя Telegram');
            }

            // Аутентифицируем пользователя
            const authResult = await authService.authenticateWithTelegram(telegramUser);
            isAuthenticated.value = true;

            // Получаем расширенные данные профиля
            const profile = await authService.getUserProfile();
            userProfile.value = {
                ...profile,
                telegram_id: telegramUser.id,
                username: telegramUser.username,
                first_name: telegramUser.first_name,
                last_name: telegramUser.last_name,
                photo_url: telegramUser.photo_url
            };

        } catch (e) {
            error.value = 'Ошибка аутентификации: ' + e.message;
            console.error('Ошибка инициализации аутентификации:', e);
        } finally {
            loading.value = false;
        }
    };

    return {
        isAuthenticated,
        userProfile,
        loading,
        error,
        initializeAuth
    };
} 