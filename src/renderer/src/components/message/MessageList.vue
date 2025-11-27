<template>
  <div class="w-full h-full flex">
    <!-- 左侧侧边栏和Sample组件 -->
    <div
      class="w-80 border-r border-gray-200 dark:border-gray-800 h-full flex flex-col overflow-hidden"
    >
      <!-- Sample内容展示区域 -->
      <div class="flex-1 overflow-y-auto p-4">
        <!-- 显示sample.txt的内容 -->
        <div v-if="sampleTitle" class="mb-12">
          <div class="mb-6">
            <h1
              class="text-2xl md:text-3xl font-bold py-4 text-center text-gray-800 dark:text-gray-100"
            >
              {{ sampleTitle }}
            </h1>
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
                v-if="showPaperBox.length > index && showPaperBox[index] === 1"
                class="mt-5"
              >
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

    <!-- 右侧原有消息列表 -->
    <div class="flex-1 h-full relative min-h-0">
      <div
        ref="messagesContainer"
        class="message-list-container relative flex-1 scrollbar-hide overflow-y-auto w-full h-full pr-12 lg:pr-12"
        @scroll="handleScroll"
      >
        <div
          ref="messageList"
          class="w-full break-all transition-opacity duration-300 pt-4"
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
      <template v-if="!capture.isCapturing.value">
        <MessageActionButtons
          :show-clean-button="!showCancelButton"
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
// === Vue Core ===
import { ref, onMounted, nextTick, watch, computed, toRef } from "vue";

// === Types ===
import { AssistantMessage, UserMessage } from "@shared/chat";

// === Components ===
import MessageItemAssistant from "./MessageItemAssistant.vue";
import MessageItemUser from "./MessageItemUser.vue";
import MessageActionButtons from "./MessageActionButtons.vue";
import ReferencePreview from "./ReferencePreview.vue";
import MessageMinimap from "./MessageMinimap.vue";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@shadcn/components/ui/dialog";
import { Button } from "@shadcn/components/ui/button";

// === Composables ===
import { useResizeObserver } from "@vueuse/core";
import { useI18n } from "vue-i18n";
import { useMessageScroll } from "@/composables/message/useMessageScroll";
import { useCleanDialog } from "@/composables/message/useCleanDialog";
import { useMessageMinimap } from "@/composables/message/useMessageMinimap";
import { useMessageCapture } from "@/composables/message/useMessageCapture";
import { useMessageRetry } from "@/composables/message/useMessageRetry";
import { useSampleData } from "@/composables/useSampleData";

// === Stores ===
import { useChatStore } from "@/stores/chat";
import { useReferenceStore } from "@/stores/reference";

// 使用composable处理sample数据
const {
  keywords,
  summary,
  showPaperBox,
  paperData,
  sampleTitle,
  sampleColumns,
  loadSampleData,
} = useSampleData();

// === Props & Emits ===
const { t } = useI18n();
const props = defineProps<{
  messages: Array<UserMessage | AssistantMessage>;
}>();

// === Stores ===
const chatStore = useChatStore();
const referenceStore = useReferenceStore();

// === Composable Integrations ===
// Scroll management
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

// Clean dialog
const cleanDialog = useCleanDialog();

// Minimap (needs scrollInfo from scroll composable)
const minimap = useMessageMinimap(scroll.scrollInfo);

// Screenshot capture
const capture = useMessageCapture();

// Message retry
const retry = useMessageRetry(toRef(props, "messages"));

// === Local State ===
const messageList = ref<HTMLDivElement>();
const visible = ref(false);
const shouldAutoFollow = ref(true);

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
    if (force) {
      shouldAutoFollow.value = true;
    }
  });
};

const scrollToBottom = (force = false) => {
  if (force) {
    shouldAutoFollow.value = true;
  }
  scheduleScrollToBottom(force);
};

// === Event Handlers ===
const handleCopyImage = async (
  messageId: string,
  parentId?: string,
  fromTop: boolean = false,
  modelInfo?: { model_name: string; model_provider: string },
) => {
  await capture.captureMessage({ messageId, parentId, fromTop, modelInfo });
};

const handleRetry = async (index: number) => {
  const triggered = await retry.retryFromUserMessage(index);
  if (triggered) {
    scrollToBottom(true);
  }
};

// === Computed ===
const showCancelButton = computed(() => {
  return chatStore.generatingThreadIds.has(chatStore.getActiveThreadId() ?? "");
});

// === Lifecycle Hooks ===
onMounted(() => {
  // Initialize scroll and visibility
  scheduleScrollToBottom(true);
  nextTick(() => {
    visible.value = true;
    setupScrollObserver();
    updateScrollInfo();
  });

  useResizeObserver(messageList, () => {
    scheduleScrollToBottom();
  });

  watch(
    () => aboveThreshold.value,
    (isAbove) => {
      shouldAutoFollow.value = !isAbove;
    },
  );

  // Update scroll info when message count changes
  watch(
    () => props.messages.length,
    (length, prevLength) => {
      const isGrowing = length > prevLength;
      const isReset = prevLength > 0 && length < prevLength;

      if (!isGrowing && !isReset) {
        return;
      }

      scheduleScrollToBottom(isReset);
    },
    { flush: "post" },
  );

  // 加载sample数据
  loadSampleData();
});

// === Expose ===
defineExpose({
  scrollToBottom,
  scrollToMessage,
  aboveThreshold,
});
</script>

<style scoped>
.message-highlight {
  background-color: rgba(59, 130, 246, 0.1);
  border-left: 3px solid rgb(59, 130, 246);
  transition: all 0.3s ease;
}

.dark .message-highlight {
  background-color: rgba(59, 130, 246, 0.15);
}
</style>
