<template>
  <div class="page-container">
    <h2 style="font-size:18px;color:#303133;margin-bottom:20px"><el-icon><Bell /></el-icon> 系统公告</h2>
    <div v-for="item in notices" :key="item.id" class="card-box" style="margin-bottom:16px">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <h3 style="font-size:16px;color:#303133">{{ item.title }}</h3>
        <span style="font-size:13px;color:#909399">{{ formatDateTime(item.createTime) }}</span>
      </div>
      <p style="font-size:14px;color:#606266;line-height:1.8">{{ item.content }}</p>
    </div>
    <el-empty v-if="notices.length === 0" description="暂无公告" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listNotice, formatDateTime } from '@/api'

const notices = ref([])

onMounted(async () => {
  const res = await listNotice()
  notices.value = res.data.records || []
})
</script>
