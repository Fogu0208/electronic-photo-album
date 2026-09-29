<template>
  <div class="page-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20" style="margin-bottom:20px">
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#667eea,#764ba2)">
          <el-icon :size="28"><User /></el-icon>
          <div class="num">{{ stats.userCount || 0 }}</div>
          <div class="label">用户总数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#f093fb,#f5576c)">
          <el-icon :size="28"><FolderOpened /></el-icon>
          <div class="num">{{ stats.albumCount || 0 }}</div>
          <div class="label">相册总数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#4facfe,#00f2fe)">
          <el-icon :size="28"><Picture /></el-icon>
          <div class="num">{{ stats.photoCount || 0 }}</div>
          <div class="label">照片总数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#fa709a,#fee140)">
          <el-icon :size="28"><ChatDotRound /></el-icon>
          <div class="num">{{ stats.pendingCommentCount || 0 }}</div>
          <div class="label">待审核评论</div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="14">
        <div class="chart-box">
          <h3>近7天照片上传趋势</h3>
          <div ref="trendChart" style="height:320px"></div>
        </div>
      </el-col>
      <el-col :span="10">
        <div class="chart-box">
          <h3>相册分类占比</h3>
          <div ref="pieChart" style="height:320px"></div>
        </div>
      </el-col>
    </el-row>

    <div class="chart-box">
      <h3>照片数 Top5 用户</h3>
      <div ref="barChart" style="height:300px"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { adminStatistic } from '@/api'

const stats = ref({})
const trendChart = ref()
const pieChart = ref()
const barChart = ref()

/** 加载统计数据 */
const loadData = async () => {
  const res = await adminStatistic()
  stats.value = res.data
  await nextTick()
  renderTrend(res.data.photoTrend || [])
  renderPie(res.data.categoryRatio || [])
  renderBar(res.data.topUsers || [])
}

/** 渲染折线图 */
const renderTrend = (data) => {
  const chart = echarts.init(trendChart.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    xAxis: { type: 'category', data: data.map(d => (d.date || '').substring(0, 10)) },
    yAxis: { type: 'value', minInterval: 1 },
    series: [{
      type: 'line', smooth: true, data: data.map(d => d.count),
      areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(64,158,255,0.3)' }, { offset: 1, color: 'rgba(64,158,255,0.02)' }
      ])},
      itemStyle: { color: '#409eff' }, lineStyle: { width: 3 }
    }]
  })
}

/** 渲染饼图 */
const renderPie = (data) => {
  const chart = echarts.init(pieChart.value)
  chart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie', radius: ['40%', '70%'], center: ['50%', '45%'],
      data: data.map(d => ({ name: d.name, value: d.value })),
      emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.2)' } },
      label: { formatter: '{b}\n{d}%' }
    }]
  })
}

/** 渲染柱状图 */
const renderBar = (data) => {
  const chart = echarts.init(barChart.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 80, right: 20, top: 20, bottom: 30 },
    xAxis: { type: 'value', minInterval: 1 },
    yAxis: { type: 'category', data: data.map(d => d.name).reverse() },
    series: [{
      type: 'bar', data: data.map(d => d.value).reverse(),
      itemStyle: { color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
        { offset: 0, color: '#667eea' }, { offset: 1, color: '#764ba2' }
      ]), borderRadius: [0, 6, 6, 0] },
      barWidth: 20
    }]
  })
}

onMounted(loadData)
</script>
