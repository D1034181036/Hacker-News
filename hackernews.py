# -*- coding: utf-8 -*-

import re
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
from translate import Translator
from datetime import datetime

def getPageData(pageNumber = 1):
  # 網頁爬蟲
  url = f'https://news.ycombinator.com/news?p={pageNumber}'
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  # 建立列表
  titleList = []
  linkList = []
  scoreList = []

  # 標題欄
  for tr in soup.find_all('tr', class_='athing'):
    titleList.append(tr.find('span', class_='titleline').find('a').text)

  # 副標題欄
  for sub in soup.find_all('td', class_='subtext'):
    linkList.append('https://news.ycombinator.com/' + sub.find_all('a')[-1].get('href'))
    score = sub.find('span', class_='score')
    scoreList.append(int(''.join(filter(str.isdigit, score.text)) or 0) if score else 0)

  # 格式化資料
  return dict(zip(['Score', 'Title', 'Link'], [scoreList, titleList, linkList]))

# 取得網站前 N 頁文章列表
news = defaultdict(list)
for i in range(3):
  page = getPageData(i+1)
  for key, value in page.items():
    news[key].extend(value)

# 翻譯標題
translator = Translator(to_lang="zh-tw")
news['Title_ZH'] = []
for title in news['Title']:
  news['Title_ZH'].append(translator.translate(title))

# 使用字典建立 DataFrame
df = pd.DataFrame(news, columns=['Score', 'Title', 'Title_ZH', 'Link'])
df.index += 1
# display(df)

# =============================

# 前處理
df = pd.DataFrame(news, columns=['Score', 'Title', 'Title_ZH', 'Link']).reset_index(drop=False)
df['index'] += 1
df['Title'] = df.apply(lambda x: f'<p>{x["Title_ZH"]}</p><a href="{x["Link"]}" target="_blank">{x["Title"]}</a>', axis=1)
df.drop(columns=['Link', 'Title_ZH'], inplace=True)
df.rename(columns={'index': '#'}, inplace=True)

html_table = df.to_html(classes='table table-striped', index=False, escape=False)
html_table = re.sub(r'<tr style="[^"]*">', '<tr>', html_table)

# 產生完整的 HTML 頁面，包含 DataTables.js 的引用
html_page = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate, max-age=0">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">

    <title>Hacker News</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.3/css/jquery.dataTables.css">
    <style>
        body {{
            margin: 10px;
        }}
        .table {{
            width: 100%;
            font-size: 14px;
        }}
        .table p {{
            margin: 0 0 6px 0;
        }}
        .table a {{
            text-decoration: none;
        }}
        .table thead tr th {{
            padding: 6px 12px;
        }}
        .dataTables_wrapper .dataTables_filter {{
            float: left;
            margin-bottom: 20px;
        }}
    </style>
    <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.js"></script>
    <script>
        $(document).ready( function () {{
            $('.table').DataTable({{
                "paging": false
            }});
        }} );
    </script>
</head>
<body>
    <h1>Hacker News</h1>
    <p>Last updated: <span style="color: red">{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span></p>
    {html_table}
</body>
</html>
"""

# 將 HTML 頁面內容儲存到文件
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html_page)
