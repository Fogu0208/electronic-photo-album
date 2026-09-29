import { defineStore } from 'pinia'
import { ref } from 'vue'

/**
 * 用户状态管理
 */
export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const role = ref(localStorage.getItem('role') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  /** 设置登录信息 */
  function setLogin(data) {
    token.value = data.token
    role.value = data.role
    userInfo.value = data.userInfo
    localStorage.setItem('token', data.token)
    localStorage.setItem('role', data.role)
    localStorage.setItem('userInfo', JSON.stringify(data.userInfo))
  }

  /** 退出登录 */
  function logout() {
    token.value = ''
    role.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    localStorage.removeItem('userInfo')
  }

  /** 更新用户信息 */
  function updateInfo(info) {
    userInfo.value = { ...userInfo.value, ...info }
    localStorage.setItem('userInfo', JSON.stringify(userInfo.value))
  }

  return { token, role, userInfo, setLogin, logout, updateInfo }
})
