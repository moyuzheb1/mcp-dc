# 第一步：先添加日志配置（确保所有步骤都有输出）
import sys
import logging

# 配置日志：强制输出到控制台，不静默任何信息
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout  # 确保输出到命令行，不被隐藏
)
logger = logging.getLogger(__name__)

# 第二步：导入依赖（每步都加日志，看是否卡在导入）
logger.info("开始加载依赖模块...")
try:
    import re
    import nltk
    import math
    import json
    import matplotlib.pyplot as plt
    from collections import defaultdict
    from nltk.corpus import stopwords, wordnet
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import List, Dict, Any
    import uvicorn
    import os
    import platform
    logger.info("✅ 所有依赖模块加载成功")
except ImportError as e:
    logger.error(f"❌ 依赖模块加载失败：缺少 {e.name}（请运行 pip install {e.name}）")
    sys.exit(1)

# 检查Python版本（FastAPI要求3.7+）
logger.info(f"当前Python版本：{platform.python_version()}")
if sys.version_info < (3, 7):
    logger.error("❌ Python版本过低！请使用Python 3.7及以上版本")
    sys.exit(1)

# ---------------------- 核心配置 ----------------------
DEFAULT_K1 = 0.9
DEFAULT_B = 0.5
DEFAULT_THRESHOLD = 0.3
PAPERS_JSON_PATH = "papers.json"
API_HOST = "0.0.0.0"
API_PORT = 2625  # 目标端口

# ---------------------- NLTK资源初始化（强制日志输出）----------------------
logger.info("开始初始化NLTK资源...")
try:
    # 测试资源是否存在，不存在则下载（添加超时控制）
    stopwords.words('english')
    wordnet.synsets('test')
    logger.info("✅ NLTK资源已存在，无需下载")
except LookupError:
    logger.info("⚠️  未找到NLTK资源，开始自动下载（首次运行需联网）...")
    try:
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        logger.info("✅ NLTK资源下载完成")
    except Exception as e:
        logger.error(f"❌ NLTK资源下载失败：{str(e)}（请检查网络连接）")
        sys.exit(1)

# ---------------------- 工具初始化 ----------------------
lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))
logger.info("✅ 工具初始化完成")

# ---------------------- 读取论文数据（添加路径日志）----------------------
def load_papers_from_file(file_path: str = PAPERS_JSON_PATH) -> List[Dict[str, str]]:
    logger.info(f"开始读取论文文件：{os.path.abspath(file_path)}")
    logger.info(f"当前工作目录：{os.getcwd()}")  # 打印当前目录，方便用户排查文件位置
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在（当前目录：{os.getcwd()}）")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            papers = json.load(f)
        
        required_fields = {"id", "title", "abstract"}
        for idx, paper in enumerate(papers):
            if not required_fields.issubset(paper.keys()):
                missing = required_fields - set(paper.keys())
                raise ValueError(f"第 {idx+1} 篇论文缺少字段：{missing}（ID：{paper.get('id', '未知')}）")
        
        if len(papers) == 0:
            raise ValueError("论文文件为空")
        
        logger.info(f"✅ 成功读取 {len(papers)} 篇论文")
        return papers
    except json.JSONDecodeError:
        raise ValueError("JSON格式错误（请用 https://json.cn/ 校验）")
    except Exception as e:
        raise RuntimeError(f"读取文件失败：{str(e)}")

# 预加载论文
GLOBAL_PAPERS = []
try:
    GLOBAL_PAPERS = load_papers_from_file()
except Exception as e:
    logger.error(f"⚠️  论文数据加载失败：{str(e)}（启动后API会返回该错误）")
    GLOBAL_PAPERS = []  # 继续启动服务，让用户通过API查看详情

# ---------------------- 数据预处理函数 ----------------------
def clean_text_en(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.lower().strip()

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN

def tokenize_en(text):
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    return [
        lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag))
        for word, tag in pos_tags
        if word not in STOPWORDS and len(word) > 1
    ]

def expand_keywords_en(query):
    expanded = tokenize_en(query)
    for word in tokenize_en(query):
        for syn in wordnet.synsets(word):
            expanded.extend([lemma.name() for lemma in syn.lemmas()])
    return list(set(expanded))

# ---------------------- BM25核心算法 ----------------------
def build_bm25_index(tokenized_docs):
    doc_freqs = defaultdict(int)
    doc_lengths = []
    term_freqs = []

    for doc in tokenized_docs:
        doc_len = len(doc)
        doc_lengths.append(doc_len)
        freq = defaultdict(int)
        for word in doc:
            freq[word] += 1
        term_freqs.append(freq)
        for word in set(doc):
            doc_freqs[word] += 1

    avgdl = sum(doc_lengths) / len(doc_lengths) if doc_lengths else 1
    return doc_freqs, doc_lengths, avgdl, term_freqs

