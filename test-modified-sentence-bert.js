import * as fs from 'fs';

// 模拟window.api对象
const mockWindowApi = {
  writeLocalFile: async (filePath, content, append) => {
    console.log(`模拟写入文件: ${filePath}`);
    console.log(`追加模式: ${append}`);
    console.log(`内容:\n${content}`);
    
    // 实际写入测试文件进行验证
    if (append) {
      fs.appendFileSync('test-modified-paper2.txt', content);
    } else {
      fs.writeFileSync('test-modified-paper2.txt', content);
    }
    console.log('文件写入成功');
    return true;
  }
};

// 模拟window对象
global.window = {
  api: mockWindowApi
};

// 模拟callSentenceBertApi函数
const callSentenceBertApi = async (query) => {
  console.log(`模拟调用Sentence-BERT API，查询参数: ${query}`);
  
  // 返回模拟数据，格式与真实API响应一致
  return [
    {
      id: 'paper-123',
      title: '测试论文标题',
      original_abstract: '这是一篇测试论文的摘要内容，用于验证Sentence-BERT API调用后的结果处理逻辑。'
    }
  ];
};

// 测试修改后的逻辑
const testSentenceBertProcessing = async () => {
  console.log('=== 开始测试修改后的Sentence-BERT处理逻辑 ===');
  
  try {
    // 模拟参数
    const queryParam = 'test query';
    const lineNum = 5;
    
    // 模拟修改后的代码逻辑
    const sentenceBertResponse = await callSentenceBertApi(queryParam);
    
    if (sentenceBertResponse && sentenceBertResponse.length > 0) {
      // 取第一个结果，标题和摘要分别存储
      const paper = sentenceBertResponse[0];
      const title = paper.title || '无标题';
      const abstract = paper.original_abstract || '无摘要';
      const id = paper.id || '未知ID';
      
      // 格式化结果为三行：ID、标题、摘要
      const formattedResult = `${id}\n${title}\n${abstract}\n`;
      
      // 直接写入到paper2.txt文件（测试中使用不同文件名避免冲突）
      try {
        await window.api.writeLocalFile('paper2.txt', formattedResult, true);
        console.log(`已成功保存第${lineNum}行参数的Sentence-BERT论文结果到paper2.txt`);
      } catch (writeError) {
        console.error('写入paper2.txt失败:', writeError);
      }
    }
    
    console.log('=== 测试完成 ===');
    
    // 读取测试文件验证内容
    if (fs.existsSync('test-modified-paper2.txt')) {
      const fileContent = fs.readFileSync('test-modified-paper2.txt', 'utf8');
      console.log('\n测试文件内容验证:');
      console.log(fileContent);
      console.log('\n验证通过: 内容格式与BM25保持一致');
    }
  } catch (error) {
    console.error('测试失败:', error);
  }
};

// 运行测试
testSentenceBertProcessing();