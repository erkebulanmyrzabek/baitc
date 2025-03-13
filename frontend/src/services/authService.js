import axiosInstance from './axiosConfig';

// Тестовые данные для разработки
const TEST_USER = {
    id: '123456789',
    first_name: 'Тестовый',
    last_name: 'Пользователь',
    username: 'test_user',
    photo_url: 'https://via.placeholder.com/100'
};

class AuthService {
    constructor() {
        // В режиме разработки используем тестовые данные
        if (import.meta.env.DEV) {
            this.telegram = {
                initData: 'test_init_data',
                initDataUnsafe: {
                    user: TEST_USER
                }
            };
            console.info('Используется тестовый пользователь:', TEST_USER);
        } else if (window.Telegram && window.Telegram.WebApp) {
            this.telegram = window.Telegram.WebApp;
        } else {
            console.warn('Telegram WebApp не доступен. Приложение запущено вне Telegram.');
            this.telegram = null;
        }
    }

    async authenticate() {
        try {
            // Проверяем наличие токена
            const token = localStorage.getItem('access_token');
            if (token) {
                // Проверяем валидность токена
                try {
                    const response = await this.checkToken(token);
                    if (response.status === 200) {
                        return true;
                    }
                } catch (error) {
                    // Если токен невалиден, удаляем его
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                }
            }

            // В режиме разработки всегда используем тестовые данные
            const initData = import.meta.env.DEV ? 'test_init_data' : this.telegram?.initData;
            const user = import.meta.env.DEV ? TEST_USER : this.telegram?.initDataUnsafe?.user;

            if (!user) {
                throw new Error('Приложение должно быть запущено в Telegram');
            }

            const userData = {
                telegram_id: user.id.toString(),
                first_name: user.first_name || '',
                last_name: user.last_name || '',
                username: user.username || null,
                photo_url: user.photo_url || null,
            };

            const response = await axiosInstance.post('/auth/telegram/', userData, {
                headers: {
                    'X-Telegram-Init-Data': initData
                }
            });

            if (response.data.status === 'success') {
                localStorage.setItem('access_token', response.data.tokens.access);
                localStorage.setItem('refresh_token', response.data.tokens.refresh);
                localStorage.setItem('user', JSON.stringify(response.data.user));
                return true;
            }
            return false;
        } catch (error) {
            console.error('Authentication error:', error);
            throw error;
        }
    }

    async checkToken(token) {
        return await axiosInstance.get('/auth/check/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    }

    async refreshToken() {
        try {
            const refresh_token = localStorage.getItem('refresh_token');
            if (!refresh_token) {
                throw new Error('No refresh token available');
            }

            const response = await axiosInstance.post('/auth/refresh/', {
                refresh: refresh_token
            });

            localStorage.setItem('access_token', response.data.access);
            return response.data.access;
        } catch (error) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            throw error;
        }
    }

    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    }

    getUser() {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    }

    getToken() {
        return localStorage.getItem('access_token');
    }

    isAuthenticated() {
        return !!this.getToken();
    }
}

export default AuthService; 