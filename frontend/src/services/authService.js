import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

class AuthService {
    async authenticateWithTelegram(telegramUser) {
        try {
            const response = await axios.post(`${API_URL}/api/auth/telegram/`, {
                telegram_id: telegramUser.id,
                username: telegramUser.username,
                first_name: telegramUser.first_name,
                last_name: telegramUser.last_name,
                photo_url: telegramUser.photo_url
            });
            
            return response.data;
        } catch (error) {
            console.error('Ошибка аутентификации:', error);
            throw error;
        }
    }

    async getUserProfile() {
        try {
            const telegramUser = window.Telegram.WebApp.initDataUnsafe.user;
            if (!telegramUser) {
                throw new Error('Не удалось получить данные пользователя Telegram');
            }
            
            const response = await axios.get(`${API_URL}/api/users/profile/`, {
                params: {
                    telegram_id: telegramUser.id
                },
                withCredentials: true
            });
            return response.data;
        } catch (error) {
            console.error('Ошибка получения профиля:', error);
            throw error;
        }
    }
}

export default new AuthService(); 