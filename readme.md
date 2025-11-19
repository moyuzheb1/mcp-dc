# 安装依赖
```bash
pnpm install
pnpm run installRuntime
# if got err: No module named 'distutils'
pip install setuptools
#BM25所用库
pip install jieba nltk pandas json5 matplotlib fastapi uvicorn pydantic
#Sentence-BERT所用库
pip install sentence-transformers torch fastapi uvicorn
```
# 开始开发
```bash
#启动electon主程序
pnpm run dev
#启动BM25筛选接口
python BM25.py 
```

# 注意:
## BM25api返回格式
{
  "results": [
    {
      "id": "string",
      "title": "string",
      "original_abstract": "string",
      "bm25_score": 0,
    }
  ],
  "total_papers": 0,
  "selected_count": 0,
  "threshold": 0.3
}
## Sentence-BERT返回格式
{
  "results": [
    {
      "id": "string",
      "title": "string",
      "original_abstract": "string",
      "similarity_score": 0,
    }
  ],
  "total_papers": 0,
  "selected_count": 0,
  "threshold": 0
}