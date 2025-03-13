import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

class AuthService {
    constructor() {
        this.telegram = window.Telegram.WebApp;
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

            // Если токена нет или он невалиден, выполняем аутентификацию
            const initData = this.telegram.initData;
            const userData = {
                telegram_id: this.telegram.initDataUnsafe.user.id.toString(),
                first_name: this.telegram.initDataUnsafe.user.first_name,
                last_name: this.telegram.initDataUnsafe.user.last_name,
                username: this.telegram.initDataUnsafe.user.username,
                photo_url: this.telegram.initDataUnsafe.user.photo_url,
            };

            const response = await axios.post(`${API_URL}/auth/telegram/`, userData, {
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
            return false;
        }
    }

    async checkToken(token) {
        return await axios.get(`${API_URL}/auth/check/`, {
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

            const response = await axios.post(`${API_URL}/auth/refresh/`, {
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