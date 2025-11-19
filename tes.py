import requests
import feedparser
import csv
import time
import re

def crawl_arxiv_cs_ai_tuna(output_file="arxiv_cs_ai_papers.csv", max_papers=10):
    # 清华 arXiv 镜像（国内秒通）
    base_url = "https://arxiv.org/api/query"
    params = {
        "search_query": "cat:cs.AI",  # 合规参数（API强制要求）
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": min(max_papers, 1000),
        "start": 0
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Accept": "application/atom+xml, application/xml, text/xml",
        "Connection": "keep-alive"
    }

    papers = []
    fetched = 0

    while fetched < max_papers:
        try:
            response = requests.get(
                base_url,
                params=params,
                headers=headers,
                timeout=30,
                allow_redirects=True,
                verify=False  # 关闭SSL验证，国内网络必备
            )
            response.raise_for_status()

            feed = feedparser.parse(response.text)
            if not feed.entries:
                print("无更多论文数据")
                break

            # 提取：论文ID + 标题 + 摘要（新增ID提取）
            for entry in feed.entries:
                # 1. 提取论文核心ID（从完整URL中截取，如 "2511.12345"）
                full_id = entry.get("id", "")  # 完整ID格式：https://arxiv.tuna.tsinghua.edu.cn/abs/2511.12345v1
                # 用正则提取核心ID（匹配 "数字.数字" 格式，忽略版本号v1/v2）
                paper_id_match = re.search(r'(\d+\.\d+)', full_id)
                paper_id = paper_id_match.group(1) if paper_id_match else "未知ID"

                # 2. 提取标题和摘要（保留原有逻辑）
                title = entry.get("title", "").strip().replace("\n", " ")
                abstract = entry.get("summary", "").strip().replace("\n", " ")

                # 过滤空数据，添加到列表
                if paper_id != "未知ID" and title and abstract:
                    papers.append({
                        "id": paper_id,  # 新增字段：论文核心ID
                        "title": title,
                        "abstract": abstract
                    })
                    fetched += 1
                if fetched >= max_papers:
                    break

            print(f"已获取 {fetched}/{max_papers} 篇论文")
            params["start"] += len(feed.entries)
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"请求失败：{e}")
            if 'response' in locals():
                print(f"API返回内容：{response.text[:500]}")
            break
        except Exception as e:
            print(f"解析失败：{e}")
            continue

    # 保存CSV（新增 paper_id 字段）
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        # 表头增加 "paper_id"
        fieldnames = ["id", "title", "abstract"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(papers)

    print(f"\n✅ 成功保存 {len(papers)} 篇论文到：{output_file}")
    print("CSV字段说明：")
    print("- id：论文核心ID（如 2511.12345，可直接访问 https://arxiv.org/abs/ID 查看原文）")
    print("- title：论文标题")
    print("- abstract：论文摘要")

if __name__ == "__main__":
    # 爬取10篇测试，成功后可修改 max_papers（建议单次≤1000）
    crawl_arxiv_cs_ai_tuna(max_papers=500)