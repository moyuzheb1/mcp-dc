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
        @click="handleNewsButtonClick"
        tooltip="最新资讯"
      >
        <div class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <Icon icon="lucide:newspaper" class="h-7 w-7 group-hover:scale-110 transition-transform duration-300" />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm">最新资讯</span>
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

const handleNewsButtonClick = async () => {
  try {
    const queryMessage = "用fetch,url=https://news.aibase.cn/news,max_length=1000,结果只包含五条新闻总结,不要有其他内容";
    console.log('发送的消息:', queryMessage);
    
    await handleSend({
      text: queryMessage,
      files: [],
      links: [],
      think: false,
      search: false
    });
  } catch (error) {
    console.error('发送消息时出错:', error);
    alert(`发送消息失败: ${(error as Error).message || '未知错误'}`);
  }
};

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