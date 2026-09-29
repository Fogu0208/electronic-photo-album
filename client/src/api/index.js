import request from './request'

/** 登录 */
export const login = (data) => request.post('/auth/login', data)
/** 注册 */
export const register = (data) => request.post('/auth/register', data)
/** 获取当前用户信息 */
export const getUserInfo = () => request.get('/auth/info')
/** 修改密码 */
export const updatePassword = (data) => request.put('/auth/password', data)
/** 修改管理员资料 */
export const updateAdminProfile = (data) => request.put('/auth/profile/admin', data)
/** 修改用户资料 */
export const updateUserProfile = (data) => request.put('/auth/profile/user', data)

/** 用户分页 */
export const pageUser = (params) => request.get('/user/page', { params })
/** 新增用户 */
export const addUser = (data) => request.post('/user', data)
/** 修改用户 */
export const updateUser = (data) => request.put('/user', data)
/** 删除用户 */
export const deleteUser = (id) => request.delete(`/user/${id}`)

/** 分类分页 */
export const pageCategory = (params) => request.get('/category/page', { params })
/** 分类列表 */
export const listCategory = () => request.get('/category/list')
/** 新增分类 */
export const addCategory = (data) => request.post('/category', data)
/** 修改分类 */
export const updateCategory = (data) => request.put('/category', data)
/** 删除分类 */
export const deleteCategory = (id) => request.delete(`/category/${id}`)

/** 相册分页 */
export const pageAlbum = (params) => request.get('/album/page', { params })
/** 相册详情 */
export const getAlbum = (id) => request.get(`/album/${id}`)
/** 公开相册 */
export const pagePublicAlbum = (params) => request.get('/album/public/page', { params })
/** 新增相册 */
export const addAlbum = (data) => request.post('/album', data)
/** 修改相册 */
export const updateAlbum = (data) => request.put('/album', data)
/** 删除相册 */
export const deleteAlbum = (id) => request.delete(`/album/${id}`)

/** 照片分页 */
export const pagePhoto = (params) => request.get('/photo/page', { params })
/** 新增照片 */
export const addPhoto = (data) => request.post('/photo', data)
/** 修改照片 */
export const updatePhoto = (data) => request.put('/photo', data)
/** 删除照片 */
export const deletePhoto = (id) => request.delete(`/photo/${id}`)

/** 评论分页 */
export const pageComment = (params) => request.get('/comment/page', { params })
/** 新增评论 */
export const addComment = (data) => request.post('/comment', data)
/** 审核评论 */
export const auditComment = (data) => request.put('/comment/audit', data)
/** 删除评论 */
export const deleteComment = (id) => request.delete(`/comment/${id}`)

/** 点赞 */
export const toggleLike = (photoId) => request.post(`/interact/like/${photoId}`)
/** 收藏 */
export const toggleFavorite = (photoId) => request.post(`/interact/favorite/${photoId}`)
/** 我的收藏 */
export const pageFavorite = (params) => request.get('/interact/favorite/page', { params })

/** 公告分页 */
export const pageNotice = (params) => request.get('/notice/page', { params })
/** 公告列表 */
export const listNotice = () => request.get('/notice/list')
/** 新增公告 */
export const addNotice = (data) => request.post('/notice', data)
/** 修改公告 */
export const updateNotice = (data) => request.put('/notice', data)
/** 删除公告 */
export const deleteNotice = (id) => request.delete(`/notice/${id}`)

/** 日志分页 */
export const pageLog = (params) => request.get('/log/page', { params })

/** 管理员统计 */
export const adminStatistic = () => request.get('/statistic/admin')
/** 用户统计 */
export const userStatistic = () => request.get('/statistic/user')

/** 文件上传 */
export const uploadFile = (file, type = 'photo') => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('type', type)
  return request.post('/file/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

/** 格式化日期 yyyy-MM-dd */
export const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.substring(0, 10)
}

/** 格式化日期时间 yyyy-MM-dd HH:mm:ss */
export const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.substring(0, 19).replace('T', ' ')
}
