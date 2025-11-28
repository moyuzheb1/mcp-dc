<template>
  <div class="app-container">
    <!-- 1. 左侧功能导航栏 (Left Sidebar) -->
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
      </nav>

      <div class="bottom-status">
        <span class="status-dot"></span> 在线
      </div>
    </aside>

    <!-- 2. 中间主要内容区 (Main Content) -->
    <main class="main-content">
      <div class="content-wrapper">
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
              {{ isDifficultyClicked === '难' ? '已标记：难' : '标记为难' }}
            </button>
            <button 
              @click="handleDifficultyButtonClick('简单')"
              class="difficulty-badge"
              :class="isDifficultyClicked === '简单' ? 'simple active' : 'simple'"
            >
               {{ isDifficultyClicked === '简单' ? '已标记：简单' : '标记为简单' }}
            </button>
          </div>
        </header>

        <!-- 核心功能：5个步骤拆解 -->
        <div class="steps-container" v-if="sampleColumns.length > 0">
          <div v-for="(column, index) in sampleColumns" :key="index" class="step-card">
            <div class="step-indicator">
              <div class="step-number">Step {{ index + 1 }}</div>
              <div class="step-line" v-if="index < sampleColumns.length - 1"></div>
            </div>
            
            <div class="step-content">
              <!-- 位置互换：步骤内容(Column)在左，关键词(Keywords)在右 -->
              <div class="step-header">
                <h3 class="step-title">{{ column }}</h3>
                <span class="step-column-tag">{{ keywords[index] || '关键步骤' }}</span>
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
                      {{ paperData[index].title }}
                    </a>
                    <div class="paper-abstract">
                      <strong>AI 摘要:</strong> {{ paperData[index].abstract }}
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
                      {{ paper2Data[index].title }}
                    </a>
                    <div class="paper-abstract">
                      <strong>S-BERT 摘要:</strong> {{ paper2Data[index].abstract }}
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
             请点击左侧按钮生成内容或刷新
           </div>
        </div>

        <!-- 最后总结 -->
        <div class="final-summary-card" v-if="summary">
          <div class="summary-header">
            <span class="icon">📝</span> 学习总结
          </div>
          <div class="summary-body">
            {{ summary }}
          </div>
        </div>
      </div>
    </main>

    <!-- 3. 右侧 AI 助手/搜索栏 (Right Sidebar) -->
    <aside class="right-sidebar">
      <div class="chat-header">
        <h3>AI 助手</h3>
        
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

      <!-- 聊天记录区域 -->
      <div class="chat-message-area relative flex-1 min-h-0">
         <div
            ref="messagesContainer"
            class="message-list-container relative flex-1 scrollbar-hide overflow-y-auto w-full h-full px-4"
            @scroll="handleScroll"
        >
            <div class="welcome-msg mt-4" v-if="messages.length === 0">
                <div class="avatar">🤖</div>
                <div class="bubble">
                    <div class="bubble-text">你好！我是你的论文助手。如果你对左侧的步骤有疑问，或者想搜索新问题，请随时在下方输入。</div>
                </div>
            </div>

            <div
                ref="messageList"
                class="w-full break-all transition-opacity duration-300 pt-4 pb-20"
                :class="{ 'opacity-0': !visible }"
            >
                <div
                    v-for="(msg, index) in messages"
                    :key="msg.id"
                    @mouseenter="minimap.handleHover(msg.id)"
                    @mouseleave="minimap.handleHover(null)"
                >
                    <MessageItemAssistant
                        v-if="msg.role === 'assistant'"
                        :ref="retry.setAssistantRef(index)"
                        :message="msg as AssistantMessage"
                        :is-capturing-image="capture.isCapturing.value"
                        @copy-image="handleCopyImage"
                        @variant-changed="scrollToMessage"
                    />
                    <MessageItemUser
                        v-else-if="msg.role === 'user'"
                        :message="msg as UserMessage"
                        @retry="handleRetry(index)"
                        @scroll-to-bottom="scrollToBottom"
                    />
                </div>
            </div>
            <div ref="scrollAnchor" class="h-8" />
        </div>

        <!-- 消息操作按钮 -->
        <template v-if="!capture.isCapturing.value">
            <MessageActionButtons
                class="absolute bottom-4 right-4 z-30"
                :show-clean-button="!showCancelButton && messages.length > 0"
                :show-scroll-button="aboveThreshold"
                @clean="cleanDialog.open"
                @scroll-to-bottom="scrollToBottom(true)"
            />
        </template>
        
        <ReferencePreview
            class="pointer-events-none"
            :show="referenceStore.showPreview"
            :content="referenceStore.currentReference"
            :rect="referenceStore.previewRect"
        />
        <MessageMinimap
            v-if="messages.length > 0"
            :messages="messages"
            :hovered-message-id="minimap.hoveredMessageId.value"
            :scroll-info="minimap.scrollInfo"
            @bar-hover="minimap.handleHover"
            @bar-click="minimap.handleClick"
        />
      </div>

      <!-- 底部固定输入框 -->
      <div class="input-area">
         <ChatInput
            ref="chatInputRef"
            key="newThread"
            variant="newThread"
            class="flex-1"
            :rows="1"
            :max-rows="5"
            :context-length="contextLength"
            @send="handleSend"
            placeholder="在此输入您的问题..." 
        >
            <template #addon-actions><span></span></template>
        </ChatInput>
      </div>
    </aside>

    <!-- 清理对话框 -->
    <Dialog v-model:open="cleanDialog.isOpen.value">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{{ t("dialog.cleanMessages.title") }}</DialogTitle>
          <DialogDescription>
            {{ t("dialog.cleanMessages.description") }}
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" @click="cleanDialog.cancel">{{
            t("dialog.cancel")
          }}</Button>
          <Button variant="destructive" @click="cleanDialog.confirm">{{
            t("dialog.cleanMessages.confirm")
          }}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
