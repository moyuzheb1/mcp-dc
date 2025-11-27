<template>
  <div class="h-full w-full flex relative">
    <!-- 侧边栏 -->
    <div
      class="w-24 h-full bg-gradient-to-b from-gray-50/80 to-gray-100/80 dark:from-gray-900/90 dark:to-gray-800/90 border-r border-gray-200/50 dark:border-gray-700/50 flex flex-col items-center py-6 gap-6 backdrop-blur-sm"
    >
      <!-- 原子+放大镜组合图标 -->
      <div
        class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-400/20 to-blue-400/20 border border-purple-200/30 dark:border-purple-700/30 flex items-center justify-center"
      >
        <img
          src="C:/Users/ASUS/Desktop/cb19e5f2778cc441e6ba9b7ad38150d2.png"
          alt="原子搜索图标"
          class="w-10 h-10 object-contain mix-blend-multiply"
        />
      </div>

      <!-- 更新内容按钮 -->
      <Button
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-purple-400/60 to-purple-500/60 hover:from-purple-500/80 hover:to-purple-600/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-purple-300/40 hover:border-purple-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleRefreshButtonClick"
        tooltip="更新内容"
      >
        <div
          class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        ></div>
        <Icon
          icon="lucide:refresh-cw"
          class="h-7 w-7 group-hover:rotate-180 transition-transform duration-500"
        />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm"
          >刷新内容</span
        >
      </Button>

      <!-- 问题生成按钮 -->
      <Button
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-amber-400/60 to-orange-400/60 hover:from-amber-500/80 hover:to-orange-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-amber-300/40 hover:border-amber-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleQuestionGenerateClick"
        tooltip="问题生成"
      >
        <div
          class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        ></div>
        <Icon
          icon="lucide:help-circle"
          class="h-7 w-7 group-hover:scale-110 transition-transform duration-300"
        />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm"
          >问题生成</span
        >
      </Button>

      <!-- 回到首页按钮 -->
      <Button
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-blue-400/60 to-cyan-400/60 hover:from-blue-500/80 hover:to-cyan-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-blue-300/40 hover:border-blue-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleBackToHome"
        tooltip="回到首页"
      >
        <div
          class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        ></div>
        <Icon
          icon="lucide:home"
          class="h-7 w-7 group-hover:scale-110 transition-transform duration-300"
        />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm"
          >回到首页</span
        >
      </Button>

      <!-- 最新资讯按钮 -->
      <Button
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-emerald-400/60 to-teal-400/60 hover:from-emerald-500/80 hover:to-teal-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 mt-auto px-3 border border-emerald-300/40 hover:border-emerald-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleProcessNewsAndGenerateQuestions"
        tooltip="处理新闻并生成问题"
      >
        <div
          class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        ></div>
        <Icon
          icon="lucide:newspaper"
          class="h-7 w-7 group-hover:scale-110 transition-transform duration-300"
        />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm"
          >新闻问题</span
        >
      </Button>

      <!-- 智能推荐按钮 -->
      <Button
        class="group relative w-20 h-16 rounded-xl bg-gradient-to-br from-indigo-400/60 to-purple-400/60 hover:from-indigo-500/80 hover:to-purple-500/80 text-white shadow-xl hover:shadow-2xl flex flex-col items-center justify-center gap-2 z-50 px-3 border border-indigo-300/40 hover:border-indigo-400/60 transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5"
        @click="handleActionButtonClick"
        tooltip="智能推荐"
      >
        <div
          class="absolute inset-0 rounded-xl bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        ></div>
        <Icon
          icon="lucide:sparkle"
          class="h-7 w-7 group-hover:rotate-12 group-hover:scale-110 transition-all duration-300"
        />
        <span class="text-xs font-semibold leading-tight drop-shadow-sm"
          >智能推荐</span
        >
      </Button>
    </div>

    <!-- 主内容区域 -->
    <div class="flex-1 flex relative">
      <!-- 主要内容显示区域 -->
      <div class="flex-1 flex flex-col items-center justify-center px-4 py-6">
        <div class="w-full max-w-5xl">
          <!-- 显示sample.txt的内容 -->
          <div v-if="sampleTitle" class="mb-12 relative">
            <div class="mb-6">
              <h1
                class="text-2xl md:text-3xl font-bold py-4 text-center text-gray-800 dark:text-gray-100"
              >
                {{ sampleTitle }}
              </h1>
            </div>
            <!-- 难度反馈按钮 -->
            <div class="absolute top-0 right-0 space-x-2">
              <button
                @click="handleDifficultyButtonClick('难')"
                :class="[
                  'px-3 py-1 rounded-md text-sm font-medium transition-all duration-200',
                  isDifficultyClicked === '难'
                    ? 'bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-800'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-200 dark:hover:bg-gray-700',
                ]"
              >
                难
              </button>
              <button
                @click="handleDifficultyButtonClick('简单')"
                :class="[
                  'px-3 py-1 rounded-md text-sm font-medium transition-all duration-200',
                  isDifficultyClicked === '简单'
                    ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 border border-green-200 dark:border-green-800'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-200 dark:hover:bg-gray-700',
                ]"
              >
                简单
              </button>
            </div>
            <div
              v-if="sampleColumns.length === 5"
              class="grid grid-cols-1 gap-6 mt-6 max-h-[600px] overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-700 scrollbar-track-transparent"
            >
              <div
                v-for="(column, index) in sampleColumns"
                :key="index"
                class="py-5 px-6 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700/50 text-center shadow-sm hover:shadow-md transition-all duration-300"
              >
                <div class="text-lg font-medium mb-2">{{ column }}</div>
                <div
                  v-if="keywords.length > index"
                  class="mt-2 text-sm text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700/50 rounded-full px-3 py-1 inline-block"
                >
                  <span class="text-gray-500 dark:text-gray-400">关键字:</span>
                  {{ keywords[index] }}
                </div>
                <!-- 基于sample.txt第7-11行的控制标志动态显示论文信息文本框 -->
                <div
                  v-if="
                    showPaperBox.length > index && showPaperBox[index] === 1
                  "
                  class="mt-5"
                >
                  <!-- paper.txt 论文 -->
                  <div class="mb-5">
                    <h3
                      class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2"
                    >
                      相关论文
                    </h3>
                    <div
                      v-if="
                        paperData.length > index &&
                        paperData[index] &&
                        paperData[index].id
                      "
                      :class="[
                        'p-5 rounded-lg border text-left shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1',
                        index === 0
                          ? 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-800'
                          : index === 1
                            ? 'bg-green-50 dark:bg-green-900/30 border-green-200 dark:border-green-800'
                            : index === 2
                              ? 'bg-purple-50 dark:bg-purple-900/30 border-purple-200 dark:border-purple-800'
                              : index === 3
                                ? 'bg-amber-50 dark:bg-amber-900/30 border-amber-200 dark:border-amber-800'
                                : 'bg-teal-50 dark:bg-teal-900/30 border-teal-200 dark:border-teal-800',
                      ]"
                    >
                      <div class="flex items-center mb-2">
                        <a
                          :href="`https://arxiv.org/abs/${paperData[index].id}`"
                          target="_blank"
                          rel="noopener noreferrer"
                          class="font-semibold text-ellipsis overflow-hidden block hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex-1"
                          title="点击查看论文"
                        >
                          {{ paperData[index].title }}
                        </a>
                        <svg
                          class="w-4 h-4 ml-2 text-blue-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                          ></path>
                        </svg>
                      </div>
                      <div
                        class="text-sm line-clamp-3 bg-white/70 dark:bg-gray-800/70 p-3 rounded-md border border-gray-100 dark:border-gray-700"
                      >
                        {{ paperData[index].abstract }}
                      </div>
                    </div>
                    <div
                      v-else
                      class="p-5 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700/50 text-center text-sm text-gray-500 dark:text-gray-400"
                    >
                      <svg
                        class="w-8 h-8 mx-auto mb-2 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="1.5"
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        ></path>
                      </svg>
                      暂无论文数据
                    </div>
                  </div>

                  <!-- paper2.txt 论文 -->
                  <div>
                    <div
                      v-if="
                        paper2Data.length > index &&
                        paper2Data[index] &&
                        paper2Data[index].id
                      "
                      :class="[
                        'p-5 rounded-lg border text-left shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1',
                        index === 0
                          ? 'bg-indigo-50 dark:bg-indigo-900/30 border-indigo-200 dark:border-indigo-800'
                          : index === 1
                            ? 'bg-pink-50 dark:bg-pink-900/30 border-pink-200 dark:border-pink-800'
                            : index === 2
                              ? 'bg-orange-50 dark:bg-orange-900/30 border-orange-200 dark:border-orange-800'
                              : index === 3
                                ? 'bg-cyan-50 dark:bg-cyan-900/30 border-cyan-200 dark:border-cyan-800'
                                : 'bg-lime-50 dark:bg-lime-900/30 border-lime-200 dark:border-lime-800',
                      ]"
                    >
                      <div class="flex items-center mb-2">
                        <a
                          :href="`https://arxiv.org/abs/${paper2Data[index].id}`"
                          target="_blank"
                          rel="noopener noreferrer"
                          class="font-semibold text-ellipsis overflow-hidden block hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors flex-1"
                          title="点击查看论文"
                        >
                          {{ paper2Data[index].title }}
                        </a>
                        <svg
                          class="w-4 h-4 ml-2 text-indigo-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                          xmlns="http://www.w3.org/2000/svg"
                        >
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                          ></path>
                        </svg>
                      </div>
                      <div
                        class="text-sm line-clamp-3 bg-white/70 dark:bg-gray-800/70 p-3 rounded-md border border-gray-100 dark:border-gray-700"
                      >
                        {{ paper2Data[index].abstract }}
                      </div>
                    </div>
                    <div
                      v-else
                      class="p-5 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700/50 text-center text-sm text-gray-500 dark:text-gray-400"
                    >
                      <svg
                        class="w-8 h-8 mx-auto mb-2 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="1.5"
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        ></path>
                      </svg>
                      暂无论文数据
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- 显示总结内容 -->
            <div
              v-if="summary"
              class="mt-10 p-8 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-lg text-center min-h-[140px] text-lg"
            >
              <div class="max-w-3xl mx-auto">
                <strong class="text-gray-800 dark:text-gray-100">{{
                  summary
                }}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 固定在右侧的输入框区域 -->
      <div
        class="w-80 h-full border-l border-gray-200 dark:border-gray-700 flex flex-col"
      >
        <div class="flex-1 flex flex-col p-4">
          <div class="mb-4">
            <h4 class="text-sm font-semibold text-gray-500 dark:text-gray-400">
              输入你的问题
            </h4>
          </div>
          <div class="flex-1 flex flex-col">
            <ChatInput
              ref="chatInputRef"
              key="newThread"
              variant="newThread"
              class="flex-1"
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
                      <span
                        class="text-xs font-semibold truncate max-w-[140px] text-foreground"
                        >{{ name }}</span
                      >
                      <Badge
                        v-for="tag in activeModel.tags"
                        :key="tag"
                        variant="outline"
                        class="py-0 px-1 rounded-lg text-[10px]"
                      >
                        {{ t(`model.tags.${tag}`) }}</Badge
                      >
                      <Icon
                        icon="lucide:chevron-right"
                        class="w-4 h-4 text-muted-foreground"
                      />
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
    </div>
  </div>
