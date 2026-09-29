<template>
  <div class="page-container">
    <div class="card-box profile-layout">
      <!-- 左侧头像 -->
      <div class="profile-left">
        <el-avatar :size="120" :src="form.avatar"><el-icon :size="48"><UserFilled /></el-icon></el-avatar>
        <h3>{{ form.nickname || form.username }}</h3>
        <el-upload :show-file-list="false" :http-request="handleAvatarUpload" accept="image/*">
          <el-button type="primary" size="small" style="margin-top:12px">更换头像</el-button>
        </el-upload>
      </div>
      <!-- 右侧表单 -->
      <div class="profile-right">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="个人资料" name="info">
            <el-form :model="form" label-width="80px" style="max-width:500px;margin-top:20px">
              <el-form-item label="用户名"><el-input v-model="form.username" disabled /></el-form-item>
              <el-form-item label="昵称"><el-input v-model="form.nickname" /></el-form-item>
              <el-form-item label="手机号"><el-input v-model="form.phone" /></el-form-item>
              <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleSaveProfile">保存修改</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="修改密码" name="password">
            <el-form :model="pwdForm" label-width="100px" style="max-width:500px;margin-top:20px">
              <el-form-item label="原密码"><el-input v-model="pwdForm.oldPassword" type="password" show-password /></el-form-item>
              <el-form-item label="新密码"><el-input v-model="pwdForm.newPassword" type="password" show-password /></el-form-item>
              <el-form-item label="确认新密码"><el-input v-model="pwdForm.confirmPassword" type="password" show-password /></el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleSavePassword">修改密码</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getUserInfo, updateAdminProfile, updatePassword, uploadFile } from '@/api'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const activeTab = ref('info')
const form = ref({})
const pwdForm = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })

const loadInfo = async () => {
  const res = await getUserInfo()
  form.value = res.data
}

const handleAvatarUpload = async ({ file }) => {
  const res = await uploadFile(file, 'avatar')
  form.value.avatar = res.data
  await updateAdminProfile(form.value)
  userStore.updateInfo({ avatar: res.data })
  ElMessage.success('头像更新成功')
}

const handleSaveProfile = async () => {
  await updateAdminProfile(form.value)
  userStore.updateInfo({ nickname: form.value.nickname, phone: form.value.phone, email: form.value.email })
  ElMessage.success('资料修改成功')
}

const handleSavePassword = async () => {
  if (pwdForm.newPassword !== pwdForm.confirmPassword) {
    ElMessage.error('两次输入的新密码不一致')
    return
  }
  await updatePassword({ oldPassword: pwdForm.oldPassword, newPassword: pwdForm.newPassword })
  ElMessage.success('密码修改成功')
  pwdForm.oldPassword = ''
  pwdForm.newPassword = ''
  pwdForm.confirmPassword = ''
}

onMounted(loadInfo)
</script>

<style scoped lang="scss">
.profile-layout {
  display: flex;
  gap: 40px;
  min-height: 400px;
}
.profile-left {
  width: 220px;
  text-align: center;
  padding: 30px 20px;
  border-right: 1px solid #ebeef5;
  h3 { margin: 16px 0 0; color: #303133; }
}
.profile-right {
  flex: 1;
}
</style>
