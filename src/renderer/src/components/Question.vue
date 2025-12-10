<template>
  <div class="app-container">
    <!-- 全局背景装饰 -->
    <div class="bg-decoration-circle circle-1"></div>
    <div class="bg-decoration-circle circle-2"></div>

    <!-- 加载状态覆盖层 -->
    <transition name="fade">
      <div v-if="loadingStatus" class="loading-overlay">
        <div class="loading-card">
          <div class="loading-spinner"></div>
          <div class="loading-info">
            <span class="loading-title">AI 科研助手工作中</span>
            <p class="loading-text">{{ loadingStatus }}</p>
          </div>
        </div>
      </div>
    </transition>

    <!-- 1. 左侧侧边栏 (Left Sidebar) -->
    <aside class="left-sidebar">
      <div class="brand">
        <div class="logo-box">
          <img src="/cb19e5f2778cc441e6ba9b7ad38150d2.png" alt="Logo" class="logo-img" />
        </div>
        <span class="logo-text">DePaper</span>
      </div>
      
      <nav class="nav-menu">
        <div class="nav-group-label">工作台</div>
        <button class="nav-btn" :class="{ active: !showMessageListUI }" @click="handleBackToHome">
          <span class="icon">🏠</span> 首页概览
        </button>
        <button class="nav-btn" @click="handleRefreshButtonClick">
          <span class="icon">🔄</span> 刷新数据
        </button>
        
        <div class="nav-group-label mt-4">工具箱</div>
        <button class="nav-btn" @click="handleQuestionGenerateClick">
          <span class="icon">✨</span> 问题生成器
        </button>
        <button class="nav-btn" @click="handleActionButtonClick">
          <span class="icon">🧠</span> 深度推荐
        </button>
        <button class="nav-btn" @click="handleStudyReportClick">
          <span class="icon">📊</span> 学习报告
        </button>
      </nav>

      <div class="sidebar-footer">
        <div class="user-card">
          <div class="avatar">R</div>
          <div class="user-info">
            <span class="username">Researcher</span>
            <span class="status"><span class="status-dot"></span> Online</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- 2. 中间主要内容区 -->
    <main class="main-content">
      
      <!-- 顶部控制栏 (模型与设置) -->
      <header class="top-bar">
        <!-- 左侧留空或放面包屑 -->
        <div class="breadcrumbs">
           <span class="crumb-icon">📍</span> {{ showMessageListUI ? '课题详情' : '科研主页' }}
        </div>

        <div class="top-bar-controls">
           <!-- 模型选择器 -->
           <Popover v-model:open="modelSelectOpen">
            <PopoverTrigger as-child>
            <button class="model-select-btn">
                <ModelIcon
                    class="w-4 h-4 mr-2"
                    :model-id="activeModel.providerId"
                    :is-dark="themeStore.isDark"
                ></ModelIcon>
                {{ name }}
                <Icon icon="lucide:chevron-down" class="ml-2 opacity-50" />
            </button>
            </PopoverTrigger>
            <PopoverContent align="end" class="w-80 p-0">
            <ModelSelect
                :type="[ModelType.Chat, ModelType.ImageGeneration]"
                @update:model="handleModelUpdate"
            />
            </PopoverContent>
          </Popover>

          <!-- 设置按钮 -->
          <ScrollablePopover
              v-model:open="settingsPopoverOpen"
              align="end"
              content-class="w-80"
              :enable-scrollable="true"
          >
            <template #trigger>
              <button class="icon-btn">
                  <Icon icon="lucide:settings-2" class="w-5 h-5" />
              </button>
            </template>
            <ChatConfig
              v-model:temperature="temperature"
              v-model:context-length="contextLength"
              v-model:max-tokens="maxTokens"
              v-model:system-prompt="systemPrompt"
              v-model:artifacts="artifacts"
              v-model:thinking-budget="thinkingBudget"
              v-model:enable-search="enableSearch"
              v-model:forced-search="forcedSearch"
              v-model:search-strategy="searchStrategy"
              v-model:reasoning-effort="reasoningEffort"
              v-model:verbosity="verbosity"
              :context-length-limit="contextLengthLimit"
              :max-tokens-limit="maxTokensLimit"
              :model-id="activeModel?.id"
              :provider-id="activeModel?.providerId"
              :model-type="activeModel?.type"
            />
          </ScrollablePopover>
        </div>
      </header>

      <!-- 视图 A：仪表盘 (Dashboard) -->
      <div v-if="!showMessageListUI" class="dashboard-wrapper">
        
        <!-- 修改点：显眼的身份卡片 -->
        <div class="identity-banner">
            <div class="identity-icon">🎓</div>
            <div class="identity-content">
                <div class="identity-label">CURRENT RESEARCH FIELD</div>
                <h2 class="identity-value">{{ userField || '读取中...' }}</h2>
            </div>
            <div class="identity-decor"></div>
        </div>

        <div class="welcome-section">
          <h1 class="welcome-title">探索未知的边界</h1>
          <p class="welcome-subtitle">DePaper 智能助手已准备就绪，基于您的研究偏好为您导航。</p>
        </div>

        <!-- 核心功能区：AI 推荐 -->
        <div class="hero-section">
          <div class="ai-hero-card" @click="handleProcessNewsAndGenerateQuestions">
            <div class="hero-content">
              <div class="hero-icon-wrapper">
                <span class="hero-icon">🤖</span>
                <div class="pulse-ring"></div>
              </div>
              <div class="hero-text">
                <h2>智能生成研究课题</h2>
                <p>基于 <strong>{{ userField }}</strong> 领域的最新动态，AI 自动挖掘最具价值的切入点。</p>
              </div>
              <button class="hero-btn">
                立即生成 <Icon icon="lucide:arrow-right" class="ml-2" />
              </button>
            </div>
            <div class="hero-bg-pattern"></div>
          </div>
        </div>

        <!-- 辅助功能区：手动输入 -->
        <div class="secondary-section">
          <div class="section-label">或者，手动探索特定方向</div>
          <div class="search-bar-wrapper">
            <input 
              type="text" 
              placeholder="输入特定的课题关键词..." 
              class="manual-input"
            />
            <button class="manual-submit-btn">
              <span class="icon">🔍</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- 视图 B：学习路径 (Learning Path) -->
      <div v-else class="content-wrapper">
        <!-- 课题标题卡片 -->
        <div class="topic-header-card">
          <div class="topic-meta">当前课题</div>
          <h1 class="topic-title">{{ sampleTitle || '课题生成中...' }}</h1>
          
          <div class="difficulty-switch">
             <button 
              @click="handleDifficultyButtonClick('简单')"
              class="diff-btn simple"
              :class="{ active: isDifficultyClicked === '简单' }"
            >
               🌱 入门
            </button>
            <button 
              @click="handleDifficultyButtonClick('难')"
              class="diff-btn hard"
              :class="{ active: isDifficultyClicked === '难' }"
            >
               🔥 进阶
            </button>
          </div>
        </div>

        <!-- 步骤瀑布流 -->
        <div class="steps-timeline" v-if="sampleColumns.length > 0">
          <div 
            v-for="(column, index) in sampleColumns" 
            :key="index" 
            class="timeline-item"
            :class="{ 'visible': activeSteps[index] }"
          >
            <div class="timeline-marker">{{ index + 1 }}</div>
            <div class="timeline-content">
              <div class="step-card-inner">
                <div class="step-top">
                  <h3 class="step-heading"><TextReveal :text="column" /></h3>
                  <span class="keyword-badge"><TextReveal :text="keywords[index] || '关键步骤'" /></span>
                </div>

                <!-- 论文推荐区域 -->
                <div class="papers-grid" v-if="showPaperBox[index] === 1">
                  <!-- Paper 1 -->
                  <a 
                    v-if="paperData[index] && paperData[index].id"
                    :href="`https://arxiv.org/abs/${paperData[index].id}`" 
                    target="_blank"
                    class="paper-mini-card"
                  >
                    <div class="paper-icon-box">📄</div>
                    <div class="paper-details">
                      <div class="paper-name"><TextReveal :text="paperData[index].title" /></div>
                      <div class="paper-desc"><TextReveal :text="paperData[index].abstract" /></div>
                    </div>
                  </a>
                  
                  <!-- Paper 2 -->
                  <a 
                    v-if="paper2Data[index] && paper2Data[index].id"
                    :href="`https://arxiv.org/abs/${paper2Data[index].id}`" 
                    target="_blank"
                    class="paper-mini-card"
                  >
                    <div class="paper-icon-box purple">📑</div>
                    <div class="paper-details">
                      <div class="paper-name"><TextReveal :text="paper2Data[index].title" /></div>
                      <div class="paper-desc"><TextReveal :text="paper2Data[index].abstract" /></div>
                    </div>
                  </a>
                </div>
                
                <div v-else class="no-paper-hint">
                  <span>✨ 此步骤侧重实操，无需额外阅读论文</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 空状态占位 -->
        <div v-else class="empty-state-container">
           <div class="empty-spinner"></div>
           <p>正在为您生成专属学习路径...</p>
        </div>

        <!-- 总结卡片 -->
        <div class="summary-card" v-if="summary">
          <div class="summary-icon">📝</div>
          <div class="summary-content">
            <h3>阶段性总结</h3>
            <p><TextReveal :text="summary" /></p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* --- 全局样式 --- */
