<template>
  <div class="app-container">
    <!-- 1. 左侧功能导航栏 (保持不变) -->
    <aside class="left-sidebar">
      <div class="brand">
        <span class="logo-icon">
          <div class="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center overflow-hidden">
             <img src="/cb19e5f2778cc441e6ba9b7ad38150d2.png" alt="Logo" class="w-full h-full object-contain" />
          </div>
        </span>
        <span class="logo-text">DePaper</span>
      </div>
      
      <nav class="nav-menu">
        <button class="nav-btn primary" @click="handleRefreshButtonClick">
          <span class="icon">🔄</span> 刷新内容
        </button>
        <button class="nav-btn" @click="handleQuestionGenerateClick">
          <span class="icon">✨</span> 问题生成
        </button>
        <button class="nav-btn" @click="handleBackToHome">
          <span class="icon">🏠</span> 回到首页
        </button>
        
        <div class="divider"></div>
        
        <button class="nav-btn" @click="handleProcessNewsAndGenerateQuestions">
          <span class="icon">📰</span> 新闻问题
        </button>
        <button class="nav-btn" @click="handleActionButtonClick">
          <span class="icon">🧠</span> 智能推荐
        </button>
        <button class="nav-btn" @click="handleStudyReportClick">
          <span class="icon">📊</span> 学习报告
        </button>
      </nav>

      <div class="bottom-status">
        <span class="status-dot"></span> 在线
      </div>
    </aside>

    <!-- 2. 中间主要内容区 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 顶部标题区 -->
        <header class="content-header">
          <div class="header-left">
            <div class="topic-tag">当前研究课题：基于深度学习的图像识别优化</div>
            <h1 class="main-title">个人研读总结报告</h1>
          </div>
          <div class="header-right">
             <span class="report-date">生成时间：2024-05-28</span>
          </div>
        </header>

        <!-- 学习报告仪表盘 -->
        <div class="dashboard-container">
          
          <!-- 第一行：关键指标卡片 -->
          <div class="stats-row">
            <div class="stat-card">
              <div class="stat-icon bg-blue-100 text-blue-600">📚</div>
              <div class="stat-info">
                <span class="stat-value">{{ studyData.paperCount }}</span>
                <span class="stat-label">已读论文篇数</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon bg-orange-100 text-orange-600">⏱️</div>
              <div class="stat-info">
                <span class="stat-value">{{ studyData.studyHours }}h</span>
                <span class="stat-label">累计研读时长</span>
              </div>
            </div>

            <!-- 修改处：改为已完成课题数 -->
            <div class="stat-card">
              <div class="stat-icon bg-purple-100 text-purple-600">🏆</div>
              <div class="stat-info">
                <span class="stat-value">{{ studyData.completedProjects }}</span>
                <span class="stat-label">已完成课题数</span>
              </div>
            </div>
          </div>

          <!-- 第二行：图表与知识点展示 -->
          <div class="analysis-row">
            <!-- 左侧：领域分布饼状图 -->
            <div class="chart-card">
              <h3>论文领域分布</h3>
              <div class="chart-content">
                <div class="pie-chart-wrapper">
                  <div class="pie-chart" :style="pieChartStyle"></div>
                  <div class="pie-legend">
                    <div v-for="(item, index) in studyData.fields" :key="index" class="legend-item">
                      <span class="dot" :style="{ backgroundColor: item.color }"></span>
                      <span class="name">{{ item.name }}</span>
                      <span class="percent">{{ item.percent }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 右侧：修改为“已掌握的知识点” -->
            <div class="knowledge-card">
              <h3>🧠 从论文中习得的知识</h3>
              <div class="knowledge-list">
                <div v-for="(item, index) in studyData.learnedKnowledge" :key="index" class="knowledge-item">
                  <div class="k-header">
                    <span class="k-title">{{ item.point }}</span>
                    <span class="k-tag">{{ item.category }}</span>
                  </div>
                  <p class="k-desc">{{ item.description }}</p>
                  <div class="k-source">
                    <span class="source-icon">📄</span> 来源: {{ item.source }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 第三行：AI 建议 -->
          <div class="ai-suggestion-card">
            <div class="ai-header">
              <span class="icon">🤖</span>
              <h3>AI 助手学习建议</h3>
            </div>
            <div class="ai-content">
              <p>{{ studyData.aiSuggestion }}</p>
              <div class="action-tags">
                <span class="tag">建议阅读：Transformers综述</span>
                <span class="tag">下一步：复现实验代码</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 模拟数据
const studyData = ref({
  paperCount: 12,
  studyHours: 28.5,
  completedProjects: 4, // 修改：已完成课题数
  fields: [
    { name: '计算机视觉', percent: 45, color: '#4f46e5' },
    { name: '自然语言处理', percent: 30, color: '#06b6d4' },
    { name: '强化学习', percent: 15, color: '#f59e0b' },
    { name: '其他', percent: 10, color: '#9ca3af' }
  ],
  // 修改：学习到的知识点数据
  learnedKnowledge: [
    { 
      point: '残差网络 (ResNet) 的退化问题解决', 
      category: '模型架构',
      description: '理解了深层网络中梯度消失的原因，以及ResNet通过引入恒等映射（Identity Mapping）来解决网络退化问题的机制。',
      source: 'Deep Residual Learning for Image Recognition'
    },
    { 
      point: '自注意力机制 (Self-Attention)', 
      category: '核心算法',
      description: '掌握了Query、Key、Value矩阵的计算过程，以及Multi-head Attention如何让模型关注输入序列的不同位置。',
      source: 'Attention Is All You Need'
    },
    { 
      point: '对比学习中的正负样本构造', 
      category: '训练策略',
      description: '学习了在无监督学习中，如何通过数据增强构造正样本对，以及Batch内负样本采样对模型效果的影响。',
      source: 'A Simple Framework for Contrastive Learning'
    }
  ],
  aiSuggestion: '您在“模型架构”方面的知识储备已经非常扎实，特别是在CNN变体方面。建议接下来的阅读重心可以稍微向“模型轻量化”或“端侧部署”转移，这将有助于您将理论知识转化为实际落地的能力。'
})

// 计算属性：生成饼图样式
const pieChartStyle = computed(() => {
  let gradientStr = ''
  let currentPercent = 0
  studyData.value.fields.forEach((field, index) => {
    const start = currentPercent
    const end = currentPercent + field.percent
    gradientStr += `${field.color} ${start}% ${end}%, `
    currentPercent = end
  })
  gradientStr = gradientStr.slice(0, -2)
  return {
    background: `conic-gradient(${gradientStr})`
  }
})

// 导航逻辑
const handleRefreshButtonClick = () => console.log('刷新内容')
const handleQuestionGenerateClick = () => router.push('/question')
const handleBackToHome = () => router.push('/chat')
const handleProcessNewsAndGenerateQuestions = () => console.log('新闻问题')
const handleActionButtonClick = () => console.log('智能推荐')
const handleStudyReportClick = () => console.log('学习报告')
</script>

<style scoped>
/* --- 全局与侧边栏样式 (保持不变) --- */
.app-container {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #f4f6f9;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  color: #333;
  overflow: hidden;
}

.left-sidebar {
  width: 240px;
  background-color: #ffffff;
  border-right: 1px solid #e1e4e8;
  display: flex;
  flex-direction: column;
  padding: 20px;
  flex-shrink: 0;
  box-shadow: 2px 0 10px rgba(0,0,0,0.02);
  z-index: 10;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 700;
  color: #4f46e5;
  margin-bottom: 40px;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  background: transparent;
  color: #555;
  font-size: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.nav-btn:hover {
  background-color: #f3f4f6;
  color: #4f46e5;
}

.nav-btn.primary {
  background-color: #4f46e5;
  color: white;
  box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);
}

.nav-btn.primary:hover {
  background-color: #4338ca;
}

.divider {
  height: 1px;
  background-color: #e5e7eb;
  margin: 10px 0;
}

.bottom-status {
  margin-top: auto;
  font-size: 12px;
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  background-color: #10b981;
  border-radius: 50%;
}

/* --- 中间内容区样式 --- */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background-color: #f8fafc;
}

.content-wrapper {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.topic-tag {
  font-size: 0.85rem;
  color: #6366f1;
  font-weight: 600;
  background-color: #e0e7ff;
  padding: 4px 12px;
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 8px;
}

.main-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.report-date {
  font-size: 0.9rem;
  color: #6b7280;
}

/* 仪表盘容器 */
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 第一行：统计卡片 */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
}

/* 第二行：分析区布局 */
.analysis-row {
  display: grid;
  grid-template-columns: 1fr 1.8fr; /* 调整右侧宽度占比更大，适合展示列表 */
  gap: 1.5rem;
}

.chart-card, .knowledge-card, .ai-suggestion-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.chart-card h3, .knowledge-card h3, .ai-suggestion-card h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1.2rem;
}

