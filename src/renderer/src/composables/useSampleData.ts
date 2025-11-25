import { ref } from 'vue';

export interface PaperData {
  id: string;
  title: string;
  abstract: string;
}

export function useSampleData() {
  // 用于存储sample.txt的关键字和总结内容
  const keywords = ref<string[]>([]);
  const summary = ref<string>('');
  // 用于存储sample.txt第7-11行的控制标志
  const showPaperBox = ref<number[]>([0, 0, 0, 0, 0]);
  // 用于存储paper.txt的论文数据
  const paperData = ref<PaperData[]>([]);
  // 用于存储sample.txt的标题和五列内容
  const sampleTitle = ref<string>('');
  const sampleColumns = ref<string[]>([]);
  // 加载状态
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // 读取sample.txt和paper.txt文件
  const loadSampleData = async () => {
    isLoading.value = true;
    error.value = null;
    
    try {
      // 读取sample.txt文件
      // @ts-ignore - 假设window.api是可用的
      const sampleFileContent = await window.api.readLocalFile('sample.txt');
      if (sampleFileContent) {
        const lines = sampleFileContent.trim().split('\n').filter(line => line.trim() !== '');
        if (lines.length > 0) {
          // 第一行作为标题
          sampleTitle.value = lines[0].trim();
          // 第2-6行作为五列内容
          if (lines.length >= 6) {
            sampleColumns.value = lines.slice(1, 6).map(line => line.trim());
          }
          // 第7-11行作为控制标志（是否显示论文框）
          if (lines.length >= 11) {
            showPaperBox.value = lines.slice(6, 11).map(line => parseInt(line.trim()) || 0);
          }
          // 第12-16行作为关键字内容
          if (lines.length >= 16) {
            keywords.value = lines.slice(11, 16).map(line => line.trim());
          }
          // 第17行作为总结内容
          if (lines.length >= 17) {
            summary.value = lines[16].trim();
          }
        }
      }
      
      // 读取paper.txt文件
      // @ts-ignore - 假设window.api是可用的
      const paperFileContent = await window.api.readLocalFile('paper.txt');
      if (paperFileContent) {
        const lines = paperFileContent.trim().split('\n').filter(line => line.trim() !== '');
        const newPaperData: PaperData[] = [];
        
        // 处理5组数据（最多）
        for (let i = 0; i < 5; i++) {
          // 计算当前组的id行索引（从0开始）
          const idIndex = i * 3;
          const titleIndex = idIndex + 1;
          const abstractIndex = idIndex + 2;
          
          // 检查索引是否有效
          if (idIndex < lines.length && titleIndex < lines.length && abstractIndex < lines.length) {
            newPaperData.push({
              id: lines[idIndex].trim(),
              title: lines[titleIndex].trim(),
              abstract: lines[abstractIndex].trim()
            });
          }
        }
        paperData.value = newPaperData;
      }
    } catch (err) {
      console.error('读取文件失败:', err);
      error.value = err instanceof Error ? err.message : 'Failed to load sample data';
    } finally {
      isLoading.value = false;
    }
  };

  // 刷新数据
  const refreshData = async () => {
    return loadSampleData();
  };

  return {
    keywords,
    summary,
    showPaperBox,
    paperData,
    sampleTitle,
    sampleColumns,
    isLoading,
    error,
    loadSampleData,
    refreshData
  };
}
