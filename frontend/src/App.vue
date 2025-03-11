<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted } from 'vue'
import axios from 'axios'
import Navbar from './components/Navbar.vue'
const initTelegramUser = async () => {
  try {
    const telegramUser = window.Telegram.WebApp.initDataUnsafe.user
    if (telegramUser) {
      const response = await axios.post('/api/users/register-telegram', {
        telegram_id: telegramUser.id.toString(),
        username: telegramUser.username,
        first_name: telegramUser.first_name,
        last_name: telegramUser.last_name,
        photo_url: telegramUser.photo_url
      })
      console.log('User registered:', response.data)
    }
  } catch (error) {
    console.error('Error registering user:', error)
  }
}
onMounted(() => {
  initTelegramUser()
})


</script>

<template>
  <RouterView />
  <Navbar />
</template>

<style scoped>

</style>