:root {
  --primary: #4f46e5;
  --bg-color: #f1f5f9;
}

.app-container {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: var(--bg-color);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  color: #334155;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.bg-decoration-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  opacity: 0.6;
}
.circle-1 {
  width: 400px;
  height: 400px;
  background: rgba(79, 70, 229, 0.1);
  top: -100px;
  left: -100px;
}
.circle-2 {
  width: 500px;
  height: 500px;
  background: rgba(14, 165, 233, 0.1);
  bottom: -100px;
  right: -100px;
}

/* --- 侧边栏 --- */
.left-sidebar {
  width: 260px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  flex-direction: column;
  padding: 24px;
  z-index: 10;
  box-shadow: 2px 0 15px rgba(0,0,0,0.03);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 40px;
}

.logo-box {
  width: 40px;
  height: 40px;
  background: #e0e7ff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo-img {
  width: 80%;
  height: 80%;
  object-fit: contain;
}

.logo-text {
  font-size: 22px;
  font-weight: 800;
  color: #1e1b4b;
}

.nav-menu {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-group-label {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 8px;
  padding-left: 12px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  background: transparent;
  color: #64748b;
  font-size: 15px;
  font-weight: 500;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.nav-btn:hover {
  background-color: white;
  color: #4f46e5;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.nav-btn.active {
  background-color: #4f46e5;
  color: white;
  box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 36px;
  height: 36px;
  background: #cbd5e1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.status {
  font-size: 12px;
  color: #10b981;
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
}

/* --- 主内容区 --- */
.main-content {
  flex: 1;
  overflow-y: auto;
  position: relative;
  z-index: 1;
  padding: 0 40px 40px 40px;
}

/* 顶部栏 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  margin-bottom: 20px;
  position: sticky;
  top: 0;
  z-index: 90;
}

.breadcrumbs {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 6px;
}

.top-bar-controls {
  display: flex;
  gap: 12px;
}

.model-select-btn {
  background: white;
  padding: 8px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  border: 1px solid transparent;
  transition: all 0.2s;
  cursor: pointer;
}

.model-select-btn:hover {
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

.icon-btn {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  transition: all 0.2s;
}

.icon-btn:hover {
  color: #4f46e5;
  transform: translateY(-1px);
}

/* --- 仪表盘 (Dashboard) --- */
.dashboard-wrapper {
  max-width: 900px;
  margin: 0 auto;
  animation: fadeIn 0.6s ease-out;
}

/* 显眼的身份 Banner */
.identity-banner {
  background: #1e1b4b; /* 深邃蓝 */
  color: white;
  padding: 24px 30px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  box-shadow: 0 10px 30px rgba(30, 27, 75, 0.3);
  position: relative;
  overflow: hidden;
}

.identity-icon {
  font-size: 32px;
  background: rgba(255,255,255,0.1);
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
}

.identity-content {
  flex: 1;
  z-index: 2;
}

.identity-label {
  font-size: 12px;
  letter-spacing: 1.5px;
  color: #a5b4fc;
  font-weight: 700;
  margin-bottom: 4px;
}

.identity-value {
  margin: 0;
  font-size: 24px;
  font-weight: 800;
  background: linear-gradient(90deg, #fff, #c7d2fe);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.identity-decor {
  position: absolute;
  top: 0; right: 0; bottom: 0; width: 50%;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.2));
  transform: skewX(-20deg) translateX(50px);
}

/* Welcome Text */
.welcome-title {
  font-size: 36px;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 10px;
  letter-spacing: -1px;
}

.welcome-subtitle {
  font-size: 16px;
  color: #64748b;
  margin-bottom: 40px;
}

/* Hero Section */
.hero-section {
  margin-bottom: 50px;
}

.ai-hero-card {
  position: relative;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  border-radius: 24px;
  padding: 50px;
  color: white;
  cursor: pointer;
  overflow: hidden;
  box-shadow: 0 20px 40px -10px rgba(79, 70, 229, 0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.ai-hero-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 25px 50px -10px rgba(79, 70, 229, 0.5);
}

.hero-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
}

.hero-icon-wrapper {
  position: relative;
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.hero-icon {
  font-size: 32px;
}

.pulse-ring {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 20px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  animation: ripple 2s infinite;
}

@keyframes ripple {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.5); opacity: 0; }
}

