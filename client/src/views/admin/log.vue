<template>
  <div class="page-container">
    <div class="card-box">
      <div class="search-bar">
        <el-input v-model="query.username" placeholder="搜索用户名" clearable style="width:220px" @clear="loadData" />
        <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon>搜索</el-button>
      </div>
      <el-table :data="tableData" stripe border>
        <el-table-column prop="id" label="ID" min-width="60" />
        <el-table-column prop="username" label="操作用户" min-width="100" />
        <el-table-column prop="userType" label="用户类型" min-width="90">
          <template #default="{ row }">
            <el-tag :type="row.userType === 'ADMIN' ? 'danger' : 'primary'" size="small">{{ row.userType === 'ADMIN' ? '管理员' : '用户' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="operation" label="操作描述" min-width="200" />
        <el-table-column prop="ip" label="IP地址" min-width="120" />
        <el-table-column label="操作时间" min-width="160">
          <template #default="{ row }">{{ formatDateTime(row.createTime) }}</template>
        </el-table-column>
      </el-table>
      <el-pagination style="margin-top:16px;justify-content:flex-end" v-model:current-page="query.pageNum" v-model:page-size="query.pageSize"
        :total="total" :page-sizes="[10,20,50]" layout="total,sizes,prev,pager,next" @change="loadData" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { pageLog, formatDateTime } from '@/api'

const tableData = ref([])
const total = ref(0)
const query = reactive({ pageNum: 1, pageSize: 10, username: '' })

const loadData = async () => {
  const res = await pageLog(query)
  tableData.value = res.data.records
  total.value = res.data.total
}

onMounted(loadData)
</script>
