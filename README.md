# VibPath 商品介紹 LINE Bot

基於 Google ADK (Agent SDK) 和 Google Gemini 的專業商品介紹 LINE Bot，專門提供產品諮詢和購買導引服務。

## 🌟 功能特色

- 🎵 **商品展示** - Flex Message 輪播 4 款產品
- 🤖 **AI 客服** - Google ADK
- 🔘 **AI 開關** - 用戶可關閉 AI 自動回覆
- ⚡ **兩層快速回覆** - 基本/產品選單切換
- 👤 **管理員暫停** - 可設定時間暫停 Bot

## 🛠️ 技術架構

```
vibpath_bot/
├── templates/              # Flex Message 模板
│   ├── custom_templates.py # 業務模板（商品產品）
│   ├── flex_templates.py   # 基礎 Flex 模板
│   └── bubble_templates.py # 進階 Bubble 模板
├── handlers/               # 處理器
│   ├── message_handler.py  # 訊息處理（含兩層快速回覆）
│   ├── postback_handler.py # 按鈕回調處理
│   └── ai_toggle_handler.py # AI 開關處理
├── services/               # 服務層
│   └── user_preference_service.py # 用戶偏好服務（整合 DB + Cache）
├── config/                 # 配置管理
│   ├── agent_prompts.py    # AI 提示詞管理
│   ├── button_config.py    # 按鈕配置
│   ├── admin_config.py     # 管理員權限與暫停管理
│   └── static_urls.py      # 靜態資源配置
├── utils/                  # 工具函數
│   ├── image_manager.py    # 圖片管理
│   ├── mongodb_client.py   # MongoDB 連線與操作
│   └── user_cache.py       # 記憶體快取（TTL）
└── tools/                  # AI 工具
    └── ai_tools.py         # AI Agent 工具函數

multi_tool_agent/
├── agent.py                # AI 代理中控台
└── utils/
    └── line_utils.py       # LINE Bot 工具 (等待動畫)

static/
├── images/
│   ├── business/           # 企業形象圖片
│   └── services/           # 產品服務圖片
└── rich_menu/              # Rich Menu 圖片
```

## 🚀 快速開始

### 1. 環境設定

複製環境變數範本並填入您的設定：

```bash
cp .env.example .env
```

### 2. 本地開發

使用 Docker Compose 進行本地開發：

```bash
# 啟動開發環境
docker compose up --build

# 測試端點
curl http://localhost:8080/health
```

### 3. 雲端部署

一鍵部署到 Google Cloud Run：

```bash
# 設定 Google Cloud SDK
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 啟用必要的 APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# 部署
./deploy.sh
```

## 📱 LINE Bot 設定