.hero-text h2 {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.hero-text p {
  font-size: 16px;
  opacity: 0.9;
  max-width: 500px;
  margin: 0;
  line-height: 1.5;
}

.hero-btn {
  margin-top: 10px;
  background: white;
  color: #4f46e5;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.hero-btn:hover {
  background: #f8fafc;
  padding-right: 30px;
}

.hero-bg-pattern {
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  background-image: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
  z-index: 1;
}

/* Secondary Section */
.secondary-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 40px;
}

.section-label {
  font-size: 14px;
  color: #94a3b8;
  font-weight: 500;
  padding-left: 10px;
}

.search-bar-wrapper {
  display: flex;
  background: white;
  padding: 10px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
  border: 1px solid transparent;
  transition: all 0.3s;
}

.search-bar-wrapper:focus-within {
  border-color: #4f46e5;
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.1);
}

.manual-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 20px;
  font-size: 16px;
  color: #334155;
  background: transparent;
}

.manual-submit-btn {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 12px;
  border: none;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.manual-submit-btn:hover {
  background: #4f46e5;
  color: white;
}

/* --- 结果视图 (Learning Path) --- */
.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease-out;
}

.topic-header-card {
  background: white;
  padding: 30px;
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
  position: relative;
  overflow: hidden;
}

.topic-meta {
  font-size: 12px;
  text-transform: uppercase;
  color: #94a3b8;
  font-weight: 700;
  letter-spacing: 1px;
  margin-bottom: 10px;
}

.topic-title {
  font-size: 28px;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 20px 0;
  line-height: 1.4;
}

.difficulty-switch {
  display: flex;
  gap: 10px;
}

.diff-btn {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s;
  background: #f8fafc;
  color: #64748b;
}

.diff-btn:hover {
  background: #e2e8f0;
}

.diff-btn.active.simple {
  background: #ecfdf5;
  color: #059669;
  border-color: #a7f3d0;
}

.diff-btn.active.hard {
  background: #fff1f2;
  color: #e11d48;
  border-color: #fecdd3;
}

/* 瀑布流步骤 */
.steps-timeline {
  display: flex;
  flex-direction: column;
  gap: 0;
  position: relative;
  padding-left: 20px;
}

.timeline-item {
  display: flex;
  gap: 30px;
  padding-bottom: 40px;
  position: relative;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease;
}

.timeline-item.visible {
  opacity: 1;
  transform: translateY(0);
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 15px;
  top: 35px;
  bottom: 0;
  width: 2px;
  background: #e2e8f0;
  z-index: 0;
}

.timeline-item:last-child::before {
  display: none;
}

