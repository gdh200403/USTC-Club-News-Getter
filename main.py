import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# 定义URL列表
urls = [f"https://young.ustc.edu.cn/15054/list{page}.htm" if page <= 50 else f"https://young.ustc.edu.cn/15054/list{page}.psp" for page in range(1, 199)]

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到所有的新闻项目
        news_items = soup.find_all('li', class_='text-li cf2')  # 注意这里的类名

        results = []
        for item in news_items:
            # 提取新闻标题和链接
            a_tags = item.find_all('a')
            if len(a_tags) > 1 and a_tags[1].text.strip():  # 确保有第二个<a>标签且有文本内容
                title = a_tags[1].text.strip()
                if "主持人俱乐部" in title:  # 筛选包含“主持人俱乐部”的标题
                    link = "https://young.ustc.edu.cn" + a_tags[1]['href']

                    # 提取日期信息
                    date_element = item.find('i')
                    date = date_element.text.strip() if date_element else ''

                    results.append({
                        'Title': title,
                        'Date': date,
                        'Link': link
                    })

        return results
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return []

# 创建DataFrame来存储所有数据
all_results = []

print("开始抓取数据...")
for url in tqdm(urls, desc="抓取进度"):
    all_results.extend(fetch_data(url))

print("数据抓取完成，正在创建DataFrame...")
df = pd.DataFrame(all_results)

# 将DataFrame保存为Excel文件
excel_filename = 'news.xlsx'
print(f"正在将数据保存到 {excel_filename}...")
df.to_excel(excel_filename, index=False)

print(f"数据已保存到 {excel_filename}")