import re
import nltk
import math
import json
import matplotlib.pyplot as plt
from collections import defaultdict
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# ---------------------- 1. 初始化NLTK资源（首次运行自动下载）----------------------
try:
    stopwords.words('english')
    wordnet.synsets('test')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

# ---------------------- 2. 配置参数（仅需修改这3处！）----------------------
INPUT_JSON = "papers.json"  # 你的JSON文件名（同文件夹下，如"my_papers.json"）
OUTPUT_JSON = "bm25_screening_results.json"  # 输出结果文件名
QUERY = "large language model"  # 你的初筛关键词（英文）

# BM25参数（英文摘要推荐值，无需改动）
K1 = 0.9  # 词频饱和系数
B = 0.5   # 文档长度归一化系数
SELECTION_THRESHOLD = 0.3  # 筛选阈值（可根据得分分布图调整）

# ---------------------- 3. 工具初始化 ----------------------
lemmatizer = WordNetLemmatizer()  # 英文词形还原器
STOPWORDS = set(stopwords.words('english'))  # 英文停用词表

# ---------------------- 4. 数据预处理函数（英文适配）----------------------
def clean_text_en(text):
    """英文文本清洗：去标点、数字、小写化"""
    text = re.sub(r'[^\w\s]', '', text)  # 去标点
    text = re.sub(r'\d+', '', text)      # 去数字
    return text.lower().strip()

def get_wordnet_pos(tag):
    """词性标签转换（用于精准词形还原）"""
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
    """英文分词+停用词过滤+词形还原"""
    tokens = word_tokenize(text)  # 分词
    pos_tags = nltk.pos_tag(tokens)  # 词性标注
    # 过滤无效词并还原
    return [
        lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag))
        for word, tag in pos_tags
        if word not in STOPWORDS and len(word) > 1
    ]

def expand_keywords_en(query):
    """关键词扩展（基于WordNet获取近义词，提升召回率）"""
    expanded = tokenize_en(query)
    for word in tokenize_en(query):
        for syn in wordnet.synsets(word):
            expanded.extend([lemma.name() for lemma in syn.lemmas()])
    return list(set(expanded))  # 去重

# ---------------------- 5. BM25核心算法 ----------------------
def build_bm25_index(tokenized_docs):
    """构建BM25索引：统计词频、文档长度等"""
    doc_freqs = defaultdict(int)  # 词出现的文档数
    doc_lengths = []              # 每篇文档的词数
    term_freqs = []               # 每篇文档的词频字典

    for doc in tokenized_docs:
        doc_len = len(doc)
        doc_lengths.append(doc_len)
        freq = defaultdict(int)
        for word in doc:
            freq[word] += 1
        term_freqs.append(freq)
        # 统计文档频率（去重）
        for word in set(doc):
            doc_freqs[word] += 1

    avgdl = sum(doc_lengths) / len(doc_lengths) if doc_lengths else 1
    return doc_freqs, doc_lengths, avgdl, term_freqs

def calculate_bm25(query, doc_freqs, doc_lengths, avgdl, term_freqs):
    """计算每篇文档的BM25得分"""
    N = len(doc_lengths)
    tokenized_query = expand_keywords_en(query)
    scores = []

    # 计算IDF（词的稀有度）
    idf = {
        word: math.log((N - doc_freqs.get(word, 0) + 0.5) / (doc_freqs.get(word, 0) + 0.5) + 1)
        for word in set(tokenized_query)
    }

    # 计算单篇文档得分
    for i in range(N):
        doc_len = doc_lengths[i]
        score = 0.0
        doc_freq = term_freqs[i]
        for word in tokenized_query:
            tf = doc_freq.get(word, 0)
            if tf == 0:
                continue
            # BM25核心公式
            denominator = tf + K1 * (1 - B + B * (doc_len / avgdl))
            score += idf[word] * (tf * (K1 + 1)) / denominator
        scores.append(score)
    return scores