.timeline-marker {
  width: 32px;
  height: 32px;
  background: #4f46e5;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  z-index: 1;
  flex-shrink: 0;
  box-shadow: 0 0 0 4px #e0e7ff;
}

.timeline-content {
  flex: 1;
}

.step-card-inner {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.02);
  border: 1px solid rgba(226, 232, 240, 0.6);
  transition: all 0.2s;
}

.step-card-inner:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.step-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.step-heading {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #334155;
}

.keyword-badge {
  background: #f1f5f9;
  color: #64748b;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
}

.papers-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.paper-mini-card {
  display: flex;
  gap: 12px;
  background: #f8fafc;
  padding: 12px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.paper-mini-card:hover {
  background: white;
  border-color: #4f46e5;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.1);
}

.paper-icon-box {
  width: 32px;
  height: 32px;
  background: #e0e7ff;
  color: #4f46e5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.paper-icon-box.purple {
  background: #f3e8ff;
  color: #9333ea;
}

.paper-details {
  flex: 1;
  min-width: 0;
}

.paper-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.paper-desc {
  font-size: 12px;
  color: #64748b;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.no-paper-hint {
  font-size: 13px;
  color: #94a3b8;
  font-style: italic;
  padding: 10px;
  text-align: center;
}

/* 总结卡片 */
.summary-card {
  margin-top: 40px;
  background: linear-gradient(to right, #ffffff, #f8fafc);
  border: 1px solid #e2e8f0;
  border-left: 4px solid #4f46e5;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  gap: 20px;
}

.summary-icon {
  font-size: 32px;
}

.summary-content h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #1e293b;
}

.summary-content p {
  margin: 0;
  font-size: 15px;
  color: #475569;
  line-height: 1.6;
}

/* 加载覆盖层 */
.loading-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(5px);
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loading-card {
  background: white;
  padding: 30px 50px;
  border-radius: 20px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.1);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  max-width: 400px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-title {
  display: block;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 5px;
}

.loading-text {
  font-size: 14px;
  color: #64748b;
}

@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import ChatInput from './chat-input/ChatInput.vue'
import { Popover, PopoverContent, PopoverTrigger } from '@shadcn/components/ui/popover'
import ScrollablePopover from './ScrollablePopover.vue'
import { Button } from '@shadcn/components/ui/button' 
import ModelIcon from './icons/ModelIcon.vue'
import { Badge } from '@shadcn/components/ui/badge'
import { Icon } from '@iconify/vue'
import ModelSelect from './ModelSelect.vue'
import { useChatStore } from '@/stores/chat'
import { MODEL_META } from '@shared/presenter'
import { useSettingsStore } from '@/stores/settings'
import { computed, nextTick, ref, watch, onMounted } from 'vue'
import { UserMessageContent } from '@shared/chat'
import ChatConfig from './ChatConfig.vue'
import { usePresenter } from '@/composables/usePresenter'
import { useThemeStore } from '@/stores/theme'
import { ModelType } from '@shared/model'
import { useRouter } from 'vue-router'
import TextReveal from './message/TextReveal.vue'

// --- 初始化与变量 ---
const configPresenter = usePresenter('configPresenter')
const threadPresenter = usePresenter('threadPresenter')
const themeStore = useThemeStore()
const router = useRouter()
const { t } = useI18n()
const chatStore = useChatStore()
const settingsStore = useSettingsStore()

const userField = ref<string>('') 
const customText = ref('');
const customTextError = ref('');
const sampleTitle = ref('');
const sampleColumns = ref<string[]>([]);
const activeModel = ref({
  name: '', id: '', providerId: '', tags: [], type: ModelType.Chat
} as { name: string, id: string, providerId: string, tags: string[], type: ModelType })

const temperature = ref(0.6)
const contextLength = ref(16384)
const contextLengthLimit = ref(16384)
const maxTokens = ref(4096)
const maxTokensLimit = ref(4096)
const systemPrompt = ref('')
const artifacts = ref(settingsStore.artifactsEffectEnabled ? 1 : 0)
const thinkingBudget = ref<number | undefined>(undefined)
const enableSearch = ref<boolean | undefined>(undefined)
const forcedSearch = ref<boolean | undefined>(undefined)
const searchStrategy = ref<'turbo' | 'max' | undefined>(undefined)
const reasoningEffort = ref<'minimal' | 'low' | 'medium' | 'high' | undefined>(undefined)
const verbosity = ref<'low' | 'medium' | 'high' | undefined>(undefined)

const loadingStatus = ref<string | null>(null)
let loadingStatusTimer: NodeJS.Timeout | null = null

const name = computed(() => {
  return activeModel.value?.name ? activeModel.value.name.split('/').pop() : '选择模型'
})

const initialized = ref(false)
const modelSelectOpen = ref(false)
const settingsPopoverOpen = ref(false)
const chatInputRef = ref<InstanceType<typeof ChatInput> | null>(null)

// Data Refs
const keywords = ref<string[]>([])
const summary = ref<string>('')
const showPaperBox = ref<number[]>([0, 0, 0, 0, 0])
const paperData = ref<Array<{id: string, title: string, abstract: string}>>([])
const paper2Data = ref<Array<{id: string, title: string, abstract: string}>>([])
const isDifficultyClicked = ref<string | null>(null)
const activeSteps = ref<boolean[]>([]);
const showMessageListUI = ref(false);

// --- 核心方法与逻辑 ---

const setLoadingStatus = (status: string, step?: number) => {
  if (loadingStatusTimer) { clearTimeout(loadingStatusTimer); loadingStatusTimer = null }
  const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  const detailedStatus = `${status}`
  loadingStatus.value = detailedStatus
  
  loadingStatusTimer = setTimeout(() => {
    if (loadingStatus.value === detailedStatus) {
      loadingStatus.value = `查询论文中...`
    }
    loadingStatusTimer = null
  }, 4000)
}

const findEnabledModel = (providerId: string, modelId: string) => {
  for (const provider of settingsStore.enabledModels) {
    if (provider.providerId === providerId) {
      for (const model of provider.models) {
        if (model.id === modelId) return { model, providerId: provider.providerId }
      }
    }
  }
  return undefined
}

const pickFirstEnabledModel = () => {
  const found = settingsStore.enabledModels
    .flatMap((p) => p.models.map((m) => ({ ...m, providerId: p.providerId })))
    .find((m) => m.type === ModelType.Chat || m.type === ModelType.ImageGeneration)
  return found
}

const setActiveFromEnabled = (m: { name: string, id: string, providerId: string, type?: ModelType }) => {
  activeModel.value = {
    name: m.name, id: m.id, providerId: m.providerId, tags: [], type: m.type ?? ModelType.Chat
  }
}

const initActiveModel = async () => {
  if (initialized.value) return
  if (chatStore.threads.length > 0) {
    const pinnedGroup = chatStore.threads.find((g) => g.dt === 'Pinned')
    const pinnedFirst = pinnedGroup?.dtThreads?.[0]
    const normalGroup = chatStore.threads.find((g) => g.dt !== 'Pinned' && g.dtThreads.length > 0)
    const normalFirst = normalGroup?.dtThreads?.[0]
    const candidate = [pinnedFirst, normalFirst]
      .filter(Boolean)
      .sort((a, b) => (b!.updatedAt || 0) - (a!.updatedAt || 0))[0] as any
    if (candidate?.settings?.modelId && candidate?.settings?.providerId) {
      const match = findEnabledModel(candidate.settings.providerId, candidate.settings.modelId)
      if (match) {
        setActiveFromEnabled({ ...match.model, providerId: match.providerId })
        initialized.value = true
        return
      }
    }
  }

  try {
    const preferredModel = (await configPresenter.getSetting('preferredModel')) as any
    if (preferredModel?.modelId && preferredModel?.providerId) {
      const match = findEnabledModel(preferredModel.providerId, preferredModel.modelId)
      if (match) {
        setActiveFromEnabled({ ...match.model, providerId: match.providerId })
        initialized.value = true
        return
      }
    }
  } catch (error) { console.warn('Failed to get user preferred model:', error) }

  const first = pickFirstEnabledModel()
  if (first) { setActiveFromEnabled(first); initialized.value = true }
}

const handleModelUpdate = (model: MODEL_META, providerId: string) => {
  activeModel.value = {
    name: model.name, id: model.id, providerId: providerId, tags: [], type: model.type ?? ModelType.Chat
  }
  chatStore.updateChatConfig({ modelId: model.id, providerId: providerId })
  configPresenter.setSetting('preferredModel', { modelId: model.id, providerId: providerId })
  modelSelectOpen.value = false
}

// Watchers
watch(() => settingsStore.enabledModels, async () => {
    if (!initialized.value) { await initActiveModel(); return }
    const current = activeModel.value
    if (!current?.id || !current?.providerId) {
      const first = pickFirstEnabledModel(); if (first) setActiveFromEnabled(first)
      return
    }
    const stillExists = !!findEnabledModel(current.providerId, current.id)
    if (!stillExists) {
      const first = pickFirstEnabledModel(); if (first) setActiveFromEnabled(first)
    }
  }, { immediate: false, deep: true })

watch(() => activeModel.value, async () => {
    const config = await configPresenter.getModelDefaultConfig(activeModel.value.id, activeModel.value.providerId)
    temperature.value = config.temperature ?? 0.7
    contextLength.value = config.contextLength/2
    maxTokens.value = config.maxTokens/2
    contextLengthLimit.value = config.contextLength/2
    maxTokensLimit.value = config.maxTokens/2
    thinkingBudget.value = config.thinkingBudget
    enableSearch.value = config.enableSearch
    forcedSearch.value = config.forcedSearch
    searchStrategy.value = config.searchStrategy
    reasoningEffort.value = config.reasoningEffort
    verbosity.value = config.verbosity
  })

watch(() => sampleColumns.value, (newColumns) => {
  if (newColumns.length > 0) {
    activeSteps.value = Array(newColumns.length).fill(false);
    newColumns.forEach((_, index) => {
      setTimeout(() => { activeSteps.value[index] = true; }, index * 800); 
    });
  }
}, { deep: true });

watch(() => chatStore.deeplinkCache, (newCache) => {
    if (newCache) {
      if (newCache.modelId) {
        const matchedModel = settingsStore.findModelByIdOrName(newCache.modelId)
        if (matchedModel) handleModelUpdate(matchedModel.model, matchedModel.providerId)
      }
      if (newCache.msg || newCache.mentions) {
        const setInputContent = () => {
          if (chatInputRef.value) {
            chatInputRef.value.clearContent()
            if (newCache.mentions) newCache.mentions.forEach((m) => chatInputRef.value?.appendMention(m))
            if (newCache.msg) chatInputRef.value.appendText(newCache.msg)
            return true
          }
          return false
        }
        if (!setInputContent()) nextTick(() => setInputContent())
      }
      if (newCache.systemPrompt) systemPrompt.value = newCache.systemPrompt
      if (newCache.autoSend && newCache.msg) {
        handleSend({ text: newCache.msg || '', files: [], links: [], think: false, search: false })
      }
      chatStore.clearDeeplinkCache()
    }
  }, { immediate: true })

// Helper Functions
const estimateTokens = (text: string): number => {
  if (!text) return 0;
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const nonChineseChars = text.length - chineseChars;
  return Math.ceil(chineseChars / 1.3 + nonChineseChars / 4);
};

const truncateTextToTokens = (text: string, maxTokens: number): string => {
  if (estimateTokens(text) <= maxTokens) return text;
  const safetyFactor = 0.8; 
  const maxChars = Math.floor(maxTokens * 1.5 * safetyFactor); 
  return text.substring(0, maxChars) + '...';
};

const extractAssistantText = (assistantMsg: any) => {
    if (!assistantMsg || !assistantMsg.content) return '';
    const parts: string[] = [];
    for (const block of assistantMsg.content) {
        if (block.type === 'content' || typeof block.content === 'string') {
            parts.push(block.content || block);
        }
    }
    return parts.join('\n').trim();
}

// API Calls
const callBM25Api = async (query: string): Promise<any[]> => {
  try {
    const apiUrl = 'http://localhost:2625/bm25/score';
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ query: query, k1: 0.9, b: 0.5 })
    });
    if (!response.ok) throw new Error(`HTTP错误！状态码：${response.status}`);
    const responseData = await response.json();
    return ((responseData as { results?: any[] }).results || []);
  } catch (err) { console.warn(`BM25调用失败: ${err}`); return []; }
};

