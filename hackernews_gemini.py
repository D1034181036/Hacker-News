# -*- coding: utf-8 -*-
# Gemini 版：一次送出全部標題翻譯，需要 .env 的 GEMINI_API_KEY、GEMINI_MODEL

import os
import json

from google import genai
from google.genai import types

from hn_common import run

MODEL = os.getenv('GEMINI_MODEL')
if not MODEL:
  raise SystemExit('請在 .env 設定 GEMINI_MODEL')

def translateTitles(titles):
  prompt = f"""把以下 Hacker News 標題翻成台灣繁體中文。
規則：程式語言、框架、函式庫、產品與公司名稱、Show HN/Ask HN 等保留英文；用台灣慣用技術用語；不要加解釋。
依原順序回傳 JSON 字串陣列，長度必須與輸入相同。

{json.dumps(titles, ensure_ascii=False)}"""

  try:
    client = genai.Client()
    res = client.models.generate_content(
      model=MODEL,
      contents=prompt,
      config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=list[str],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
      ),
    )
    result = json.loads(res.text)
    if len(result) == len(titles):
      return result
    print(f'翻譯數量不符：{len(result)} / {len(titles)}')
  except Exception as e:
    print(f'翻譯失敗：{e}')
  return titles  # 失敗就退回原文

run(translateTitles)
