# AI Employee Lab V1.1

通用 AI 員工工作管理原型（繁體中文）。

## 功能
- 六位預設角色：Eve、Joseph、Luke、Solomon、Nehemiah、Paul
- 新增員工、工作指派、待辦／工作中／待核准／完成／失敗狀態
- 人工核准門檻、成果證據欄位、事件紀錄
- 瀏覽器本機儲存、JSON 匯出及匯入、總 PM 週報
- 虛擬辦公室燈號依任務資料計算

## 重要限制
這是 **本機人工操作的管理原型**，不是已串接的 Claude Code、Codex 或 Grok AI Agent。燈號不能代表真實 Agent 執行狀態。資料保存在各裝置瀏覽器的 localStorage，不會跨裝置同步。勿輸入密碼、敏感資料或真實醫療、財務個資。

## 使用
開啟網站的 index.html，新增任務，按「開始工作」，輸入成果及證據，送交人工審核，再由使用者核准完成。可匯出 JSON 備份。

## 驗收
程式碼已提交 GitHub；尚未完成瀏覽器端端到端測試、真實 AI 執行串接或多 Agent 自動協作。正式上線驗收前需逐項實測。

## 部署
本專案為純靜態網頁，GitHub Pages 可從 main 分支根目錄發佈。到 Settings → Pages → Build and deployment，選 Deploy from a branch，Branch: main，Folder: /(root)，Save。