</template>

<script setup lang="ts">
// 脚本部分保持不变，此处省略以节省空间
// 实际使用时需要保留原有的<script>内容
import { useI18n } from "vue-i18n";
import ChatInput from "./chat-input/ChatInput.vue";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@shadcn/components/ui/popover";
import ScrollablePopover from "./ScrollablePopover.vue";
import { Button } from "@shadcn/components/ui/button";
import ModelIcon from "./icons/ModelIcon.vue";
import { Badge } from "@shadcn/components/ui/badge";
import { Icon } from "@iconify/vue";
import ModelSelect from "./ModelSelect.vue";
import { useChatStore } from "@/stores/chat";
import { MODEL_META } from "@shared/presenter";
import { useSettingsStore } from "@/stores/settings";
import { computed, nextTick, ref, watch, onMounted } from "vue";
import { UserMessageContent } from "@shared/chat";
import ChatConfig from "./ChatConfig.vue";
import { usePresenter } from "@/composables/usePresenter";
import { useThemeStore } from "@/stores/theme";
import { ModelType } from "@shared/model";
import { useRouter } from "vue-router";

const configPresenter = usePresenter("configPresenter");
const threadPresenter = usePresenter("threadPresenter");
const themeStore = useThemeStore();
const router = useRouter();

interface PreferredModel {
  modelId: string;
  providerId: string;
}

