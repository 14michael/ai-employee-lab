# 個人 AI 工作台｜後端原型 V0.3

這是**開發用原型**，不是已部署或已完成的 AI 工作台。

## 啟動
```bash
pip install -r requirements.txt
export WORKBENCH_TOKEN="replace-with-a-long-secret"
uvicorn api:app --host 127.0.0.1 --port 8080
```
Windows PowerShell 使用 `$env:WORKBENCH_TOKEN="..."`。

## 測試
```bash
pytest -q
```

## 已實作
Bearer token 驗證、SQLite 資料持久化、任務／知識／技能／智能體／手冊／交接紀錄 CRUD、狀態更新、健康檢查。

## 未實作與限制
沒有登入、Supabase、多租戶隔離、AI 模型呼叫、文件解析、排程或 Bot 自主協作。SQLite 適用於本機原型，不能直接當成 Netlify 正式後端；不得將 token 寫入公開前端。正式版必須使用 Supabase Auth + RLS，並將 AI 金鑰放在伺服器端。
