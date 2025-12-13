<template>
  <div class="paper-analysis-view">
    <div class="container">
      <h1 class="title">论文拆解</h1>
      <p class="subtitle">上传学术论文，AI帮你快速拆解核心内容</p>

      <!-- 上传区域 -->
      <div v-if="!analysisResult" class="upload-section">
        <div
          ref="dropZone"
          class="drop-zone"
          :class="{ 'dragover': isDragging }"
          @dragover.prevent="handleDragOver"
          @dragleave.prevent="handleDragLeave"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <div class="drop-zone-content">
            <div class="upload-icon">📄</div>
            <h3>拖拽文件到此处或点击上传</h3>
            <p>支持 PDF、Word 或 TXT 格式，单个文件不超过 50MB</p>
            <input
              ref="fileInput"
              type="file"
              accept=".pdf,.doc,.docx,.txt"
              @change="handleFileChange"
              class="file-input"
            />
          </div>
        </div>
      </div>

      <!-- 分析进度 -->
      <div v-if="isAnalyzing" class="analysis-progress">
        <div class="progress-container">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
          </div>
          <div class="progress-text">{{ progress }}%</div>
        </div>
        <p class="analysis-status">正在分析论文内容，请稍候...</p>
      </div>

      <!-- 分析结果 -->
      <div v-if="analysisResult" class="analysis-result">
        <div class="result-header">
          <h2>分析结果：{{ analysisResult.title }}</h2>
          <button class="new-analysis-btn" @click="newAnalysis">重新分析</button>
        </div>

        <div class="result-content">
          <!-- 论文摘要 -->
          <section class="result-section">
            <h3 class="section-title">📋 论文摘要</h3>
            <div class="section-content">{{ analysisResult.abstract }}</div>
          </section>

          <!-- 论文结构 -->
          <section class="result-section">
            <h3 class="section-title">📊 论文结构</h3>
            <ul class="paper-structure">
              <li v-for="(section, index) in analysisResult.structure" :key="index" class="structure-item">
                <span class="structure-number">{{ section.number }}</span>
                <span class="structure-title">{{ section.title }}</span>
                <span class="structure-page">{{ section.page }}页</span>
              </li>
            </ul>
          </section>

          <!-- 核心内容拆解 -->
          <section class="result-section">
            <h3 class="section-title">🔍 核心内容拆解</h3>
            <div class="core-content">
              <div v-for="(content, index) in analysisResult.coreContent" :key="index" class="content-item">
                <h4 class="content-title">{{ content.title }}</h4>
                <p class="content-text">{{ content.text }}</p>
              </div>
            </div>
          </section>

          <!-- 关键点总结 -->
          <section class="result-section">
            <h3 class="section-title">📝 关键点总结</h3>
            <div class="key-points">
              <div v-for="(point, index) in analysisResult.keyPoints" :key="index" class="key-point-item">
                <span class="point-number">{{ index + 1 }}</span>
                <span class="point-text">{{ point }}</span>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// === Vue Core ===
import { ref, onMounted, onUnmounted } from 'vue'

// === Composables ===
import { useRouter } from 'vue-router'
import { usePresenter } from '@/composables/usePresenter'
import { useToast } from '@/components/use-toast'

const router = useRouter()
const filePresenter = usePresenter('filePresenter')
const { toast } = useToast()

// 文件输入引用
const fileInput = ref<HTMLInputElement | null>(null)
const dropZone = ref<HTMLDivElement | null>(null)

// 状态管理
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const isAnalyzing = ref(false)
const progress = ref(0)
const analysisResult = ref<any>(null)
let progressInterval: ReturnType<typeof setInterval> | null = null

// 触发文件选择对话框
const triggerFileInput = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    processFile(target.files[0])
  }
}

// 处理拖拽事件
const handleDragOver = () => {
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (files && files.length > 0) {
    processFile(files[0])
  }
}

// 处理文件
const processFile = (file: File) => {
  // 检查文件类型
  const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
  if (!allowedTypes.includes(file.type)) {
    toast({ title: '错误', description: '请上传 PDF、Word 或 TXT 格式的文件', variant: 'destructive' })
    return
  }

  // 检查文件大小 (最大 50MB)
  if (file.size > 50 * 1024 * 1024) {
    toast({ title: '错误', description: '文件大小不能超过 50MB', variant: 'destructive' })
    return
  }

  selectedFile.value = file
  analyzePaper()
}

// 分析论文
const analyzePaper = async () => {
  if (!selectedFile.value) return

  isAnalyzing.value = true
  progress.value = 0

  // 模拟进度条
  progressInterval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.floor(Math.random() * 10) + 5
    }
  }, 300)

  try {
    let paperContent = ''

    // 根据文件类型读取内容
    if (selectedFile.value.type === 'text/plain') {
      paperContent = await readTextFile(selectedFile.value)
    } else {
      // 对于其他格式，需要使用文件演示器处理
      const path = window.api.getPathForFile(selectedFile.value)
      const mimeType = await filePresenter.getMimeType(path)
      const messageFile = await filePresenter.prepareFile(path, mimeType)
      paperContent = messageFile?.content || ''
    }

    // 模拟AI分析
    await new Promise(resolve => setTimeout(resolve, 2000))
    clearInterval(progressInterval!)
    progress.value = 100

    // 模拟分析结果
    analysisResult.value = generateMockAnalysis(paperContent, selectedFile.value.name)
  } catch (error) {
    console.error('分析论文失败:', error)
    toast({ title: '错误', description: '分析论文时发生错误', variant: 'destructive' })
  } finally {
    isAnalyzing.value = false
  }
}

// 读取文本文件
const readTextFile = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      resolve(e.target?.result as string)
    }
    reader.onerror = reject
    reader.readAsText(file)
  })
}

