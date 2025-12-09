<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { usePresenter } from '@/composables/usePresenter'

// --- 基础配置 ---
const router = useRouter()
const configPresenter = usePresenter('configPresenter')

// logo图片地址 (本地icon.png)
const logoUrl = '/icon.png'

// --- 状态管理 ---
const currentStage = ref(1) // 1: 欢迎, 2: 问卷, 3: 结果/选择
const currentQuestionIndex = ref(0)
const isCalculating = ref(false)
const isSkipped = ref(false) // 标记用户是否跳过了问卷

const userAnswers = reactive<Record<number, string>>({})
const finalSelectedField = ref('') // 最终选择的ID

// --- 问卷数据配置 (保持不变) ---
const questions = [
  {
    id: 1,
    text: "想象你正在玩一款非常复杂的解谜游戏，你最享受的过程是：",
    options: [
      { key: 'A', text: "欣赏画面和特效：被精美的场景、光影效果吸引。" },
      { key: 'B', text: "破解机关逻辑：思考机关背后的逻辑链条，享受智力挑战。" },
      { key: 'C', text: "寻找系统漏洞：试图卡墙、穿模，看看游戏会不会崩。" },
      { key: 'D', text: "惊叹NPC的反应：角色像真人一样聪明，好奇它怎么听懂人话的。" }
    ]
  },
  {
    id: 2,
    text: "在高中数学课上，你对以下哪种内容的接受度最高？",
    options: [
      { key: 'A', text: "几何与立体图形：空间想象力不错，喜欢看图说话。" },
      { key: 'B', text: "概率与统计：喜欢分析数据趋势，从数字里找规律。" },
      { key: 'C', text: "严谨的证明题：喜欢从已知条件一步步推导的逻辑过程。" },
      { key: 'D', text: "不太喜欢数学：更喜欢动手做实验，或者直接看到结果。" }
    ]
  },
  {
    id: 3,
    text: "如果让你用乐高积木搭一个城堡，你更倾向于：",
    options: [
      { key: 'A', text: "设计外观：专注于造型、配色，怎么看着舒服。" },
      { key: 'B', text: "搭建地基与骨架：确保结构稳固，哪怕内部别人看不见。" },
      { key: 'C', text: "编写说明书：制定一套标准步骤，让其他人也能快速搭建。" },
      { key: 'D', text: "研究积木本身：好奇积木的卡扣原理，想发明新形状。" }
    ]
  },
  {
    id: 4,
    text: "假设未来发明了一款全能机器人管家，你最想知道它背后的什么秘密？",
    options: [
      { key: 'A', text: "它的“大脑”：它是怎么学会思考和理解情感的？" },
      { key: 'B', text: "它的“神经”：指令传输有多快？断网了还能工作吗？" },
      { key: 'C', text: "它的“安全性”：黑客能不能控制它？隐私会不会泄露？" },
      { key: 'D', text: "它的“应用”：能不能帮医生分析DNA，或者帮我炒股。" }
    ]
  },
  {
    id: 5,
    text: "当你使用的APP突然闪退或变慢时，你的第一反应是：",
    options: [
      { key: 'A', text: "烦躁/吐槽体验：界面设计太烂，用户体验极差。" },
      { key: 'B', text: "好奇原因：是内存不够？还是刚才的操作触发了Bug？" },
      { key: 'C', text: "担心数据：我的聊天记录会不会丢？密码安全吗？" },
      { key: 'D', text: "无所谓/重启：重启能解决99%的问题，能用就行。" }
    ]
  },
  {
    id: 6,
    text: "如果给你一项超能力用于计算机世界，你希望是：",
    options: [
      { key: 'A', text: "透视眼：把复杂数据瞬间变成看懂的酷炫图表。" },
      { key: 'B', text: "读心术：让电脑完全理解我的人话，甚至预判我。" },
      { key: 'C', text: "极速者：让全世界的电脑运行速度提升100倍。" },
      { key: 'D', text: "规则制定者：创造一种完美语言，让程序都没有Bug。" }
    ]
  },
  {
    id: 7,
    text: "在团队合作完成作业时，你通常扮演什么角色？",
    options: [
      { key: 'A', text: "展示者/美化者：负责做PPT，排版得漂漂亮亮。" },
      { key: 'B', text: "核心攻坚者：最难啃的逻辑硬骨头由我搞定。" },
      { key: 'C', text: "挑错者/测试员：检查错误，梳理流程。" },
      { key: 'D', text: "跨界联络员：把技术应用到其他领域解决实际问题。" }
    ]
  },
  {
    id: 8,
    text: "对于“枯燥的重复劳动”（比如整理一千个文件），你的态度是？",
    options: [
      { key: 'A', text: "难以忍受：一定要写个脚本程序自动完成它。" },
      { key: 'B', text: "寻找规律：观察文件特征，通过数据分析来归类。" },
      { key: 'C', text: "耐心完成：为了宏大的目标，可以忍受基础工作。" },
      { key: 'D', text: "直接放弃：找别人来做。" }
    ]
  }
]

