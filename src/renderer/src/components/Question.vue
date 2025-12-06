<template>
  <div class="app-container">
    <!-- 加载状态提示 -->
    <div v-if="loadingStatus" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <p class="loading-text">{{ loadingStatus }}</p>
      </div>
    </div>
    <!-- 1. 左侧功能导航栏 (Left Sidebar) -->
    <aside class="left-sidebar">
      <div class="brand">
        <span class="logo-icon">
          <!-- 保持原有Logo图片逻辑 -->
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

    <!-- 2. 中间主要内容区 (Main Content) -->
    <main class="main-content">
      <!-- 默认视图：课题输入界面 -->
      <div v-if="!showMessageListUI" class="content-wrapper">
        <!-- 顶部标题区 -->
        <header class="content-header">
          <div class="topic-tag">研究课题</div>
          <h1 class="main-title">输入你想研究的课题</h1>
        </header>

        <!-- 输入框区域 -->
        <div class="input-section">
          <div class="input-container">
            <input 
              type="text" 
              placeholder="请输入你想研究的课题，例如：机器学习在自然语言处理中的应用" 
              class="topic-input"
            />
            <button class="submit-btn">
              <span class="icon">🚀</span> 开始研究
            </button>
          </div>
        </div>

        <!-- AI推荐区域 -->
        <div class="ai-recommendation-section">
          <div class="recommendation-header">
            <span class="icon">🤖</span> AI热点推荐
          </div>
          <div class="recommendation-content">
            <div class="recommendation-text">
              AI自动根据 你的偏好 和 计算机科学领域 的新闻热点推荐相关课题
            </div>
            <div class="recommendation-tags">
              <span class="tag">大模型</span>
              <span class="tag">多模态</span>
              <span class="tag">AI安全</span>
              <span class="tag">智能推荐</span>
              <span class="tag">边缘计算</span>
            </div>
            <button class="refresh-recommendation-btn" @click="handleProcessNewsAndGenerateQuestions">
              <span class="icon">🧠</span> AI推荐课题
            </button>
          </div>
        </div>
      </div>
      
      <!-- 消息列表视图：来自MessageList.vue -->
      <div v-else class="content-wrapper">
        <!-- 顶部标题区 -->
        <header class="content-header">
          <div class="topic-tag">当前课题</div>
         <h1 class="main-title">{{ sampleTitle || '点击生成问题或输入开始学习' }}</h1>
          
          <!-- 难度控制区 -->
          <div class="difficulty-controls">
            <button 
              @click="handleDifficultyButtonClick('难')"
              class="difficulty-badge"
              :class="isDifficultyClicked === '难' ? 'hard active' : 'hard'"
            >
              <TextReveal :text="isDifficultyClicked === '难' ? '已标记：难' : '标记为难'" />
            </button>
            <button 
              @click="handleDifficultyButtonClick('简单')"
              class="difficulty-badge"
              :class="isDifficultyClicked === '简单' ? 'simple active' : 'simple'"
            >
               <TextReveal :text="isDifficultyClicked === '简单' ? '已标记：简单' : '标记为简单'" />
            </button>
          </div>
        </header>

        <!-- 核心功能：5个步骤拆解 -->
        <div class="steps-container" v-if="sampleColumns.length > 0">
          <div 
            v-for="(column, index) in sampleColumns" 
            :key="index" 
            class="step-card"
            :class="{ 'active': activeSteps[index] }"
          >
            <div class="step-indicator">
              <div class="step-number">Step {{ index + 1 }}</div>
              <div class="step-line" v-if="index < sampleColumns.length - 1"></div>
            </div>
            
            <div class="step-content">
              <!-- 位置互换：步骤内容(Column)在左，关键词(Keywords)在右 -->
              <div class="step-header">
                <h3 class="step-title"><TextReveal :text="column" /></h3>
                <span class="step-column-tag"><TextReveal :text="keywords[index] || '关键步骤'" /></span>
              </div>

              <!-- 论文列表 -->
              <div class="papers-list" v-if="showPaperBox[index] === 1">
                <!-- 论文 1 (BM25) -->
                <div class="paper-item" v-if="paperData[index] && paperData[index].id">
                  <div class="paper-icon">📄</div>
                  <div class="paper-info">
                    <a 
                      :href="`https://arxiv.org/abs/${paperData[index].id}`" 
                      target="_blank" 
                      class="paper-title hover:text-indigo-600 transition-colors"
                    >
                      <TextReveal :text="paperData[index].title" /></a>
                    <div class="paper-abstract">
                      <strong>AI 摘要:</strong> <TextReveal :text="paperData[index].abstract" />
                    </div>
                  </div>
                </div>
                <div v-else class="no-paper">BM25 暂无论文数据</div>

                <!-- 论文 2 (S-BERT) -->
                <div class="paper-item" v-if="paper2Data[index] && paper2Data[index].id">
                  <div class="paper-icon">📑</div>
                  <div class="paper-info">
                    <a 
                      :href="`https://arxiv.org/abs/${paper2Data[index].id}`" 
                      target="_blank" 
                      class="paper-title hover:text-indigo-600 transition-colors"
                    >
                      <TextReveal :text="paper2Data[index].title" /></a>
                    <div class="paper-abstract">
                      <strong>AI 摘要:</strong> <TextReveal :text="paper2Data[index].abstract" />
                    </div>
                  </div>
                </div>
                 <div v-else class="no-paper">Sentence-BERT 暂无论文数据</div>
              </div>
              
              <div v-else class="no-paper-box">
                <span class="text-gray-400 text-sm italic">此步骤无需查阅额外论文</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
           <div class="text-center text-gray-400 py-10">
             <TextReveal :text="'请点击左侧按钮生成内容或刷新'" />
           </div>
        </div>

        <!-- 最后总结 -->
        <div class="final-summary-card" v-if="summary">
          <div class="summary-header">
            <span class="icon">📝</span> 学习总结
          </div>
          <div class="summary-body">
            <TextReveal :text="summary" />
          </div>
        </div>
      </div>
    
      <div class="chat-header">
        
        <!-- 模型选择器 -->
        <Popover v-model:open="modelSelectOpen">
            <PopoverTrigger as-child>
            <button class="model-tag-btn">
                <ModelIcon
                    class="w-3 h-3 mr-1"
                    :model-id="activeModel.providerId"
                    :is-dark="themeStore.isDark"
                ></ModelIcon>
                {{ name }}
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
            <button class="settings-btn ml-2">
                <Icon icon="lucide:settings-2" class="w-4 h-4" />
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

      
    </main>
  </div>
