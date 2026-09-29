<template>
  <div class="page-container">
    <el-row :gutter="20" style="margin-bottom:20px">
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#667eea,#764ba2)">
          <el-icon :size="28"><FolderOpened /></el-icon>
          <div class="num">{{ stats.albumCount || 0 }}</div>
          <div class="label">我的相册</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#4facfe,#00f2fe)">
          <el-icon :size="28"><Picture /></el-icon>
          <div class="num">{{ stats.photoCount || 0 }}</div>
          <div class="label">我的照片</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#fa709a,#fee140)">
          <el-icon :size="28"><Star /></el-icon>
          <div class="num">{{ stats.favoriteCount || 0 }}</div>
          <div class="label">我的收藏</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card" style="background:linear-gradient(135deg,#f093fb,#f5576c)">
          <el-icon :size="28"><Pointer /></el-icon>
          <div class="num">{{ stats.totalLikes || 0 }}</div>
          <div class="label">获赞总数</div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="14">
        <div class="chart-box">
          <h3>我的近7天上传趋势</h3>
          <div ref="trendChart" style="height:320px"></div>
        </div>
      </el-col>
      <el-col :span="10">
        <div class="chart-box">
          <h3>我的相册分类分布</h3>
          <div ref="pieChart" style="height:320px"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { userStatistic } from '@/api'

const stats = ref({})
const trendChart = ref()
const pieChart = ref()

const loadData = async () => {
  const res = await userStatistic()
  stats.value = res.data
  await nextTick()
  renderTrend(res.data.photoTrend || [])
  renderPie(res.data.categoryRatio || [])
}

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
        { offset: 0, color: 'rgba(102,126,234,0.3)' }, { offset: 1, color: 'rgba(102,126,234,0.02)' }
      ])},
      itemStyle: { color: '#667eea' }, lineStyle: { width: 3 }
    }]
  })
}

const renderPie = (data) => {
  const chart = echarts.init(pieChart.value)
  chart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie', radius: ['40%', '70%'], center: ['50%', '45%'],
      data: data.filter(d => d.value > 0).map(d => ({ name: d.name, value: d.value })),
      label: { formatter: '{b}\n{d}%' }
    }]
  })
}

onMounted(loadData)
</script>
