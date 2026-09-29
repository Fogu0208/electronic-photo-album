import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

/**
 * Axios请求封装
 */
const request = axios.create({
  baseURL: '/api',
  timeout: 30000
})

/** 请求拦截器 - 添加Token */
request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = 'Bearer ' + token
  }
  return config
})

/** 响应拦截器 - 统一处理 */
request.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code === 200) {
      return res
    }
    if (res.code === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('userInfo')
      router.push('/login')
      ElMessage.error(res.msg || '登录已过期')
      return Promise.reject(res)
    }
    ElMessage.error(res.msg || '操作失败')
    return Promise.reject(res)
  },
  error => {
    ElMessage.error('网络异常')
    return Promise.reject(error)
  }
)

export default request