</template>

<style scoped>
/* 主容器样式 */
.app-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

/* 左侧边栏样式 */
.left-sidebar {
  width: 240px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  background: rgba(102, 126, 234, 0.1);
  color: #333;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateX(5px);
}

.nav-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.nav-btn.primary:hover {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}

.bottom-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 8px;
  font-size: 12px;
  color: #666;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4ade80;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* 主内容区域样式 */
.main-content {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.content-header {
  margin-bottom: 40px;
  text-align: center;
}

.topic-tag {
  display: inline-block;
  padding: 8px 16px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 15px;
}

.main-title {
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  transform: translateX(60px); /* 将标题向右移动10像素 */
}

/* 输入框区域样式 */
.input-section {
  margin-bottom: 40px;
}

.input-container {
  display: flex;
  gap: 15px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.topic-input {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
}

.topic-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* AI推荐区域样式 */
.ai-recommendation-section {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.recommendation-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.recommendation-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.recommendation-text {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
}

.recommendation-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag {
  padding: 8px 16px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: pointer;
}

.tag:hover {
  background: rgba(102, 126, 234, 0.2);
  transform: translateY(-2px);
}

.refresh-recommendation-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 8px;
  background: white;
  color: #667eea;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
}

.refresh-recommendation-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  border-color: #667eea;
}

/* 加载状态样式 */
.loading-overlay {
  position: fixed;
  top: 20px;
  right: 20px;
  left: auto;
  bottom: auto;
  background-color: transparent;
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  z-index: 1000;
  /* 移除背景模糊效果 */
}

.loading-content {
  background-color: transparent;
  padding: 10px;
  border-radius: 0;
  box-shadow: none;
  text-align: left;
  animation: none;
}

.loading-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 10px 0 0;
  display: inline-block;
  vertical-align: middle;
}

