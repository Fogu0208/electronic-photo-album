<template>
  <div class="page-container">
    <div class="search-bar" style="margin-bottom:20px">
      <el-input v-model="query.name" placeholder="搜索公开相册" clearable style="width:240px" @clear="loadData" />
      <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon>搜索</el-button>
    </div>
    <div class="album-grid">
      <div class="album-card" v-for="item in albums" :key="item.id" @click="viewAlbum(item)">
        <div class="cover">
          <img :src="item.cover || '/uploads31/photo/default.jpg'" />
          <span class="count">{{ item.photoCount || 0 }} 张</span>
        </div>
        <div class="detail">
          <h3>{{ item.name }}</h3>
          <p>{{ item.username }} · {{ item.categoryName || '未分类' }}</p>
          <p style="margin-top:4px">{{ item.description || '暂无描述' }}</p>
        </div>
      </div>
    </div>
    <el-empty v-if="albums.length === 0" description="暂无公开相册" />
    <el-pagination v-if="total > 0" style="margin-top:20px;justify-content:center" v-model:current-page="query.pageNum"
      v-model:page-size="query.pageSize" :total="total" :page-sizes="[12,24]" layout="total,prev,pager,next" @change="loadData" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { pagePublicAlbum } from '@/api'

const router = useRouter()
const albums = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 12, name: '' })

const loadData = async () => {
  const res = await pagePublicAlbum(query)
  albums.value = res.data.records
  total.value = res.data.total
}

const viewAlbum = (item) => {
  router.push(`/user/albumDetail/${item.id}`)
}

onMounted(loadData)
</script>