部署完成後，在 [LINE Developers Console](https://developers.line.biz/) 設定 Webhook URL：

```
https://your-service-url/webhook
```

### 可用端點

#### Webhook 端點
- `POST /webhook` - LINE Bot 訊息處理（LINE 平台專用）
- `POST /callback` - 通用回調端點
- `GET /` - 服務狀態
- `GET /health` - 健康檢查
- `GET /static/*` - 靜態檔案服務（如不使用 GCS）

#### RESTful API 端點
- `GET /api/users` - 列出所有用戶偏好設定
- `GET /api/users/{user_id}/preferences` - 取得指定用戶的偏好設定
- `PUT /api/users/{user_id}/preferences` - 更新用戶偏好設定
- `DELETE /api/users/{user_id}/preferences` - 刪除用戶偏好設定（重置為預設）

## 🎵 產品功能

### 主要產品線

1. **舒曼波 (7.83Hz)** - 助眠放鬆
2. **13頻脈輪波** - 瑜珈脈輪系統
3. **γ波 (40Hz)** - 輔助專注
4. **雙頻 α/θ波** - 多頻率組合

### 使用方式

向您的 LINE Bot 發送以下訊息或使用 Quick Reply：

- **「公司介紹」** - 查看企業資訊
- **「商品介紹」** - 瀏覽4種產品輪播
- **「選單」** - 顯示服務選單
- **「幫助」** - 查看使用說明

### Quick Reply 互動

- 🏢 公司介紹 → 企業資訊
- 🎵 商品介紹 → 產品輪播
- 📋 選單 → 服務選單
- 💡 快速解說 → AI 產品說明

### Postback 詳細解說

每個產品都有詳細的技術說明：
- 🌍 7.83Hz 舒曼波說明
- 🧠 13頻脈輪系統說明
- ⚡ 40Hz γ波說明
- 🔄 雙頻 α/θ波說明

## 🔌 RESTful API 使用

### API 基礎資訊

Base URL: `https://your-service-url`

所有 API 回應格式：
```json
{
  "status": "success",
  "data": { ... }
}
```

### 1. 列出所有用戶偏好設定

```bash
GET /api/users
```

**回應範例：**
```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "userId": "U1234567890abcdef",
      "aiReplyEnabled": true,
      "lastUpdated": "2025-01-15T10:30:00Z"
    },
    {
      "userId": "U9876543210fedcba",
      "aiReplyEnabled": false,
      "lastUpdated": "2025-01-15T11:45:00Z"
    }
  ]
}
```

### 2. 取得指定用戶的偏好設定

```bash
GET /api/users/{user_id}/preferences
```

**範例：**
```bash
curl https://your-service-url/api/users/U1234567890abcdef/preferences
```

**回應範例：**
```json
{
  "status": "success",
  "data": {
    "userId": "U1234567890abcdef",
    "aiReplyEnabled": true
  }
}
```

### 3. 更新用戶偏好設定

```bash
PUT /api/users/{user_id}/preferences
Content-Type: application/json

{
  "aiReplyEnabled": false
}
```

**範例：**
```bash
curl -X PUT https://your-service-url/api/users/U1234567890abcdef/preferences \
  -H "Content-Type: application/json" \
  -d '{"aiReplyEnabled": false}'
```

**回應範例：**
```json
{
  "status": "success",
  "message": "User preferences updated successfully",
  "data": {
    "userId": "U1234567890abcdef",
    "aiReplyEnabled": false
  }
}
```

### 4. 刪除用戶偏好設定（重置為預設）

```bash
DELETE /api/users/{user_id}/preferences
```

**範例：**
```bash
curl -X DELETE https://your-service-url/api/users/U1234567890abcdef/preferences
```

**回應範例：**
```json
{
  "status": "success",
  "message": "User preferences deleted (deleted 1 document)",
  "data": {
    "userId": "U1234567890abcdef",
    "deletedCount": 1
  }
}
```

### API 錯誤處理

API 錯誤會返回適當的 HTTP 狀態碼：

- `400 Bad Request` - 請求參數錯誤
- `404 Not Found` - 資源不存在
- `500 Internal Server Error` - 伺服器錯誤
- `503 Service Unavailable` - MongoDB 未連線

**錯誤回應範例：**
```json
{
  "detail": "aiReplyEnabled field is required"
}
```

## 👤 管理員功能

### 設定管理員

在 `.env` 檔案中設定管理員的 LINE User ID：

```env
ADMIN_USER_IDS=U1234567890abcdef123:U1234567890abcdef
```

支援多個管理員，用 `:` 分隔（不要有空格）。

### 管理員指令

| 指令 | 說明 |
|------|------|
| `暫停` | 暫停 1 小時（預設） |
| `暫停15分鐘` `暫停15分` `暫停15m` `暫停15min` | 暫停指定分鐘 |
| `暫停2小時` `暫停2小` `暫停2h` `暫停2hr` | 暫停指定小時 |
| `恢復` `繼續` `resume` | 恢復運作 |
| `狀態` `status` | 查看狀態 |
| `指令` `commands` `admin` | 顯示管理指令說明 |

支援有無空格皆可，例如：`暫停 15分鐘` 或 `暫停15分鐘`

**運作邏輯：**
- 暫停期間 Bot 完全靜默（管理指令除外）
- 時間到達自動恢復
- 管理員一般訊息同樣不回應

## 📊 監控與維護

### 檢視日誌

```bash
# 即時日誌
gcloud logs tail --service=your-service-name

# 錯誤日誌
gcloud logs read "resource.type=cloud_run_revision AND severity=ERROR"
```

### 服務管理

```bash
# 查看所有服務
gcloud run services list --region=asia-east1

# 刪除舊服務
gcloud run services delete old-service-name --region=asia-east1
```

## 📄 授權

本專案採用 MIT 授權條款。

---

🚀 **快速部署**: 執行 `./deploy.sh` 立即部署到 Google Cloud Run！