// --- 领域定义 ---
const fields = [
  { id: 'AI', name: '人工智能与数据智能', icon:'🧠', desc: '让电脑像人一样思考，挖掘数据规律。包括机器学习、深度学习、数据挖掘、NLP等。适合数学基础较好、喜欢探索智能本质的你。' },
  { id: 'Graphics', name: '视觉、图形与交互', icon:'🎨', desc: '创造酷炫画面，研究人机体验。包括计算机视觉、图形学、AR/VR、HCI等。适合视觉敏感、兼具技术与艺术感的你。' },
  { id: 'Systems', name: '系统与网络', icon:'⚙️', desc: '构建底层基础设施，追求极致性能。包括操作系统、分布式系统、网络、高性能计算。适合硬核、喜欢底层原理的你。' },
  { id: 'Security', name: '安全与隐私', icon:'🛡️', desc: '攻防博弈，保护系统与数据。包括网络安全、密码学、区块链。适合好奇心强、喜欢寻找漏洞和解谜的你。' },
  { id: 'Theory', name: '理论计算机科学', icon:'📐', desc: '探索计算极限，推导数学证明。包括算法设计、计算复杂性、量子计算。适合逻辑严密、喜欢数学推导的你。' },
  { id: 'SE', name: '软件工程与程序语言', icon:'📝', desc: '研究代码质量，创造开发工具。包括软件测试、程序语言设计(PL)、DevOps。适合追求规范、喜欢造轮子的你。' },
  { id: 'Interdisciplinary', name: '交叉学科应用', icon:'🧬', desc: '用计算机技术解决其他领域难题。包括生物信息学、计算金融、机器人等。适合知识面广、喜欢跨界创新的你。' }
]

// --- 逻辑控制 ---

// 1. 开始问卷
const startSurvey = () => {
  isSkipped.value = false
  currentStage.value = 2
}

// 2. 跳过问卷，直接去选择
const skipSurvey = () => {
  isSkipped.value = true
  finalSelectedField.value = 'AI' // 默认选中第一个
  currentStage.value = 3
}

// 3. 选择答案
const selectOption = (qId: number, key: string) => {
  userAnswers[qId] = key
  setTimeout(() => {
    if (currentQuestionIndex.value < questions.length - 1) {
      currentQuestionIndex.value++
    } else {
      finishSurvey()
    }
  }, 200)
}

// 4. 结算
const finishSurvey = () => {
  isCalculating.value = true
  
  const scores: Record<string, number> = { AI: 0, Graphics: 0, Systems: 0, Security: 0, Theory: 0, SE: 0, Interdisciplinary: 0 }
  const map = (qIdx: number, key: string, field: string) => { if (userAnswers[qIdx] === key) scores[field] += 1 }

  // 判分逻辑 (同前)
  map(1, 'D', 'AI'); map(2, 'B', 'AI'); map(4, 'A', 'AI'); map(6, 'B', 'AI'); map(8, 'B', 'AI');
  map(1, 'A', 'Graphics'); map(2, 'A', 'Graphics'); map(3, 'A', 'Graphics'); map(5, 'A', 'Graphics'); map(6, 'A', 'Graphics'); map(7, 'A', 'Graphics');
  map(1, 'B', 'Systems'); map(3, 'B', 'Systems'); map(4, 'B', 'Systems'); map(5, 'D', 'Systems'); map(6, 'C', 'Systems');
  map(1, 'C', 'Security'); map(4, 'C', 'Security'); map(5, 'C', 'Security');
  map(1, 'B', 'Theory'); map(2, 'C', 'Theory'); map(7, 'B', 'Theory');
  map(3, 'C', 'SE'); map(3, 'D', 'SE'); map(5, 'B', 'SE'); map(6, 'D', 'SE'); map(7, 'C', 'SE'); map(8, 'A', 'SE');
  map(4, 'D', 'Interdisciplinary'); map(7, 'D', 'Interdisciplinary');

  let maxScore = -1
  let recommended = 'AI'
  for (const [field, score] of Object.entries(scores)) {
    if (score > maxScore) {
      maxScore = score
      recommended = field
    }
  }

  setTimeout(() => {
    finalSelectedField.value = recommended
    isCalculating.value = false
    currentStage.value = 3
  }, 800)
}

