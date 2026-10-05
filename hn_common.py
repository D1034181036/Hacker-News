# -*- coding: utf-8 -*-
# 共用：抓 Hacker News、產生 index.html

import os
from html import escape
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv('OUTPUT_DIR') or 'public')
PAGES = 3

def getPageData(pageNumber = 1):
  response = requests.get(f'https://news.ycombinator.com/news?p={pageNumber}', timeout=30)
  soup = BeautifulSoup(response.text, 'html.parser')

  items = []
  for tr in soup.find_all('tr', class_='athing'):
    sub = tr.find_next_sibling('tr').find('td', class_='subtext')
    score = sub.find('span', class_='score')
    items.append({
      'title': tr.find('span', class_='titleline').find('a').text,
      'link': f'https://news.ycombinator.com/{sub.find_all("a")[-1].get("href")}',
      'score': int(''.join(filter(str.isdigit, score.text)) or 0) if score else 0,
    })
  return items

def run(translateTitles):
  # 取得前 N 頁文章並翻譯標題
  news = [item for i in range(PAGES) for item in getPageData(i + 1)]
  for item, zh in zip(news, translateTitles([n['title'] for n in news])):
    item['title_zh'] = zh

  rows = '\n'.join(f"""        <tr>
          <td>{i}</td>
          <td>{n['score']}</td>
          <td><p>{escape(n['title_zh'])}</p><a href="{escape(n['link'])}" target="_blank">{escape(n['title'])}</a></td>
        </tr>""" for i, n in enumerate(news, 1))

  html_page = f"""<!DOCTYPE html>
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
    <table border="1" class="dataframe table table-striped">
      <thead>
        <tr><th>#</th><th>Score</th><th>Title</th></tr>
      </thead>
      <tbody>
{rows}
      </tbody>
    </table>
</body>
</html>
"""

  os.makedirs(OUTPUT_DIR, exist_ok=True)
  with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_page)
