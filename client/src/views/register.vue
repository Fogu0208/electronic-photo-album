<template>
  <div class="register-page">
    <div class="register-card">
      <div class="register-header">
        <el-icon :size="48" color="#409eff"><Camera /></el-icon>
        <h2>用户注册</h2>
        <p>创建您的电子相册账号</p>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入昵称" prefix-icon="UserFilled" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请确认密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号(选填)" prefix-icon="Phone" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width:100%" @click="handleRegister">注 册</el-button>
        </el-form-item>
        <div class="register-footer">
          已有账号？<router-link to="/login">返回登录</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '', nickname: '', password: '', confirmPassword: '', phone: ''
})

/** 确认密码校验 */
const validateConfirm = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }],
  confirmPassword: [{ required: true, message: '请确认密码', trigger: 'blur' }, { validator: validateConfirm, trigger: 'blur' }]
}

/** 注册处理 */
const handleRegister = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await register({ username: form.username, nickname: form.nickname, password: form.password, phone: form.phone })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.register-page {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
}
.register-card {
  width: 420px;
  padding: 40px;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.register-header {
  text-align: center;
  margin-bottom: 30px;
  h2 { font-size: 22px; color: #303133; margin: 12px 0 6px; }
  p { color: #909399; font-size: 14px; }
}
.register-footer {
  text-align: center;
  font-size: 14px;
  color: #909399;
  a { color: #409eff; text-decoration: none; &:hover { text-decoration: underline; } }
}
</style>