def calculate_bm25(query, doc_freqs, doc_lengths, avgdl, term_freqs, k1=DEFAULT_K1, b=DEFAULT_B):
    N = len(doc_lengths)
    tokenized_query = expand_keywords_en(query)
    scores = []

    idf = {
        word: math.log((N - doc_freqs.get(word, 0) + 0.5) / (doc_freqs.get(word, 0) + 0.5) + 1)
        for word in set(tokenized_query)
    }

    for i in range(N):
        doc_len = doc_lengths[i]
        score = 0.0
        doc_freq = term_freqs[i]
        for word in tokenized_query:
            tf = doc_freq.get(word, 0)
            if tf == 0:
                continue
            denominator = tf + k1 * (1 - b + b * (doc_len / avgdl))
            score += idf[word] * (tf * (k1 + 1)) / denominator
        scores.append(score)
    return scores

# ---------------------- 结果处理函数（简化返回字段）----------------------
def process_papers(query: str, k1: float = DEFAULT_K1, b: float = DEFAULT_B) -> List[Dict[str, Any]]:
    if not GLOBAL_PAPERS:
        raise ValueError("未加载到有效论文数据，请检查：1. papers.json是否在当前目录 2. JSON格式是否正确 3. 是否包含id/title/abstract字段")
    
    abstracts = [paper["abstract"] for paper in GLOBAL_PAPERS]
    cleaned_abs = [clean_text_en(abs_text) for abs_text in abstracts]
    tokenized_abs = [tokenize_en(abs_text) for abs_text in cleaned_abs]
    
    doc_freqs, doc_lengths, avgdl, term_freqs = build_bm25_index(tokenized_abs)
    bm25_scores = calculate_bm25(query, doc_freqs, doc_lengths, avgdl, term_freqs, k1, b)
    
    # 核心修改：仅保留 id、title、original_abstract + 评分相关字段
    results = []
    for i, paper in enumerate(GLOBAL_PAPERS):
        results.append({
            "id": paper["id"],  # 保留
            "title": paper["title"],  # 保留
            "original_abstract": paper["abstract"],  # 保留
            "bm25_score": round(bm25_scores[i], 4),  # 保留（用于判断相关性强弱）
            "is_selected": 1 if bm25_scores[i] > DEFAULT_THRESHOLD else 0  # 保留（用于判断是否入选）
        })
    
    results.sort(key=lambda x: x["bm25_score"], reverse=True)
    return results

# ---------------------- API接口定义（同步简化响应模型）----------------------
app = FastAPI(title="BM25论文筛选API", description="仅需传入查询关键词，返回相关性排序结果（简化字段）")

class BM25Request(BaseModel):
    query: str  # 唯一必填参数
    k1: float = DEFAULT_K1
    b: float = DEFAULT_B

# 简化响应模型：明确返回字段
class PaperResult(BaseModel):
    id: str
    title: str
    original_abstract: str
    bm25_score: float
    is_selected: int

class BM25Response(BaseModel):
    results: List[PaperResult]  # 用简化后的PaperResult模型
    total_papers: int
    selected_count: int
    threshold: float = DEFAULT_THRESHOLD

@app.post("/bm25/score", response_model=BM25Response, summary="获取论文相关性评分")
async def score_papers(request: BM25Request):
    try:
        results = process_papers(query=request.query, k1=request.k1, b=request.b)
        selected_count = sum(1 for res in results if res["is_selected"] == 1)
        return {
            "results": results,
            "total_papers": len(results),
            "selected_count": selected_count,
            "threshold": DEFAULT_THRESHOLD
        }
    except Exception as e:
        logger.error(f"API处理失败：{str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ---------------------- 启动逻辑（强制日志输出）----------------------
if __name__ == "__main__":
    logger.info("=== BM25论文筛选API 开始启动 ===")
    logger.info(f"📡 服务配置：{API_HOST}:{API_PORT}")
    logger.info(f"📄 论文文件路径：{os.path.abspath(PAPERS_JSON_PATH)}")
    logger.info("⚠️  启动后请勿关闭终端（关闭将停止服务）")
    logger.info("💡 访问 http://localhost:2625/docs 可测试API")
    
    try:
        # 启动服务（添加日志回调，确保启动状态可见）
        uvicorn.run(
            app=app,
            host=API_HOST,
            port=API_PORT,
            log_level="info",
            access_log=False  # 关闭访问日志，只保留启动日志
        )
    except Exception as e:
        logger.error(f"❌ 服务启动失败：{str(e)}")
        # 针对常见错误给出提示
        if "address already in use" in str(e).lower():
            logger.error("💡 解决方案：端口2625已被占用，请关闭占用程序，或修改代码中API_PORT为其他端口（如2626）")
        elif "permission denied" in str(e).lower():
            logger.error("💡 解决方案：无权限使用该端口（Windows需以管理员身份运行终端，Linux/Mac需加sudo）")
        sys.exit(1)