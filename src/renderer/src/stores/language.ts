import { defineStore } from 'pinia'
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

export const useLanguageStore = defineStore('language', () => {
  const { locale } = useI18n({ useScope: 'global' })
  const language = ref<string>('zh-CN') // 固定为简体中文
  const dir = ref<'auto' | 'rtl' | 'ltr'>('auto')
  
  // 初始化设置
  const initLanguage = async () => {
    try {
      // 固定使用简体中文
      locale.value = 'zh-CN'
      dir.value = 'auto'
    } catch (error) {
      console.error('初始化语言失败:', error)
    }
  }

  // 在 store 创建时初始化
  onMounted(async () => {
    await initLanguage()
  })

  return {
    language,
    initLanguage,
    dir
  }
})