const { t } = useI18n();
const chatStore = useChatStore();
const settingsStore = useSettingsStore();
const customText = ref("");
const customTextError = ref("");
const sampleTitle = ref("");
const sampleColumns = ref<string[]>([]);
const activeModel = ref({
  name: "",
  id: "",
  providerId: "",
  tags: [],
  type: ModelType.Chat,
} as {
  name: string;
  id: string;
  providerId: string;
  tags: string[];
  type: ModelType;
});

const temperature = ref(0.6);
const contextLength = ref(16384);
const contextLengthLimit = ref(16384);
const maxTokens = ref(4096);
const maxTokensLimit = ref(4096);
const systemPrompt = ref("");
const artifacts = ref(settingsStore.artifactsEffectEnabled ? 1 : 0);
const thinkingBudget = ref<number | undefined>(undefined);
const enableSearch = ref<boolean | undefined>(undefined);
const forcedSearch = ref<boolean | undefined>(undefined);
const searchStrategy = ref<"turbo" | "max" | undefined>(undefined);
const reasoningEffort = ref<"minimal" | "low" | "medium" | "high" | undefined>(
  undefined,
);
const verbosity = ref<"low" | "medium" | "high" | undefined>(undefined);

const name = computed(() => {
  return activeModel.value?.name ? activeModel.value.name.split("/").pop() : "";
});

watch(
  () => activeModel.value,
  async () => {
    const config = await configPresenter.getModelDefaultConfig(
      activeModel.value.id,
      activeModel.value.providerId,
    );
    temperature.value = config.temperature ?? 0.7;
    contextLength.value = config.contextLength;
    maxTokens.value = config.maxTokens;
    contextLengthLimit.value = config.contextLength;
    maxTokensLimit.value = config.maxTokens;
    thinkingBudget.value = config.thinkingBudget;
    enableSearch.value = config.enableSearch;
    forcedSearch.value = config.forcedSearch;
    searchStrategy.value = config.searchStrategy;
    reasoningEffort.value = config.reasoningEffort;
    verbosity.value = config.verbosity;
  },
);

const initialized = ref(false);

const findEnabledModel = (providerId: string, modelId: string) => {
  for (const provider of settingsStore.enabledModels) {
    if (provider.providerId === providerId) {
      for (const model of provider.models) {
        if (model.id === modelId) {
          return { model, providerId: provider.providerId };
        }
      }
    }
  }
  return undefined;
};

const pickFirstEnabledModel = () => {
  const found = settingsStore.enabledModels
    .flatMap((p) => p.models.map((m) => ({ ...m, providerId: p.providerId })))
    .find(
      (m) => m.type === ModelType.Chat || m.type === ModelType.ImageGeneration,
    );
  return found;
};

const setActiveFromEnabled = (m: {
  name: string;
  id: string;
  providerId: string;
  type?: ModelType;
}) => {
  activeModel.value = {
    name: m.name,
    id: m.id,
    providerId: m.providerId,
    tags: [],
    type: m.type ?? ModelType.Chat,
  };
};

const initActiveModel = async () => {
  if (initialized.value) return;
  if (chatStore.threads.length > 0) {
    const pinnedGroup = chatStore.threads.find((g) => g.dt === "Pinned");
    const pinnedFirst = pinnedGroup?.dtThreads?.[0];
    const normalGroup = chatStore.threads.find(
      (g) => g.dt !== "Pinned" && g.dtThreads.length > 0,
    );
    const normalFirst = normalGroup?.dtThreads?.[0];
    const candidate = [pinnedFirst, normalFirst]
      .filter(Boolean)
      .sort((a, b) => (b!.updatedAt || 0) - (a!.updatedAt || 0))[0] as
      | typeof pinnedFirst
      | undefined;
    if (candidate?.settings?.modelId && candidate?.settings?.providerId) {
      const match = findEnabledModel(
        candidate.settings.providerId,
        candidate.settings.modelId,
      );
      if (match) {
        setActiveFromEnabled({ ...match.model, providerId: match.providerId });
        initialized.value = true;
        return;
      }
    }
  }

  try {
    const preferredModel = (await configPresenter.getSetting(
      "preferredModel",
    )) as PreferredModel | undefined;
    if (preferredModel?.modelId && preferredModel?.providerId) {
      const match = findEnabledModel(
        preferredModel.providerId,
        preferredModel.modelId,
      );
      if (match) {
        setActiveFromEnabled({ ...match.model, providerId: match.providerId });
        initialized.value = true;
        return;
      }
    }
  } catch (error) {
    console.warn("Failed to get user preferred model:", error);
  }

  const first = pickFirstEnabledModel();
  if (first) {
    setActiveFromEnabled(first);
    initialized.value = true;
  }
};

