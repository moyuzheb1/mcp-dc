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