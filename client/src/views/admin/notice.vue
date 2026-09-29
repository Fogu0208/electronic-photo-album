<template>
  <div class="page-container">
    <div class="card-box">
      <div class="search-bar">
        <el-button type="success" @click="openDialog()"><el-icon><Plus /></el-icon>发布公告</el-button>
      </div>
      <el-table :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="content" label="内容" min-width="300" show-overflow-tooltip />
        <el-table-column label="发布时间" min-width="160">
          <template #default="{ row }">{{ formatDateTime(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="openDialog(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination style="margin-top:16px;justify-content:flex-end" v-model:current-page="query.pageNum" v-model:page-size="query.pageSize"
        :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next" @change="loadData" />
    </div>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑公告' : '发布公告'" width="550px">
      <el-form :model="form" label-width="60px">
        <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="内容"><el-input v-model="form.content" type="textarea" :rows="5" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { pageNotice, addNotice, updateNotice, deleteNotice, formatDateTime } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const query = reactive({ pageNum: 1, pageSize: 10 })
const form = ref({})

const loadData = async () => {
  const res = await pageNotice(query)
  tableData.value = res.data.records
  total.value = res.data.total
}

const openDialog = (row) => {
  form.value = row ? { ...row } : { title: '', content: '' }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (form.value.id) await updateNotice(form.value)
  else await addNotice(form.value)
  ElMessage.success('操作成功')
  dialogVisible.value = false
  loadData()
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除该公告吗？', '提示', { type: 'warning' }).then(async () => {
    await deleteNotice(id)
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

onMounted(loadData)
</script>
