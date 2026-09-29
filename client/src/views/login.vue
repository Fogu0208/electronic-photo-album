<template>
  <div class="login-page">
    <!-- 左侧品牌展示区 -->
    <div class="login-brand">
      <div class="brand-bg">
        <!-- 动态渐变层 -->
        <div class="gradient-flow"></div>
        <!-- 浮动光斑 -->
        <div class="light-orbs">
          <span v-for="n in 5" :key="n" class="orb" :class="`orb-${n}`"></span>
        </div>
        <!-- 漂浮粒子 -->
        <div class="particles">
          <span v-for="n in 20" :key="n" class="particle" :style="particleStyle(n)"></span>
        </div>
        <!-- 照片网格 -->
        <div class="photo-mosaic">
          <div v-for="i in 6" :key="i" class="mosaic-item" :class="`item-${i}`">
            <el-icon :size="28"><Picture /></el-icon>
          </div>
        </div>
        <div class="brand-overlay"></div>
      </div>
      <div class="brand-content">
        <div class="brand-logo">
          <div class="logo-ring"></div>
          <el-icon :size="36"><Camera /></el-icon>
        </div>
        <h1 class="brand-title">电子相册管理系统</h1>
        <p class="brand-desc">珍藏每一刻美好，管理您的数字影像世界</p>
        <ul class="brand-features">
          <li v-for="(feat, idx) in features" :key="idx" :style="{ animationDelay: `${0.6 + idx * 0.15}s` }">
            <el-icon><Check /></el-icon> {{ feat }}
          </li>
        </ul>
      </div>
    </div>

    <!-- 右侧登录表单区 -->
    <div class="login-form-wrap">
      <!-- 右侧背景装饰 -->
      <div class="form-bg-deco">
        <span class="deco-circle deco-1"></span>
        <span class="deco-circle deco-2"></span>
      </div>

      <div class="login-form-box">
        <div class="form-glow-border"></div>
        <div class="form-inner">
          <div class="form-header">
            <h2>欢迎回来</h2>
            <p>请登录您的账号以继续</p>
          </div>

          <!-- 角色切换 -->
          <div class="role-tabs">
            <div class="role-slider" :class="{ 'slide-right': form.role === 'ADMIN' }"></div>
            <button
              type="button"
              class="role-tab"
              :class="{ active: form.role === 'USER' }"
              @click="form.role = 'USER'"
            >
              <el-icon><User /></el-icon>
              普通用户
            </button>
            <button
              type="button"
              class="role-tab"
              :class="{ active: form.role === 'ADMIN' }"
              @click="form.role = 'ADMIN'"
            >
              <el-icon><Setting /></el-icon>
              管理员
            </button>
          </div>

          <el-form ref="formRef" :model="form" :rules="rules" size="large" class="login-form">
            <el-form-item prop="username">
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                prefix-icon="User"
                class="custom-input"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                prefix-icon="Lock"
                show-password
                class="custom-input"
                @keyup.enter="handleLogin"
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                :loading="loading"
                class="login-btn"
                @click="handleLogin"
              >
                <span class="btn-text">登 录</span>
                <span class="btn-shine"></span>
              </el-button>
            </el-form-item>
          </el-form>

          <div class="login-footer" v-if="form.role === 'USER'">
            还没有账号？
            <router-link to="/register">立即注册</router-link>
          </div>
        </div>
      </div>

      <p class="copyright">© 2026 电子相册管理系统</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { login } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref()
const loading = ref(false)