.loading-text {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin: 0;
  display: inline-block;
  vertical-align: middle;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 5px 10px;
  border-radius: 4px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 图标样式 */
.icon {
  font-size: 18px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .left-sidebar {
    width: 100%;
    height: auto;
    flex-direction: row;
    padding: 15px 20px;
  }
  
  .nav-menu {
    flex-direction: row;
    flex: 1;
  }
  
  .main-content {
    padding: 20px;
  }
  
  .input-container {
    flex-direction: column;
  }
}
</style>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import ChatInput from './chat-input/ChatInput.vue'
import { Popover, PopoverContent, PopoverTrigger } from '@shadcn/components/ui/popover'
import ScrollablePopover from './ScrollablePopover.vue'
import { Button } from '@shadcn/components/ui/button' // 保留引用以防子组件需要，虽模板中主要用原生css
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

const configPresenter = usePresenter('configPresenter')
const threadPresenter = usePresenter('threadPresenter')
const themeStore = useThemeStore()
const router = useRouter()

interface PreferredModel {
  modelId: string
  providerId: string
}

const { t } = useI18n()
const chatStore = useChatStore()
const settingsStore = useSettingsStore()
const customText = ref('');
const customTextError = ref('');
const sampleTitle = ref('');
const sampleColumns = ref<string[]>([]);
const activeModel = ref({
  name: '',
  id: '',
  providerId: '',
  tags: [],
  type: ModelType.Chat
} as {
  name: string
  id: string
  providerId: string
  tags: string[]
  type: ModelType
})

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

// 加载状态
const loadingStatus = ref<string | null>(null)
// 定时器ID
let loadingStatusTimer: NodeJS.Timeout | null = null

// 步骤计数器
// 设置加载状态并添加超时监控
const setLoadingStatus = (status: string, step?: number) => {
  // 清除之前的定时器
  if (loadingStatusTimer) {
    clearTimeout(loadingStatusTimer)
    loadingStatusTimer = null
  }
  

  // 更新状态，添加步骤信息
  const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false })
  const detailedStatus = `${status} (${timestamp})`
  loadingStatus.value = detailedStatus
  
  // 设置新的定时器，0.5秒后检查状态是否改变
  loadingStatusTimer = setTimeout(() => {
    // 如果状态仍然是当前设置的状态，则显示"查询论文中"
    if (loadingStatus.value === detailedStatus) {
      loadingStatus.value = `查询论文中... (${new Date().toLocaleTimeString('zh-CN', { hour12: false })})`
    }
    loadingStatusTimer = null
  }, 4000)
}

const name = computed(() => {
  return activeModel.value?.name ? activeModel.value.name.split('/').pop() : '选择模型'
})

watch(
  () => activeModel.value,
  async () => {
    const config = await configPresenter.getModelDefaultConfig(
      activeModel.value.id,
      activeModel.value.providerId
    )
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
  }
)

const initialized = ref(false)