const callSentenceBertApi = async (query: string): Promise<any[]> => {
  try {
    const apiUrl = 'http://localhost:2378/sentence-bert/match';
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ query: query })
    });
    if (!response.ok) throw new Error(`HTTP错误！状态码：${response.status}`);
    const responseData = await response.json();
    return ((responseData as { results?: any[] }).results || []);
  } catch (err) { console.warn(`Sentence-BERT调用失败: ${err}`); return []; }
};

// --- 业务逻辑处理 ---

const handleDifficultyButtonClick = (difficulty: string) => {
  isDifficultyClicked.value = difficulty;
  console.log(`用户标记当前内容为: ${difficulty}`);
}

const handleQuestionGenerateClick = () => { router.push('/question') }
const handleBackToHome = () => { showMessageListUI.value = false; }
const handleStudyReportClick = () => { router.push('/study-report') }

const handleActionButtonClick = async () => {
  try {
    const fileContent = await window.api.readLocalFile('user-preferences.txt');
    if (fileContent) {
      const queryMessage = `请你用arxiv-mcp-server的工具查找三篇和${fileContent}有关的论文，要新一点，sort_by参数为date。`;
      await handleSend({ text: queryMessage, files: [], links: [], think: false, search: false });
    } else {
      alert('用户偏好文件内容为空，请检查项目根目录下的user-preferences.txt文件');
    }
  } catch (error) { alert(`操作失败: ${(error as Error).message}`); }
};