// 5. 完成并跳转
const completeOnboarding = async () => {
  console.log('User Field:', finalSelectedField.value)
  await configPresenter.setSetting('init_complete', true)
  // await configPresenter.setSetting('research_field', finalSelectedField.value) 
  router.push('/thread/new')
}

const progressPercentage = computed(() => {
  return ((currentQuestionIndex.value + 1) / questions.length) * 100
})

// 获取当前选中的领域对象
const currentFieldObj = computed(() => {
  return fields.find(f => f.id === finalSelectedField.value)
})
</script>

<template>
  <div class="onboarding-container">
    <div class="background-decor"></div>
    
    <!-- 主窗口：使用大尺寸容器 -->
    <div class="main-window">
      
      <!-- 阶段 1: 欢迎页 -->
      <transition name="fade" mode="out-in">
        <div v-if="currentStage === 1" class="stage-content welcome-layout" key="stage1">
          <div class="welcome-left">
            <img :src="logoUrl" alt="DePaper Logo" class="big-logo" />
            <h1 class="app-title">DePaper</h1>
            <h2 class="app-subtitle">你的桌面级科研领航员</h2>
            <div class="divider"></div>
            <p class="desc-text">
              科研的第一步，是找到属于你的方向。<br>
              我们将通过一个<strong>简单的 8 题趣味问卷</strong>，<br>
              分析你的思维偏好，为你推荐最适合的计算机科研领域。
            </p>
            
            <div class="action-area">
              <button class="primary-button big-btn" @click="startSurvey">
                开始探索偏好
              </button>
              
              <div class="skip-area">
                <span class="skip-hint">已经明确自己的方向了？</span>
                <button class="text-button" @click="skipSurvey">
                  跳过问卷，直接选择 &rarr;
                </button>
              </div>
            </div>
          </div>
          <div class="welcome-right-decor">
            <!-- 背景网格纹理 -->
            <div class="grid-overlay"></div>
            
            <!-- 装饰元素 1: 神经网络/数据结构 (右上) -->
            <div class="float-item item-1">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="18" cy="5" r="3"></circle>
                <circle cx="6" cy="12" r="3"></circle>
                <circle cx="18" cy="19" r="3"></circle>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
              </svg>
            </div>

            <!-- 装饰元素 2: 代码符号 (左下) -->
            <div class="float-item item-2">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
              </svg>
            </div>

            <!-- 装饰元素 3: 原子/物理/核心 (中间偏右) -->
            <div class="float-item item-3">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="2"></circle>
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"></path>
                <ellipse cx="12" cy="12" rx="3" ry="8" transform="rotate(45 12 12)"></ellipse>
                <ellipse cx="12" cy="12" rx="3" ry="8" transform="rotate(-45 12 12)"></ellipse>
              </svg>
            </div>

            <!-- 装饰元素 4: 论文/文档 (左上) -->
            <div class="float-item item-4">
               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <line x1="10" y1="9" x2="8" y2="9"></line>
              </svg>
            </div>

            <!-- 装饰光晕 -->
            <div class="glow-effect"></div>
          </div>
        </div>

        <!-- 阶段 2: 问卷调查 (全屏宽阔布局) -->
        <div v-else-if="currentStage === 2" class="stage-content survey-layout" key="stage2">
          <div class="survey-top">
            <div class="progress-container">
              <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <span class="q-counter">Q{{ currentQuestionIndex + 1 }} / {{ questions.length }}</span>
          </div>

          <div class="question-wrapper">
            <h2 class="question-text">{{ questions[currentQuestionIndex].text }}</h2>
            
            <!-- 桌面端 2x2 网格布局 -->
            <div class="options-grid-desktop">
              <button 
                v-for="opt in questions[currentQuestionIndex].options" 
                :key="opt.key"
                class="option-card"
                @click="selectOption(questions[currentQuestionIndex].id, opt.key)"
              >
                <div class="opt-key-circle">{{ opt.key }}</div>
                <span class="opt-text">{{ opt.text }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 阶段 3: 结果/选择 (左右分栏布局) -->
        <div v-else-if="currentStage === 3" class="stage-content result-layout" key="stage3">
          <div class="result-sidebar">
            <div class="sidebar-header">
              <h3 v-if="!isSkipped">🎯 推荐结果</h3>
              <h3 v-else>📂 选择领域</h3>
              <p class="sidebar-desc" v-if="!isSkipped">基于测试，我们推荐：</p>
              <p class="sidebar-desc" v-else>请选择你感兴趣的方向：</p>
            </div>
            
            <div class="field-list">
              <div 
                v-for="field in fields" 
                :key="field.id"
                class="field-item"
                :class="{ active: finalSelectedField === field.id, recommended: (!isSkipped && finalSelectedField === field.id) }"
                @click="finalSelectedField = field.id"
              >
                <span class="field-icon">{{ field.icon }}</span>
                <span class="field-name">{{ field.name }}</span>
                <span v-if="!isSkipped && finalSelectedField === field.id" class="badge">推荐</span>
              </div>
            </div>
          </div>

          <div class="result-main">
            <div class="detail-card">
              <div class="detail-header">
                <span class="huge-icon">{{ currentFieldObj?.icon }}</span>
                <h2>{{ currentFieldObj?.name }}</h2>
              </div>
              <div class="detail-body">
                <p class="detail-desc">{{ currentFieldObj?.desc }}</p>
                <div class="detail-features">
                  <h4>DePaper 将为你准备：</h4>
                  <ul>
                    <li>✅ 该领域的课题推荐</li>
                    <li>✅ 一个专门服务你的科研AI助手</li>
                    <li>✅ 为你定制的学习报告</li>
                  </ul>
                </div>
              </div>
              <div class="detail-footer">
                <p class="confirm-hint">如果这不是你想要的，可以点击左侧列表切换</p>
                <button class="primary-button big-btn confirm-btn" @click="completeOnboarding">
                  确定并进入工作台
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
/* --- 全局与容器 --- */
.onboarding-container {
  width: 100vw;
  height: 100vh;
  background-color: #f1f5f9;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  color: #334155;
}

/* 装饰背景 */
.background-decor {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(circle at 10% 20%, rgba(79, 70, 229, 0.05) 0%, transparent 40%),
              radial-gradient(circle at 90% 80%, rgba(14, 165, 233, 0.05) 0%, transparent 40%);
  z-index: 0;
}

/* 主窗口 - 桌面级尺寸 */
.main-window {
  position: relative;
  z-index: 1;
  width: 90%;
  max-width: 1200px;
  height: 85vh; /* 占据屏幕高度的 85% */
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 20px 50px -12px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.8);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.stage-content {
  width: 100%;
  height: 100%;
  display: flex;
}

/* --- Stage 1: Welcome --- */
.welcome-layout {
  display: flex;
  flex-direction: row;
}

.welcome-left {
  flex: 1;
  padding: 60px 80px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}

.big-logo {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  margin-bottom: 24px;
}

.app-title {
  font-size: 48px;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  line-height: 1;
}

.app-subtitle {
  font-size: 24px;
  font-weight: 500;
  color: #64748b;
  margin-top: 10px;
  margin-bottom: 20px;
}

.divider {
  width: 60px;
  height: 4px;
  background: #4f46e5;
  margin: 20px 0 40px;
  border-radius: 2px;
}

.desc-text {
  font-size: 18px;
  line-height: 1.6;
  color: #475569;
  max-width: 500px;
  margin-bottom: 50px;
}

.action-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.big-btn {
  padding: 18px 48px;
  font-size: 18px;
  min-width: 240px;
}

.skip-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

.skip-hint {
  font-size: 14px;
  color: #94a3b8;
}

.text-button {
  background: none;
  border: none;
  color: #4f46e5;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  text-decoration: underline;
  text-underline-offset: 4px;
}

.text-button:hover {
  color: #4338ca;
}

/* --- 右侧科研主题背景（新版：柔和通透风格） --- */
.welcome-right-decor {
  flex: 1;
  /* 修改1：颜色不再是死黑蓝，而是更柔和的靛蓝到紫罗兰的渐变，衔接更自然 */
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  /* 给左侧边缘加一点内阴影，让过渡不那么生硬 */
  box-shadow: inset 10px 0 20px -10px rgba(0, 0, 0, 0.1);
}

/* 网格纹理 */
.grid-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  /* 网格线稍微亮一点 */
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  z-index: 1;
  opacity: 0.3; /* 整体网格淡一点，不要喧宾夺主 */
}

