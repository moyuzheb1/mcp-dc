<template>
  <div class="h-full w-full flex relative">
    <!-- 侧边栏 -->
    <div class="w-24 h-full bg-gradient-to-b from-gray-50/80 to-gray-100/80 dark:from-gray-900/90 dark:to-gray-800/90 border-r border-gray-200/50 dark:border-gray-700/50 flex flex-col items-center py-6 gap-6 backdrop-blur-sm">
      <!-- 第一行留空，未来放icon -->
      <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400/20 to-blue-400/20 border border-purple-200/30 dark:border-purple-700/30"></div>
      
      <!-- 更新内容按钮 -->
      <Button 
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-purple-400/60 to-purple-500/60 hover:from-purple-500/80 hover:to-purple-600/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-purple-300/40 hover:border-purple-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleRefreshButtonClick"
        tooltip="更新内容"
      >
        <div class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <Icon icon="lucide:refresh-cw" class="h-7 w-7 group-hover:rotate-180 transition-transform duration-500" />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm">刷新内容</span>
      </Button>
      
      <!-- 问题生成按钮 -->
      <Button 
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-amber-400/60 to-orange-400/60 hover:from-amber-500/80 hover:to-orange-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-amber-300/40 hover:border-amber-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleQuestionGenerateClick"
        tooltip="问题生成"
      >
        <div class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <Icon icon="lucide:help-circle" class="h-7 w-7 group-hover:scale-110 transition-transform duration-300" />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm">问题生成</span>
      </Button>
      
      <!-- 回到首页按钮 -->
      <Button 
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-blue-400/60 to-cyan-400/60 hover:from-blue-500/80 hover:to-cyan-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-blue-300/40 hover:border-blue-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleBackToHome"
        tooltip="回到首页"
      >
        <div class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <Icon icon="lucide:home" class="h-7 w-7 group-hover:scale-110 transition-transform duration-300" />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm">回到首页</span>
      </Button>
      
      <!-- 最新资讯按钮 -->
      <Button 
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-emerald-400/60 to-teal-400/60 hover:from-emerald-500/80 hover:to-teal-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 mt-auto px-3 border border-emerald-300/40 hover:border-emerald-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleProcessNewsAndGenerateQuestions"
        tooltip="处理新闻并生成问题"
      >
        <div class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <Icon icon="lucide:newspaper" class="h-7 w-7 group-hover:scale-110 transition-transform duration-300" />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm">新闻问题</span>
      </Button>
      
      <!-- 智能推荐按钮 -->
      <Button 
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-indigo-400/60 to-purple-400/60 hover:from-indigo-500/80 hover:to-purple-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-indigo-300/40 hover:border-indigo-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleActionButtonClick"
        tooltip="智能推荐"
      >
        <div class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <Icon icon="lucide:sparkle" class="h-7 w-7 group-hover:rotate-12 group-hover:scale-110 transition-all duration-300" />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm">智能推荐</span>
      </Button>
    </div>
    
    <!-- 主内容区域 -->
    <div class="flex-1 flex flex-col items-center justify-between relative">
      <div class="w-full grow flex flex-col items-center justify-center px-4">
        <div class="w-full max-w-2xl">
          <h1 v-if="customText" class="text-xl md:text-2xl font-bold py-4 text-center whitespace-pre-line">{{ customText }}</h1>
          <h1 v-else class="text-xl md:text-2xl font-bold py-4">{{ t('newThread.greeting') }}</h1>
          <h3 v-if="!customText" class="text-lg px-8 pb-2">{{ t('newThread.prompt') }}</h3>
          <p v-if="customTextError" class="text-sm text-red-500 px-8 mt-2">{{ customTextError }}</p>
        </div>
      </div>
      
      <!-- 固定在底部的输入框区域 -->
      <div class="w-full px-4 py-4 pb-16">
        <ChatInput
          ref="chatInputRef"
          key="newThread"
          variant="newThread"
          class="w-full"
          :rows="3"
          :max-rows="10"
          :context-length="contextLength"
          @send="handleSend"
        >
          <template #addon-actions>
            <Popover v-model:open="modelSelectOpen">
              <PopoverTrigger as-child>
                <Button
                  variant="ghost"
                  class="flex items-center gap-1.5 h-7 px-2 rounded-md text-xs font-semibold text-muted-foreground hover:bg-muted/60 hover:text-foreground dark:text-white/70 dark:hover:bg-muted/60 dark:hover:text-white"
                  size="sm"
                >
                  <ModelIcon
                    class="w-4 h-4"
                    :model-id="activeModel.providerId"
                    :is-dark="themeStore.isDark"
                  ></ModelIcon>
                  <span class="text-xs font-semibold truncate max-w-[140px] text-foreground">{{
                    name
                  }}</span>
                  <Badge
                    v-for="tag in activeModel.tags"
                    :key="tag"
                    variant="outline"
                    class="py-0 px-1 rounded-lg text-[10px]"
                  >
                    {{ t(`model.tags.${tag}`) }}</Badge
                  >
                  <Icon icon="lucide:chevron-right" class="w-4 h-4 text-muted-foreground" />
                </Button>
              </PopoverTrigger>
              <PopoverContent align="end" class="w-80 p-0">
                <ModelSelect
                  :type="[ModelType.Chat, ModelType.ImageGeneration]"
                  @update:model="handleModelUpdate"
                />
              </PopoverContent>
            </Popover>

            <ScrollablePopover
              v-model:open="settingsPopoverOpen"
              align="end"
              content-class="w-80"
              :enable-scrollable="true"
            >
              <template #trigger>
                <Button
                  class="h-7 w-7 rounded-md border border-border/60 hover:border-border dark:border-white/10 dark:bg-white/[0.04] dark:text-white/70 dark:hover:border-white/25 dark:hover:bg-white/15 dark:hover:text-white"
                  size="icon"
                  variant="outline"
                >
                  <Icon icon="lucide:settings-2" class="w-4 h-4" />
                </Button>
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
          </template>
        </ChatInput>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 脚本部分保持不变，此处省略以节省空间
