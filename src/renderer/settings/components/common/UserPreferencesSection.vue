<template>
  <div class="space-y-4">
    <h3 class="text-lg font-semibold">用户偏好</h3>
    <div class="p-4 border rounded-lg bg-card/50">
      <pre class="whitespace-pre-wrap text-sm text-muted-foreground">{{ preferencesContent }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const preferencesContent = ref('加载中...')

onMounted(async () => {
  try {
    // 通过IPC与主进程通信，读取user-preferences.txt文件
    const fileContent = await window.api.readLocalFile('user-preferences.txt');
    
    if (fileContent) {
      preferencesContent.value = fileContent;
      console.log('成功加载用户偏好设置');
    } else {
      preferencesContent.value = '用户偏好设置文件为空';
      console.warn('用户偏好设置文件为空');
    }
  } catch (error) {
    preferencesContent.value = '无法加载用户偏好设置\n请确保user-preferences.txt文件存在且可读';
    console.error('加载用户偏好设置失败:', error);
  }
})
</script>