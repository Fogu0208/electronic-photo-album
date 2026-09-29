<template>
  <div class="page-container">
    <div class="card-box">
      <div class="search-bar">
        <el-input v-model="query.name" placeholder="搜索照片名称" clearable style="width:220px" @clear="loadData" />
        <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon>搜索</el-button>
      </div>
      <el-table :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column label="照片" min-width="80">
          <template #default="{ row }">
            <el-image :src="row.url" style="width:50px;height:50px;border-radius:6px" fit="cover" :preview-src-list="[row.url]" preview-teleported />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="120" />
        <el-table-column prop="username" label="上传者" min-width="100" />
        <el-table-column prop="albumName" label="所属相册" min-width="120" />
        <el-table-column prop="likeCount" label="点赞" min-width="60" />
        <el-table-column label="上传时间" min-width="160">
          <template #default="{ row }">{{ formatDateTime(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="margin-top:16px;justify-content:flex-end" v-model:current-page="query.pageNum" v-model:page-size="query.pageSize"
        :total="total" :page-sizes="[12,24,48]" layout="total,sizes,prev,pager,next" @change="loadData" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { pagePhoto, deletePhoto, formatDateTime } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 12, name: '' })

const loadData = async () => {
  const res = await pagePhoto(query)
  tableData.value = res.data.records
  total.value = res.data.total
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除该照片吗？', '提示', { type: 'warning' }).then(async () => {
    await deletePhoto(id)
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

onMounted(loadData)
</script>
