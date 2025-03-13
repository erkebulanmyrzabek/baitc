import axiosInstance from './axiosConfig';

class HackathonService {
    async getAllHackathons() {
        try {
            const response = await axiosInstance.get('/hackathons/');
            return response.data;
        } catch (error) {
            console.error('Ошибка при получении хакатонов:', error);
            throw error;
        }
    }

    async getActiveHackathons() {
        try {
            const response = await axiosInstance.get('/hackathons/active/');
            return response.data;
        } catch (error) {
            console.error('Ошибка при получении активных хакатонов:', error);
            throw error;
        }
    }

    async registerForHackathon(hackathonId) {
        try {
            const response = await axiosInstance.post(`/hackathons/${hackathonId}/register/`);
            return response.data;
        } catch (error) {
            console.error('Ошибка при регистрации на хакатон:', error);
            throw error;
        }
    }

    async unregisterFromHackathon(hackathonId) {
        try {
            const response = await axiosInstance.post(`/hackathons/${hackathonId}/unregister/`);
            return response.data;
        } catch (error) {
            console.error('Ошибка при отмене регистрации:', error);
            throw error;
        }
    }

    async getHackathon(id) {
        const response = await axiosInstance.get(`/hackathons/${id}/`);
        return response.data;
    }
}

export const hackathonService = new HackathonService(); 