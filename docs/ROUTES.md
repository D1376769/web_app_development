# 路由設計 (API Design) - 讀書筆記本系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁/儀表板** | GET | `/` | `templates/index.html` | 顯示系統概況與今日推薦複習清單 |
| **筆記列表** | GET | `/notes` | `templates/notes/index.html` | 顯示所有筆記，支援標籤過濾 |
| **新增筆記頁面** | GET | `/notes/new` | `templates/notes/new.html` | 顯示建立雙層筆記的表單 |
| **建立筆記** | POST | `/notes` | — | 接收表單，存入 DB，重導向至列表 |
| **筆記詳情** | GET | `/notes/<id>` | `templates/notes/detail.html` | 顯示單篇筆記的完整內容與標籤 |
| **編輯筆記頁面** | GET | `/notes/<id>/edit` | `templates/notes/edit.html` | 顯示編輯表單，帶入原有資料 |
| **更新筆記** | POST | `/notes/<id>/update` | — | 接收表單，更新 DB，重導向至詳情頁 |
| **刪除筆記** | POST | `/notes/<id>/delete` | — | 刪除筆記後重導向至列表頁 |
| **錯題/盲點清單** | GET | `/review/weakspots` | `templates/review/weakspots.html` | 顯示被標記為不熟的筆記列表 |
| **測驗模式** | GET | `/review/quiz` | `templates/review/quiz.html` | 載入測驗題目與閃卡介面 |
| **提交測驗結果** | POST | `/review/quiz/submit`| — | 接收使用者熟悉度回饋，更新排程 |

## 2. 每個路由的詳細說明

### `main_routes` (首頁)
- **`GET /`**
  - 輸入：無
  - 處理邏輯：從 Model 取得 `next_review_date` <= 今天的筆記（`get_due_for_review()`）。
  - 輸出：渲染 `index.html`。

### `note_routes` (筆記管理)
- **`GET /notes`**
  - 輸入：URL 參數 `tag` (選填，用於過濾)
  - 處理邏輯：查詢所有筆記，若有 `tag` 則過濾。
  - 輸出：渲染 `notes/index.html`。
- **`POST /notes`**
  - 輸入：表單欄位 `summary`, `extension`, `tags`
  - 處理邏輯：呼叫 `Note.create()` 與 `Tag.set_note_tags()`。
  - 輸出：重導向至 `/notes`。
  - 錯誤處理：若必填欄位 `summary` 為空，重新渲染 `notes/new.html` 並顯示錯誤訊息。
- **`GET /notes/<id>/edit`**
  - 輸入：URL 路徑參數 `id`
  - 處理邏輯：取得筆記資料與關聯標籤。
  - 輸出：渲染 `notes/edit.html`。若找不到筆記則回傳 404。
- **`POST /notes/<id>/update`**
  - 輸入：表單欄位 `summary`, `extension`, `tags`, `is_weakspot`
  - 處理邏輯：更新筆記與標籤關聯。
  - 輸出：重導向至 `/notes/<id>`。

### `review_routes` (測驗與複習)
- **`GET /review/quiz`**
  - 輸入：無
  - 處理邏輯：隨機或依照到期順序取出一篇需要複習的筆記。
  - 輸出：渲染 `review/quiz.html`。若無題目則顯示提示訊息。
- **`POST /review/quiz/submit`**
  - 輸入：表單欄位 `note_id`, `familiarity` (1=不熟, 2=普通, 3=熟悉)
  - 處理邏輯：呼叫 `Note.update_review_schedule()` 更新間隔重複資料。
  - 輸出：重導向回 `/review/quiz` 繼續下一題。

## 3. Jinja2 模板清單

所有的模板都將繼承自 `templates/base.html`：

- `templates/base.html`: 共用佈局 (Header, Footer, 導覽列, CSS/JS 引入)
- `templates/index.html`: 儀表板首頁
- `templates/notes/index.html`: 筆記列表頁
- `templates/notes/new.html`: 新增筆記表單
- `templates/notes/detail.html`: 單筆檢視頁
- `templates/notes/edit.html`: 編輯筆記表單
- `templates/review/weakspots.html`: 錯題/盲點列表
- `templates/review/quiz.html`: 閃卡測驗頁面

## 4. 路由骨架程式碼
請參考 `app/routes/` 目錄下的 Python 檔案。
