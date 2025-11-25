# 第一步：添加日志配置
import sys
import logging
import os
import platform
import csv
import numpy as np
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 导入CORS中间件
from pydantic import BaseModel
import uvicorn
from sentence_transformers import SentenceTransformer, util
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# 第二步：导入依赖并检查
logger.info("开始加载依赖模块...")
try:
    # 核心依赖检查
    import torch  # sentence-transformers依赖PyTorch
    logger.info(f"✅ PyTorch版本: {torch.__version__}")
    logger.info("✅ 所有依赖模块加载成功")
except ImportError as e:
    logger.error(f"❌ 依赖模块加载失败：缺少 {e.name}（请运行 pip install {e.name}）")
    sys.exit(1)

# 检查Python版本
logger.info(f"当前Python版本：{platform.python_version()}")
if sys.version_info < (3, 7):
    logger.error("❌ Python版本过低！请使用Python 3.7及以上版本")
    sys.exit(1)

# ---------------------- 核心配置 ----------------------
DEFAULT_MODEL = "all-MiniLM-L6-v2"  # 轻量级Sentence-BERT模型
DEFAULT_THRESHOLD = 0.5  # 相似度阈值
PAPERS_CSV_PATH = "papers.csv"  # 论文CSV文件路径
API_HOST = "0.0.0.0"
API_PORT = 2378  # 与BM25区分端口

# ---------------------- 模型初始化 ----------------------
logger.info(f"开始加载Sentence-BERT模型：{DEFAULT_MODEL}...")
try:
    model = SentenceTransformer("./local_models/all-MiniLM-L6-v2")  # 替换为实际本地模型路径
    logger.info("✅ Sentence-BERT模型加载成功")
except Exception as e:
    logger.error(f"❌ 模型加载失败：{str(e)}（请检查网络连接或模型名称）")
    sys.exit(1)

# ---------------------- 读取论文数据 ----------------------
def load_papers_from_file(file_path: str = PAPERS_CSV_PATH) -> List[Dict[str, str]]:
    logger.info(f"开始读取论文文件：{os.path.abspath(file_path)}")
    logger.info(f"当前工作目录：{os.getcwd()}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在（当前目录：{os.getcwd()}）")
    
    try:
        papers = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                papers.append({
                    "id": row["id"],
                    "title": row["title"],
                    "abstract": row["abstract"]
                })
        
        required_fields = {"id", "title", "abstract"}
        for idx, paper in enumerate(papers):
            if not required_fields.issubset(paper.keys()):
                missing = required_fields - set(paper.keys())
                raise ValueError(f"第 {idx+1} 篇论文缺少字段：{missing}（ID：{paper.get('id', '未知')}）")
        
        if len(papers) == 0:
            raise ValueError("论文文件为空")
        
        logger.info(f"✅ 成功读取 {len(papers)} 篇论文")
        return papers
    except Exception as e:
        raise RuntimeError(f"读取文件失败：{str(e)}")

# 预加载论文及生成嵌入
GLOBAL_PAPERS = []
PAPER_EMBEDDINGS = None  # 存储论文摘要的嵌入向量

try:
    GLOBAL_PAPERS = load_papers_from_file()
    # 生成摘要嵌入
    logger.info("开始生成论文摘要嵌入（首次运行可能耗时）...")
    abstracts = [paper["abstract"] for paper in GLOBAL_PAPERS]
    PAPER_EMBEDDINGS = model.encode(abstracts, convert_to_tensor=True)
    logger.info(f"✅ 成功生成 {len(GLOBAL_PAPERS)} 篇论文的嵌入向量")
except Exception as e:
    logger.error(f"⚠️  论文数据或嵌入生成失败：{str(e)}（启动后API会返回该错误）")
    GLOBAL_PAPERS = []
    PAPER_EMBEDDINGS = None

# ---------------------- 数据预处理函数 ----------------------
def clean_text(text: str) -> str:
    """简单文本清理"""
    import re
    text = re.sub(r'\s+', ' ', text)  # 合并空格
    return text.strip()

