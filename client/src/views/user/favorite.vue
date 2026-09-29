<template>
  <div class="page-container">
    <h2 style="font-size:18px;color:#303133;margin-bottom:20px"><el-icon><Star /></el-icon> 我的收藏</h2>
    <div class="photo-grid">
      <div class="photo-card" v-for="item in photos" :key="item.id">
        <div class="img-wrap">
          <el-image :src="item.url" fit="cover" style="width:100%;height:100%" :preview-src-list="[item.url]" />
        </div>
        <div class="info">
          <div class="title">{{ item.name || '未命名' }}</div>
          <div class="meta">
            <span><el-icon><Pointer /></el-icon> {{ item.likeCount || 0 }}</span>
            <span>{{ formatDateTime(item.createTime) }}</span>
          </div>
        </div>
      </div>
    </div>
    <el-empty v-if="photos.length === 0" description="还没有收藏的照片" />
    <el-pagination v-if="total > 0" style="margin-top:20px;justify-content:center" v-model:current-page="query.pageNum"
      v-model:page-size="query.pageSize" :total="total" layout="total,prev,pager,next" @change="loadData" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { pageFavorite, formatDateTime } from '@/api'

const photos = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 12 })

const loadData = async () => {
  const res = await pageFavorite(query)
  photos.value = res.data.records
  total.value = res.data.total
}

onMounted(loadData)
</script>
