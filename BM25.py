# 第一步：先添加日志配置
import sys
import logging
import csv
import pickle
import os
import re
import nltk
import math
from collections import defaultdict
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import platform

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ---------------------- 核心配置 ----------------------
DEFAULT_K1 = 0.9
DEFAULT_B = 0.5
DEFAULT_THRESHOLD = 0.3
PAPERS_CSV_PATH = "papers.csv"
API_HOST = "0.0.0.0"
API_PORT = 2625
# 新增：索引缓存文件路径
INDEX_CACHE_FILE = "bm25_index.pkl"

# ---------------------- NLTK资源初始化 ----------------------
logger.info("开始初始化NLTK资源...")
try:
    stopwords.words('english')
    wordnet.synsets('test')
    logger.info("✅ NLTK资源已存在")
except LookupError:
    logger.info("⚠️  未找到NLTK资源，开始自动下载...")
    try:
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        logger.info("✅ NLTK资源下载完成")
    except Exception as e:
        logger.error(f"❌ NLTK资源下载失败：{str(e)}")
        sys.exit(1)

# ---------------------- 工具初始化 ----------------------
lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))
logger.info("✅ 工具初始化完成")

# ---------------------- 全局变量 ----------------------
GLOBAL_PAPERS = []
# 新增：全局索引变量
GLOBAL_BM25_INDEX = None

# ---------------------- 【你的原始加载函数】 ----------------------
# 这里请粘贴你原来可以正常运行的 load_papers_from_file 函数
# 为了演示，我假设它长这样。如果你的不同，请务必替换成你的版本！
def load_papers_from_file(file_path: str = PAPERS_CSV_PATH) -> List[Dict[str, str]]:
    logger.info(f"开始读取论文文件：{os.path.abspath(file_path)}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    papers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # 假设你的列名是 'id', 'title', 'abstract'，如果不是，请修改
        for row in reader:
            papers.append({
                "id": row["id"],
                "title": row["title"],
                "abstract": row["abstract"]
            })
    
    logger.info(f"✅ 成功读取 {len(papers)} 篇论文")
    return papers

# ---------------------- 数据预处理和BM25算法（无改动） ----------------------
def clean_text_en(text):
    if not text: return ""
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text.lower().strip()

def get_wordnet_pos(tag):
    if tag.startswith('J'): return wordnet.ADJ
    elif tag.startswith('V'): return wordnet.VERB
    elif tag.startswith('N'): return wordnet.NOUN
    elif tag.startswith('R'): return wordnet.ADV
    return wordnet.NOUN

def tokenize_en(text):
    if not text: return []
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    return [
        lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag))
        for word, tag in pos_tags
        if word not in STOPWORDS and len(word) > 1
    ]

def expand_keywords_en(query):
    expanded = tokenize_en(query)
    for word in expanded.copy():
        try:
            for syn in wordnet.synsets(word)[:2]:
                expanded.extend([lemma.name() for lemma in syn.lemmas()[:3]])
        except:
            continue
    return list(set(expanded))

def build_bm25_index(tokenized_docs):
    logger.info("开始构建BM25索引...")
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
    logger.info("✅ BM25索引构建完成")
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
            if tf == 0: continue
            denominator = tf + k1 * (1 - b + b * (doc_len / avgdl))
            score += idf[word] * (tf * (k1 + 1)) / denominator
        scores.append(score)
    return scores

# ---------------------- 【新增】索引加载和保存函数 ----------------------
def save_index(index_data, cache_file=INDEX_CACHE_FILE):
    """将索引数据保存到文件"""
    try:
        with open(cache_file, 'wb') as f:
            pickle.dump(index_data, f)
        logger.info(f"✅ 索引已保存到 {cache_file}")
    except Exception as e:
        logger.warning(f"⚠️  保存索引失败: {e}")

def load_index(cache_file=INDEX_CACHE_FILE) -> tuple:
    """从文件加载索引数据"""
    if not os.path.exists(cache_file):
        logger.warning(f"❌ 索引文件 {cache_file} 不存在")
        return None
    
    try:
        with open(cache_file, 'rb') as f:
            index_data = pickle.load(f)
        logger.info(f"✅ 已从 {cache_file} 加载索引")
        return index_data
    except Exception as e:
        logger.error(f"❌ 加载索引失败: {e}")
        os.remove(cache_file) # 删除损坏的索引文件
        logger.info("⚠️  已删除损坏的索引文件，将重新构建")
        return None