// 生成模拟分析结果
const generateMockAnalysis = (content: string, fileName: string) => {
  // 从文件名中提取论文标题
  const title = fileName.replace(/\.[^/.]+$/, "")

  return {
    title,
    abstract: `这是一篇关于${title}的学术论文。本文探讨了该领域的最新研究进展、核心理论和实践应用，通过实证研究和理论分析，提出了新的观点和方法。论文结构清晰，论证充分，对相关领域的研究具有重要参考价值。`,
    structure: [
      { number: '1', title: '引言', page: 1 },
      { number: '2', title: '文献综述', page: 3 },
      { number: '3', title: '研究方法', page: 7 },
      { number: '4', title: '实验结果', page: 12 },
      { number: '5', title: '讨论与分析', page: 18 },
      { number: '6', title: '结论与展望', page: 25 }
    ],
    coreContent: [
      {
        title: '研究背景',
        text: '随着人工智能技术的快速发展，自然语言处理在学术研究中的应用越来越广泛。本文旨在探讨如何利用先进的NLP技术提高学术论文的阅读和理解效率。'
      },
      {
        title: '核心方法',
        text: '本文提出了一种基于Transformer的论文内容拆解模型，该模型能够自动识别论文的结构、提取核心观点，并生成简洁的摘要。实验结果表明，该方法在多种评估指标上均优于现有方法。'
      },
      {
        title: '主要发现',
        text: '研究发现，AI辅助的论文拆解能够显著提高科研人员的阅读效率，减少信息获取时间。同时，该方法还能够帮助读者更好地理解论文的核心内容和逻辑结构。'
      }
    ],
    keyPoints: [
      '提出了一种新的论文内容拆解模型',
      '实验结果表明该方法优于现有技术',
      '能够显著提高科研人员的阅读效率',
      '有助于更好地理解论文的核心内容和逻辑结构',
      '为学术文献的自动处理提供了新的思路'
    ]
  }
}

// 重新分析
const newAnalysis = () => {
  analysisResult.value = null
  selectedFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 清理定时器
onUnmounted(() => {
  if (progressInterval) {
    clearInterval(progressInterval)
  }
})
</script>

<style scoped>
.paper-analysis-view {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 2rem 1rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  padding: 2rem 2rem 0.5rem;
  text-align: center;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
  padding: 0 2rem 2rem;
  text-align: center;
}

.upload-section {
  padding: 3rem 2rem;
}

.drop-zone {
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #fafafa;
}

.drop-zone:hover {
  border-color: #409eff;
  background-color: #f0f8ff;
}

.drop-zone.dragover {
  border-color: #409eff;
  background-color: #e6f7ff;
  transform: scale(1.02);
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.drop-zone h3 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  color: #333;
}

.drop-zone p {
  margin: 0 0 1.5rem;
  color: #666;
  font-size: 0.95rem;
}

.file-input {
  display: none;
}

.analysis-progress {
  padding: 3rem 2rem;
  text-align: center;
}

.progress-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.progress-bar {
  width: 60%;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #409eff;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: 600;
  color: #333;
  min-width: 40px;
}

.analysis-status {
  color: #666;
  font-size: 1rem;
}

.analysis-result {
  padding: 2rem;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.result-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
}

.new-analysis-btn {
  background-color: #409eff;
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background-color 0.3s ease;
}

.new-analysis-btn:hover {
  background-color: #66b1ff;
}

.result-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.result-section {
  background-color: #fafafa;
  border-radius: 8px;
  padding: 1.5rem;
}

.section-title {
  margin: 0 0 1rem;
  font-size: 1.3rem;
  color: #333;
}

.section-content {
  color: #555;
  line-height: 1.8;
}

.paper-structure {
  list-style: none;
  padding: 0;
  margin: 0;
}

.structure-item {
  display: flex;
  align-items: center;
  padding: 0.8rem 0;
  border-bottom: 1px solid #eee;
}

.structure-item:last-child {
  border-bottom: none;
}

.structure-number {
  font-weight: 600;
  color: #409eff;
  margin-right: 1rem;
  min-width: 30px;
}

.structure-title {
  flex: 1;
  color: #333;
}

.structure-page {
  color: #999;
  font-size: 0.85rem;
}

.core-content {
  display: grid;
  gap: 1.5rem;
}

.content-item {
  background-color: white;
  padding: 1rem;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.content-title {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
  color: #409eff;
}

.content-text {
  margin: 0;
  color: #555;
  line-height: 1.7;
}

.key-points {
  display: grid;
  gap: 1rem;
}

.key-point-item {
  display: flex;
  align-items: flex-start;
  background-color: white;
  padding: 1rem;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.point-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #409eff;
  color: white;
  border-radius: 50%;
  font-size: 0.85rem;
  font-weight: 600;
  margin-right: 1rem;
  flex-shrink: 0;
  margin-top: 0.2rem;
}

.point-text {
  flex: 1;
  color: #555;
  line-height: 1.7;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    border-radius: 0;
  }

  .title {
    font-size: 2rem;
    padding: 1.5rem 1rem 0.5rem;
  }

  .subtitle {
    padding: 0 1rem 1.5rem;
    font-size: 1rem;
  }

  .upload-section {
    padding: 2rem 1rem;
  }

  .drop-zone {
    padding: 2rem 1rem;
  }

  .drop-zone h3 {
    font-size: 1.3rem;
  }

  .result-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .result-header h2 {
    font-size: 1.5rem;
  }

  .analysis-result {
    padding: 1.5rem 1rem;
  }

  .progress-container {
    flex-direction: column;
    gap: 0.5rem;
  }

  .progress-bar {
    width: 80%;
  }
}
</style>
