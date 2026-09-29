<template>
  <div class="page-container">
    <div class="card-box">
      <div class="search-bar">
        <el-input v-model="query.name" placeholder="搜索相册名称" clearable style="width:220px" @clear="loadData" />
        <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon>搜索</el-button>
      </div>
      <el-table :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column label="封面" min-width="80">
          <template #default="{ row }">
            <el-image :src="row.cover" style="width:50px;height:50px;border-radius:6px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="相册名称" min-width="120" />
        <el-table-column prop="username" label="所属用户" min-width="100" />
        <el-table-column prop="categoryName" label="分类" min-width="80" />
        <el-table-column label="公开" min-width="70">
          <template #default="{ row }">
            <el-tag :type="row.isPublic === 1 ? 'success' : 'info'" size="small">{{ row.isPublic === 1 ? '公开' : '私密' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="photoCount" label="照片数" min-width="70" />
        <el-table-column prop="viewCount" label="浏览量" min-width="70" />
        <el-table-column label="创建时间" min-width="160">
          <template #default="{ row }">{{ formatDateTime(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="margin-top:16px;justify-content:flex-end" v-model:current-page="query.pageNum" v-model:page-size="query.pageSize"
        :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next" @change="loadData" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { pageAlbum, deleteAlbum, formatDateTime } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10, name: '' })

const loadData = async () => {
  const res = await pageAlbum(query)
  tableData.value = res.data.records
  total.value = res.data.total
}

const handleDelete = (row) => {
  if (row.photoCount > 0) {
    ElMessage.warning('相册内还有照片，请先删除全部照片后再删除相册')
    return
  }
  ElMessageBox.confirm(`确定删除相册「${row.name}」吗？`, '删除确认', { type: 'warning' }).then(async () => {
    await deleteAlbum(row.id)
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

onMounted(loadData)
</script>
