import { createRouter, createWebHistory } from 'vue-router'

/**
 * 路由配置
 */
const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/login.vue'), meta: { title: '登录' } },
  { path: '/register', name: 'Register', component: () => import('@/views/register.vue'), meta: { title: '注册' } },
  {
    path: '/admin',
    component: () => import('@/layout/index.vue'),
    meta: { role: 'ADMIN' },
    redirect: '/admin/home',
    children: [
      { path: 'home', name: 'AdminHome', component: () => import('@/views/admin/home.vue'), meta: { title: '首页', icon: 'HomeFilled' } },
      { path: 'user', name: 'AdminUser', component: () => import('@/views/admin/user.vue'), meta: { title: '用户管理', icon: 'User' } },
      { path: 'category', name: 'AdminCategory', component: () => import('@/views/admin/category.vue'), meta: { title: '分类管理', icon: 'Menu' } },
      { path: 'album', name: 'AdminAlbum', component: () => import('@/views/admin/album.vue'), meta: { title: '相册管理', icon: 'PictureFilled' } },
      { path: 'photo', name: 'AdminPhoto', component: () => import('@/views/admin/photo.vue'), meta: { title: '照片管理', icon: 'Camera' } },
      { path: 'comment', name: 'AdminComment', component: () => import('@/views/admin/comment.vue'), meta: { title: '评论审核', icon: 'ChatDotRound' } },
      { path: 'notice', name: 'AdminNotice', component: () => import('@/views/admin/notice.vue'), meta: { title: '公告管理', icon: 'Bell' } },
      { path: 'log', name: 'AdminLog', component: () => import('@/views/admin/log.vue'), meta: { title: '操作日志', icon: 'Document' } },
      { path: 'profile', name: 'AdminProfile', component: () => import('@/views/admin/profile.vue'), meta: { title: '个人中心', icon: 'Setting', hidden: true } }
    ]
  },
  {
    path: '/user',
    component: () => import('@/layout/index.vue'),
    meta: { role: 'USER' },
    redirect: '/user/home',
    children: [
      { path: 'home', name: 'UserHome', component: () => import('@/views/user/home.vue'), meta: { title: '首页', icon: 'HomeFilled' } },
      { path: 'plaza', name: 'UserPlaza', component: () => import('@/views/user/plaza.vue'), meta: { title: '相册广场', icon: 'Grid' } },
      { path: 'myAlbum', name: 'UserMyAlbum', component: () => import('@/views/user/myAlbum.vue'), meta: { title: '我的相册', icon: 'FolderOpened' } },
      { path: 'albumDetail/:id', name: 'UserAlbumDetail', component: () => import('@/views/user/albumDetail.vue'), meta: { title: '相册详情', icon: 'Picture', hidden: true } },
      { path: 'favorite', name: 'UserFavorite', component: () => import('@/views/user/favorite.vue'), meta: { title: '我的收藏', icon: 'Star' } },
      { path: 'notice', name: 'UserNotice', component: () => import('@/views/user/notice.vue'), meta: { title: '系统公告', icon: 'Bell' } },
      { path: 'profile', name: 'UserProfile', component: () => import('@/views/user/profile.vue'), meta: { title: '个人中心', icon: 'Setting', hidden: true } }
    ]
  },
  { path: '/', redirect: '/login' },
  { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/** 路由守卫 */
router.beforeEach((to, from, next) => {
  document.title = (to.meta.title ? to.meta.title + ' - ' : '') + 'Python电子相册管理系统'
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  if (to.path === '/login' || to.path === '/register') {
    next()
    return
  }
  if (!token) {
    next('/login')
    return
  }
  const requiredRole = to.matched.find(r => r.meta.role)?.meta.role
  if (requiredRole && requiredRole !== role) {
    next(role === 'ADMIN' ? '/admin/home' : '/user/home')
    return
  }
  next()
})

export default router