const findEnabledModel = (providerId: string, modelId: string) => {
  for (const provider of settingsStore.enabledModels) {
    if (provider.providerId === providerId) {
      for (const model of provider.models) {
        if (model.id === modelId) {
          return { model, providerId: provider.providerId }
        }
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

const setActiveFromEnabled = (m: {
  name: string
  id: string
  providerId: string
  type?: ModelType
}) => {
  activeModel.value = {
    name: m.name,
    id: m.id,
    providerId: m.providerId,
    tags: [],
    type: m.type ?? ModelType.Chat
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
      .sort((a, b) => (b!.updatedAt || 0) - (a!.updatedAt || 0))[0] as
      | typeof pinnedFirst
      | undefined
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
    const preferredModel = (await configPresenter.getSetting('preferredModel')) as
      | PreferredModel
      | undefined
    if (preferredModel?.modelId && preferredModel?.providerId) {
      const match = findEnabledModel(preferredModel.providerId, preferredModel.modelId)
      if (match) {
        setActiveFromEnabled({ ...match.model, providerId: match.providerId })
        initialized.value = true
        return
      }
    }
  } catch (error) {
    console.warn('Failed to get user preferred model:', error)
  }

  const first = pickFirstEnabledModel()
  if (first) {
    setActiveFromEnabled(first)
    initialized.value = true
  }
}

watch(
  () => settingsStore.enabledModels,
  async () => {
    if (!initialized.value) {
      await initActiveModel()
      return
    }

    const current = activeModel.value
    if (!current?.id || !current?.providerId) {
      const first = pickFirstEnabledModel()
      if (first) setActiveFromEnabled(first)
      return
    }
    const stillExists = !!findEnabledModel(current.providerId, current.id)
    if (!stillExists) {
      const first = pickFirstEnabledModel()
      if (first) setActiveFromEnabled(first)
    }
  },
  { immediate: false, deep: true }
)

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
// 添加视图切换状态变量
const showMessageListUI = ref(false);

// 监听sampleColumns变化，当有数据时开始依次显示步骤卡片
watch(() => sampleColumns.value, (newColumns) => {
  if (newColumns.length > 0) {
    // 重置步骤状态
    activeSteps.value = Array(newColumns.length).fill(false);
    
    // 依次激活每个步骤卡片
    newColumns.forEach((_, index) => {
      setTimeout(() => {
        activeSteps.value[index] = true;
      }, index * 7000); // 每个步骤间隔2000ms显示
    });
  }
}, { deep: true }); // 移除immediate: true，避免组件初始化时自动触发动画

// Functionality
const handleDifficultyButtonClick = (difficulty: string) => {
  isDifficultyClicked.value = difficulty;
  
  const notification = document.createElement('div');
  notification.className = `fixed top-4 right-4 px-4 py-2 rounded-md text-white font-medium transition-opacity duration-300 z-50 ${difficulty === '难' ? 'bg-red-500' : 'bg-green-500'}`;
  notification.textContent = `已标记为${difficulty}`;
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.opacity = '0';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 2000);
  
  console.log(`用户标记当前内容为: ${difficulty}`);
}

const handleModelUpdate = (model: MODEL_META, providerId: string) => {
  activeModel.value = {
    name: model.name,
    id: model.id,
    providerId: providerId,
    tags: [],
    type: model.type ?? ModelType.Chat
  }
  chatStore.updateChatConfig({
    modelId: model.id,
    providerId: providerId
  })

  configPresenter.setSetting('preferredModel', {
    modelId: model.id,
    providerId: providerId
  })

  modelSelectOpen.value = false
}


// Deep link and initialization Logic
watch(
  () => chatStore.deeplinkCache,
  (newCache) => {
    if (newCache) {
      if (newCache.modelId) {
        const matchedModel = settingsStore.findModelByIdOrName(newCache.modelId)
        if (matchedModel) {
          handleModelUpdate(matchedModel.model, matchedModel.providerId)
        }
      }
      if (newCache.msg || newCache.mentions) {
        const setInputContent = () => {
          if (chatInputRef.value) {
            const chatInput = chatInputRef.value
            chatInput.clearContent()
            if (newCache.mentions) {
              newCache.mentions.forEach((mention) => {
                chatInput.appendMention(mention)
              })
            }
            if (newCache.msg) {
              chatInput.appendText(newCache.msg)
            }
            return true
          }
          return false
        }

        if (!setInputContent()) {
          nextTick(() => {
            if (!setInputContent()) {
              setTimeout(() => {
                if (!setInputContent()) {
                  console.warn('[NewThread] Failed to set input content after retries')
                }
              }, 100)
            }
          })
        }
      }
      if (newCache.systemPrompt) {
        systemPrompt.value = newCache.systemPrompt
      }
      if (newCache.autoSend && newCache.msg) {
        handleSend({
          text: newCache.msg || '',
          files: [],
          links: [],
          think: false,
          search: false
        })
      }
      chatStore.clearDeeplinkCache()
    }
  },
  { immediate: true }
)

onMounted(async () => {
  configPresenter.getDefaultSystemPrompt().then((prompt) => {
    systemPrompt.value = prompt
  })
  await initActiveModel()
  
  try {
    const fileContent = await window.api.readLocalFile('custom-welcome.txt');
    if (fileContent) {
      customText.value = fileContent.trim();
    }
  } catch (error) {
    console.error('读取自定义欢迎文本失败:', error);
    customTextError.value = '无法读取自定义欢迎文本';
  }
  
  // Read sample.txt
  try {
    const sampleFileContent = await window.api.readLocalFile('sample.txt');
    if (sampleFileContent) {
      const lines = sampleFileContent.trim().split('\n').filter(line => line.trim() !== '');
      if (lines.length > 0) {
        sampleTitle.value = lines[0].trim();
        if (lines.length >= 6) {
          sampleColumns.value = lines.slice(1, 6).map(line => line.trim());
        }
        if (lines.length >= 11) {
          showPaperBox.value = lines.slice(6, 11).map(line => parseInt(line.trim()) || 0);
        }
        if (lines.length >= 16) {
          keywords.value = lines.slice(11, 16).map(line => line.trim());
        }
        if (lines.length >= 17) {
          summary.value = lines[16].trim();
        }
        
        // 初始化步骤卡片状态为未激活，不触发动画
        activeSteps.value = Array(sampleColumns.value.length).fill(false);
      }
    }
  } catch (error) {
    console.error('读取sample.txt失败:', error);
  }
  
  // Read paper.txt
  try {
    const paperFileContent = await window.api.readLocalFile('paper.txt');
    if (paperFileContent) {
      const lines = paperFileContent.trim().split('\n').filter(line => line.trim() !== '');
      const newPaperData: Array<{id: string, title: string, abstract: string}> = [];
      for (let i = 0; i < 5; i++) {
        const idIndex = i * 3;
        const titleIndex = idIndex + 1;
        const abstractIndex = idIndex + 2;
        if (idIndex < lines.length && titleIndex < lines.length && abstractIndex < lines.length) {
          newPaperData.push({
            id: lines[idIndex].trim(),
            title: lines[titleIndex].trim(),
            abstract: lines[abstractIndex].trim()
          });
        }
      }
      paperData.value = newPaperData;
    }
  } catch (error) {
    console.error('读取paper.txt失败:', error);
  }
  
  // Read paper2.txt
  try {
    const paper2FileContent = await window.api.readLocalFile('paper2.txt');
    if (paper2FileContent) {
      const lines = paper2FileContent.trim().split('\n').filter(line => line.trim() !== '');
      const newPaper2Data: Array<{id: string, title: string, abstract: string}> = [];
      for (let i = 0; i < 5; i++) {
        const idIndex = i * 3;
        const titleIndex = idIndex + 1;
        const abstractIndex = idIndex + 2;
        if (idIndex < lines.length && titleIndex < lines.length && abstractIndex < lines.length) {
          newPaper2Data.push({
            id: lines[idIndex].trim(),
            title: lines[titleIndex].trim(),
            abstract: lines[abstractIndex].trim()
          });
        }
      }
      paper2Data.value = newPaper2Data;
    }
  } catch (error) {
    console.error('读取paper2.txt失败:', error);
  }
})

// Original Action Handlers (Kept exactly as logic requires)
const handleActionButtonClick = async () => {
  try {
    const fileContent = await window.api.readLocalFile('user-preferences.txt');
    if (fileContent) {
      const queryMessage = `请你用arxiv-mcp-server的工具查找三篇和${fileContent}有关的论文，要新一点，sort_by参数为date。你的回答应该遵循以下格式，每行小标题加粗：标题：此处为对应标题\n摘要：此处为对应摘要，中文，控制在二十字以内\n链接：此处为对应论文链接`;
      await handleSend({
        text: queryMessage,
        files: [],
        links: [],
        think: false,
        search: false
      });
    } else {
      alert('用户偏好文件内容为空，请检查项目根目录下的user-preferences.txt文件');
    }
  } catch (error) {
    alert(`读取或发送消息失败: ${(error as Error).message || '未知错误'}`);
  }
};

// API Call Functions (BM25 & SentenceBert)
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
  } catch (err) {
    console.warn(`BM25调用失败: ${err}`);
    return [];
  }
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
  } catch (err) {
    console.warn(`Sentence-BERT调用失败: ${err}`);
    return [];
  }
};