watch(
  () => settingsStore.enabledModels,
  async () => {
    if (!initialized.value) {
      await initActiveModel();
      return;
    }

    const current = activeModel.value;
    if (!current?.id || !current?.providerId) {
      const first = pickFirstEnabledModel();
      if (first) setActiveFromEnabled(first);
      return;
    }
    const stillExists = !!findEnabledModel(current.providerId, current.id);
    if (!stillExists) {
      const first = pickFirstEnabledModel();
      if (first) setActiveFromEnabled(first);
    }
  },
  { immediate: false, deep: true },
);

const modelSelectOpen = ref(false);
const settingsPopoverOpen = ref(false);
const chatInputRef = ref<InstanceType<typeof ChatInput> | null>(null);

// 用于存储sample.txt的关键字和总结内容
const keywords = ref<string[]>([]);
const summary = ref<string>("");
// 用于存储sample.txt第7-11行的控制标志
const showPaperBox = ref<number[]>([0, 0, 0, 0, 0]);
// 用于存储paper.txt的论文数据
const paperData = ref<Array<{ id: string; title: string; abstract: string }>>(
  [],
);
// 用于存储paper2.txt的论文数据
const paper2Data = ref<Array<{ id: string; title: string; abstract: string }>>(
  [],
);
// 用于记录难度按钮点击状态
const isDifficultyClicked = ref<string | null>(null);

