<template>
  <div class="page-container">
    <div class="card-box album-header-box">
      <el-button class="back-btn" text @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>返回
      </el-button>
      <div class="album-header-main">
        <div class="album-info">
          <h2>{{ album.name }}</h2>
          <p>{{ album.description || '暂无描述' }} · {{ album.photoCount || 0 }} 张照片</p>
        </div>
        <div class="album-actions" v-if="isOwner">
          <el-upload :show-file-list="false" :http-request="handleUpload" accept="image/*" multiple>
            <el-button type="primary"><el-icon><Upload /></el-icon>上传照片</el-button>
          </el-upload>
        </div>
      </div>
    </div>

    <div class="photo-grid">
      <div class="photo-card" v-for="(item, index) in photos" :key="item.id">
        <div class="img-wrap">
          <el-image
            :src="item.url"
            fit="cover"
            style="width:100%;height:100%"
            :preview-src-list="previewUrlList"
            :initial-index="index"
            preview-teleported
          />
          <div
            v-if="canDeletePhoto(item)"
            class="photo-delete-zone"
            @click.stop="handleDelete(item)"
          >
            <span class="photo-delete-icon">❌</span>
          </div>
        </div>
        <div class="info">
          <div class="title" :class="{ editable: isOwner }" @click="isOwner && openRename(item)">
            <span>{{ item.name || '未命名' }}</span>
            <el-icon v-if="isOwner" class="edit-icon"><Edit /></el-icon>
          </div>
          <div class="meta">
            <span><el-icon><Pointer /></el-icon> {{ item.likeCount || 0 }}</span>
            <span>{{ formatDateTime(item.createTime) }}</span>
          </div>
          <div class="action-bar">
            <el-button :type="item.liked ? 'danger' : 'default'" size="small" @click.stop="handleLike(item)">
              <el-icon><Pointer /></el-icon>{{ item.liked ? '已赞' : '点赞' }}
            </el-button>
            <el-button :type="item.favorited ? 'warning' : 'default'" size="small" @click.stop="handleFavorite(item)">
              <el-icon><Star /></el-icon>{{ item.favorited ? '已藏' : '收藏' }}
            </el-button>
            <el-button size="small" @click.stop="openComment(item)"><el-icon><ChatDotRound /></el-icon>评论</el-button>
          </div>
        </div>
      </div>
    </div>
    <el-empty v-if="photos.length === 0" description="相册还没有照片" />

    <!-- 评论对话框 -->
    <el-dialog v-model="commentVisible" title="照片评论" width="520px">
      <div v-loading="commentLoading" class="comment-list">
        <div v-for="c in comments" :key="c.id" class="comment-item">
          <div class="comment-meta">
            <span class="comment-user">{{ c.username || '匿名用户' }}</span>
            <span class="comment-time">{{ formatDateTime(c.createTime) }}</span>
          </div>
          <div class="comment-content">{{ c.content }}</div>
        </div>
        <el-empty v-if="!commentLoading && comments.length === 0" description="暂无评论" :image-size="60" />
      </div>
      <el-divider content-position="left">发表评论</el-divider>
      <el-input v-model="commentContent" type="textarea" :rows="3" placeholder="请输入评论内容" maxlength="500" show-word-limit />
      <template #footer>
        <el-button @click="commentVisible = false">取消</el-button>
        <el-button type="primary" :loading="commentSubmitting" @click="submitComment">提交</el-button>
      </template>
    </el-dialog>

    <!-- 修改照片名称对话框 -->
    <el-dialog v-model="renameVisible" title="修改照片名称" width="450px">
      <el-input v-model="renameName" placeholder="请输入照片名称" maxlength="100" show-word-limit />
      <template #footer>
        <el-button @click="renameVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRename">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/store/user'
import { getAlbum, pagePhoto, addPhoto, updatePhoto, deletePhoto, toggleLike, toggleFavorite, pageComment, addComment, uploadFile, formatDateTime } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const userStore = useUserStore()
const album = ref({})
const photos = ref([])
const commentVisible = ref(false)
const commentContent = ref('')
const comments = ref([])
const commentLoading = ref(false)
const commentSubmitting = ref(false)
const currentPhoto = ref(null)
const renameVisible = ref(false)
const renameName = ref('')
const renamePhoto = ref(null)

const isOwner = computed(() => Number(album.value.userId) === Number(userStore.userInfo?.id))
/** 预览图片 URL 列表 */
const previewUrlList = computed(() => photos.value.map(p => p.url))

/** 判断当前用户是否可删除该照片 */
const canDeletePhoto = (item) => {
  const currentUserId = Number(userStore.userInfo?.id)
  return currentUserId && (isOwner.value || Number(item.userId) === currentUserId)
}

