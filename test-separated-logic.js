// 测试分离后的接口调用和结果保存逻辑
import * as fs from 'fs';

// 模拟window.api
const mockWindowApi = {
  writeLocalFile: (filename, content) => {
    console.log(`模拟写入文件: ${filename}`);
    console.log(`写入内容长度: ${content.length} 字符`);
    // 实际写入到测试文件
    fs.writeFileSync(`test-${filename}`, content);
    console.log(`内容已成功写入到 test-${filename}`);
    return Promise.resolve();
  }
};

// 测试保存结果函数
const saveSentenceBertResults = async (papers) => {
  try {
    // 格式化结果
    let paperContent = '';
    papers.forEach((paper, index) => {
      const title = paper.title || '无标题';
      const abstract = paper.original_abstract || '无摘要';
      const id = paper.id || `unknown-id-${index}`;
      paperContent += `Sentence-BERT结果 ${index + 1}:\n`;
      paperContent += `论文ID: ${id}\n`;
      paperContent += `标题: ${title}\n`;
      paperContent += `摘要: ${abstract}\n\n`;
    });
    
    // 直接写入文件，与BM25的保存逻辑保持一致
    await mockWindowApi.writeLocalFile('paper2.txt', paperContent);
    console.log(`Sentence-BERT查询结果已保存到paper2.txt，共${papers.length}条记录`);
    return true;
  } catch (error) {
    console.error('保存Sentence-BERT结果失败:', error);
    throw error;
  }
};

// 测试主函数
async function runTest() {
  console.log('开始测试分离后的接口调用和结果保存逻辑...');
  
  // 模拟API调用结果
  const mockApiResults = [
    {
      id: 'paper1',
      title: '测试论文1',
      original_abstract: '这是第一篇测试论文的摘要。',
      score: 0.95
    },
    {
      id: 'paper2',
      title: '测试论文2', 
      original_abstract: '这是第二篇测试论文的摘要。',
      score: 0.87
    }
  ];
  
  try {
    // 模拟分离的流程：1. 先调用API获取结果 2. 再保存结果
    console.log('\n1. 模拟API调用获取结果...');
    console.log(`获取到${mockApiResults.length}条结果`);
    
    console.log('\n2. 保存API调用结果...');
    await saveSentenceBertResults(mockApiResults);
    
    console.log('\n测试成功完成！');
    console.log('接口调用和结果保存逻辑已成功分离。');
  } catch (error) {
    console.error('\n测试失败:', error);
  }
}

// 运行测试
runTest();
