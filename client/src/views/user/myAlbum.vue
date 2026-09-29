<template>
  <div class="page-container">
    <div class="card-box">
      <div class="search-bar">
        <el-input v-model="query.name" placeholder="搜索相册" clearable style="width:220px" @clear="loadData" />
        <el-button type="primary" @click="loadData"><el-icon><Search /></el-icon>搜索</el-button>
        <el-button type="success" @click="openDialog()"><el-icon><Plus /></el-icon>创建相册</el-button>
      </div>
      <div class="album-grid">
        <div class="album-card" v-for="item in albums" :key="item.id" @click="goDetail(item.id)">
          <div class="cover">
            <img :src="item.cover || '/uploads31/photo/default.jpg'" />
            <span class="count">{{ item.photoCount || 0 }} 张</span>
          </div>
          <div class="detail">
            <h3>{{ item.name }}</h3>
            <p>
              <el-tag :type="item.isPublic === 1 ? 'success' : 'info'" size="small">{{ item.isPublic === 1 ? '公开' : '私密' }}</el-tag>
              {{ item.categoryName || '未分类' }}
            </p>
            <div class="album-card-actions" @click.stop>
              <el-button type="primary" size="small" @click="openEditDialog(item)">
                <el-icon><Edit /></el-icon>修改
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(item)">
                <el-icon><Delete /></el-icon>删除
              </el-button>
            </div>
          </div>
        </div>
      </div>
      <el-empty v-if="albums.length === 0" description="还没有相册，创建一个吧" />
    </div>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="相册名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.categoryId" placeholder="选择分类" style="width:100%">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
        <el-form-item label="是否公开">
          <el-switch v-model="form.isPublic" :active-value="1" :inactive-value="0" active-text="公开" inactive-text="私密" />
        </el-form-item>
        <el-form-item label="封面">
          <el-upload :show-file-list="false" :http-request="handleCoverUpload" accept="image/*">
            <el-image v-if="form.cover" :src="form.cover" style="width:120px;height:80px;border-radius:6px" fit="cover" />
            <el-button v-else size="small">上传封面</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { pageAlbum, addAlbum, updateAlbum, deleteAlbum, listCategory, uploadFile } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const albums = ref([])
const categories = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const query = reactive({ pageNum: 1, pageSize: 50, name: '', userId: userStore.userInfo?.id })
const form = ref({})

/** 对话框标题 */
const dialogTitle = computed(() => isEdit.value ? '修改相册' : '创建相册')

const loadData = async () => {
  query.userId = userStore.userInfo?.id
  const res = await pageAlbum(query)
  albums.value = res.data.records
}

const loadCategories = async () => {
  const res = await listCategory()
  categories.value = res.data
}

const openDialog = () => {
  isEdit.value = false
  form.value = { name: '', categoryId: null, description: '', isPublic: 1, cover: '' }
  dialogVisible.value = true
}

/** 打开修改相册对话框 */
const openEditDialog = (item) => {
  isEdit.value = true
  form.value = {
    id: item.id,
    name: item.name,
    categoryId: item.categoryId,
    description: item.description || '',
    isPublic: item.isPublic,
    cover: item.cover || ''
  }
  dialogVisible.value = true
}

const handleCoverUpload = async ({ file }) => {
  const res = await uploadFile(file, 'photo')
  form.value.cover = res.data
}

const handleSave = async () => {
  if (!form.value.name?.trim()) {
    ElMessage.warning('请输入相册名称')
    return
  }
  if (isEdit.value) {
    await updateAlbum({ ...form.value, name: form.value.name.trim() })
    ElMessage.success('修改成功')
  } else {
    await addAlbum(form.value)
    ElMessage.success('创建成功')
  }
  dialogVisible.value = false
  loadData()
}

const goDetail = (id) => router.push(`/user/albumDetail/${id}`)

/** 删除相册（相册内有照片时不允许删除） */
const handleDelete = (item) => {
  if (item.photoCount > 0) {
    ElMessage.warning('相册内还有照片，请先删除全部照片后再删除相册')
    return
  }
  ElMessageBox.confirm(`确定删除相册「${item.name}」吗？`, '删除确认', { type: 'warning' }).then(async () => {
    await deleteAlbum(item.id)
    ElMessage.success('删除成功')
    loadData()
  }).catch(() => {})
}

onMounted(() => { loadData(); loadCategories() })
</script>

<style scoped>
.album-card-actions {
  margin-top: 10px;
  display: flex;
  gap: 8px;
}
</style>