const handleRefreshButtonClick = async () => {
  console.log('刷新按钮被点击');
  try {
    setLoadingStatus('开始执行问题生成，等待处理...');
    let sampleContent = '';
    try { sampleContent = await window.api.readLocalFile('output.txt'); } catch (err) { alert('无法读取sample.txt文件'); return; }
    
    const lines = sampleContent.split('\n');
    let paperContent: string[][] = [];
    let paperContent2: string[][] = [];
    let hasValidCalls = false;

    const checkLineAndCallApi = async (lineIndex: number, paramLineIndex: number, paperContentIndex: number) => {
      while (paperContent.length <= paperContentIndex) paperContent.push([]);
      while (paperContent2.length <= paperContentIndex) paperContent2.push([]);
      
      if (lines.length > lineIndex) {
        const lineContent = lines[lineIndex].trim();
        if (lineContent === '1') {
          if (lines.length > paramLineIndex) {
            const queryParam = lines[paramLineIndex].trim();
            if (queryParam) {
              const bm25Response = await callBM25Api(queryParam);
              if (bm25Response && bm25Response.length > 0) {
                const paper = bm25Response[0];
                paperContent[paperContentIndex] = [paper.id || '未知ID', paper.title || '无标题', paper.original_abstract || '无摘要'];
                hasValidCalls = true;
              }
              try {
                const sentenceBertResponse = await callSentenceBertApi(queryParam);
                if (sentenceBertResponse && sentenceBertResponse.length > 0) {
                  const paper = sentenceBertResponse[0];
                  paperContent2[paperContentIndex] = [paper.id || '未知ID', paper.title || '无标题', paper.original_abstract || '无摘要'];
                }
              } catch (e) { console.error(e) }
            }
          }
        } else if (lineContent === '0') {
           paperContent[paperContentIndex] = ['1', '1', '1'];
           paperContent2[paperContentIndex] = ['1', '1', '1'];
           hasValidCalls = true;
        }
      }
    };
    
    await checkLineAndCallApi(6, 11, 1);
    await checkLineAndCallApi(7, 12, 2);
    await checkLineAndCallApi(8, 13, 3);
    await checkLineAndCallApi(9, 14, 4);
    await checkLineAndCallApi(10, 15, 5);
    
    if (!hasValidCalls) {
      paperContent = [['default-id-1', '默认论文标题1', '摘要1'], ['1']];
    }
    
    const flattenedContent: string[] = []; 
    const flattenedContent2: string[] = [];
    paperContent.forEach(subArray => subArray.forEach(line => flattenedContent.push(line)));
    paperContent2.forEach(subArray => subArray.forEach(line => flattenedContent2.push(line)));
    
    await window.api.writeLocalFile('paper.txt', flattenedContent.join('\n'));
    await window.api.writeLocalFile('paper2.txt', flattenedContent2.join('\n'));
    setLoadingStatus('文件更新完成');
    setTimeout(() => { loadingStatus.value = null; }, 1000);
  } catch (error) {
    loadingStatus.value = null;
    alert(`操作失败: ${(error as Error).message}`);
  }
};

