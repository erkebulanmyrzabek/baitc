import axios from 'axios';

// Создаем инстанс axios с базовым URL и настройками CORS
const axiosInstance = axios.create({
    baseURL: (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
});

// Добавляем перехватчик для добавления токена к запросам
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Добавляем перехватчик для обработки ошибок
axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Если получаем 401, пробуем обновить токен
            const refresh_token = localStorage.getItem('refresh_token');
            if (refresh_token) {
                try {
                    const response = await axios.post(
                        `${import.meta.env.VITE_API_URL}/api/auth/refresh/`,
                        { refresh: refresh_token }
                    );
                    
                    if (response.data.access) {
                        localStorage.setItem('access_token', response.data.access);
                        // Повторяем исходный запрос с новым токеном
                        error.config.headers.Authorization = `Bearer ${response.data.access}`;
                        return axiosInstance(error.config);
                    }
                } catch (refreshError) {
                    // Если не удалось обновить токен, очищаем хранилище
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    // Перенаправляем на страницу входа или показываем сообщение
                    window.location.href = '/';
                }
            }
        }
        return Promise.reject(error);
    }
);

export default axiosInstance; 