const form = reactive({ username: '', password: '', role: 'USER' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

/** 功能亮点列表 */
const features = ['智能相册分类管理', '高清照片云端存储', '安全可靠的权限控制']

/** 生成粒子随机样式 */
const particleStyle = (n) => {
  const left = ((n * 37 + 13) % 100)
  const size = 2 + (n % 4)
  const duration = 8 + (n % 12)
  const delay = (n * 0.7) % 10
  return {
    left: `${left}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDuration: `${duration}s`,
    animationDelay: `${delay}s`
  }
}

/** 登录处理 */
const handleLogin = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    const res = await login(form)
    userStore.setLogin(res.data)
    ElMessage.success('登录成功')
    router.push(form.role === 'ADMIN' ? '/admin/home' : '/user/home')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-page {
  width: 100%;
  height: 100vh;
  display: flex;
  overflow: hidden;
}

/* ===== 左侧品牌区 ===== */
.login-brand {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
}

.brand-bg {
  position: absolute;
  inset: 0;
  background: #0a1628;
  overflow: hidden;
}

/* 动态渐变流动 */
.gradient-flow {
  position: absolute;
  inset: -50%;
  background: conic-gradient(
    from 0deg at 50% 50%,
    #0f2027, #1a3a5c, #2c5364, #1e5799, #409eff,
    #7b68ee, #2c5364, #203a43, #0f2027
  );
  animation: gradientRotate 12s linear infinite;
  opacity: 0.85;
}

@keyframes gradientRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 浮动光斑 */
.light-orbs {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;

  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(40px);
    animation: orbFloat 8s ease-in-out infinite;

    &.orb-1 {
      width: 200px; height: 200px;
      background: rgba(64, 158, 255, 0.35);
      top: 10%; left: 15%;
      animation-duration: 10s;
    }
    &.orb-2 {
      width: 160px; height: 160px;
      background: rgba(123, 104, 238, 0.3);
      top: 60%; left: 50%;
      animation-duration: 12s;
      animation-delay: -3s;
    }
    &.orb-3 {
      width: 120px; height: 120px;
      background: rgba(103, 194, 58, 0.2);
      top: 30%; right: 10%;
      animation-duration: 9s;
      animation-delay: -5s;
    }
    &.orb-4 {
      width: 180px; height: 180px;
      background: rgba(230, 162, 60, 0.2);
      bottom: 10%; left: 30%;
      animation-duration: 11s;
      animation-delay: -2s;
    }
    &.orb-5 {
      width: 100px; height: 100px;
      background: rgba(245, 108, 108, 0.25);
      top: 5%; right: 30%;
      animation-duration: 7s;
      animation-delay: -4s;
    }
  }
}

@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -20px) scale(1.1); }
  50% { transform: translate(-20px, 30px) scale(0.95); }
  75% { transform: translate(15px, 15px) scale(1.05); }
}

/* 漂浮粒子 */
.particles {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;

  .particle {
    position: absolute;
    bottom: -10px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    animation: particleRise linear infinite;
  }
}

@keyframes particleRise {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% { opacity: 1; }
  90% { opacity: 0.6; }
  100% {
    transform: translateY(-100vh) translateX(30px);
    opacity: 0;
  }
}

/* 照片网格 */
.photo-mosaic {
  position: absolute;
  inset: 0;
  z-index: 3;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 12px;
  padding: 40px;
  opacity: 0.12;

  .mosaic-item {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.15);
    animation: mosaicFloat 6s ease-in-out infinite;

    &.item-1 { animation-delay: 0s; transform: rotate(-3deg); }
    &.item-2 { animation-delay: -1s; transform: rotate(2deg); }
    &.item-3 { animation-delay: -2s; transform: rotate(-1deg); }
    &.item-4 { animation-delay: -3s; transform: rotate(3deg); }
    &.item-5 { animation-delay: -4s; transform: rotate(-2deg); }
    &.item-6 { animation-delay: -5s; transform: rotate(1deg); }
  }
}

@keyframes mosaicFloat {
  0%, 100% { transform: translateY(0) rotate(var(--r, 0deg)); }
  50% { transform: translateY(-12px) rotate(calc(var(--r, 0deg) + 2deg)); }
}

.brand-overlay {
  position: absolute;
  inset: 0;
  z-index: 4;
  background: radial-gradient(circle at 30% 70%, rgba(64, 158, 255, 0.2) 0%, transparent 60%);
  animation: overlayPulse 6s ease-in-out infinite;
}

@keyframes overlayPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

/* 品牌内容 */
.brand-content {
  position: relative;
  z-index: 5;
  color: #fff;
  padding: 60px;
  max-width: 480px;
  animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.brand-logo {
  position: relative;
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #409eff, #66b1ff);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 28px;
  box-shadow: 0 8px 32px rgba(64, 158, 255, 0.45);
  animation: logoPulse 3s ease-in-out infinite;

  .logo-ring {
    position: absolute;
    inset: -6px;
    border-radius: 20px;
    border: 2px solid rgba(64, 158, 255, 0.4);
    animation: ringExpand 3s ease-in-out infinite;
  }
}

@keyframes logoPulse {
  0%, 100% { box-shadow: 0 8px 32px rgba(64, 158, 255, 0.45); }
  50% { box-shadow: 0 8px 48px rgba(64, 158, 255, 0.7), 0 0 60px rgba(64, 158, 255, 0.2); }
}

@keyframes ringExpand {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.15); opacity: 0; }
}

.brand-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 12px;
  line-height: 1.3;
  background: linear-gradient(90deg, #fff 0%, #a8d8ff 40%, #fff 80%, #c4b5fd 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: textShimmer 4s linear infinite;
}

@keyframes textShimmer {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}

.brand-desc {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.6;
  margin-bottom: 36px;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.brand-features {
  list-style: none;
  padding: 0;

  li {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    color: rgba(255, 255, 255, 0.85);
    margin-bottom: 14px;
    animation: fadeInUp 0.6s ease-out both;

    .el-icon {
      color: #67c23a;
      font-size: 18px;
      animation: checkPop 0.5s ease-out both;
    }
  }
}

@keyframes checkPop {
  0% { transform: scale(0); }
  70% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

/* ===== 右侧表单区 ===== */
.login-form-wrap {
  width: 480px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(160deg, #f0f4ff 0%, #f8fafc 50%, #eef2ff 100%);
  padding: 40px;
  position: relative;
  overflow: hidden;
}

/* 右侧装饰圆 */
.form-bg-deco {
  position: absolute;
  inset: 0;
  pointer-events: none;

  .deco-circle {
    position: absolute;
    border-radius: 50%;
    animation: decoDrift 15s ease-in-out infinite;

    &.deco-1 {
      width: 300px; height: 300px;
      background: radial-gradient(circle, rgba(64, 158, 255, 0.08) 0%, transparent 70%);
      top: -80px; right: -80px;
    }
    &.deco-2 {
      width: 250px; height: 250px;
      background: radial-gradient(circle, rgba(123, 104, 238, 0.06) 0%, transparent 70%);
      bottom: -60px; left: -60px;
      animation-delay: -7s;
    }
  }
}

@keyframes decoDrift {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(20px, -15px); }
}

.login-form-box {
  position: relative;
  width: 100%;
  max-width: 380px;
  border-radius: 20px;
  padding: 2px;
  animation: slideInRight 0.8s ease-out;
  z-index: 1;
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}

/* 表单流光边框 */
.form-glow-border {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  background: conic-gradient(
    from 0deg,
    #409eff, #7b68ee, #67c23a, #e6a23c, #f56c6c, #409eff
  );
  animation: borderSpin 4s linear infinite;
  z-index: 0;
}

@keyframes borderSpin {
  0% { filter: hue-rotate(0deg); }
  100% { filter: hue-rotate(360deg); }
}

.form-inner {
  position: relative;
  background: #fff;
  border-radius: 18px;
  padding: 44px 36px;
  z-index: 1;
}

.form-header {
  margin-bottom: 32px;
  animation: fadeInUp 0.6s ease-out 0.3s both;

  h2 {
    font-size: 26px;
    color: #1a1a2e;
    font-weight: 700;
    margin-bottom: 8px;
  }

  p {
    font-size: 14px;
    color: #909399;
  }
}

/* 角色切换 - 滑动指示器 */
.role-tabs {
  position: relative;
  display: flex;
  background: #f0f2f5;
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 28px;
}

.role-slider {
  position: absolute;
  top: 4px;
  left: 4px;
  width: calc(50% - 4px);
  height: calc(100% - 8px);
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.15);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 0;

  &.slide-right {
    transform: translateX(100%);
  }
}

.role-tab {
  flex: 1;
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 0;
  border: none;
  background: transparent;
  border-radius: 10px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  transition: color 0.3s;

  &:hover { color: #409eff; }

  &.active {
    color: #409eff;
    font-weight: 600;
  }
}

.login-form {
  :deep(.el-form-item) {
    margin-bottom: 22px;
    animation: fadeInUp 0.5s ease-out both;

    &:nth-child(1) { animation-delay: 0.4s; }
    &:nth-child(2) { animation-delay: 0.5s; }
    &:nth-child(3) { animation-delay: 0.6s; }
  }

  :deep(.el-input__wrapper) {
    border-radius: 10px;
    padding: 4px 12px;
    box-shadow: 0 0 0 1px #e4e7ed inset;
    transition: box-shadow 0.3s, transform 0.2s;

    &:hover {
      box-shadow: 0 0 0 1px #c0c4cc inset;
      transform: translateY(-1px);
    }

    &.is-focus {
      box-shadow: 0 0 0 1px #409eff inset, 0 0 12px rgba(64, 158, 255, 0.15);
      transform: translateY(-1px);
    }
  }
}

.login-btn {
  position: relative;
  width: 100%;
  height: 44px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  background: linear-gradient(135deg, #409eff, #337ecc, #409eff);
  background-size: 200% 100%;
  border: none;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  animation: btnGradient 3s ease infinite;

  .btn-text {
    position: relative;
    z-index: 1;
  }

  .btn-shine {
    position: absolute;
    top: 0;
    left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: btnShine 3s ease-in-out infinite;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(64, 158, 255, 0.45);
  }

  &:active {
    transform: translateY(0);
  }
}

@keyframes btnGradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes btnShine {
  0% { left: -100%; }
  50%, 100% { left: 150%; }
}

.login-footer {
  text-align: center;
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
  animation: fadeInUp 0.5s ease-out 0.7s both;

  a {
    color: #409eff;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;

    &:hover {
      color: #337ecc;
      text-decoration: underline;
    }
  }
}

.copyright {
  position: absolute;
  bottom: 24px;
  font-size: 12px;
  color: #c0c4cc;
  z-index: 1;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
  .login-page {
    flex-direction: column;
  }

  .login-brand {
    flex: none;
    height: 220px;
  }

  .brand-content {
    padding: 30px;
    text-align: center;

    h1 { font-size: 22px; }

    .brand-desc,
    .brand-features { display: none; }

    .brand-logo {
      margin: 0 auto 12px;
      width: 48px;
      height: 48px;
    }
  }

  .particles .particle:nth-child(n+11) { display: none; }

  .login-form-wrap {
    width: 100%;
    flex: 1;
    padding: 24px;
  }
}

/* 减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