/* 装饰光晕 */
.glow-effect {
  position: absolute;
  width: 500px;
  height: 500px;
  /* 修改2：光晕改为亮白色，增加通透感 */
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 60%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 2;
}

/* 悬浮图标通用样式 */
.float-item {
  position: absolute;
  z-index: 3;
  /* 修改3：大幅提升不透明度，从0.15改为0.6，并在hover时更亮 */
  color: #fff;
  opacity: 0.6; 
  filter: drop-shadow(0 2px 10px rgba(0,0,0,0.1));
  animation: float-anim 6s ease-in-out infinite;
  transition: opacity 0.3s ease;
}

/* 鼠标放上去时，图标变亮，增加互动感 */
.welcome-right-decor:hover .float-item {
  opacity: 0.9;
}

.float-item svg {
  width: 100%;
  height: 100%;
  stroke-width: 1.5; /* 线条稍微细一点，显精致 */
}

/* --- 图标位置微调 (保持不变或微调) --- */
.item-1 { /* 神经网络 */
  width: 140px;
  height: 140px;
  top: 10%;
  right: 10%;
  animation-delay: 0s;
  transform: rotate(10deg);
}

.item-2 { /* 代码 */
  width: 110px;
  height: 110px;
  bottom: 15%;
  left: 10%;
  animation-delay: 2s;
}