const handleProcessNewsAndGenerateQuestions = async () => {
  try {
    setLoadingStatus('AI正在分析任务需求，准备处理新闻内容...', 1);
    const newsQuery = `用fetch,url=https://news.aibase.cn/news,max_length=500,结果只包含三条最重要的新闻总结,每条30字以内,不要有其他内容`;
    const tabId = window.api.getWebContentsId();
    setTimeout(() => { if (!loadingStatus.value?.includes('查询论文中')) setLoadingStatus('正在从aibase.cn获取最新科技新闻...'); }, 800);

    const newsThreadId = await threadPresenter.createConversation('新闻处理', {
      providerId: activeModel.value.providerId,
      modelId: activeModel.value.id,
      systemPrompt: '你是一个简洁的信息提取助手。',
      temperature: temperature.value,
      contextLength: 16000,
      maxTokens: 500,
      verbosity: 0,
      enabledMcpTools: chatStore.chatConfig.enabledMcpTools
    } as any, tabId);
    
    setLoadingStatus('正在发送新闻查询请求...');
    await threadPresenter.sendMessage(newsThreadId, JSON.stringify({
      text: newsQuery, files: [], links: [], think: false, search: false
    }), "user");
    await threadPresenter.startStreamCompletion(newsThreadId, undefined, {});

    setLoadingStatus('正在解析新闻数据...');
    const msgsRes: any = await threadPresenter.getMessages(newsThreadId, 1, 100);
    const assistantMsg = msgsRes?.list?.find((m: any) => m.role === 'assistant' && m.content && m.content.length > 0);
    let newsContent = assistantMsg ? extractAssistantText(assistantMsg) : '';

    if (!newsContent) { alert('未获取到新闻内容'); loadingStatus.value = null; return; }
    
    setLoadingStatus(`新闻获取完成，正在生成结构化问题...`);
    newsContent = truncateTextToTokens(newsContent, 300);

    const systemPromptForGen = `你是一个专业的AI助手。请从新闻中提取信息并生成结构化问题。`;
    const instructions = `请严格按照以下优先级和步骤处理提供的新闻内容，仅输出指定核心内容：
    (此处省略部分指令文本，保持原逻辑的一致性，确保输出格式正确)...
    输出格式要求：
    [具体问题]
    [子过程 1]...[子过程 5]
    1/0 (5行)
    [专业词汇] (5行)
    [总结]
    `; // 注意：为了代码简洁这里省略了长指令，实际运行时请确保这里是完整的 prompt

    const detailedInstructions = `请严格按照以下优先级和步骤处理提供的新闻内容，仅输出指定核心内容：
核心任务步骤
先从新闻全文提炼 5 个核心科技关键词（内部使用，不用输出），聚焦技术名称、创新应用等强相关维度；
筛选优先级：优先挑选有具体实现过程、技术流程可拆解的关键词（若多个符合，选与新闻核心关联最紧密的 1 个）；
针对选中的关键词，生成 1 个大框架问题，需覆盖其核心技术过程、关键要点或实践逻辑；
基于该关键词的通用技术实现逻辑 ，推导 5 个关键过程 / 要点，生成对应的子过程，聚焦细节拆解。
针对每个子过程，根据其技术难度自行判断是否需要给予用户论文推荐，需要则为1，不需要则为0；
然后分别针对每个子过程生成对应的ai领域学术专业词汇，只有专业词汇要求英文，且有抽象性和学术性，用于论文的检索（如machine learning、computer vision）；
最后根据子过程生成一段简短的针对大框架问题的解决过程的总结，尽量精简而不失要点。
输出格式要求：
[具体问题]（直接输出问题内容，不要带括号）
[子过程 1]
[子过程 2]
[子过程 3]
[子过程 4]（直接输出，不要带括号等占位符）
[子过程5]
1/0
1/0
1/0(1表示要推荐，0表示不要推荐）
1/0
1/0
[子过程1的专业词汇]
[子过程2的专业词汇](只有专业词汇需要英文）
[子过程3的专业词汇]
[子过程4的专业词汇]
[子过程5的专业词汇]
[总结]
注意事项
关键词筛选必须紧扣 “有具体实现过程”，排除无明确技术流程的概念类词汇；
大框架问题需围绕 “过程”“步骤”“要点” 展开，不偏离技术落地逻辑；
子过程需对应不同技术模块，不重复、不遗漏关键环节，聚焦 “具体实现”“技术细节”“操作逻辑”；
专业词汇要能用于相关领域的论文检索，且只有专业词汇是英文，其他内容是中文；
仅输出上述指定内容，不添加关键词、解答或其他无关信息，格式简洁可直接使用。
请基于上述要求，处理我提供的新闻内容，完整输出选中关键词对应的大框架问题、子过程、是否推荐、专业词汇、总结等信息。`;

    const questionThreadId = await threadPresenter.createConversation('新闻问题生成', {
          providerId: activeModel.value.providerId,
          modelId: activeModel.value.id,
          systemPrompt: systemPromptForGen,
          temperature: 0.3, 
          contextLength: 16000,
          maxTokens: 1000,
          verbosity: 0,
          enabledMcpTools: chatStore.chatConfig.enabledMcpTools
    } as any, tabId);

    const combinedText = `${detailedInstructions}\n\n${newsContent}`;
    await threadPresenter.sendMessage(questionThreadId, JSON.stringify({
        text: combinedText, files: [], links: [], think: false, search: false
    }), "user");
    await threadPresenter.startStreamCompletion(questionThreadId, undefined, {});

    setLoadingStatus('正在整理最终问题结构...');
    const qMsgsRes: any = await threadPresenter.getMessages(questionThreadId, 1, 100);
    const qMsg = qMsgsRes?.list?.find((m: any) => m.role === 'assistant');
    
    if(qMsg) {
      const questionStructure = extractAssistantText(qMsg);
      if (questionStructure) {
        let cleaned = questionStructure.replace(/关键词\d/g, '').split('\n').filter(l => l.trim() !== '').join('\n');
        await window.api.writeLocalFile('output.txt', cleaned);
        await window.api.writeLocalFile('sample.txt', cleaned);
        
        const lines = cleaned.trim().split('\n').filter(line => line.trim() !== '');
        if (lines.length > 0) {
          sampleTitle.value = lines[0].trim();
          if (lines.length >= 6) sampleColumns.value = lines.slice(1, 6).map(line => line.trim());
          if (lines.length >= 11) showPaperBox.value = lines.slice(6, 11).map(line => parseInt(line.trim()) || 0);
          if (lines.length >= 16) keywords.value = lines.slice(11, 16).map(line => line.trim());
          if (lines.length >= 17) summary.value = lines[16].trim();
        }
        setLoadingStatus('生成成功，正在切换视图...');
        showMessageListUI.value = true;
      }
    }
    setTimeout(() => { loadingStatus.value = null; }, 1000);
  } catch (error) {
    loadingStatus.value = null;
    alert(`处理失败: ${(error as Error).message}`);
  }
}

