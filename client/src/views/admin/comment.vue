<template>
  <div class="page-container">
    <div class="card-box">
      <div class="search-bar">
        <el-select v-model="query.status" placeholder="审核状态" clearable style="width:140px" @change="loadData">
          <el-option label="待审核" :value="0" />
          <el-option label="已通过" :value="1" />
          <el-option label="已驳回" :value="2" />
        </el-select>
        <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon>搜索</el-button>
      </div>
      <el-table :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="username" label="评论用户" min-width="100" />
        <el-table-column prop="photoName" label="照片" min-width="120" />
        <el-table-column prop="content" label="评论内容" min-width="200" show-overflow-tooltip />
        <el-table-column label="状态" min-width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 0 ? 'warning' : row.status === 1 ? 'success' : 'danger'" size="small">
              {{ row.status === 0 ? '待审核' : row.status === 1 ? '已通过' : '已驳回' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="评论时间" min-width="160">
          <template #default="{ row }">{{ formatDateTime(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.status === 0" type="success" link @click="handleAudit(row.id, 1)">通过</el-button>
            <el-button v-if="row.status === 0" type="warning" link @click="handleAudit(row.id, 2)">驳回</el-button>
            <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
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
import { pageComment, auditComment, deleteComment, formatDateTime } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10, status: null })

const loadData = async () => {
  const res = await pageComment(query)
  tableData.value = res.data.records
  total.value = res.data.total
}

const handleAudit = async (id, status) => {
  await auditComment({ id, status })
  ElMessage.success(status === 1 ? '已通过' : '已驳回')
  loadData()
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除该评论吗？', '提示', { type: 'warning' }).then(async () => {
    await deleteComment(id)
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

onMounted(loadData)
</script>