// === Imports ===
import { ref, onMounted, nextTick, watch, computed, toRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'
import { useResizeObserver } from "@vueuse/core"

// Logic & Stores
import { useChatStore } from '@/stores/chat'
import { useSettingsStore } from '@/stores/settings'
import { useThemeStore } from '@/stores/theme'
import { useReferenceStore } from "@/stores/reference"
import { usePresenter } from '@/composables/usePresenter'
import { MODEL_META } from '@shared/presenter'
import { ModelType } from '@shared/model'
import { AssistantMessage, UserMessage, UserMessageContent } from "@shared/chat"

// === 修改了这里的引用路径：使用 ../ 返回上一级目录 ===
// Components that are likely in parent folder
import ChatInput from '../chat-input/ChatInput.vue' 
import ScrollablePopover from '../ScrollablePopover.vue'
import ModelSelect from '../ModelSelect.vue'
import ChatConfig from '../ChatConfig.vue'
import ModelIcon from '../icons/ModelIcon.vue' 

// Components that are likely in CURRENT folder (message/)
import MessageItemAssistant from "./MessageItemAssistant.vue"
import MessageItemUser from "./MessageItemUser.vue"
import MessageActionButtons from "./MessageActionButtons.vue"
import ReferencePreview from "./ReferencePreview.vue"
import MessageMinimap from "./MessageMinimap.vue"

// Shadcn Components (Paths usually aliased, keep as is)
import { Popover, PopoverContent, PopoverTrigger } from '@shadcn/components/ui/popover'
import { Button } from '@shadcn/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@shadcn/components/ui/dialog"

// Composables
import { useMessageScroll } from "@/composables/message/useMessageScroll"
import { useCleanDialog } from "@/composables/message/useCleanDialog"
import { useMessageMinimap } from "@/composables/message/useMessageMinimap"
import { useMessageCapture } from "@/composables/message/useMessageCapture"
import { useMessageRetry } from "@/composables/message/useMessageRetry"

// === Setup & Props ===
const { t } = useI18n()
const router = useRouter()
const chatStore = useChatStore()
const settingsStore = useSettingsStore()
const themeStore = useThemeStore()
const referenceStore = useReferenceStore()
const configPresenter = usePresenter('configPresenter')
const threadPresenter = usePresenter('threadPresenter')

// Props
const props = defineProps<{
  messages: Array<UserMessage | AssistantMessage>;
}>();

// === Data Logic ===
const sampleTitle = ref('');
const sampleColumns = ref<string[]>([]);
const keywords = ref<string[]>([])
const summary = ref<string>('')
const showPaperBox = ref<number[]>([0, 0, 0, 0, 0])
// 显式定义数组类型以修复 TS 报错
const paperData = ref<Array<{id: string, title: string, abstract: string}>>([])
const paper2Data = ref<Array<{id: string, title: string, abstract: string}>>([])
const isDifficultyClicked = ref<string | null>(null)

// === Model Logic ===
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
const modelSelectOpen = ref(false)
const settingsPopoverOpen = ref(false)
const chatInputRef = ref<InstanceType<typeof ChatInput> | null>(null)

// Config refs
const temperature = ref(0.6)
const contextLength = ref(16384)
const maxTokens = ref(4096)
const contextLengthLimit = ref(16384)
const maxTokensLimit = ref(4096)
const systemPrompt = ref('')
const artifacts = ref(settingsStore.artifactsEffectEnabled ? 1 : 0)
const thinkingBudget = ref<number | undefined>(undefined)
const enableSearch = ref<boolean | undefined>(undefined)
const forcedSearch = ref<boolean | undefined>(undefined)
const searchStrategy = ref<'turbo' | 'max' | undefined>(undefined)
const reasoningEffort = ref<'minimal' | 'low' | 'medium' | 'high' | undefined>(undefined)
const verbosity = ref<'low' | 'medium' | 'high' | undefined>(undefined)

const name = computed(() => activeModel.value?.name ? activeModel.value.name.split('/').pop() : '选择模型')

// === Chat Message Logic ===
const scroll = useMessageScroll();
const {
  messagesContainer,
  scrollAnchor,
  aboveThreshold,
  scrollToBottom: scrollToBottomImmediate,
  scrollToMessage,
  handleScroll,
  updateScrollInfo,
  setupScrollObserver,
} = scroll;

const cleanDialog = useCleanDialog();
const minimap = useMessageMinimap(scroll.scrollInfo);
const capture = useMessageCapture();
const retry = useMessageRetry(toRef(props, "messages"));

const messageList = ref<HTMLDivElement>();
const visible = ref(false);
const shouldAutoFollow = ref(true);
const showCancelButton = computed(() => chatStore.generatingThreadIds.has(chatStore.getActiveThreadId() ?? ""));

const scheduleScrollToBottom = (force = false) => {
  nextTick(() => {
    const container = messagesContainer.value;
    if (!container) {
      scrollToBottomImmediate();
      shouldAutoFollow.value = true;
      return;
    }
    const shouldScroll = force || shouldAutoFollow.value;
    if (!shouldScroll) {
      updateScrollInfo();
      return;
    }
    scrollToBottomImmediate();
    if (force) shouldAutoFollow.value = true;
  });
};

const scrollToBottom = (force = false) => {
  if (force) shouldAutoFollow.value = true;
  scheduleScrollToBottom(force);
};

const handleCopyImage = async (messageId: string, parentId?: string, fromTop: boolean = false, modelInfo?: any) => {
  await capture.captureMessage({ messageId, parentId, fromTop, modelInfo });
};

const handleRetry = async (index: number) => {
  const triggered = await retry.retryFromUserMessage(index);
  if (triggered) scrollToBottom(true);
};

// === Initialization & Model Selection ===
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
  return settingsStore.enabledModels.flatMap((p) => p.models.map((m) => ({ ...m, providerId: p.providerId })))
    .find((m) => m.type === ModelType.Chat || m.type === ModelType.ImageGeneration)
}
const setActiveFromEnabled = (m: any) => {
  activeModel.value = { name: m.name, id: m.id, providerId: m.providerId, tags: [], type: m.type ?? ModelType.Chat }
}
const initActiveModel = async () => {
  if (chatStore.threads.length > 0) {
    // Attempt to restore model (simplified)
  }
  const first = pickFirstEnabledModel()
  if (first) setActiveFromEnabled(first)
}

