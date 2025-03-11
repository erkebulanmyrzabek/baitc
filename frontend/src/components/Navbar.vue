<template>
    <nav class="navbar">
        <div class="nav-content">
            <RouterLink to="/" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                </div>
                <span>Главная</span>
            </RouterLink>

            <RouterLink to="/hackathons" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
                    </svg>
                </div>
                <span>Хакатоны</span>
            </RouterLink>

            <RouterLink to="/rating" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
                        <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
                        <line x1="6" y1="1" x2="6" y2="4"></line>
                        <line x1="10" y1="1" x2="10" y2="4"></line>
                        <line x1="14" y1="1" x2="14" y2="4"></line>
                    </svg>
                </div>
                <span>Рейтинг</span>
            </RouterLink>

            <RouterLink to="/shop" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="9" cy="21" r="1"></circle>
                        <circle cx="20" cy="21" r="1"></circle>
                        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                    </svg>
                </div>
                <span>Магазин</span>
            </RouterLink>

            <RouterLink to="/profile" class="nav-item" active-class="active">
                <div class="nav-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <span>Профиль</span>
            </RouterLink>
        </div>
    </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.navbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: white;
    box-shadow: 0 -1px 10px rgba(0, 0, 0, 0.1);
    padding: 10px 0;
    z-index: 1000;
}

.nav-content {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    color: #64748b;
    font-size: 0.75rem;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.nav-item:hover {
    color: #6366f1;
    transform: translateY(-2px);
}

.nav-item.active {
    color: #6366f1;
}

.nav-icon {
    width: 24px;
    height: 24px;
    margin-bottom: 4px;
}

.nav-icon svg {
    width: 100%;
    height: 100%;
}

@media (min-width: 768px) {
    .navbar {
        top: 0;
        bottom: auto;
        padding: 15px 0;
    }

    .nav-content {
        max-width: 1200px;
    }

    .nav-item {
        flex-direction: row;
        font-size: 0.875rem;
        gap: 8px;
    }

    .nav-icon {
        margin-bottom: 0;
    }
}
</style>