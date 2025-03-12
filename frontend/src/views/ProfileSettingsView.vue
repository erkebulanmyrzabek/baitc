<script setup>
import { ref, onMounted } from 'vue'
import { useMiniApp } from 'vue-tg'

const MiniApp = useMiniApp()

const API_URL = import.meta.env.VITE_API_URL

// Список технологий
const techStack = [
    { id: 'ai', name: 'AI/ML' },
    { id: 'blockchain', name: 'Blockchain' },
    { id: 'frontend', name: 'Frontend' },
    { id: 'backend', name: 'Backend' },
    { id: 'mobile', name: 'Mobile Development' },
    { id: 'devops', name: 'DevOps' },
    { id: 'gamedev', name: 'Game Development' },
    { id: 'cybersecurity', name: 'Cybersecurity' },
    { id: 'data_science', name: 'Data Science' },
    { id: 'iot', name: 'IoT' },
    { id: 'ar_vr', name: 'AR/VR' },
    { id: 'cloud', name: 'Cloud Computing' }
]

// Настройки пользователя
const userSettings = ref({
    personalInfo: {
        name: '',
        age: null,
        gender: '',
        phone: '',
        city: '',
        email: ''
    },
    preferences: {
        techStack: [],
        language: 'ru',
        theme: 'system'
    }
})

// Опции для выбора
const genderOptions = [
    { value: 'male', label: 'Мужской' },
    { value: 'female', label: 'Женский' },
    { value: 'other', label: 'Другой' }
]

const themeOptions = [
    { value: 'system', label: 'Системная (Telegram)' },
    { value: 'dark', label: 'Темная' },
    { value: 'light', label: 'Светлая' }
]

const languageOptions = [
    { value: 'ru', label: 'Русский' },
    { value: 'en', label: 'English' },
    { value: 'kk', label: 'Қазақша' }
]

// Состояние загрузки и ошибок
const loading = ref(false)
const error = ref(null)
const successMessage = ref('')