const handleSend = async (content: UserMessageContent) => {
  const sampleFileContent = await window.api.readLocalFile('output.txt');
  await chatStore.createThread(content.text, {
    providerId: activeModel.value.providerId, modelId: activeModel.value.id,
    systemPrompt: sampleFileContent, temperature: temperature.value,
    contextLength: contextLength.value, maxTokens: maxTokens.value,
    artifacts: artifacts.value as 0 | 1, thinkingBudget: thinkingBudget.value,
    enableSearch: enableSearch.value, forcedSearch: forcedSearch.value,
    searchStrategy: searchStrategy.value, reasoningEffort: reasoningEffort.value,
    verbosity: verbosity.value, enabledMcpTools: chatStore.chatConfig.enabledMcpTools
  } as any)
  chatStore.sendMessage(content)
}

onMounted(async () => {
  configPresenter.getDefaultSystemPrompt().then((prompt) => { systemPrompt.value = prompt })
  await initActiveModel()
  
  try {
     const prefContent = await window.api.readLocalFile('user-preferences.txt');
     userField.value = prefContent ? prefContent.trim() : '计算机科学';
  } catch (e) { userField.value = '计算机科学'; }

  try {
    const fileContent = await window.api.readLocalFile('custom-welcome.txt');
    if (fileContent) customText.value = fileContent.trim();
  } catch (e) {}

  try {
    const sampleFileContent = await window.api.readLocalFile('sample.txt');
    if (sampleFileContent) {
      const lines = sampleFileContent.trim().split('\n').filter(l => l.trim() !== '');
      if (lines.length > 0) {
        sampleTitle.value = lines[0].trim();
        if (lines.length >= 6) sampleColumns.value = lines.slice(1, 6).map(l => l.trim());
        if (lines.length >= 11) showPaperBox.value = lines.slice(6, 11).map(l => parseInt(l.trim()) || 0);
        if (lines.length >= 16) keywords.value = lines.slice(11, 16).map(l => l.trim());
        if (lines.length >= 17) summary.value = lines[16].trim();
        activeSteps.value = Array(sampleColumns.value.length).fill(false);
      }
    }
  } catch (e) {}
  
// Load papers helper
  const loadPapers = async (filename: string, target: any) => {
      try {
        const content = await window.api.readLocalFile(filename);
        if (content) {
            const lines = content.trim().split('\n').filter(l => l.trim() !== '');
            
            // --- 修改点开始：显式定义类型 ---
            const newData: Array<{id: string, title: string, abstract: string}> = [];
            // --- 修改点结束 ---

            for (let i = 0; i < 5; i++) {
                // 确保索引不越界
                if (i*3+2 < lines.length) {
                    newData.push({
                        id: lines[i*3], 
                        title: lines[i*3+1], 
                        abstract: lines[i*3+2]
                    });
                }
            }
            target.value = newData;
        }
      } catch (e) {
        console.error(`Error loading papers from ${filename}:`, e);
      }
  };
  await loadPapers('paper.txt', paperData);
  await loadPapers('paper2.txt', paper2Data);
})
</script>