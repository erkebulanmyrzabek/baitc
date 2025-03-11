<template>
  <div class="shop-page">
    <div class="shop-header">
      <h1>Магазин</h1>
      <p class="shop-description">
        Обменяйте заработанные кристаллы на уникальные товары и привилегии
      </p>
    </div>

    <div class="filters-section">
      <div class="search-filter">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Поиск товаров..."
          @input="filterProducts"
        >
      </div>

      <div class="category-filter">
        <select v-model="selectedCategory" @change="filterProducts">
          <option value="all">Все категории</option>
          <option v-for="category in categories" 
                  :key="category.id" 
                  :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>

      <div class="type-filter">
        <select v-model="selectedType" @change="filterProducts">
          <option value="all">Все типы</option>
          <option value="physical">Физические товары</option>
          <option value="digital">Цифровые товары</option>
          <option value="premium">Премиум-статус</option>
        </select>
      </div>
    </div>

    <div class="products-grid">
      <div v-for="product in filteredProducts" 
           :key="product.id" 
           class="product-card"
           :class="{ 'out-of-stock': !product.is_in_stock }">
        <div class="product-image">
          <img :src="product.image" :alt="product.name">
          <div class="product-type" :class="product.product_type">
            {{ getProductTypeLabel(product.product_type) }}
          </div>
        </div>
        <div class="product-content">
          <h3 class="product-title">{{ product.name }}</h3>
          <p class="product-description">{{ product.description }}</p>
          <div class="product-meta">
            <span class="product-price">{{ product.price }} кристаллов</span>
            <span v-if="product.product_type === 'premium'" class="duration">
              {{ product.premium_duration_days }} дней
            </span>
          </div>
          <button 
            class="buy-button" 
            :disabled="!product.is_in_stock"
            @click="buyProduct(product)">
            {{ product.is_in_stock ? 'Купить' : 'Нет в наличии' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="filteredProducts.length === 0" class="no-products">
      <p>Товары не найдены</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const products = ref([])
const categories = ref([])
const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedType = ref('all')

// Фильтрация товаров
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === 'all' || product.category?.id === selectedCategory.value
    const matchesType = selectedType.value === 'all' || product.product_type === selectedType.value
    return matchesSearch && matchesCategory && matchesType
  })
})

// Получение метки типа товара
const getProductTypeLabel = (type) => {
  const labels = {
    physical: 'Физический товар',
    digital: 'Цифровой товар',
    premium: 'Премиум'
  }
  return labels[type] || type
}

// Методы
const filterProducts = () => {
  // Можно добавить дополнительную логику фильтрации
}

const buyProduct = async (product) => {
  try {
    const response = await axios.post(`/api/shop/products/buy/${product.id}/`)
    // Обработка успешной покупки
    console.log('Покупка успешна:', response.data)
  } catch (error) {
    console.error('Ошибка при покупке:', error)
  }
}

const fetchProducts = async () => {
  try {
    const [productsRes, categoriesRes] = await Promise.all([
      axios.get('/api/shop/products/'),
      axios.get('/api/shop/categories/')
    ])
    products.value = productsRes.data
    categories.value = categoriesRes.data
  } catch (error) {
    console.error('Error fetching shop data:', error)
  }
}

onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.shop-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.shop-header {
  text-align: center;
  margin-bottom: 40px;
}

.shop-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 15px;
}

.shop-description {
  color: #6b7280;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

.filters-section {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.search-filter input,
.category-filter select,
.type-filter select {
  padding: 10px 15px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #4b5563;
  background-color: white;
  transition: all 0.3s ease;
}

.search-filter input {
  width: 300px;
}

.search-filter input:focus,
.category-filter select:focus,
.type-filter select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.product-card.out-of-stock {
  opacity: 0.7;
}

.product-image {
  position: relative;
  width: 100%;
  padding-top: 75%;
  background: #f8f9fa;
}

.product-image img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-type {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 15px;
  font-size: 0.8rem;
  color: white;
}

.product-type.physical {
  background: #6366f1;
}

.product-type.digital {
  background: #8b5cf6;
}

.product-type.premium {
  background: #f59e0b;
}

.product-content {
  padding: 20px;
}

.product-title {
  margin: 0 0 10px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1f2937;
}

.product-description {
  color: #6b7280;
  font-size: 0.9rem;
  margin-bottom: 15px;
  line-height: 1.5;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.product-price {
  font-weight: 600;
  color: #059669;
}

.duration {
  color: #6b7280;
  font-size: 0.9rem;
}

.buy-button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 6px;
  background: #6366f1;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.buy-button:hover:not(:disabled) {
  background: #4f46e5;
}

.buy-button:disabled {
  background: #e5e7eb;
  cursor: not-allowed;
}

.no-products {
  text-align: center;
  padding: 40px;
  color: #6b7280;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  .shop-header h1 {
    font-size: 2rem;
  }

  .filters-section {
    flex-direction: column;
  }

  .search-filter input {
    width: 100%;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }
}
</style>