# ---------------------- 【优化后】结果处理函数 ----------------------
def process_papers(query: str, k1: float = DEFAULT_K1, b: float = DEFAULT_B) -> List[Dict[str, Any]]:
    # 打印查询参数
    logger.info(f"查询参数: {query}")
    global GLOBAL_BM25_INDEX

    if not GLOBAL_PAPERS:
        raise ValueError("未加载到有效论文数据")
    
    # 核心优化：如果索引已在内存中，直接使用
    if GLOBAL_BM25_INDEX is None:
        # 尝试从文件加载索引
        GLOBAL_BM25_INDEX = load_index()

        # 如果文件中没有索引，则现场构建并保存
        if GLOBAL_BM25_INDEX is None:
            logger.info("索引未找到，正在进行首次预处理和索引构建（此过程仅一次）...")
            abstracts = [paper["abstract"] for paper in GLOBAL_PAPERS]
            cleaned_abs = [clean_text_en(abs_text) for abs_text in abstracts]
            tokenized_abs = [tokenize_en(abs_text) for abs_text in cleaned_abs]
            GLOBAL_BM25_INDEX = build_bm25_index(tokenized_abs)
            # 保存索引供下次使用
            save_index(GLOBAL_BM25_INDEX)
    
    # 使用内存中的索引进行快速计算
    doc_freqs, doc_lengths, avgdl, term_freqs = GLOBAL_BM25_INDEX
    bm25_scores = calculate_bm25(query, doc_freqs, doc_lengths, avgdl, term_freqs, k1, b)
    
    # 结果处理
    results = []
    for i, paper in enumerate(GLOBAL_PAPERS):
        results.append({
            "id": paper["id"],
            "title": paper["title"],
            "original_abstract": paper["abstract"],
            "bm25_score": round(bm25_scores[i], 4),
        })
    
    results.sort(key=lambda x: x["bm25_score"], reverse=True)
    return results[:1]

# ---------------------- API接口和启动逻辑（无改动） ----------------------
app = FastAPI(title="BM25论文筛选API", description="优化版：预缓存索引，实现毫秒级响应")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BM25Request(BaseModel):
    query: str
    k1: float = DEFAULT_K1
    b: float = DEFAULT_B

class PaperResult(BaseModel):
    id: str
    title: str
    original_abstract: str
    bm25_score: float

class BM25Response(BaseModel):
    results: List[PaperResult]
    total_papers: int
    selected_count: int
    threshold: float = DEFAULT_THRESHOLD

@app.post("/bm25/score", response_model=BM25Response, summary="获取论文相关性评分")
async def score_papers(request: BM25Request):
    # 打印查询参数
    logger.info(f"查询参数: {request.query}")
    try:
        results = process_papers(query=request.query, k1=request.k1, b=request.b)
        return {
            "results": results,
            "total_papers": len(GLOBAL_PAPERS),
            "selected_count": len(results),
            "threshold": DEFAULT_THRESHOLD
        }
    except Exception as e:
        logger.error(f"API处理失败：{str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

def start_server():
    try:
        global GLOBAL_PAPERS
        GLOBAL_PAPERS = load_papers_from_file()
        
        logger.info("=== BM25论文筛选API（优化版）开始启动 ===")
        logger.info(f"📡 服务配置：{API_HOST}:{API_PORT}")
        logger.info(f"📄 论文文件路径：{os.path.abspath(PAPERS_CSV_PATH)}")
        logger.info("💡 首次查询可能较慢（需构建索引），后续查询将为毫秒级")
        logger.info("💡 访问 http://localhost:2625/docs 可测试API")
        
        uvicorn.run(
            app=app,
            host=API_HOST,
            port=API_PORT,
            log_level="info",
            access_log=True,
            reload=False,
            workers=1
        )
    except Exception as e:
        logger.error(f"❌ 服务启动失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()