// 处理难度按钮点击事件
const handleDifficultyButtonClick = (difficulty: string) => {
  isDifficultyClicked.value = difficulty;

  // 显示反馈提示
  const notification = document.createElement("div");
  notification.className = `fixed top-4 right-4 px-4 py-2 rounded-md text-white font-medium transition-opacity duration-300 ${difficulty === "难" ? "bg-red-500" : "bg-green-500"}`;
  notification.textContent = `已标记为${difficulty}`;
  document.body.appendChild(notification);

  // 2秒后自动消失
  setTimeout(() => {
    notification.style.opacity = "0";
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 2000);

  console.log(`用户标记当前内容为: ${difficulty}`);
};

const handleModelUpdate = (model: MODEL_META, providerId: string) => {
  activeModel.value = {
    name: model.name,
    id: model.id,
    providerId: providerId,
    tags: [],
    type: model.type ?? ModelType.Chat,
  };
  chatStore.updateChatConfig({
    modelId: model.id,
    providerId: providerId,
  });

  configPresenter.setSetting("preferredModel", {
    modelId: model.id,
    providerId: providerId,
  });

  modelSelectOpen.value = false;
};

watch(
  () => chatStore.deeplinkCache,
  (newCache) => {
    if (newCache) {
      if (newCache.modelId) {
        const matchedModel = settingsStore.findModelByIdOrName(
          newCache.modelId,
        );
        console.log("matchedModel", matchedModel);
        if (matchedModel) {
          handleModelUpdate(matchedModel.model, matchedModel.providerId);
        }
      }
      if (newCache.msg || newCache.mentions) {
        const setInputContent = () => {
          if (chatInputRef.value) {
            console.log(
              "[NewThread] Setting input content, msg:",
              newCache.msg,
            );
            const chatInput = chatInputRef.value;
            chatInput.clearContent();
            if (newCache.mentions) {
              newCache.mentions.forEach((mention) => {
                chatInput.appendMention(mention);
              });
            }
            if (newCache.msg) {
              console.log("[NewThread] Appending text:", newCache.msg);
              chatInput.appendText(newCache.msg);
            }
            return true;
          }
          return false;
        };

        if (!setInputContent()) {
          console.log("[NewThread] ChatInput ref not ready, retrying...");
          nextTick(() => {
            if (!setInputContent()) {
              setTimeout(() => {
                if (!setInputContent()) {
                  console.warn(
                    "[NewThread] Failed to set input content after retries",
                  );
                }
              }, 100);
            }
          });
        }
      }
      if (newCache.systemPrompt) {
        systemPrompt.value = newCache.systemPrompt;
      }
      if (newCache.autoSend && newCache.msg) {
        handleSend({
          text: newCache.msg || "",
          files: [],
          links: [],
          think: false,
          search: false,
        });
      }
      chatStore.clearDeeplinkCache();
    }
  },
  { immediate: true },
);

onMounted(async () => {
  configPresenter.getDefaultSystemPrompt().then((prompt) => {
    systemPrompt.value = prompt;
  });
  await initActiveModel();

  try {
    const fileContent = await window.api.readLocalFile("custom-welcome.txt");
    if (fileContent) {
      customText.value = fileContent.trim();
    }
  } catch (error) {
    console.error("读取自定义欢迎文本失败:", error);
    customTextError.value = "无法读取自定义欢迎文本";
  }

  // 读取sample.txt文件
  try {
    const sampleFileContent = await window.api.readLocalFile("sample.txt");
    if (sampleFileContent) {
      const lines = sampleFileContent
        .trim()
        .split("\n")
        .filter((line) => line.trim() !== "");
      if (lines.length > 0) {
        // 第一行作为标题
        sampleTitle.value = lines[0].trim();
        // 第2-6行作为五列内容
        if (lines.length >= 6) {
          sampleColumns.value = lines.slice(1, 6).map((line) => line.trim());
        }
        // 第7-11行作为控制标志（是否显示论文框）
        if (lines.length >= 11) {
          showPaperBox.value = lines
            .slice(6, 11)
            .map((line) => parseInt(line.trim()) || 0);
        }
        // 第12-16行作为关键字内容
        if (lines.length >= 16) {
          keywords.value = lines.slice(11, 16).map((line) => line.trim());
        }
        // 第17行作为总结内容
        if (lines.length >= 17) {
          summary.value = lines[16].trim();
        }
      }
    }
  } catch (error) {
    console.error("读取sample.txt失败:", error);
  }

  // 读取paper.txt文件，提取论文数据
  try {
    const paperFileContent = await window.api.readLocalFile("paper.txt");
    if (paperFileContent) {
      const lines = paperFileContent
        .trim()
        .split("\n")
        .filter((line) => line.trim() !== "");
      // 根据特定行号映射关系构建paperData：id在1,4,7,10,13行，标题在2,5,8,11,14行，摘要在3,6,9,12,15行
      const newPaperData: Array<{
        id: string;
        title: string;
        abstract: string;
      }> = [];
      // 处理5组数据（最多）
      for (let i = 0; i < 5; i++) {
        // 计算当前组的id行索引（从0开始）
        const idIndex = i * 3;
        const titleIndex = idIndex + 1;
        const abstractIndex = idIndex + 2;

        // 检查索引是否有效
        if (
          idIndex < lines.length &&
          titleIndex < lines.length &&
          abstractIndex < lines.length
        ) {
          newPaperData.push({
            id: lines[idIndex].trim(),
            title: lines[titleIndex].trim(),
            abstract: lines[abstractIndex].trim(),
          });
        }
      }
      paperData.value = newPaperData;
    }
  } catch (error) {
    console.error("读取paper.txt失败:", error);
  }

  // 读取paper2.txt文件，提取论文数据
  try {
    const paper2FileContent = await window.api.readLocalFile("paper2.txt");
    if (paper2FileContent) {
      const lines = paper2FileContent
        .trim()
        .split("\n")
        .filter((line) => line.trim() !== "");
      // 使用与paper.txt相同的格式解析paper2.txt
      const newPaper2Data: Array<{
        id: string;
        title: string;
        abstract: string;
      }> = [];
      // 处理5组数据（最多）
      for (let i = 0; i < 5; i++) {
        // 计算当前组的id行索引（从0开始）
        const idIndex = i * 3;
        const titleIndex = idIndex + 1;
        const abstractIndex = idIndex + 2;

        // 检查索引是否有效
        if (
          idIndex < lines.length &&
          titleIndex < lines.length &&
          abstractIndex < lines.length
        ) {
          newPaper2Data.push({
            id: lines[idIndex].trim(),
            title: lines[titleIndex].trim(),
            abstract: lines[abstractIndex].trim(),
          });
        }
      }
      paper2Data.value = newPaper2Data;
    }
  } catch (error) {
    console.error("读取paper2.txt失败:", error);
  }
});

// 刷新sample.txt和paper.txt的内容

// 原有的最新资讯按钮处理函数已替换为handleProcessNewsAndGenerateQuestions

const handleActionButtonClick = async () => {
  try {
    const fileContent = await window.api.readLocalFile("user-preferences.txt");

    if (fileContent) {
      console.log("读取到的偏好内容:", fileContent);
      const queryMessage = `请你用arxiv-mcp-server的工具查找三篇和${fileContent}有关的论文，要新一点，sort_by参数为date。你的回答应该遵循以下格式，每行小标题加粗：标题：此处为对应标题\n摘要：此处为对应摘要，中文，控制在二十字以内\n链接：此处为对应论文链接`;
      console.log("构建的查询消息:", queryMessage);

      await handleSend({
        text: queryMessage,
        files: [],
        links: [],
        think: false,
        search: false,
      });
    } else {
      console.error("文件内容为空");
      alert(
        "用户偏好文件内容为空，请检查项目根目录下的user-preferences.txt文件",
      );
    }
  } catch (error) {
    console.error("读取文件并发送消息时出错:", error);
    alert(`读取或发送消息失败: ${(error as Error).message || "未知错误"}`);
  }
};

const handleRefreshButtonClick = async () => {
  console.log("刷新按钮被点击");
  try {
    // 显示正在处理的提示
    alert("开始执行问题生成，将等待30秒后处理...");

    // 等待30秒
    console.log("等待30秒...");

    // 读取sample.txt文件
    let sampleContent = "";
    try {
      sampleContent = await window.api.readLocalFile("sample.txt");
      console.log("读取到的sample.txt内容:", sampleContent);
    } catch (err) {
      console.error("无法读取sample.txt文件:", err);
      alert("无法读取sample.txt文件");
      return;
    }

    // 解析sample.txt的所有行
    const lines = sampleContent.split("\n");
    console.log("sample.txt总行数:", lines.length);

    // 初始化paperContent数组 - 使用二维数组以便处理多行内容
    let paperContent: string[][] = []; // 初始化为空数组

    let hasValidCalls = false;

    let paperContent2: string[][] = []; // 初始化为空数组

    // 定义检查和调用接口的通用函数
    const checkLineAndCallApi = async (
      lineIndex: number,
      paramLineIndex: number,
      lineNum: number,
      paramLineNum: number,
      paperContentIndex: number,
    ) => {
      // 确保paperContent有足够的子数组
      while (paperContent.length <= paperContentIndex) {
        paperContent.push([]);
      }
      while (paperContent2.length <= paperContentIndex) {
        paperContent2.push([]);
      }

      // 检查指定行是否包含'1'或'0'
      if (lines.length > lineIndex) {
        const lineContent = lines[lineIndex].trim();

        if (lineContent === "1") {
          console.log(
            `第${lineNum}行包含1，准备使用第${paramLineNum}行内容作为参数调用接口`,
          );
          // 确保参数行存在
          if (lines.length > paramLineIndex) {
            // 获取参数行内容并去除首尾空白
            const queryParam = lines[paramLineIndex].trim();
            console.log(
              `第${lineNum}行对应的参数(第${paramLineNum}行内容):`,
              queryParam,
            );

            // 只有当参数不为空时才调用接口
            if (queryParam) {
              // 1. 调用BM25 API
              const bm25Response = await callBM25Api(queryParam);
              if (bm25Response && bm25Response.length > 0) {
                // 取第一个结果，标题和摘要分别存储为两行
                const paper = bm25Response[0];
                const title = paper.title || "无标题";
                const abstract = paper.original_abstract || "无摘要";
                const id = paper.id || "未知ID";
                paperContent[paperContentIndex] = [id, title, abstract]; // id一行，标题一行，摘要一行
                hasValidCalls = true;
                console.log(`已成功获取第${lineNum}行参数的BM25论文结果`);
              }

              // 2. 同时调用Sentence-BERT API接口
              try {
                // 调用Sentence-BERT API
                const sentenceBertResponse =
                  await callSentenceBertApi(queryParam);

                // 保存Sentence-BERT结果到paper2.txt，与BM25处理方式保持一致
                if (sentenceBertResponse && sentenceBertResponse.length > 0) {
                  // 取第一个结果，标题和摘要分别存储
                  const paper = sentenceBertResponse[0];
                  const title = paper.title || "无标题";
                  const abstract = paper.original_abstract || "无摘要";
                  const id = paper.id || "未知ID";

                  // 格式化结果为三行：ID、标题、摘要
                  paperContent2[paperContentIndex] = [id, title, abstract]; // id一行，标题一行，摘要一行
                }
              } catch (sentenceError) {
                console.error("调用Sentence-BERT API失败:", sentenceError);
                // 不中断流程，继续执行BM25的结果处理
              }
            } else {
              console.warn(`第${paramLineNum}行内容为空，跳过API调用`);
            }
          } else {
            console.warn(`第${paramLineNum}行不存在`);
          }
        } else if (lineContent === "0") {
          // 如果包含'0'，写入三行'1'
          console.log(`第${lineNum}行包含0，设置为三行'1'`);
          paperContent[paperContentIndex] = ["1", "1", "1"];
          paperContent2[paperContentIndex] = ["1", "1", "1"];
          hasValidCalls = true;
        }
        // 其他情况保持默认的['1']
      }
    };

    // 按行分别处理第7-11行
    // 第7行(索引6) -> 第12行(索引11) -> 存储到paperContent[1]
    await checkLineAndCallApi(6, 11, 7, 12, 1);
    // 第8行(索引7) -> 第13行(索引12) -> 存储到paperContent[2]
    await checkLineAndCallApi(7, 12, 8, 13, 2);
    // 第9行(索引8) -> 第14行(索引13) -> 存储到paperContent[3]
    await checkLineAndCallApi(8, 13, 9, 14, 3);
    // 第10行(索引9) -> 第15行(索引14) -> 存储到paperContent[4]
    await checkLineAndCallApi(9, 14, 10, 15, 4);
    // 第11行(索引10) -> 第16行(索引15) -> 存储到paperContent[5]
    await checkLineAndCallApi(10, 15, 11, 16, 5);

    if (!hasValidCalls) {
      // 如果没有有效的调用，使用默认内容
      console.log("没有有效的API调用，使用默认内容");
      // 使用二维数组结构，包含id、标题和摘要三行格式
      paperContent = [
        ["default-id-1", "默认论文标题1", "这是默认论文1的摘要"], // 第一组（包含id、标题和摘要）
        ["default-id-2", "默认论文标题2", "这是默认论文2的摘要"], // 第二组
        ["default-id-3", "默认论文标题3", "这是默认论文3的摘要"], // 第三组
        ["1"], // 最后一行
      ];
    }

    // 展平二维数组为一维数组，用于写入文件
    const flattenedContent: string[] = [];
    const flattenedContent2: string[] = [];
    paperContent.forEach((subArray) => {
      subArray.forEach((line) => flattenedContent.push(line));
    });
    paperContent2.forEach((subArray) => {
      subArray.forEach((line) => flattenedContent2.push(line));
    });

    console.log("准备写入paper.txt的内容:", flattenedContent);

    // 写入paper.txt文件
    try {
      await window.api.writeLocalFile("paper.txt", flattenedContent.join("\n"));
      console.log("成功写入paper.txt文件");
      alert("paper.txt文件已成功更新");
    } catch (error) {
      console.error("写入paper.txt文件失败:", error);
      alert("写入paper.txt文件失败");
    }
    // 写入paper2.txt文件
    try {
      await window.api.writeLocalFile(
        "paper2.txt",
        flattenedContent2.join("\n"),
      );
      console.log("成功写入paper2.txt文件");
      alert("paper2.txt文件已成功更新");
    } catch (error) {
      console.error("写入paper2.txt文件失败:", error);
      alert("写入paper2.txt文件失败");
    }
  } catch (error) {
    console.error("刷新按钮处理失败:", error);
    alert(`操作失败: ${(error as Error).message || "未知错误"}`);
  }
};

// BM25接口调用函数
const callBM25Api = async (query: string): Promise<any[]> => {
  try {
    console.log("准备发送BM25请求，查询参数:", query);

    const apiUrl = "http://localhost:2625/bm25/score";
    const requestBody = {
      query: query,
      k1: 0.9,
      b: 0.5,
    };

    const startTime = performance.now();
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(requestBody),
    });
    const endTime = performance.now();

    const responseTime = Math.round(endTime - startTime);
    console.log(
      `BM25请求完成，状态码: ${response.status}，响应时间: ${responseTime}ms`,
    );

    if (!response.ok) {
      throw new Error(`HTTP错误！状态码：${response.status}`);
    }

    const responseData = await response.json();
    console.log("BM25接口返回结果:", responseData);

    // 正确提取results字段中的论文列表
    const papers = (responseData as { results?: any[] }).results || [];
    console.log(`本次调用返回的论文数量:`, papers.length);

    return papers;
  } catch (err) {
    // 改进的错误处理
    console.error("调用BM25接口失败:", err);
    let errorMessage = "连接BM25服务失败";
    if (err instanceof Error) {
      errorMessage = err.message;
    } else {
      errorMessage = String(err);
    }
    // 不在这里显示alert，避免多次调用时弹出多个alert
    console.warn(`警告: ${errorMessage}`);
    return [];
  }
};

