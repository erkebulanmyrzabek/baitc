<template>
    <div class="navbar">
        <div class="navbar-left">
            <div class="navbar-left-item">
                <RouterLink to="/">Home</RouterLink>
            </div>
            <div class="navbar-left-item">
                <RouterLink to="/hackathons">Hackathons</RouterLink>
            </div>
            <div class="navbar-left-item">
                <RouterLink to="/shop">Shop</RouterLink>
            </div>
            <div class="navbar-left-item">
                <RouterLink to="/rating">Rating</RouterLink>
            </div>
            <div class="navbar-left-item">
                <RouterLink to="/profile">Profile</RouterLink>
            </div>
        </div>
    </div>
</template>

<style scoped>
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    border-top: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 20px;
    width: 100%;
    max-width: 100vw;
    box-sizing: border-box;
    margin: 0;
}

.navbar-left {
    display: flex;
    flex-direction: row;
    gap: clamp(12px, 3vw, 32px);
    width: 100%;
    justify-content: space-around;
    flex-wrap: nowrap;
}

.navbar-left-item {
    color: #1a1a1a;
    font-size: clamp(14px, 3vw, 16px);
    font-weight: 500;
    transition: all 0.3s ease;
    padding: clamp(8px, 1.5vw, 12px) clamp(12px, 2.5vw, 24px);
    border-radius: 12px;
    white-space: nowrap;
    flex: 1;
    text-align: center;
    min-width: 0;
}

.navbar-left-item:hover {
    color: #000;
    background-color: rgba(255, 255, 255, 0.9);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

@media screen and (max-width: 600px) {
    .navbar {
        padding: 16px 8px;
        border-radius: 16px 16px 0 0;
    }
    
    .navbar-left {
        gap: 8px;
        justify-content: space-between;
    }
    
    .navbar-left-item {
        padding: 8px 12px;
        font-size: 13px;
    }
}

@media screen and (max-width: 400px) {
    .navbar {
        padding: 12px 6px;
    }
    
    .navbar-left {
        gap: 4px;
    }
    
    .navbar-left-item {
        padding: 6px 8px;
        font-size: 12px;
    }
}

@media screen and (max-width: 320px) {
    .navbar-left-item {
        font-size: 11px;
        padding: 5px 6px;
    }
}
</style>