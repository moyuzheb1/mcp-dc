<template>
  <span class="text-reveal">
    <span 
      v-for="(char, index) in displayedText" 
      :key="index"
      class="reveal-char"
      :style="{
        animationDelay: `${index * speed}ms`,
        opacity: 1
      }"
    >
      {{ char }}
    </span>
  </span>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';

interface Props {
  text: string;
  speed?: number; // 每个字符的显示延迟，单位毫秒
  delay?: number; // 开始动画的延迟，单位毫秒
  revealAllOnHover?: boolean; // 鼠标悬停时是否立即显示所有文本
}

const props = withDefaults(defineProps<Props>(), {
  speed: 100,
  delay: 0,
  revealAllOnHover: true
});

const fullText = ref(props.text);
const displayedLength = ref(0);
const isHovered = ref(false);

// 计算当前要显示的文本
const displayedText = computed(() => {
  if (isHovered.value && props.revealAllOnHover) {
    return fullText.value;
  }
  return fullText.value.slice(0, displayedLength.value);
});

// 开始逐字显示动画
const startReveal = () => {
  let currentIndex = 0;
  const interval = setInterval(() => {
    if (currentIndex < fullText.value.length) {
      displayedLength.value++;
      currentIndex++;
    } else {
      clearInterval(interval);
    }
  }, props.speed);
};

// 监听文本变化，重新开始动画
watch(() => props.text, (newText) => {
  fullText.value = newText;
  displayedLength.value = 0;
  setTimeout(() => startReveal(), props.delay);
}, { immediate: true });

// 组件挂载时开始动画
onMounted(() => {
  if (fullText.value) {
    setTimeout(() => startReveal(), props.delay);
  }
});

// 暴露鼠标悬停状态
const handleMouseEnter = () => {
  isHovered.value = true;
};

const handleMouseLeave = () => {
  isHovered.value = false;
};

defineExpose({
  handleMouseEnter,
  handleMouseLeave
});
</script>

<style scoped>
.text-reveal {
  display: inline;
}

.reveal-char {
  opacity: 0;
  animation: fadeIn 0.1s ease forwards;
  display: inline-block;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>