/* 饼图样式 */
.chart-content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem 0;
}

.pie-chart-wrapper {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.pie-chart {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  position: relative;
  flex-shrink: 0;
}

.pie-chart::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
}

.pie-legend {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.legend-item .dot {
  width: 10px;
  height: 10px;
  border-radius: 2px;
}

/* 知识点卡片样式 (新) */
.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

/* 滚动条美化 */
.knowledge-list::-webkit-scrollbar {
  width: 4px;
}
.knowledge-list::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 4px;
}

.knowledge-item {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 1rem;
  border-left: 4px solid #6366f1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.k-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.k-title {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.95rem;
}

.k-tag {
  font-size: 0.75rem;
  background-color: #e0e7ff;
  color: #4f46e5;
  padding: 2px 8px;
  border-radius: 4px;
}

.k-desc {
  font-size: 0.875rem;
  color: #4b5563;
  line-height: 1.5;
  margin: 0;
}

.k-source {
  font-size: 0.75rem;
  color: #9ca3af;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
}

/* 辅助颜色类 */
.bg-blue-100 { background-color: #dbeafe; }
.text-blue-600 { color: #2563eb; }
.bg-orange-100 { background-color: #ffedd5; }
.text-orange-600 { color: #ea580c; }
.bg-purple-100 { background-color: #f3e8ff; } /* 新增紫色背景 */
.text-purple-600 { color: #9333ea; } /* 新增紫色文字 */

/* AI 建议卡片 */
.ai-suggestion-card {
  background: linear-gradient(to right, #ffffff, #f5f3ff);
  border: 1px solid #e0e7ff;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.ai-header .icon {
  font-size: 1.5rem;
}

.ai-content p {
  color: #4b5563;
  line-height: 1.6;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.action-tags {
  display: flex;
  gap: 0.75rem;
}

.tag {
  background-color: #4f46e5;
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
}
</style>