// 实际使用时需要保留原有的<script>内容
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

const name = computed(() => {
  return activeModel.value?.name ? activeModel.value.name.split('/').pop() : ''
})

watch(
  () => activeModel.value,
  async () => {
    const config = await configPresenter.getModelDefaultConfig(
      activeModel.value.id,
      activeModel.value.providerId
    )
    temperature.value = config.temperature ?? 0.7
    contextLength.value = config.contextLength
    maxTokens.value = config.maxTokens
    contextLengthLimit.value = config.contextLength
    maxTokensLimit.value = config.maxTokens
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

watch(
  () => chatStore.deeplinkCache,
  (newCache) => {
    if (newCache) {
      if (newCache.modelId) {
        const matchedModel = settingsStore.findModelByIdOrName(newCache.modelId)
        console.log('matchedModel', matchedModel)
        if (matchedModel) {
          handleModelUpdate(matchedModel.model, matchedModel.providerId)
        }
      }
      if (newCache.msg || newCache.mentions) {
        const setInputContent = () => {
          if (chatInputRef.value) {
            console.log('[NewThread] Setting input content, msg:', newCache.msg)
            const chatInput = chatInputRef.value
            chatInput.clearContent()
            if (newCache.mentions) {
              newCache.mentions.forEach((mention) => {
                chatInput.appendMention(mention)
              })
            }
            if (newCache.msg) {
              console.log('[NewThread] Appending text:', newCache.msg)
              chatInput.appendText(newCache.msg)
            }
            return true
          }
          return false
        }

        if (!setInputContent()) {
          console.log('[NewThread] ChatInput ref not ready, retrying...')
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
})

// 原有的最新资讯按钮处理函数已替换为handleProcessNewsAndGenerateQuestions

const handleActionButtonClick = async () => {
  try {
    const fileContent = await window.api.readLocalFile('user-preferences.txt');
    
    if (fileContent) {
      console.log('读取到的偏好内容:', fileContent);
      const queryMessage = `请你用arxiv-mcp-server的工具查找三篇和${fileContent}有关的论文，要新一点，sort_by参数为date。你的回答应该遵循以下格式，每行小标题加粗：标题：此处为对应标题\n摘要：此处为对应摘要，中文，控制在二十字以内\n链接：此处为对应论文链接`;
      console.log('构建的查询消息:', queryMessage);
      
      await handleSend({
        text: queryMessage,
        files: [],
        links: [],
        think: false,
        search: false
      });
    } else {
      console.error('文件内容为空');
      alert('用户偏好文件内容为空，请检查项目根目录下的user-preferences.txt文件');
    }
  } catch (error) {
    console.error('读取文件并发送消息时出错:', error);
    alert(`读取或发送消息失败: ${(error as Error).message || '未知错误'}`);
  }
};

const handleRefreshButtonClick = async () => {
  console.log('刷新按钮被点击');
  try {
    let userPref = '';
    try {
      userPref = (await window.api.readLocalFile('user-preferences.txt')) || '';
      console.log('读取到的用户偏好:', userPref);
    } catch (err) {
      console.warn('无法读取 user-preferences.txt，继续使用空偏好', err);
      userPref = '';
    }

    const combinedQuery = `用fetch,url=https://news.aibase.cn/news,max_length=1000,结果只包含五条新闻总结,每条二十字以内,不要有其他内容`;
    console.log('构建的查询消息:', combinedQuery);

    const tabId = window.api.getWebContentsId();
    
    try {
      const threadId = await threadPresenter.createConversation(
        '欢迎语刷新', 
        {
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
        } as any,
        tabId
      );
      console.log('创建的线程ID:', threadId);
      
      const messageContent = JSON.stringify({
        text: combinedQuery,
        files: [],
        links: [],
        think: false,
        search: false
      });
      
      await threadPresenter.sendMessage(threadId, messageContent, "user");
      
      await threadPresenter.startStreamCompletion(threadId, undefined, {});
      
      const extractAssistantText = (assistantMsg: any) => {
        if (!assistantMsg || !assistantMsg.content) return '';
        const parts: string[] = [];
        for (const block of assistantMsg.content) {
          if (!block) continue;
          if (block.type === 'content' && block.content) parts.push(block.content);
          else if (block.type === 'reasoning_content' && block.content) parts.push(block.content);
          else if (block.type === 'tool_call' && block.tool_call && block.tool_call.response) parts.push(block.tool_call.response);
          else if (typeof block.content === 'string') parts.push(block.content);
        }
        return parts.join('\n').trim();
      }

      let assistantText = '';
      const maxAttempts = 60;
      for (let i = 0; i < maxAttempts; i++) {
        await new Promise((r) => setTimeout(r, 1000));
        try {
          const msgsRes: any = await threadPresenter.getMessages(threadId, 1, 100)
          const assistantMsg = msgsRes?.list?.find((m: any) => m.role === 'assistant' && m.content && m.content.length > 0)
          if (assistantMsg) {
            assistantText = extractAssistantText(assistantMsg)
            if (assistantText && assistantText.length > 0) break
          }
        } catch (err) {
          console.warn('获取消息时出错，稍候重试', err)
        }
      }

      if (!assistantText) {
        console.log('未获取到助手响应，使用默认文本');
        assistantText = "感谢您的使用！我是您的AI助手，随时为您提供帮助。请随时提问，我会尽力为您解答。";
      }

      console.log('最终使用的文本:', assistantText);
      
      try {
        const lines = assistantText.split('\n');
        const lastNineLines = lines.slice(-9).join('\n').trim();
        
        await window.api.writeLocalFile('custom-welcome.txt', lastNineLines);
        customText.value = lastNineLines;
        customTextError.value = '';
        console.log('成功写入custom-welcome.txt文件（只保留最后九行）');
      } catch (error) {
        console.error('写入custom-welcome.txt文件失败:', error);
        customTextError.value = '无法写入自定义欢迎文本';
        alert('保存失败，请检查应用是否有写入权限');
      }
    } catch (error) {
      console.error('处理刷新请求时出错:', error);
      alert(`刷新失败: ${(error as Error).message || '未知错误'}`);
    }
  } catch (error) {
    console.error('刷新按钮处理失败:', error);
    alert(`刷新失败: ${(error as Error).message || '未知错误'}`);
  }
}

const handleQuestionGenerateClick = () => {
  router.push('/question')
}

const handleBackToHome = () => {
  router.push('/chat')
}

// 简单的token估算函数
const estimateTokens = (text: string): number => {
  if (!text) return 0;
  // 中文字符计数
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  // 非中文字符计数（英文、数字、标点等）
  const nonChineseChars = text.length - chineseChars;
  // 中文字符按1个token约1.3个字符估算，非中文字符按1个token约4个字符估算
  const tokens = Math.ceil(chineseChars / 1.3 + nonChineseChars / 4);
  return tokens;
};

// 调试模式开关（可根据需要启用）
const debugMode = true;

// 增强的日志函数
const debugLog = (message: string, data?: any) => {
  if (debugMode) {
    console.log(`[新闻处理调试] ${message}`, data || '');
  }
};

// 截断文本以控制token数量
const truncateTextToTokens = (text: string, maxTokens: number): string => {
  if (estimateTokens(text) <= maxTokens) return text;
  
  // 简单截断策略：从开头保留，同时留出一些缓冲
  const safetyFactor = 0.8; // 安全系数，确保不会超过限制
  const maxChars = Math.floor(maxTokens * 1.5 * safetyFactor); // 保守估计
  
  return text.substring(0, maxChars) + '...（内容已截断以控制长度）';
};

const handleProcessNewsAndGenerateQuestions = async () => {
  debugLog('开始处理新闻并生成问题结构');
  try {
    // 1. 首先获取新闻内容，修改查询减少返回内容
    const newsQuery = `用fetch,url=https://news.aibase.cn/news,max_length=500,结果只包含三条最重要的新闻总结,每条30字以内,不要有其他内容`;
      debugLog('构建的新闻查询消息:', newsQuery);

    const tabId = window.api.getWebContentsId();
    
    try {
      // 创建线程获取新闻，减少上下文长度以避免token超限
      const modelContextLimit = contextLength.value || 32000;
      const newsThreadId = await threadPresenter.createConversation(
        '新闻处理', 
        {
          providerId: activeModel.value.providerId,
          modelId: activeModel.value.id,
          systemPrompt: '你是一个简洁的信息提取助手。', // 使用极简系统提示
          temperature: temperature.value,
          contextLength: Math.min(modelContextLimit, 16000), // 减少新闻获取时的上下文长度
          maxTokens: 500, // 限制输出token数
          artifacts: artifacts.value as 0 | 1,
          thinkingBudget: thinkingBudget.value,
          enableSearch: enableSearch.value,
          forcedSearch: forcedSearch.value,
          searchStrategy: searchStrategy.value,
          reasoningEffort: reasoningEffort.value,
          verbosity: 0, // 最低冗余度
          enabledMcpTools: chatStore.chatConfig.enabledMcpTools
        } as any,
        tabId
      );
      debugLog('创建的新闻线程ID:', newsThreadId);
      
      const newsMessageContent = JSON.stringify({
        text: newsQuery,
        files: [],
        links: [],
        think: false,
        search: false
      });
      
      await threadPresenter.sendMessage(newsThreadId, newsMessageContent, "user");
      await threadPresenter.startStreamCompletion(newsThreadId, undefined, {});
      
      // 提取新闻内容的函数
      const extractAssistantText = (assistantMsg: any) => {
        if (!assistantMsg || !assistantMsg.content) return '';
        const parts: string[] = [];
        for (const block of assistantMsg.content) {
          if (!block) continue;
          if (block.type === 'content' && block.content) parts.push(block.content);
          else if (block.type === 'reasoning_content' && block.content) parts.push(block.content);
          else if (block.type === 'tool_call' && block.tool_call && block.tool_call.response) parts.push(block.tool_call.response);
          else if (typeof block.content === 'string') parts.push(block.content);
        }
        return parts.join('\n').trim();
      }

      let newsContent = '';
      const maxAttempts = 30; // 减少重试次数以避免频繁请求
      let retryDelay = 2000; // 增加初始延迟时间
      for (let i = 0; i < maxAttempts; i++) {
        await new Promise((r) => setTimeout(r, retryDelay));
        try {
          const msgsRes: any = await threadPresenter.getMessages(newsThreadId, 1, 100)
          const assistantMsg = msgsRes?.list?.find((m: any) => m.role === 'assistant' && m.content && m.content.length > 0)
          if (assistantMsg) {
            newsContent = extractAssistantText(assistantMsg)
            if (newsContent && newsContent.length > 0) break
          }
        } catch (err) {
          debugLog('获取新闻消息时出错，稍候重试', err)
          // 检测429错误并增加延迟
          if (err instanceof Error && (err.message.includes('429') || err.message.includes('too many requests'))) {
            debugLog('检测到429错误，增加延迟时间');
            retryDelay *= 1.5; // 指数退避
            if (retryDelay > 10000) retryDelay = 10000; // 设置最大延迟
          }
        }
      }

      if (!newsContent) {
        console.log('未获取到新闻内容');
        alert('未能获取到新闻内容，请稍后再试');
        return;
      }

      // 截断新闻内容以控制token数量（由于提示词变长，进一步降低新闻内容限制）
      newsContent = truncateTextToTokens(newsContent, 300); // 降低限制到300个token，增加安全余量
      debugLog('获取并截断的新闻内容:', newsContent);
      const newsTokens = estimateTokens(newsContent);
      debugLog('估算的新闻内容token数:', newsTokens);
      debugLog('新闻内容原始长度/截断后长度:', `${newsContent.length}`);
      
      // 2. 使用简洁的系统提示词
      const systemPromptForQuestionGeneration = `你是一个专业的AI助手，擅长从新闻内容中提取关键信息并生成结构化问题。请严格按照用户提供的指令处理新闻内容。`;
      
      // 创建新线程生成问题结构，合理设置参数以避免token超限
      const questionThreadId = await threadPresenter.createConversation(
        '新闻问题生成', 
        {
          providerId: activeModel.value.providerId,
          modelId: activeModel.value.id,
          systemPrompt: systemPromptForQuestionGeneration, // 使用专用的系统提示
          temperature: 0.3, // 降低温度以获得更精确的输出
          contextLength: modelContextLimit,
          maxTokens: 1000, // 限制输出token数
          artifacts: artifacts.value as 0 | 1,
          thinkingBudget: thinkingBudget.value,
          enableSearch: false, // 不需要搜索
          forcedSearch: false,
          searchStrategy: searchStrategy.value,
          reasoningEffort: reasoningEffort.value,
          verbosity: 0, // 最低冗长度，确保简洁输出
          enabledMcpTools: chatStore.chatConfig.enabledMcpTools
        } as any,
        tabId
      );
      debugLog('创建的问题生成线程ID:', questionThreadId);
      
      // 3. 更新为新的AI新闻科技关键词精准问题生成提示词
      const detailedInstructions = `AI新闻科技关键词精准问题生成提示词：
 核心任务步骤 
 1. 关键词提炼：从新闻全文提取6个核心科技关键词，必须是适用于学术论文检索的专业术语，包含具体的技术名称、算法、框架、协议或实现方法等，每行单独列出，无多余格式。 
 2. 关键词筛选：优先挑选有明确技术实现过程、可拆解具体流程的关键词（若多个符合，选与新闻核心技术关联最紧密的1个）。 
 3. 大框架问题生成：针对选中关键词，生成1个覆盖其核心技术过程、关键实现步骤或实践要点的概括性问题（围绕过程、步骤、机制等落地逻辑）。这是必须输出的第一行内容，绝对不能遗漏！ 
 4. 关键技术环节输出：基于关键词的通用技术逻辑+新闻隐含技术模块，拆解出5个关键技术环节（聚焦具体实现细节、技术原理、操作逻辑等维度），并为每个关键技术环节标注论文推荐标记（1表示需要，0表示不需要，依据是否涉及前沿研究、算法创新或学术争议）。 
 输出格式要求（严格按照以下顺序）： 
 1. 首先输出大框架问题（具体问题），必须作为第一行输出，绝对不能遗漏！必须包含过程、步骤、要点等技术落地导向词汇 
 2. 然后输出5个关键技术环节，每个占一行 
 3. 接着输出5个论文推荐标记，每个占一行，只能是0或1 
 4. 最后输出6个关键词，每个占一行，必须是适用于学术论文检索的专业术语，包含具体的技术名称、算法、框架、协议或实现方法 
 注意事项： 
 1. 关键词筛选：严格排除无明确技术流程的概念类词汇，优先保留包含具体技术名称、算法名称、框架名称、协议名称或实现方法的专业术语。每个关键词必须是适用于学术论文检索的专业术语，具有明确技术指向。 
 2. 大框架问题必须作为第一行输出，这是强制性要求，绝对不能遗漏或放置在其他位置。 
 3. 关键技术环节标注：涉及前沿算法、学术争议的标1；基础操作类标0。 
 4. 格式规范：仅输出规定的12行内容，不添加其他说明，确保结构简洁。 
 5. 绝对禁止输出任何占位符文本！例如："关键词1"、"关键词2"、"关键词3"、"关键词4"、"关键词5"、"关键词6"等占位符文本都不能出现。
 6. 只输出实际从新闻中提取的关键词，每个关键词必须是适用于学术论文检索的专业术语，完整且有意义。
 示例输出格式： 
 视频生成模型中扩散模型架构的核心优化步骤和关键技术要点有哪些？ 
 需要处理扩散模型在视频生成中时间序列数据的连贯性； 
 多帧特征融合技术在视频生成模型中的具体实现流程；
 条件输入处理模块对视频生成的主题一致性和细节还原度的影响； 
 对抗训练策略在视频生成模型优化中面临的技术挑战； 
 时间一致性优化算法的常用评估指标和调优方法； 
 1 
 1 
 1 
 1 
 0 
 视频生成模型 
 扩散模型架构 
 时间一致性优化 
 多帧特征融合 
 条件输入处理 
 对抗训练策略
 识别核心技术点、分析实现机制、拆解关键步骤、总结优化策略、评估应用效果`;
      
      // 组合指导和新闻内容，并确保总token数不超过限制
      let combinedText = `${detailedInstructions}

请处理以下新闻内容并生成问题结构：

${newsContent}`;
      
      const instructionsTokens = estimateTokens(detailedInstructions);
      debugLog('指导内容token估算:', instructionsTokens);
      
      // 计算并确保总token数不超过模型限制（由于提示词变长，预留更多token给输出）
      const maxInputTokens = modelContextLimit - 1200; // 进一步增加预留token数，应对更长的提示词
      
      if (estimateTokens(combinedText) > maxInputTokens) {
        // 如果总内容过长，进一步减少新闻内容
        const instructionsTokens = estimateTokens(detailedInstructions);
        const remainingTokensForNews = maxInputTokens - instructionsTokens - 50; // 留出一些缓冲
        newsContent = truncateTextToTokens(newsContent, remainingTokensForNews);
        combinedText = `${detailedInstructions}

请处理以下新闻内容并生成问题结构：

${newsContent}`;
      }
      
      debugLog('估算的总输入token数:', estimateTokens(combinedText));
      debugLog('模型上下文限制/可用输入token数:', `${modelContextLimit}/${maxInputTokens}`);
      
      let questionMessageContent = JSON.stringify({
        text: combinedText,
        files: [],
        links: [],
        think: false,
        search: false
      });
      
      // 发送消息前再次检查token数
      const finalTokens = estimateTokens(JSON.parse(questionMessageContent).text);
      debugLog('发送前最终检查的token数:', finalTokens);
      
      // 如果token数仍然很高，再次减少内容（增加安全阈值）
      if (finalTokens > maxInputTokens * 0.9) { // 使用90%的限制作为警告阈值
        debugLog(`警告：内容仍然过长 (${finalTokens} tokens)，尝试进一步简化`);
        // 进一步简化指导内容，使用更简洁的格式
        const ultraSimplifiedInstructions = `AI新闻科技关键词精准问题生成：
1. 生成1个大框架问题（必须作为第一行输出，绝对不能遗漏！必须包含过程、步骤、要点等技术落地导向词汇）
2. 生成5个关键技术环节，每个一行
3. 生成5个0/1论文推荐标记，每个一行
4. 提取并输出6个核心科技关键词，每个一行，必须是适用于学术论文检索的专业术语，包含具体的技术名称、算法、框架、协议或实现方法
5. 绝对禁止输出"关键词1"、"关键词2"等任何占位符文本！
6. 只输出实际从新闻中提取的适用于学术论文检索的有意义专业术语关键词！
识别核心技术点、分析实现机制、拆解关键步骤、总结优化策略、评估应用效果`;
        
        // 只保留最重要的新闻内容，进一步减少长度
        const minimalNewsContent = truncateTextToTokens(newsContent, 100); // 进一步减少到100token，应对更长的提示词
        combinedText = `${ultraSimplifiedInstructions}

${minimalNewsContent}`;
        
        const newTokens = estimateTokens(combinedText);
        debugLog('使用超简化指导，新的token估算:', newTokens);
        
        // 更新消息内容
        questionMessageContent = JSON.stringify({
          text: combinedText,
          files: [],
          links: [],
          think: false,
          search: false
        });
      }
      
      try {
        await threadPresenter.sendMessage(questionThreadId, questionMessageContent, "user");
        // 添加延迟以避免请求过快
        await new Promise((r) => setTimeout(r, 1000));
        await threadPresenter.startStreamCompletion(questionThreadId, undefined, {});
      } catch (error) {
        debugLog('发送消息或开始流式完成时出错:', error);
        // 捕获可能的token超限错误，提供更友好的错误信息
        if (error instanceof Error && error.message.includes('maximum context length')) {
          alert('内容过长导致模型无法处理。请尝试使用更简短的新闻内容或降低请求的复杂度。');
          return;
        }
        // 捕获429错误，提供更友好的错误信息
        if (error instanceof Error && (error.message.includes('429') || error.message.includes('too many requests'))) {
          alert('请求频率过高，请稍后再试。系统已优化请求间隔，您可以等待一会儿后重试。');
          return;
        }
        throw error;
      }

      let questionStructure = '';
      let questionRetryDelay = 2000; // 增加初始延迟时间
      for (let i = 0; i < maxAttempts; i++) {
        await new Promise((r) => setTimeout(r, questionRetryDelay));
        try {
          const msgsRes: any = await threadPresenter.getMessages(questionThreadId, 1, 100)
          const assistantMsg = msgsRes?.list?.find((m: any) => m.role === 'assistant' && m.content && m.content.length > 0)
          if (assistantMsg) {
            questionStructure = extractAssistantText(assistantMsg)
            if (questionStructure && questionStructure.length > 0) break
          }
        } catch (err) {
          debugLog('获取问题结构时出错，稍候重试', err)
          // 检测429错误并增加延迟
          if (err instanceof Error && (err.message.includes('429') || err.message.includes('too many requests'))) {
            debugLog('检测到429错误，增加延迟时间');
            questionRetryDelay *= 1.5; // 指数退避
            if (questionRetryDelay > 10000) questionRetryDelay = 10000; // 设置最大延迟
          }
        }
      }

      if (!questionStructure) {
        debugLog('未获取到问题结构');
        alert('未能生成问题结构，请稍后再试');
        return;
      }

      debugLog('生成的问题结构:', questionStructure);
      debugLog('生成的问题结构token估算:', estimateTokens(questionStructure));
      
      // 后处理问题结构，清理占位符文本和格式
      let cleanedQuestionStructure = questionStructure;
      
      // 清理占位符文本
      cleanedQuestionStructure = cleanedQuestionStructure.replace(/关键词1|关键词2|关键词3|关键词4|关键词5|关键词6/g, '');
      // 移除空行
      cleanedQuestionStructure = cleanedQuestionStructure.split('\n')
        .filter(line => line.trim() !== '')
        .join('\n');
      
      debugLog('清理后的问题结构:', cleanedQuestionStructure);
      
      // 显示清理后的问题结构
      alert(`生成的问题结构：\n\n${cleanedQuestionStructure}`);
      debugLog('处理完成，问题结构已显示给用户');
      
    } catch (error) {
      debugLog('处理新闻和生成问题结构时出错:', error);
      alert(`处理失败: ${(error as Error).message || '未知错误'}`);
    }
  } catch (error) {
    debugLog('处理新闻按钮点击失败:', error);
    alert(`处理失败: ${(error as Error).message || '未知错误'}`);
  } finally {
    debugLog('新闻处理流程结束');
  }
}

const handleSend = async (content: UserMessageContent) => {
  const threadId = await chatStore.createThread(content.text, {
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
  console.log('threadId', threadId, activeModel.value)
  chatStore.sendMessage(content)
}
</script>