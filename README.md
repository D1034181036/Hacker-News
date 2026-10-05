# Hacker News

功能：抓 Hacker News 前 3 頁，翻譯標題後輸出 `index.html`。

```bash
pip install -r requirements.txt
```

## 免費版

```bash
python hackernews.py
```

> 使用 `translate` 套件（MyMemory 免費 API），逐句翻譯，每日額度有限，通常設定一天兩次。

## Gemini 版

複製 `.env.example` 為 `.env`，填入 `GEMINI_API_KEY` 與 `GEMINI_MODEL`。

```bash
python hackernews_gemini.py
```

> 使用 Gemini API，所有標題一次送出，技術用語較準確。

## 輸出位置

預設輸出到專案下的 `public/index.html`，可在 `.env` 用 `OUTPUT_DIR` 指定（相對於專案目錄，或絕對路徑）：

```
OUTPUT_DIR=public
```

## 排程（Linux crontab）

`crontab -e`，每天 08:00、14:00 更新：

```cron
0 8,14 * * * cd /path/to/Hacker-News && python3 hackernews_gemini.py
```
