# -*- coding: utf-8 -*-
# 免費版：translate 套件（MyMemory），一句一句送，匿名每日約 5000 字元額度

from translate import Translator

from hn_common import run

def translateTitles(titles):
  translator = Translator(to_lang='zh-tw')
  result = []
  for title in titles:
    try:
      result.append(translator.translate(title))
    except Exception as e:
      print(f'翻譯失敗：{e}')
      result.append(title)  # 失敗就退回原文
  return result

run(translateTitles)