# ---------------------- Sentence-BERT核心算法 ----------------------
def calculate_similarity(query: str) -> List[float]:
    """计算查询与所有论文摘要的余弦相似度"""
    if PAPER_EMBEDDINGS is None:
        raise ValueError("论文嵌入向量未初始化")
    
    # 生成查询嵌入
    query_embedding = model.encode(clean_text(query), convert_to_tensor=True)
    
    # 计算余弦相似度
    cos_scores = util.cos_sim(query_embedding, PAPER_EMBEDDINGS)[0]
    return cos_scores.cpu().numpy().tolist()  # 转换为CPU并返回列表

# ---------------------- 结果处理函数 ----------------------
def process_papers(query: str, threshold: float = DEFAULT_THRESHOLD) -> List[Dict[str, Any]]:
    if not GLOBAL_PAPERS or PAPER_EMBEDDINGS is None:
        raise ValueError("未加载到有效论文数据，请检查：1. papers.csv是否在当前目录 2. CSV格式是否正确 3. 是否包含id/title/abstract字段")
    
    # 计算相似度
    similarities = calculate_similarity(query)
    
    # 构建结果
    results = []
    for i, paper in enumerate(GLOBAL_PAPERS):
        score = round(similarities[i], 4)
        results.append({
            "id": paper["id"],
            "title": paper["title"],
            "original_abstract": paper["abstract"],
            "similarity_score": score
        })
    
    # 按相似度降序排序
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    # 只返回分数最高的一篇论文
    return results[:1]

# ---------------------- API接口定义 ----------------------
app = FastAPI(title="Sentence-BERT论文匹配API", description="基于句子嵌入的论文相关性匹配接口")

# 配置CORS跨域，解决OPTIONS请求405错误
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有源（生产环境建议指定具体域名）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法（包括OPTIONS预检请求）
    allow_headers=["*"],  # 允许所有请求头
)

class SentenceBERTRequest(BaseModel):
    query: str  # 查询关键词/句子
    threshold: float = DEFAULT_THRESHOLD  # 相似度阈值

class PaperResult(BaseModel):
    id: str
    title: str
    original_abstract: str
    similarity_score: float

class SentenceBERTResponse(BaseModel):
    results: List[PaperResult]
    total_papers: int
    selected_count: int  # 保留字段名但实际代表最高分数论文数（总是1）
    threshold: float

@app.post("/sentence-bert/match", response_model=SentenceBERTResponse, summary="获取论文相似度匹配结果")
async def match_papers(request: SentenceBERTRequest):
    try:
        results = process_papers(query=request.query, threshold=request.threshold)
        # 只返回分数最高的一篇论文，所以selected_count总是1
        return {
            "results": results,
            "total_papers": len(results),
            "selected_count": 1,  # 因为只返回最高分数的一篇论文
            "threshold": request.threshold
        }
    except Exception as e:
        logger.error(f"API处理失败：{str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------- 启动逻辑 ----------------------
if __name__ == "__main__":
    # Windows系统切换事件循环（解决连接重置问题）
    if platform.system() == "Windows":
        import asyncio
        from asyncio import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    
    logger.info("=== Sentence-BERT论文匹配API 开始启动 ===")
    logger.info(f"📡 服务配置：{API_HOST}:{API_PORT}")
    logger.info(f"🤖 使用模型：{DEFAULT_MODEL}")
    logger.info("⚠️  启动后请勿关闭终端（关闭将停止服务）")
    logger.info("💡 访问 http://localhost:2378/docs 可测试API")
    
    try:
        uvicorn.run(
            app=app,
            host=API_HOST,
            port=API_PORT,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"❌ 服务启动失败：{str(e)}")
        if "address already in use" in str(e).lower():
            logger.error("💡 解决方案：端口2378已被占用，请关闭占用程序，或修改代码中API_PORT为其他端口（如2627）")
        elif "permission denied" in str(e).lower():
            logger.error("💡 解决方案：无权限使用该端口（Windows需以管理员身份运行终端，Linux/Mac需加sudo）")
        sys.exit(1)