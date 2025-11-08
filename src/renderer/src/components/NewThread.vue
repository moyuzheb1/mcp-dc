<template>
  <div class="h-full w-full flex flex-col items-center justify-between relative">
    <!-- 右上角刷新按钮 -->
    <Button 
      class="absolute top-4 right-4 h-10 px-4 bg-purple-600 hover:bg-purple-700 text-white rounded-full shadow-lg z-50 flex items-center justify-center gap-2 w-auto min-w-[120px] text-center"
      @click="handleRefreshButtonClick"
    >
      <Icon icon="lucide:refresh-cw" class="h-4 w-4" />
      <span>更新内容</span>
    </Button>
    <div class="w-full grow flex flex-col items-center justify-center px-4">
      <!-- 移除logo图标 -->
      <!-- <img src="@/assets/logo-dark.png" class="w-24 h-24" loading="lazy" /> -->
      <!-- 替换原有的欢迎语，显示自定义文本 -->
      <div class="w-full max-w-2xl">
        <h1 v-if="customText" class="text-xl md:text-2xl font-bold py-4 text-center whitespace-pre-line">{{ customText }}</h1>
        <!-- 如果自定义文本为空或出错，显示默认欢迎语 -->
        <h1 v-else class="text-xl md:text-2xl font-bold py-4">{{ t('newThread.greeting') }}</h1>
        <h3 v-if="!customText" class="text-lg px-8 pb-2">{{ t('newThread.prompt') }}</h3>
        <!-- 显示错误信息（如果有） -->
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
    
    <!-- 右下角深绿色按钮 -->
    <Button 
      class="absolute bottom-4 right-[145px] h-10 px-4 bg-green-800 hover:bg-green-900 text-white rounded-full shadow-lg z-50 flex items-center justify-center gap-2 w-auto min-w-[120px] text-center"
      @click="handleNewsButtonClick"
    >
      <Icon icon="lucide:newspaper" class="h-4 w-4" />
      <span>最新资讯</span>
    </Button>
    
    <!-- 右下角蓝色长条按钮 -->
    <Button 
      class="absolute bottom-4 right-4 h-10 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg z-50 flex items-center justify-center gap-2 w-auto min-w-[120px] text-center"
      @click="handleActionButtonClick"
    >
      <Icon icon="lucide:sparkle" class="h-4 w-4" />
      <span>智能推荐</span>
    </Button>
  </div>
</template>

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

const configPresenter = usePresenter('configPresenter')
const threadPresenter = usePresenter('threadPresenter')
const themeStore = useThemeStore()
// 定义偏好模型的类型
interface PreferredModel {
  modelId: string
  providerId: string
}

const { t } = useI18n()
const chatStore = useChatStore()
const settingsStore = useSettingsStore()
// 添加新的响应式变量来存储自定义文本
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
    // console.log('activeModel', activeModel.value)
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
    // console.log('temperature', temperature.value)
    // console.log('contextLength', contextLength.value)
    // console.log('maxTokens', maxTokens.value)
  }
)
// 初始化与校验逻辑：只在激活时初始化一次；仅监听 enabledModels 变化做有效性校验
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
  // 1) 尝试根据最近会话（区分 pinned/非 pinned）选择
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

  // 2) 尝试用户上次选择的偏好模型
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

  // 3) 选择第一个可用模型
  const first = pickFirstEnabledModel()
  if (first) {
    setActiveFromEnabled(first)
    initialized.value = true
  }
}

// 仅监听 enabledModels：
// - 若未初始化，进行一次初始化
// - 若已初始化但当前模型不再可用，则回退到第一个 enabled 模型
watch(
  () => settingsStore.enabledModels,
  async () => {
    if (!initialized.value) {
      await initActiveModel()
      return
    }

    // 校验当前模型是否仍可用
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

  // 保存用户的模型偏好设置
  configPresenter.setSetting('preferredModel', {
    modelId: model.id,
    providerId: providerId
  })

  modelSelectOpen.value = false
}

// 监听 deeplinkCache 变化
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
      // 清理缓存
      chatStore.clearDeeplinkCache()
    }
  },
  { immediate: true }
)

onMounted(async () => {
  configPresenter.getDefaultSystemPrompt().then((prompt) => {
    systemPrompt.value = prompt
  })
  // 组件激活时初始化一次默认模型
  await initActiveModel()
  
  // 尝试从根目录的custom-welcome.txt文件读取自定义欢迎文本
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
    
    // 调用handleSend函数发送消息
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
    // 使用通过contextBridge暴露的API读取user-preferences.txt文件
    const fileContent = await window.api.readLocalFile('user-preferences.txt');
    
    if (fileContent) {
      console.log('读取到的偏好内容:', fileContent);
      // 构建查询消息
      const queryMessage = `请你用arxiv-mcp-server的工具查找三篇和${fileContent}有关的论文，要新一点，sort_by参数为date。你的回答应该遵循以下格式，每行小标题加粗：标题：此处为对应标题\n摘要：此处为对应摘要，中文，控制在二十字以内\n链接：此处为对应论文链接`;
      console.log('构建的查询消息:', queryMessage);
      
      // 调用handleSend函数发送构建的查询消息
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

// 处理刷新按钮点击事件：
// 1) 基于用户偏好与抓取到的最新资讯构建查询（通过MCP工具fetch请求），
// 2) 在新会话中发送该查询，等待助手生成结果，
// 3) 将生成的文本写入项目根目录的 custom-welcome.txt（覆盖原文件），并更新界面显示。
const handleRefreshButtonClick = async () => {
  try {
    // 读取用户偏好（如果存在）
    let userPref = '';
    try {
      userPref = (await window.api.readLocalFile('user-preferences.txt')) || '';
    } catch (err) {
      console.warn('无法读取 user-preferences.txt，继续使用空偏好', err);
      userPref = '';
    }

    // 构建综合查询：同时利用新闻抓取工具并结合用户偏好让模型输出欢迎语
    const combinedQuery = `用fetch,url=https://news.aibase.cn/news,max_length=1000,结果只包含五条新闻总结,不要有其他内容`;

    // 创建一个新会话并发送消息（复用现有配置）
    const threadId = await chatStore.createThread(combinedQuery, {
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

    await chatStore.sendMessage({
      text: combinedQuery,
      files: [],
      links: [],
      think: false,
      search: false
    })

    // 辅助函数：从助手消息块中抽取可读文本
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

    // 等待助手响应（轮询），最多等待 60 秒
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
      alert('未能在规定时间内获取到生成的欢迎语，请稍后重试。')
      return
    }

    // 将结果写入根目录的 custom-welcome.txt（覆盖）
    try {
      await window.api.writeLocalFile('custom-welcome.txt', assistantText)
      customText.value = assistantText
      customTextError.value = ''
      // 可选：提醒用户已更新
      console.log('custom-welcome.txt 已更新')
    } catch (err) {
      console.error('写入 custom-welcome.txt 失败:', err)
      customTextError.value = '无法保存自定义欢迎文本'
      alert('保存失败，请检查应用是否有写入权限')
    }
  } catch (error) {
    console.error('刷新按钮处理失败:', error)
    alert(`刷新失败: ${(error as Error).message || '未知错误'}`)
  }
}

// 直接使用chatStore中的数据，不需要自定义函数来获取历史记录
// 下面的函数在handleRefreshButtonClick中直接使用chatStore数据

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