const loadAlbum = async () => {
  const res = await getAlbum(route.params.id)
  album.value = res.data || {}
}

const loadPhotos = async () => {
  const res = await pagePhoto({ pageNum: 1, pageSize: 100, albumId: route.params.id })
  photos.value = res.data.records
}

const handleUpload = async ({ file }) => {
  const res = await uploadFile(file, 'photo')
  await addPhoto({
    albumId: route.params.id,
    name: file.name,
    url: res.data,
    fileSize: file.size
  })
  ElMessage.success('上传成功')
  loadPhotos()
  loadAlbum()
}

const handleLike = async (item) => {
  await toggleLike(item.id)
  item.liked = !item.liked
  item.likeCount = item.liked ? (item.likeCount || 0) + 1 : Math.max(0, (item.likeCount || 0) - 1)
}

const handleFavorite = async (item) => {
  await toggleFavorite(item.id)
  item.favorited = !item.favorited
  ElMessage.success(item.favorited ? '收藏成功' : '取消收藏')
}

/** 加载指定照片的已审核评论列表 */
const loadComments = async (photoId) => {
  commentLoading.value = true
  try {
    const res = await pageComment({ photoId, status: 1, pageNum: 1, pageSize: 100 })
    comments.value = res.data.records || []
  } finally {
    commentLoading.value = false
  }
}

/** 打开评论弹窗并加载评论列表 */
const openComment = async (item) => {
  currentPhoto.value = item
  commentContent.value = ''
  commentVisible.value = true
  await loadComments(item.id)
}

/** 提交评论 */
const submitComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  commentSubmitting.value = true
  try {
    await addComment({ photoId: currentPhoto.value.id, content: commentContent.value })
    commentContent.value = ''
    ElMessage.success('评论已提交，等待审核')
  } finally {
    commentSubmitting.value = false
  }
}

const handleDelete = (item) => {
  ElMessageBox.confirm(`确定删除照片「${item.name || '未命名'}」吗？`, '删除确认', { type: 'warning' }).then(async () => {
    await deletePhoto(item.id)
    ElMessage.success('删除成功')
    loadPhotos()
    loadAlbum()
  }).catch(() => {})
}

/** 打开修改照片名称对话框 */
const openRename = (item) => {
  renamePhoto.value = item
  renameName.value = item.name || ''
  renameVisible.value = true
}

/** 提交照片名称修改 */
const submitRename = async () => {
  const name = renameName.value.trim()
  if (!name) {
    ElMessage.warning('请输入照片名称')
    return
  }
  await updatePhoto({ id: renamePhoto.value.id, name })
  renamePhoto.value.name = name
  ElMessage.success('名称修改成功')
  renameVisible.value = false
}

onMounted(() => { loadAlbum(); loadPhotos() })
</script>

<style scoped>
.album-header-box {
  margin-bottom: 20px;
}

.back-btn {
  padding-left: 0;
  margin-bottom: 8px;
  color: #606266;
}

.back-btn:hover {
  color: #409eff;
}

.album-header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.album-info h2 {
  font-size: 20px;
  color: #303133;
}

.album-info p {
  color: #909399;
  margin-top: 6px;
}

.album-actions {
  flex-shrink: 0;
}

.title.editable {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.title.editable:hover {
  color: #409eff;
}

.title .edit-icon {
  font-size: 14px;
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.2s;
}

.title.editable:hover .edit-icon {
  opacity: 1;
}

.action-bar {
  margin-top: 8px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.action-bar :deep(.el-button) {
  width: 100%;
  margin-left: 0;
  padding: 5px 4px;
}

.action-bar :deep(.el-button > span) {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
  white-space: nowrap;
}

/** 照片右上角删除热区 */
.photo-delete-zone {
  position: absolute;
  top: 0;
  right: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 6px;
  z-index: 10;
  cursor: pointer;
}

/** 删除图标：默认隐藏，鼠标移入右上角热区时显示 */
.photo-delete-icon {
  font-size: 16px;
  line-height: 1;
  opacity: 0;
  transition: opacity 0.2s;
  user-select: none;
}

.photo-delete-zone:hover .photo-delete-icon {
  opacity: 1;
}

/** 评论列表区域 */
.comment-list {
  max-height: 280px;
  overflow-y: auto;
  margin-bottom: 4px;
}

.comment-item {
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.comment-user {
  font-size: 13px;
  font-weight: 500;
  color: #303133;
}

.comment-time {
  font-size: 12px;
  color: #909399;
}

.comment-content {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
  word-break: break-all;
}
</style>