// Sentence-BERT接口调用函数
const callSentenceBertApi = async (query: string): Promise<any[]> => {
  try {
    console.log("准备发送Sentence-BERT请求，查询参数:", query);

    // 确保与BM25使用相同的API URL结构
    const apiUrl = "http://localhost:2378/sentence-bert/match";
    // 保持与BM25相同的请求参数格式，即使Sentence-BERT可能不使用k1和b参数
    const requestBody = {
      query: query,
    };

    const startTime = performance.now();
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(requestBody),
    });
    const endTime = performance.now();

    const responseTime = Math.round(endTime - startTime);
    console.log(
      `Sentence-BERT请求完成，状态码: ${response.status}，响应时间: ${responseTime}ms`,
    );

    if (!response.ok) {
      throw new Error(`HTTP错误！状态码：${response.status}`);
    }

    const responseData = await response.json();
    console.log("Sentence-BERT接口返回结果:", responseData);

    // 假设返回格式与BM25类似，提取results字段
    const papers = (responseData as { results?: any[] }).results || [];
    console.log(`本次Sentence-BERT调用返回的论文数量:`, papers.length);

    return papers;
  } catch (err) {
    // 改进的错误处理
    console.error("调用Sentence-BERT接口失败:", err);
    let errorMessage = "连接Sentence-BERT服务失败";
    if (err instanceof Error) {
      errorMessage = err.message;
    } else {
      errorMessage = String(err);
    }
    console.warn(`警告: ${errorMessage}`);
    return [];
  }
};

