import axios from 'axios';
import AuthService from './authService';

const authService = new AuthService();

// Создаем инстанс axios с базовым URL
const axiosInstance = axios.create({
    baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api'
});

// Добавляем интерцептор для запросов
axiosInstance.interceptors.request.use(
    config => {
        const token = authService.getToken();
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Добавляем интерцептор для ответов
axiosInstance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // Если ошибка 401 и это не запрос на обновление токена
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Пробуем обновить токен
                const newToken = await authService.refreshToken();
                
                // Обновляем заголовок в оригинальном запросе
                originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                
                // Повторяем оригинальный запрос с новым токеном
                return axiosInstance(originalRequest);
            } catch (refreshError) {
                // Если не удалось обновить токен, выходим из системы
                authService.logout();
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default axiosInstance; 