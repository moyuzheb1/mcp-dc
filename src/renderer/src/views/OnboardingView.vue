<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePresenter } from '@/composables/usePresenter'

const router = useRouter()
const configPresenter = usePresenter('configPresenter')
const currentStage = ref(1)

// 跳转到下一个阶段
const goToNextStage = () => {
  if (currentStage.value < 3) {
    currentStage.value++
  }
}

// 开始使用应用，跳转到NewThread页面
const startUsingApp = async () => {
  // 设置初始化完成标志，下次启动不再显示引导页
  await configPresenter.setSetting('init_complete', true)
  router.push('/thread/new')
}

// 测试用：重置初始化标志（可在控制台调用）
window.resetInitComplete = async () => {
  await configPresenter.setSetting('init_complete', false)
  console.log('init_complete已重置为false，下次启动将显示引导页')
}
</script>

<template>
  <div class="onboarding-container">
    <!-- 第一阶段：应用介绍+欢迎语 -->
    <div v-if="currentStage === 1" class="stage-container">
      <div class="content-wrapper">
        <h1 class="title">欢迎使用DePaper</h1>
        <p class="description">
          DePaper是您的智能研究助手，帮助您高效管理和探索研究课题。
        </p>
        <p class="sub-description">
          让我们一起开始您的研究之旅吧！
        </p>
        <button class="next-button" @click="goToNextStage">
          下一步
        </button>
      </div>
    </div>

    <!-- 第二阶段：用户偏好调查 -->
    <div v-if="currentStage === 2" class="stage-container">
      <div class="content-wrapper">
        <h1 class="title">告诉我们您的偏好</h1>
        <p class="description">
          我们将根据您的研究领域和兴趣，为您提供更精准的建议。
        </p>
        
        <!-- 简单的偏好选择示例 -->
        <div class="preferences-container">
          <div class="preference-item">
            <label class="preference-label">
              <input type="checkbox" class="preference-checkbox">
              <span class="preference-text">计算机科学</span>
            </label>
          </div>
          <div class="preference-item">
            <label class="preference-label">
              <input type="checkbox" class="preference-checkbox">
              <span class="preference-text">人工智能</span>
            </label>
          </div>
          <div class="preference-item">
            <label class="preference-label">
              <input type="checkbox" class="preference-checkbox">
              <span class="preference-text">数据分析</span>
            </label>
          </div>
          <div class="preference-item">
            <label class="preference-label">
              <input type="checkbox" class="preference-checkbox">
              <span class="preference-text">自然语言处理</span>
            </label>
          </div>
        </div>
        
        <div class="button-group">
          <button class="back-button" @click="currentStage = 1">
            上一步
          </button>
          <button class="start-button" @click="startUsingApp">
            开始使用
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.onboarding-container {
  width: 100vw;
  height: 100vh;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.stage-container {
  width: 100%;
  max-width: 800px;
  padding: 0 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content-wrapper {
  text-align: center;
  padding: 40px;
}

.title {
  font-size: 36px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
}

.description {
  font-size: 18px;
  color: #666;
  margin-bottom: 15px;
  line-height: 1.6;
}

.sub-description {
  font-size: 16px;
  color: #888;
  margin-bottom: 40px;
  line-height: 1.6;
}

.next-button {
  padding: 15px 40px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  background-color: #4f46e5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.next-button:hover {
  background-color: #4338ca;
  transform: translateY(-2px);
}

.preferences-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin: 30px 0 40px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.preference-item {
  text-align: left;
}

.preference-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  color: #333;
  cursor: pointer;
}

.preference-checkbox {
  width: 18px;
  height: 18px;
  accent-color: #4f46e5;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.back-button {
  padding: 15px 30px;
  font-size: 16px;
  font-weight: 600;
  color: #666;
  background-color: transparent;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  border-color: #d1d5db;
  background-color: #f9fafb;
}

.start-button {
  padding: 15px 40px;
  font-size: 16px;
  font-weight: 600;
  color: white;
  background-color: #4f46e5;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.start-button:hover {
  background-color: #4338ca;
  transform: translateY(-2px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .title {
    font-size: 28px;
  }
  
  .description {
    font-size: 16px;
  }
  
  .sub-description {
    font-size: 14px;
  }
  
  .button-group {
    flex-direction: column;
    align-items: center;
  }
  
  .back-button, .start-button, .next-button {
    width: 100%;
    max-width: 300px;
  }
}
</style>