const handleRefreshButtonClick = async () => {
  console.log('刷新按钮被点击');
  try {
    alert('开始执行问题生成，将等待30秒后处理...');
    
    // Read Sample
    let sampleContent = '';
    try {
      sampleContent = await window.api.readLocalFile('output.txt');
    } catch (err) {
      alert('无法读取sample.txt文件');
      return;
    }
    
    const lines = sampleContent.split('\n');
    let paperContent: string[][] = [];
    let paperContent2: string[][] = [];
    let hasValidCalls = false;

    const checkLineAndCallApi = async (lineIndex: number, paramLineIndex: number, lineNum: number, paramLineNum: number, paperContentIndex: number) => {
      while (paperContent.length <= paperContentIndex) paperContent.push([]);
      while (paperContent2.length <= paperContentIndex) paperContent2.push([]);
      
      if (lines.length > lineIndex) {
        const lineContent = lines[lineIndex].trim();
        if (lineContent === '1') {
          if (lines.length > paramLineIndex) {
            const queryParam = lines[paramLineIndex].trim();
            if (queryParam) {
              // BM25
              const bm25Response = await callBM25Api(queryParam);
              if (bm25Response && bm25Response.length > 0) {
                const paper = bm25Response[0];
                paperContent[paperContentIndex] = [paper.id || '未知ID', paper.title || '无标题', paper.original_abstract || '无摘要'];
                hasValidCalls = true;
              }
              // Sentence-BERT
              try {
                const sentenceBertResponse = await callSentenceBertApi(queryParam);
                if (sentenceBertResponse && sentenceBertResponse.length > 0) {
                  const paper = sentenceBertResponse[0];
                  paperContent2[paperContentIndex] = [paper.id || '未知ID', paper.title || '无标题', paper.original_abstract || '无摘要'];
                }
              } catch (sentenceError) { console.error(sentenceError) }
            }
          }
        } else if (lineContent === '0') {
           paperContent[paperContentIndex] = ['1', '1', '1'];
           paperContent2[paperContentIndex] = ['1', '1', '1'];
           hasValidCalls = true;
        }
      }
    };
    
    // Process lines 7-11
    await checkLineAndCallApi(6, 11, 7, 12, 1);
    await checkLineAndCallApi(7, 12, 8, 13, 2);
    await checkLineAndCallApi(8, 13, 9, 14, 3);
    await checkLineAndCallApi(9, 14, 10, 15, 4);
    await checkLineAndCallApi(10, 15, 11, 16, 5);
    
    if (!hasValidCalls) {
      paperContent = [
        ['default-id-1', '默认论文标题1', '摘要1'],
        ['1']
      ];
    }
    
    const flattenedContent: string[] = []; 
    const flattenedContent2: string[] = [];
    paperContent.forEach(subArray => subArray.forEach(line => flattenedContent.push(line)));
    paperContent2.forEach(subArray => subArray.forEach(line => flattenedContent2.push(line)));
    
    try {
      await window.api.writeLocalFile('paper.txt', flattenedContent.join('\n'));
      await window.api.writeLocalFile('paper2.txt', flattenedContent2.join('\n'));
      alert('文件已成功更新');
    } catch (error) {
      alert('写入文件失败');
    }
  } catch (error) {
    alert(`操作失败: ${(error as Error).message}`);
  }
};