.item-3 { /* 核心原子 */
  width: 220px;
  height: 220px;
  top: 40%;
  left: 50%;
  /* 这个大图标稍微淡一点，作为背景烘托 */
  opacity: 0.25; 
  animation-delay: 1s;
}

.item-4 { /* 文档 */
  width: 90px;
  height: 90px;
  top: 15%;
  left: 15%;
  animation-delay: 3s;
  transform: rotate(-15deg);
}

/* 漂浮动画 */
@keyframes float-anim {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-15px); } 
  100% { transform: translateY(0px); }
}
.c1 { width: 300px; height: 300px; top: -50px; right: -50px; }
.c2 { width: 150px; height: 150px; bottom: 100px; left: 50px; }

/* --- Stage 2: Survey --- */
.survey-layout {
  flex-direction: column;
  padding: 40px 80px;
}

.survey-top {
  margin-bottom: 40px;
}

.progress-container {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  margin-bottom: 10px;
}

.progress-bar {
  height: 100%;
  background: #4f46e5;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.q-counter {
  font-size: 14px;
  color: #64748b;
  font-weight: 600;
}

.question-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.question-text {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 50px;
  color: #1e293b;
  text-align: center;
}

.options-grid-desktop {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 双栏 */
  gap: 24px;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

.option-card {
  display: flex;
  align-items: center;
  padding: 30px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.option-card:hover {
  border-color: #4f46e5;
  box-shadow: 0 10px 20px rgba(79, 70, 229, 0.05);
  transform: translateY(-2px);
}

.opt-key-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  margin-right: 20px;
  flex-shrink: 0;
  transition: all 0.2s;
}

.option-card:hover .opt-key-circle {
  background: #4f46e5;
  color: white;
}

.opt-text {
  font-size: 18px;
  line-height: 1.5;
  color: #334155;
}

/* --- Stage 3: Result/Selection --- */
.result-layout {
  display: flex;
  flex-direction: row;
}

.result-sidebar {
  width: 320px;
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 30px;
  border-bottom: 1px solid #e2e8f0;
}

.sidebar-header h3 {
  margin: 0 0 5px 0;
  font-size: 18px;
}

.sidebar-desc {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.field-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.field-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 5px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.field-item:hover {
  background: #e2e8f0;
}

.field-item.active {
  background: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  border: 1px solid #cbd5e1;
}

.field-icon {
  margin-right: 10px;
  font-size: 18px;
}

.field-name {
  font-size: 15px;
  font-weight: 500;
  flex: 1;
}

.badge {
  font-size: 10px;
  background: #4f46e5;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
}

.result-main {
  flex: 1;
  padding: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
}

.detail-card {
  max-width: 600px;
  text-align: center;
}

.huge-icon {
  font-size: 80px;
  display: block;
  margin-bottom: 20px;
}

.detail-header h2 {
  font-size: 36px;
  margin-bottom: 30px;
  color: #1e293b;
}

.detail-desc {
  font-size: 18px;
  line-height: 1.6;
  color: #475569;
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 30px;
}

.detail-features {
  text-align: left;
  margin-bottom: 40px;
}

.detail-features h4 {
  margin-bottom: 15px;
  color: #1e293b;
}

.detail-features ul {
  list-style: none;
  padding: 0;
}

.detail-features li {
  margin-bottom: 10px;
  font-size: 16px;
  color: #64748b;
}

.confirm-hint {
  font-size: 14px;
  color: #94a3b8;
  margin-bottom: 15px;
}

.confirm-btn {
  width: 100%;
}

/* --- Common Buttons --- */
.primary-button {
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);
}

.primary-button:hover {
  background: #4338ca;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px -1px rgba(79, 70, 229, 0.4);
}

/* --- Animations --- */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>