# ---------------------- 6. JSON数据读写 ----------------------
def read_json_data(file_path):
    """读取含id/title/abstract的JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 校验必填字段
        required_fields = {"id", "title", "abstract"}
        for item in data:
            if not required_fields.issubset(item.keys()):
                raise ValueError(f"JSON缺少必填字段！某条数据字段：{list(item.keys())}")
        print(f"✅ 成功读取 {len(data)} 篇论文（字段：id/title/abstract）")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ 未找到文件 {file_path}，请确认文件在同文件夹下")
    except json.JSONDecodeError:
        raise ValueError("❌ JSON格式错误，请检查文件内容")

def save_results(data, cleaned_abstracts, tokenized_abstracts, scores):
    """保存筛选结果到JSON（保留原始字段+处理结果）"""
    results = []
    for i, item in enumerate(data):
        results.append({
            "id": item["id"],
            "title": item["title"],
            "original_abstract": item["abstract"],
            "cleaned_abstract": cleaned_abstracts[i],
            "tokenized_abstract": tokenized_abstracts[i],
            "bm25_score": round(scores[i], 4),
            "is_selected": 1 if scores[i] > SELECTION_THRESHOLD else 0
        })
    # 按BM25得分降序排序
    results.sort(key=lambda x: x["bm25_score"], reverse=True)
    # 保存文件
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"✅ 结果已保存到 {OUTPUT_JSON}")
    return results

# ---------------------- 7. 结果可视化与输出 ----------------------
def visualize_score_distribution(scores):
    """绘制BM25得分分布图（辅助调整阈值）"""
    plt.figure(figsize=(8, 4))
    plt.hist(scores, bins=10, color='#2E86AB', alpha=0.7, edgecolor='black')
    plt.xlabel('BM25 Score')
    plt.ylabel('Number of Papers')
    plt.title('BM25 Score Distribution (English Abstracts)')
    plt.axvline(x=SELECTION_THRESHOLD, color='red', linestyle='--', label=f'Threshold: {SELECTION_THRESHOLD}')
    plt.legend()
    plt.tight_layout()
    plt.show()

def print_top_results(results, top_n=5):
    """打印得分最高的N篇论文（快速查看）"""
    print(f"\n🏆 Top {top_n} 高相关论文：")
    for i, res in enumerate(results[:top_n]):
        print(f"\nRank {i+1} | Score: {res['bm25_score']}")
        print(f"ID: {res['id']}")
        print(f"Title: {res['title']}")
        print(f"Abstract (first 100 chars): {res['original_abstract'][:100]}...")

# ---------------------- 8. 主流程（一键运行）----------------------
if __name__ == "__main__":
    print("=== 开始BM25英文文献初筛 ===")
    # 步骤1：读取JSON数据
    raw_data = read_json_data(INPUT_JSON)
    # 步骤2：提取摘要并预处理
    abstracts = [item["abstract"] for item in raw_data]
    cleaned_abs = [clean_text_en(abs) for abs in abstracts]
    tokenized_abs = [tokenize_en(abs) for abs in cleaned_abs]
    print("✅ 数据预处理完成（清洗+分词+词形还原）")
    # 步骤3：计算BM25得分
    doc_freqs, doc_lengths, avgdl, term_freqs = build_bm25_index(tokenized_abs)
    bm25_scores = calculate_bm25(QUERY, doc_freqs, doc_lengths, avgdl, term_freqs)
    print("✅ BM25得分计算完成")
    # 步骤4：保存结果
    final_results = save_results(raw_data, cleaned_abs, tokenized_abs, bm25_scores)
    # 步骤5：可视化+打印Top结果
    visualize_score_distribution(bm25_scores)
    print_top_results(final_results, top_n=5)
    # 统计筛选结果
    selected_count = sum([1 for res in final_results if res["is_selected"] == 1])
    print(f"\n=== 筛选完成 ===")
    print(f"总论文数：{len(final_results)}")
    print(f"入选论文数：{selected_count}")