const handleQuestionGenerateClick = () => {
  router.push('/question')
}

const handleBackToHome = () => {
  router.push('/chat')
}

const handleStudyReportClick = () => {
  router.push('/study-report')
}

// Token helper
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

const handleProcessNewsAndGenerateQuestions = async () => {
  try {
    
    
    
    // 显示AI思考中状态 - 更详细的描述
    setLoadingStatus('AI正在分析任务需求，准备处理新闻内容...', 1);
    
    const newsQuery = `用fetch,url=https://news.aibase.cn/news,max_length=500,结果只包含三条最重要的新闻总结,每条30字以内,不要有其他内容`;
    const tabId = window.api.getWebContentsId();
    
    // 显示正在从aibase.cn查找资料状态 - 更详细的描述
    setTimeout(() => {
      // 检查是否已经超时显示"查询论文中"
      if (!loadingStatus.value?.includes('查询论文中')) {
        setLoadingStatus('正在从aibase.cn获取最新科技新闻，筛选重要信息...');
      }
    }, 800);
    


    // 1. Fetch News
    setLoadingStatus('正在创建新闻处理会话，准备调用AI模型获取新闻数据...');
    
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
    
    setLoadingStatus('正在发送新闻查询请求到aibase.cn，获取最新AI科技资讯...');
    
    await threadPresenter.sendMessage(newsThreadId, JSON.stringify({
      text: newsQuery, files: [], links: [], think: false, search: false
    }), "user");
    
    setLoadingStatus('正在等待AI模型处理新闻数据，提取关键信息和核心内容...');
    
    await threadPresenter.startStreamCompletion(newsThreadId, undefined, {});

    // Helper to get text
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

    


    let newsContent = '';
    // Polling logic (simplified for brevity, original logic preserved in spirit)
    setLoadingStatus('正在轮询获取新闻处理结果，解析和整理关键信息...');
    
    //await new Promise(r => setTimeout(r, 4000));
    const msgsRes: any = await threadPresenter.getMessages(newsThreadId, 1, 100);
    const assistantMsg = msgsRes?.list?.find((m: any) => m.role === 'assistant' && m.content && m.content.length > 0);
    if(assistantMsg) newsContent = extractAssistantText(assistantMsg);

    if (!newsContent) { 
      alert('未获取到新闻内容'); 
      loadingStatus.value = null;
      // 清除定时器
      if (loadingStatusTimer) {
        clearTimeout(loadingStatusTimer)
        loadingStatusTimer = null
      }
      return; 
    }
    
    // 显示获取到的新闻内容摘要
    const newsSummary = newsContent.substring(0, 100) + '...'
    setLoadingStatus(`新闻获取完成：${newsSummary}，正在准备生成结构化问题...`);
    
    newsContent = truncateTextToTokens(newsContent, 300);

    // 2. Generate Structure
    const systemPromptForQuestionGeneration = `你是一个专业的AI助手。请从新闻中提取信息并生成结构化问题。`;
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
请基于上述要求，处理我提供的新闻内容，完整输出选中关键词对应的大框架问题、子过程、是否推荐、专业词汇、总结等信息。
输出示例：
DeepSeekMath - V2 模型实现奥数金牌级数学能力的核心技术实现过程和关键要点是什么收集国际奥数等多类高难度数学竞赛真题构建专项训练数据集基于深度学习框架搭建适配数学推理的模型网络架构与参数体系采用定理证明专项训练法强化模型对复杂数学逻辑的推导能力通过多轮竞赛真题测试迭代优化模型的解题准确率与步骤规范性开展跨竞赛场景适配测试确保模型在不同数学赛事场景的通用性11100Mathematical competition dataset constructionDeep learning network architectureTheorem - proving specialized trainingModel accuracy iterative optimizationCross - competition scenario adaptation testing先收集多类高难度数学竞赛真题构建专项数据集，再搭建适配数学推理的深度学习网络架构，接着通过定理证明专项训练强化模型逻辑推导能力，随后依托多轮真题测试优化解题准确率，最后经跨竞赛场景测试保障通用性，以此实现 DeepSeekMath - V2 模型达到奥数金牌级的数学解题能力。
`;

    setLoadingStatus('正在创建问题生成会话，配置AI模型参数准备分析新闻内容...');
    
    const questionThreadId = await threadPresenter.createConversation('新闻问题生成', {
          providerId: activeModel.value.providerId,
          modelId: activeModel.value.id,
          systemPrompt: systemPromptForQuestionGeneration,
          temperature: 0.3, 
          contextLength: 16000,
          maxTokens: 1000,
          verbosity: 0,
          enabledMcpTools: chatStore.chatConfig.enabledMcpTools
    } as any, tabId);

    setLoadingStatus('正在准备详细的问题生成指令，结合新闻内容和分析要求...');
    
    const combinedText = `${detailedInstructions}\n\n${newsContent}`;
    
    setLoadingStatus('正在发送问题生成请求，AI将提取核心技术要点和关键词...');
    
    await threadPresenter.sendMessage(questionThreadId, JSON.stringify({
        text: combinedText, files: [], links: [], think: false, search: false
    }), "user");
    
    setLoadingStatus('正在深度分析新闻内容，生成结构化问题框架和子问题...');
    
    await threadPresenter.startStreamCompletion(questionThreadId, undefined, {});

    // Polling for structure
    let questionStructure = '';
    // Polling logic with status update
    setLoadingStatus('正在轮询获取问题生成结果，整理和优化最终问题结构...');
    
    //await new Promise(r => setTimeout(r, 4000));
    const qMsgsRes: any = await threadPresenter.getMessages(questionThreadId, 1, 100);
    const qMsg = qMsgsRes?.list?.find((m: any) => m.role === 'assistant');
    if(qMsg) {
      questionStructure = extractAssistantText(qMsg);
      // 清除加载状态
      loadingStatus.value = null;
    }

    if (questionStructure) {
        let cleaned = questionStructure.replace(/关键词\d/g, '').split('\n').filter(l => l.trim() !== '').join('\n');
        setLoadingStatus('问题结构生成完成，正在保存到本地文件(output.txt)中...');
        await window.api.writeLocalFile('output.txt', cleaned);
        
        // 同时保存到sample.txt，以便在当前页面显示更新后的内容
        await window.api.writeLocalFile('sample.txt', cleaned);
        
        // 直接更新本地变量，避免重新读取文件
        const lines = cleaned.trim().split('\n').filter(line => line.trim() !== '');
        if (lines.length > 0) {
          sampleTitle.value = lines[0].trim();
          if (lines.length >= 6) {
            sampleColumns.value = lines.slice(1, 6).map(line => line.trim());
          }
          if (lines.length >= 11) {
            showPaperBox.value = lines.slice(6, 11).map(line => parseInt(line.trim()) || 0);
          }
          if (lines.length >= 16) {
            keywords.value = lines.slice(11, 16).map(line => line.trim());
          }
          if (lines.length >= 17) {
            summary.value = lines[16].trim();
          }
          
        }
        
        setLoadingStatus('结构化问题生成成功，步骤卡片正在更新...');

        // 切换到MessageList的UI视图
        showMessageListUI.value = true;
        // 短暂延迟以便用户看到最后一个状态
        setTimeout(() => {
          loadingStatus.value = null;
        }, 1000);
    } else {
        loadingStatus.value = null;
        //alert('未能生成问题结构');
    }
  } catch (error) {
    // 清除加载状态
    loadingStatus.value = null;
    // 清除定时器
    if (loadingStatusTimer) {
      clearTimeout(loadingStatusTimer)
      loadingStatusTimer = null
    }
    //alert(`处理失败: ${(error as Error).message}`);
  } finally {
    // 清除定时器
    if (loadingStatusTimer) {
      clearTimeout(loadingStatusTimer)
      loadingStatusTimer = null
    }
  }
}

const handleSend = async (content: UserMessageContent) => {
  const sampleFileContent = await window.api.readLocalFile('output.txt');
  const threadId = await chatStore.createThread(content.text, {
    providerId: activeModel.value.providerId,
    modelId: activeModel.value.id,
    systemPrompt: sampleFileContent,
    temperature: temperature.value,
    contextLength: contextLength.value,
    maxTokens: maxTokens.value,
    artifacts: artifacts.value as 0 | 1,
    thinkingBudget: thinkingBudget.value,
    enableSearch: enableSearch.value,
    forcedSearch: forcedSearch.value,
    searchStrategy: searchStrategy.value,
    reasoningEffort: reasoningEffort.value,
    verbosity: verbosity.value,
    enabledMcpTools: chatStore.chatConfig.enabledMcpTools
  } as any)
  chatStore.sendMessage(content)
}
</script>

<style scoped>
/* 
  全局布局设置 - 来自目标UI
*/
.app-container {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #f4f6f9;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  color: #333;
  overflow: hidden;
}

/* 1. 左侧侧边栏样式 */
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

/* 2. 中间内容区样式 */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background-color: #f8fafc;
}

.content-wrapper {
  padding: 40px;
  max-width: 1000px;
  margin: 0 auto;
}

/* 顶部 Header */
.content-header {
  margin-bottom: 40px;
  position: relative;
}

.topic-tag {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #6b7280;
  font-weight: 600;
  margin-bottom: 8px;
}

.main-title {
  font-size: 28px;
  font-weight: 800;
  color: #111827;
  line-height: 1.3;
  margin-bottom: 16px;
  padding-right: 150px; /* 留出右上角空间 */
}

/* 难度控制器样式 */
.difficulty-controls {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}

.difficulty-badge {
  display: inline-flex;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.difficulty-badge.hard {
  background-color: #fff1f2;
  color: #e11d48;
  border-color: #fecdd3;
}
.difficulty-badge.hard.active, .difficulty-badge.hard:hover {
    background-color: #e11d48;
    color: white;
}

.difficulty-badge.simple {
  background-color: #ecfdf5;
  color: #059669;
  border-color: #a7f3d0;
}
.difficulty-badge.simple.active, .difficulty-badge.simple:hover {
    background-color: #059669;
    color: white;
}

/* 步骤卡片 */
.steps-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.step-card {
  display: flex;
  gap: 20px;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.step-card.active {
  opacity: 1;
  transform: translateY(0);
}

/* 为步骤线添加动画 */
.step-line {
  opacity: 0;
  height: 0;
  transition: opacity 0.3s ease, height 0.3s ease;
  transition-delay: 0.3s;
}

.step-card.active .step-line {
  opacity: 1;
  height: 100%;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
}

.step-number {
  background-color: #4f46e5;
  color: white;
  font-size: 12px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 6px;
  z-index: 2;
  white-space: nowrap;
}

.step-line {
  flex: 1;
  width: 2px;
  background-color: #e5e7eb;
  margin-top: 8px;
  margin-bottom: -38px;
}

.step-content {
  flex: 1;
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
  border: 1px solid #f3f4f6;
  transition: transform 0.2s;
  min-width: 0; /* 防止子元素溢出 */
}

.step-content:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid #f3f4f6;
  padding-bottom: 12px;
}

.step-title {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.step-column-tag {
  background-color: #e0e7ff;
  color: #4338ca;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.papers-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.paper-item {
  display: flex;
  gap: 12px;
  background-color: #f9fafb;
  padding: 12px;
  border-radius: 8px;
}

.paper-icon {
  font-size: 20px;
}

.paper-info {
  flex: 1;
  min-width: 0; /* 防止文本溢出 */
}

.paper-title {
  display: block;
  margin: 0 0 6px 0;
  font-size: 15px;
  color: #111827;
  font-weight: 600;
  text-decoration: none;
}

.paper-abstract {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.5;
  background: #fff;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
}

.no-paper, .no-paper-box {
  font-size: 13px;
  color: #9ca3af;
  font-style: italic;
  padding: 10px;
  text-align: center;
  background: #f9fafb;
  border-radius: 8px;
}

.final-summary-card {
  margin-top: 40px;
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%);
  color: white;
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
}

.summary-header {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.summary-body {
  font-size: 15px;
  line-height: 1.6;
  opacity: 0.95;
}

/* 3. 右侧侧边栏样式 */
.right-sidebar {
  width: 340px;
  background-color: #ffffff;
  border-left: 1px solid #e1e4e8;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  position: relative;
  z-index: 10;
}

.chat-header {
  padding: 20px;
  border-radius: 12px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  gap: 15px;
  margin: 0 auto;
  max-width: 1000px;
  margin-top: 20px;
  margin-bottom: 20px;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.model-tag-btn {
  display: flex;
  align-items: center;
  font-size: 14px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 10px 16px;
  border-radius: 8px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}
.model-tag-btn:hover {
    background: rgba(102, 126, 234, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.2);
}

.settings-btn {
    color: #667eea;
    background: rgba(102, 126, 234, 0.1);
    border: 2px solid rgba(102, 126, 234, 0.3);
    cursor: pointer;
    padding: 10px 16px;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-size: 14px;
    font-weight: 500;
}
.settings-btn:hover {
    background: rgba(102, 126, 234, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.2);
}

.chat-history-placeholder {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    padding-bottom: 100px;
    background: #fff;
}

.welcome-msg {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}
.welcome-msg .avatar {
    width: 32px;
    height: 32px;
    background: #eff6ff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.welcome-msg .bubble-text {
    background-color: #f3f4f6;
    color: #1f2937;
    padding: 10px 14px;
    border-radius: 12px;
    border-top-left-radius: 2px;
    font-size: 13px;
    line-height: 1.4;
}

/* 底部输入框区域 - 适配 ChatInput 组件 */
.input-area {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  background: white;
  border-top: 1px solid #f3f4f6;
  z-index: 20;
}

/* 覆盖 ChatInput 内部的一些默认样式使其更贴合边栏 */
:deep(.chat-input-container) {
    border-color: #e5e7eb !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
:deep(textarea) {
    font-size: 13px !important;
    padding: 8px !important;
}

/* 滚动条美化 */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #9ca3af; }
</style>