// Загрузка данных пользователя
onMounted(async () => {
    try {
        loading.value = true
        const response = await fetch(`${API_URL}/api/users/profile/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        })

        if (!response.ok) {
            throw new Error('Ошибка при получении данных профиля')
        }

        const data = await response.json()
        userSettings.value = {
            personalInfo: {
                name: data.name || '',
                age: data.age || null,
                gender: data.gender || '',
                phone: data.phone || '',
                city: data.city || '',
                email: data.email || ''
            },
            preferences: {
                techStack: data.tech_stack || [],
                language: data.language || 'ru',
                theme: data.theme || 'system'
            }
        }
    } catch (e) {
        error.value = 'Ошибка при загрузке данных: ' + e.message
        console.error('Ошибка при загрузке профиля:', e)
    } finally {
        loading.value = false
    }
})

// Валидация данных перед отправкой
const validateSettings = () => {
    const errors = []
    const { personalInfo } = userSettings.value

    if (!personalInfo.name.trim()) {
        errors.push('Имя обязательно для заполнения')
    }

    if (personalInfo.age && (personalInfo.age < 0 || personalInfo.age > 120)) {
        errors.push('Укажите корректный возраст')
    }

    if (personalInfo.email && !personalInfo.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        errors.push('Укажите корректный email')
    }

    if (personalInfo.phone && !personalInfo.phone.match(/^\+?[\d\s-()]+$/)) {
        errors.push('Укажите корректный номер телефона')
    }

    return errors
}

// Сохранение настроек
const saveSettings = async () => {
    try {
        const errors = validateSettings()
        if (errors.length > 0) {
            error.value = errors.join('. ')
            return
        }

        loading.value = true
        error.value = null

        const response = await fetch(`${API_URL}/api/users/profile/`, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
                name: userSettings.value.personalInfo.name,
                age: userSettings.value.personalInfo.age,
                gender: userSettings.value.personalInfo.gender,
                phone: userSettings.value.personalInfo.phone,
                city: userSettings.value.personalInfo.city,
                email: userSettings.value.personalInfo.email,
                tech_stack: userSettings.value.preferences.techStack,
                language: userSettings.value.preferences.language,
                theme: userSettings.value.preferences.theme
            })
        })

        if (!response.ok) {
            const errorData = await response.json()
            throw new Error(errorData.message || 'Ошибка при сохранении настроек')
        }

        successMessage.value = 'Настройки успешно сохранены'
        setTimeout(() => {
            successMessage.value = ''
        }, 3000)
    } catch (e) {
        error.value = e.message || 'Ошибка при сохранении настроек'
        console.error('Ошибка при сохранении настроек:', e)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="settings-container">
        <h1>Настройки профиля</h1>

        <div v-if="loading" class="loading">
            Загрузка...
        </div>

        <div v-else-if="error" class="error">
            {{ error }}
        </div>

        <div v-else class="settings-form">
            <!-- Личная информация -->
            <section class="settings-section">
                <h2>Личная информация</h2>
                
                <div class="form-group">
                    <label for="name">Имя</label>
                    <input 
                        id="name"
                        v-model="userSettings.personalInfo.name"
                        type="text"
                        placeholder="Введите ваше имя"
                    >
                </div>

                <div class="form-group">
                    <label for="age">Возраст</label>
                    <input 
                        id="age"
                        v-model="userSettings.personalInfo.age"
                        type="number"
                        min="0"
                        placeholder="Введите ваш возраст"
                    >
                </div>

                <div class="form-group">
                    <label for="gender">Пол</label>
                    <select 
                        id="gender"
                        v-model="userSettings.personalInfo.gender"
                    >
                        <option value="">Выберите пол</option>
                        <option 
                            v-for="option in genderOptions" 
                            :key="option.value" 
                            :value="option.value"
                        >
                            {{ option.label }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="phone">Телефон</label>
                    <input 
                        id="phone"
                        v-model="userSettings.personalInfo.phone"
                        type="tel"
                        placeholder="Введите ваш телефон"
                    >
                </div>

                <div class="form-group">
                    <label for="city">Город</label>
                    <input 
                        id="city"
                        v-model="userSettings.personalInfo.city"
                        type="text"
                        placeholder="Введите ваш город"
                    >
                </div>

                <div class="form-group">
                    <label for="email">Email</label>
                    <input 
                        id="email"
                        v-model="userSettings.personalInfo.email"
                        type="email"
                        placeholder="Введите ваш email"
                    >
                </div>
            </section>

            <!-- Предпочтения -->
            <section class="settings-section">
                <h2>Предпочтения</h2>

                <div class="form-group">
                    <label>Технологический стек</label>
                    <div class="tech-stack-grid">
                        <label 
                            v-for="tech in techStack" 
                            :key="tech.id"
                            class="tech-checkbox"
                        >
                            <input 
                                type="checkbox"
                                v-model="userSettings.preferences.techStack"
                                :value="tech.id"
                            >
                            <span>{{ tech.name }}</span>
                        </label>
                    </div>
                </div>

                <div class="form-group">
                    <label for="language">Язык приложения</label>
                    <select 
                        id="language"
                        v-model="userSettings.preferences.language"
                    >
                        <option 
                            v-for="option in languageOptions" 
                            :key="option.value" 
                            :value="option.value"
                        >
                            {{ option.label }}
                        </option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="theme">Тема приложения</label>
                    <select 
                        id="theme"
                        v-model="userSettings.preferences.theme"
                    >
                        <option 
                            v-for="option in themeOptions" 
                            :key="option.value" 
                            :value="option.value"
                        >
                            {{ option.label }}
                        </option>
                    </select>
                </div>
            </section>

            <div class="form-actions">
                <button 
                    @click="saveSettings" 
                    :disabled="loading"
                    class="save-button"
                >
                    {{ loading ? 'Сохранение...' : 'Сохранить настройки' }}
                </button>
            </div>

            <div v-if="successMessage" class="success-message">
                {{ successMessage }}
            </div>
        </div>
    </div>
</template>

<style scoped>
.settings-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    color: #1f2937;
    margin-bottom: 30px;
    font-size: 1.8rem;
}

.settings-section {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
    color: #374151;
    margin-bottom: 20px;
    font-size: 1.4rem;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    color: #4b5563;
    font-weight: 500;
}

input[type="text"],
input[type="number"],
input[type="tel"],
input[type="email"],
select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 1rem;
    color: #1f2937;
}

input[type="text"]:focus,
input[type="number"]:focus,
input[type="tel"]:focus,
input[type="email"]:focus,
select:focus {
    outline: none;
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

.tech-stack-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
}

.tech-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
}

.tech-checkbox input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

.form-actions {
    margin-top: 30px;
    display: flex;
    justify-content: flex-end;
}

.save-button {
    background: #6366f1;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.save-button:hover {
    background: #4f46e5;
}

.save-button:disabled {
    background: #9ca3af;
    cursor: not-allowed;
}

.loading {
    text-align: center;
    padding: 40px;
    color: #6b7280;
}

.error {
    text-align: center;
    padding: 20px;
    color: #ef4444;
    background: #fee2e2;
    border-radius: 6px;
    margin-bottom: 20px;
}

.success-message {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #10b981;
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        transform: translateY(100%);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

@media (max-width: 768px) {
    .settings-container {
        padding: 16px;
    }

    .tech-stack-grid {
        grid-template-columns: 1fr;
    }

    h1 {
        font-size: 1.5rem;
    }

    h2 {
        font-size: 1.2rem;
    }
}
</style> 