watch(() => activeModel.value, async () => {
  const config = await configPresenter.getModelDefaultConfig(activeModel.value.id, activeModel.value.providerId)
  temperature.value = config.temperature ?? 0.7
  // ... other configs can be synced here if needed
})

// === Handlers ===
const handleDifficultyButtonClick = (difficulty: string) => {
  isDifficultyClicked.value = difficulty;
  // UI logic only
}
const handleRefreshButtonClick = async () => { 
  // Refresh logic placeholder (similar to original code)
}
const handleQuestionGenerateClick = () => router.push('/question')
const handleBackToHome = () => router.push('/chat')
const handleProcessNewsAndGenerateQuestions = async () => { /* ... */ }
const handleActionButtonClick = async () => { /* ... */ }

const handleModelUpdate = (model: MODEL_META, providerId: string) => {
  activeModel.value = { name: model.name, id: model.id, providerId, tags: [], type: model.type ?? ModelType.Chat }
  chatStore.updateChatConfig({ modelId: model.id, providerId })
  modelSelectOpen.value = false
}

const handleSend = async (content: UserMessageContent) => {
  await chatStore.createThread(content.text, {
    providerId: activeModel.value.providerId,
    modelId: activeModel.value.id,
    systemPrompt: systemPrompt.value,
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
  scrollToBottom(true)
}

// === Lifecycle Hooks ===
onMounted(async () => {
  // 1. Scroll & Message
  scheduleScrollToBottom(true);
  nextTick(() => {
    visible.value = true;
    setupScrollObserver();
    updateScrollInfo();
  });
  useResizeObserver(messageList, () => scheduleScrollToBottom());

  // 2. Read Local Files (Sample / Papers)
  try {
    const sampleFileContent = await window.api.readLocalFile('sample.txt');
    if (sampleFileContent) {
      const lines = sampleFileContent.trim().split('\n').filter(line => line.trim() !== '');
      if (lines.length > 0) {
        sampleTitle.value = lines[0].trim();
        if (lines.length >= 6) sampleColumns.value = lines.slice(1, 6).map(line => line.trim());
        if (lines.length >= 11) showPaperBox.value = lines.slice(6, 11).map(line => parseInt(line.trim()) || 0);
        if (lines.length >= 16) keywords.value = lines.slice(11, 16).map(line => line.trim());
        if (lines.length >= 17) summary.value = lines[16].trim();
      }
    }
  } catch (error) { console.error('Sample read error', error) }

  // 3. Read BM25 Papers (FIXED TS ERROR HERE)
  try {
    const paperFileContent = await window.api.readLocalFile('paper.txt');
    if (paperFileContent) {
      const lines = paperFileContent.trim().split('\n').filter(line => line.trim() !== '');
      // 显式指定类型，避免 never[] 推断错误
      const newPaperData: Array<{id: string, title: string, abstract: string}> = [];
      for (let i = 0; i < 5; i++) {
         const base = i * 3;
         if(base+2 < lines.length) {
             newPaperData.push({ id: lines[base], title: lines[base+1], abstract: lines[base+2] })
         }
      }
      paperData.value = newPaperData;
    }
  } catch (e) {}

  // 4. Read S-BERT Papers (FIXED TS ERROR HERE)
  try {
    const paper2FileContent = await window.api.readLocalFile('paper2.txt');
    if (paper2FileContent) {
       const lines = paper2FileContent.trim().split('\n').filter(line => line.trim() !== '');
       // 显式指定类型
       const newPaperData: Array<{id: string, title: string, abstract: string}> = [];
       for (let i = 0; i < 5; i++) {
         const base = i * 3;
         if(base+2 < lines.length) {
             newPaperData.push({ id: lines[base], title: lines[base+1], abstract: lines[base+2] })
         }
       }
       paper2Data.value = newPaperData;
    }
  } catch (e) {}

  // 5. Config Init
  configPresenter.getDefaultSystemPrompt().then(p => systemPrompt.value = p)
  await initActiveModel()
});

watch(() => props.messages.length, (length, prevLength) => {
    const isGrowing = length > prevLength;
    const isReset = prevLength > 0 && length < prevLength;
    if (isGrowing || isReset) scheduleScrollToBottom(isReset);
}, { flush: "post" });

// Expose
defineExpose({ scrollToBottom, scrollToMessage, aboveThreshold });
</script>

<style scoped>
/* 全局布局设置 */
.app-container {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #f4f6f9;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  color: #333;
  overflow: hidden;
}

/* 左侧侧边栏 */
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

/* 中间内容区 */
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
  padding-right: 150px;
}

/* 难度控制器 */
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
  min-width: 0;
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
  min-width: 0;
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

/* 右侧侧边栏 */
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
  padding: 16px 20px;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  flex-shrink: 0;
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
  font-size: 11px;
  background: #f3f4f6;
  color: #4b5563;
  padding: 4px 8px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}
.model-tag-btn:hover {
    background: #e5e7eb;
}
.settings-btn {
    color: #9ca3af;
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
}
.settings-btn:hover {
    background: #f3f4f6;
    color: #4b5563;
}
.chat-message-area {
    flex: 1;
    overflow: hidden;
    background: #fff;
    display: flex;
    flex-direction: column;
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

/* 输入框区域 */
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
:deep(.chat-input-container) {
    border-color: #e5e7eb !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
:deep(textarea) {
    font-size: 13px !important;
    padding: 8px !important;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #9ca3af; }

/* 消息高亮 */
.message-highlight {
  background-color: rgba(59, 130, 246, 0.1);
  border-left: 3px solid rgb(59, 130, 246);
  transition: all 0.3s ease;
}
.dark .message-highlight {
  background-color: rgba(59, 130, 246, 0.15);
}
</style>