const handleQuestionGenerateClick = () => {
  router.push("/question");
};

const handleBackToHome = () => {
  router.push("/chat");
};

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
    console.log(`[新闻处理调试] ${message}`, data || "");
  }
};

// 截断文本以控制token数量
const truncateTextToTokens = (text: string, maxTokens: number): string => {
  if (estimateTokens(text) <= maxTokens) return text;

  // 简单截断策略：从开头保留，同时留出一些缓冲
  const safetyFactor = 0.8; // 安全系数，确保不会超过限制
  const maxChars = Math.floor(maxTokens * 1.5 * safetyFactor); // 保守估计

  return text.substring(0, maxChars) + "...（内容已截断以控制长度）";
};

const handleProcessNewsAndGenerateQuestions = async () => {
  debugLog("开始处理新闻并生成问题结构");
  try {
    // 1. 首先获取新闻内容，修改查询减少返回内容
    const newsQuery = `用fetch,url=https://news.aibase.cn/news,max_length=500,结果只包含三条最重要的新闻总结,每条30字以内,不要有其他内容`;
    debugLog("构建的新闻查询消息:", newsQuery);

    const tabId = window.api.getWebContentsId();

    try {
      // 创建线程获取新闻，减少上下文长度以避免token超限
      const modelContextLimit = contextLength.value || 32000;
      const newsThreadId = await threadPresenter.createConversation(
        "新闻处理",
        {
          providerId: activeModel.value.providerId,
          modelId: activeModel.value.id,
          systemPrompt: "你是一个简洁的信息提取助手。", // 使用极简系统提示
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
          enabledMcpTools: chatStore.chatConfig.enabledMcpTools,
        } as any,
        tabId,
      );
      debugLog("创建的新闻线程ID:", newsThreadId);

      const newsMessageContent = JSON.stringify({
        text: newsQuery,
        files: [],
        links: [],
        think: false,
        search: false,
      });

      await threadPresenter.sendMessage(
        newsThreadId,
        newsMessageContent,
        "user",
      );
      await threadPresenter.startStreamCompletion(newsThreadId, undefined, {});

      // 提取新闻内容的函数
      const extractAssistantText = (assistantMsg: any) => {
        if (!assistantMsg || !assistantMsg.content) return "";
        const parts: string[] = [];
        for (const block of assistantMsg.content) {
          if (!block) continue;
          if (block.type === "content" && block.content)
            parts.push(block.content);
          else if (block.type === "reasoning_content" && block.content)
            parts.push(block.content);
          else if (
            block.type === "tool_call" &&
            block.tool_call &&
            block.tool_call.response
          )
            parts.push(block.tool_call.response);
          else if (typeof block.content === "string") parts.push(block.content);
        }
        return parts.join("\n").trim();
      };

      let newsContent = "";
      const maxAttempts = 30; // 减少重试次数以避免频繁请求
      let retryDelay = 2000; // 增加初始延迟时间
      for (let i = 0; i < maxAttempts; i++) {
        await new Promise((r) => setTimeout(r, retryDelay));
        try {
          const msgsRes: any = await threadPresenter.getMessages(
            newsThreadId,
            1,
            100,
          );
          const assistantMsg = msgsRes?.list?.find(
            (m: any) =>
              m.role === "assistant" && m.content && m.content.length > 0,
          );
          if (assistantMsg) {
            newsContent = extractAssistantText(assistantMsg);
            if (newsContent && newsContent.length > 0) break;
          }
        } catch (err) {
          debugLog("获取新闻消息时出错，稍候重试", err);
          // 检测429错误并增加延迟
          if (
            err instanceof Error &&
            (err.message.includes("429") ||
              err.message.includes("too many requests"))
          ) {
            debugLog("检测到429错误，增加延迟时间");
            retryDelay *= 1.5; // 指数退避
            if (retryDelay > 10000) retryDelay = 10000; // 设置最大延迟
          }
        }
      }

      if (!newsContent) {
        console.log("未获取到新闻内容");
        alert("未能获取到新闻内容，请稍后再试");
        return;
      }

      // 截断新闻内容以控制token数量（由于提示词变长，进一步降低新闻内容限制）
      newsContent = truncateTextToTokens(newsContent, 300); // 降低限制到300个token，增加安全余量
      debugLog("获取并截断的新闻内容:", newsContent);
      const newsTokens = estimateTokens(newsContent);
      debugLog("估算的新闻内容token数:", newsTokens);
      debugLog("新闻内容原始长度/截断后长度:", `${newsContent.length}`);

      // 2. 使用简洁的系统提示词
      const systemPromptForQuestionGeneration = `你是一个专业的AI助手，擅长从新闻内容中提取关键信息并生成结构化问题。请严格按照用户提供的指令处理新闻内容。`;

      // 创建新线程生成问题结构，合理设置参数以避免token超限
      const questionThreadId = await threadPresenter.createConversation(
        "新闻问题生成",
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
          enabledMcpTools: chatStore.chatConfig.enabledMcpTools,
        } as any,
        tabId,
      );
      debugLog("创建的问题生成线程ID:", questionThreadId);

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
      debugLog("指导内容token估算:", instructionsTokens);

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

      debugLog("估算的总输入token数:", estimateTokens(combinedText));
      debugLog(
        "模型上下文限制/可用输入token数:",
        `${modelContextLimit}/${maxInputTokens}`,
      );

      let questionMessageContent = JSON.stringify({
        text: combinedText,
        files: [],
        links: [],
        think: false,
        search: false,
      });

      // 发送消息前再次检查token数
      const finalTokens = estimateTokens(
        JSON.parse(questionMessageContent).text,
      );
      debugLog("发送前最终检查的token数:", finalTokens);

      // 如果token数仍然很高，再次减少内容（增加安全阈值）
      if (finalTokens > maxInputTokens * 0.9) {
        // 使用90%的限制作为警告阈值
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
        debugLog("使用超简化指导，新的token估算:", newTokens);

        // 更新消息内容
        questionMessageContent = JSON.stringify({
          text: combinedText,
          files: [],
          links: [],
          think: false,
          search: false,
        });
      }

      try {
        await threadPresenter.sendMessage(
          questionThreadId,
          questionMessageContent,
          "user",
        );
        // 添加延迟以避免请求过快
        await new Promise((r) => setTimeout(r, 1000));
        await threadPresenter.startStreamCompletion(
          questionThreadId,
          undefined,
          {},
        );
      } catch (error) {
        debugLog("发送消息或开始流式完成时出错:", error);
        // 捕获可能的token超限错误，提供更友好的错误信息
        if (
          error instanceof Error &&
          error.message.includes("maximum context length")
        ) {
          alert(
            "内容过长导致模型无法处理。请尝试使用更简短的新闻内容或降低请求的复杂度。",
          );
          return;
        }
        // 捕获429错误，提供更友好的错误信息
        if (
          error instanceof Error &&
          (error.message.includes("429") ||
            error.message.includes("too many requests"))
        ) {
          alert(
            "请求频率过高，请稍后再试。系统已优化请求间隔，您可以等待一会儿后重试。",
          );
          return;
        }
        throw error;
      }

      let questionStructure = "";
      let questionRetryDelay = 2000; // 增加初始延迟时间
      for (let i = 0; i < maxAttempts; i++) {
        await new Promise((r) => setTimeout(r, questionRetryDelay));
        try {
          const msgsRes: any = await threadPresenter.getMessages(
            questionThreadId,
            1,
            100,
          );
          const assistantMsg = msgsRes?.list?.find(
            (m: any) =>
              m.role === "assistant" && m.content && m.content.length > 0,
          );
          if (assistantMsg) {
            questionStructure = extractAssistantText(assistantMsg);
            if (questionStructure && questionStructure.length > 0) break;
          }
        } catch (err) {
          debugLog("获取问题结构时出错，稍候重试", err);
          // 检测429错误并增加延迟
          if (
            err instanceof Error &&
            (err.message.includes("429") ||
              err.message.includes("too many requests"))
          ) {
            debugLog("检测到429错误，增加延迟时间");
            questionRetryDelay *= 1.5; // 指数退避
            if (questionRetryDelay > 10000) questionRetryDelay = 10000; // 设置最大延迟
          }
        }
      }

      if (!questionStructure) {
        debugLog("未获取到问题结构");
        alert("未能生成问题结构，请稍后再试");
        return;
      }

      debugLog("生成的问题结构:", questionStructure);
      debugLog("生成的问题结构token估算:", estimateTokens(questionStructure));

      // 后处理问题结构，清理占位符文本和格式
      let cleanedQuestionStructure = questionStructure;

      // 清理占位符文本
      cleanedQuestionStructure = cleanedQuestionStructure.replace(
        /关键词1|关键词2|关键词3|关键词4|关键词5|关键词6/g,
        "",
      );
      // 移除空行
      cleanedQuestionStructure = cleanedQuestionStructure
        .split("\n")
        .filter((line) => line.trim() !== "")
        .join("\n");

      debugLog("清理后的问题结构:", cleanedQuestionStructure);

      // 显示清理后的问题结构
      alert(`生成的问题结构：\n\n${cleanedQuestionStructure}`);
      debugLog("处理完成，问题结构已显示给用户");
    } catch (error) {
      debugLog("处理新闻和生成问题结构时出错:", error);
      alert(`处理失败: ${(error as Error).message || "未知错误"}`);
    }
  } catch (error) {
    debugLog("处理新闻按钮点击失败:", error);
    alert(`处理失败: ${(error as Error).message || "未知错误"}`);
  } finally {
    debugLog("新闻处理流程结束");
  }
};

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
    enabledMcpTools: chatStore.chatConfig.enabledMcpTools,
  } as any);
  console.log("threadId", threadId, activeModel.value);
  chatStore.sendMessage(content);
};
</script>
