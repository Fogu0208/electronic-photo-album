<template>
  <div class="page-container">
    <div class="card-box">
      <div class="search-bar">
        <el-input v-model="query.name" placeholder="搜索分类名称" clearable style="width:220px" @clear="loadData" />
        <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon>搜索</el-button>
        <el-button type="success" @click="openDialog()"><el-icon><Plus /></el-icon>新增分类</el-button>
      </div>
      <el-table :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="name" label="分类名称" min-width="120" />
        <el-table-column prop="sortNum" label="排序号" min-width="80" />
        <el-table-column prop="remark" label="备注" min-width="200" />
        <el-table-column label="创建时间" min-width="160">
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

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑分类' : '新增分类'" width="450px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="排序号"><el-input-number v-model="form.sortNum" :min="0" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" type="textarea" /></el-form-item>
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
import { pageCategory, addCategory, updateCategory, deleteCategory, formatDateTime } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const tableData = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const query = reactive({ pageNum: 1, pageSize: 10, name: '' })
const form = ref({})

const loadData = async () => {
  const res = await pageCategory(query)
  tableData.value = res.data.records
  total.value = res.data.total
}

const openDialog = (row) => {
  form.value = row ? { ...row } : { name: '', sortNum: 0, remark: '' }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (form.value.id) await updateCategory(form.value)
  else await addCategory(form.value)
  ElMessage.success('操作成功')
  dialogVisible.value = false
  loadData()
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定删除该分类吗？', '提示', { type: 'warning' }).then(async () => {
    await deleteCategory(id)
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

onMounted(loadData)
</script>
