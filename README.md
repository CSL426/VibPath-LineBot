# VibPath 商品介紹 LINE Bot

基於 Google ADK (Agent SDK) 和 Google Gemini 的專業商品介紹 LINE Bot，專門提供產品諮詢和購買導引服務。

## 🌟 功能特色

- 🎵 **商品產品展示** - 舒曼波、α/θ波、γ波、13頻脈輪波產品介紹
- 🛒 **商品購買導引** - 直接連結蝦皮商店，方便下單
- 🤖 **AI 產品客服** - 基於 Google Gemini 2.0 Flash 的專業產品諮詢
- 📱 **Flex Message 展示** - 美觀的圖文訊息和輪播介面
- ⚡ **Quick Reply 快速操作** - 便捷的按鈕式互動
- 🔧 **Postback 互動** - 詳細的產品解說和技術說明
- 👤 **管理員功能** - 支援暫停/恢復 Bot 運作，方便維護管理
- ☁️ **雲端部署** - 針對 Google Cloud Run 優化

## 🛠️ 技術架構

```
vibpath_bot/
├── templates/              # Flex Message 模板
│   ├── custom_templates.py # 業務模板（商品產品）
│   ├── flex_templates.py   # 基礎 Flex 模板
│   └── bubble_templates.py # 進階 Bubble 模板
├── handlers/               # 處理器
│   ├── message_handler.py  # 訊息處理
│   ├── postback_handler.py # 按鈕回調處理
│   └── quick_reply.py      # 快速回覆
├── config/                 # 配置管理
│   ├── agent_prompts.py    # AI 提示詞管理
│   ├── button_config.py    # 按鈕配置
│   ├── admin_config.py     # 管理員權限與暫停管理
│   └── static_urls.py      # 靜態資源配置
└── utils/                  # 工具函數
    └── image_manager.py    # 圖片管理

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

### 技術堆疊

- **Python 3.10** - 主要程式語言
- **FastAPI** - 高效能異步 Web 框架
- **LINE Messaging API** - LINE Bot 通訊
- **Google ADK** - AI 代理開發框架
- **Google Gemini 2.0 Flash** - 語言模型
- **Docker** - 容器化部署
- **Google Cloud Run** - 雲端託管
- **Google Cloud Storage** - 靜態資源託管（可選）

## 🚀 快速開始

### 1. 環境設定

複製環境變數範本並填入您的設定：

```bash
cp .env.example .env
```

編輯 `.env` 檔案：

```env
# LINE Bot Configuration
ChannelSecret=your_line_channel_secret_here
ChannelAccessToken=your_line_channel_access_token_here

# Google AI Configuration
GOOGLE_API_KEY=your_google_ai_api_key_here

# Google Cloud Project
GOOGLE_CLOUD_PROJECT=your-project-id

# Admin Configuration
ADMIN_USER_IDS=Uxxx:Uyyy  # 管理員 LINE User ID (用 : 分隔)
TIMEZONE=Asia/Taipei      # 時區設定 (預設 UTC+8)

# Static Assets Base URL (可選)
STATIC_BASE_URL=https://storage.googleapis.com/your-bucket
```

**說明：**
- **ADMIN_USER_IDS**: 在日誌中查看或使用 LINE Developers Console 測試工具取得
- **TIMEZONE**: 支援所有 IANA 時區名稱，例如 `Asia/Taipei`、`Asia/Tokyo`、`UTC` 等

### 2. 本地開發

使用 Docker Compose 進行本地開發：

```bash
# 啟動開發環境
docker-compose up --build

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

### 4. 靜態資源部署（可選）

使用 Google Cloud Storage 託管圖片：

```bash
# 創建 bucket
gsutil mb -p your-project -c standard -l asia-east1 gs://your-bucket

# 上傳圖片並設為公開
gsutil -m cp -r static/images gs://your-bucket/
gsutil -m acl ch -r -u AllUsers:R gs://your-bucket/images
```

## 📱 LINE Bot 設定

部署完成後，在 [LINE Developers Console](https://developers.line.biz/) 設定 Webhook URL：

```
https://your-service-url/webhook
```

### 可用端點

- `GET /` - 服務狀態
- `GET /health` - 健康檢查
- `POST /webhook` - LINE Bot 訊息處理
- `POST /callback` - 通用回調端點
- `GET /static/*` - 靜態檔案服務（如不使用 GCS）

## 🎵 產品功能

### 主要產品線

1. **舒曼波 (7.83Hz)** - 助眠放鬆
2. **13頻脈輪波** - 瑜珈能量調理
3. **γ波 (40Hz)** - 專注力提升
4. **雙頻複合治療** - 多頻率組合

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
- 🌍 7.83Hz 舒曼共振原理
- 🧠 13頻脈輪系統說明
- ⚡ 40Hz γ波專注效果
- 🔄 雙頻複合治療機制

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

## 🔐 安全性

- 使用環境變數管理敏感資訊
- LINE Bot Webhook 使用簽名驗證
- Cloud Run 服務預設使用 HTTPS
- 靜態資源支援 CDN 加速

## 📈 擴展性

### 新增功能模組

1. **新增產品線** - 在配置檔案中添加新產品資訊
2. **新增互動方式** - 擴展 Quick Reply 或 Postback 功能
3. **API 整合** - 透過工具模組整合外部服務

### 效能優化

- Docker Layer Caching 減少建構時間
- Cloud Run 自動擴縮容
- GCS 靜態資源託管降低服務負載
- 異步處理提升回應速度


## 📄 授權

本專案採用 MIT 授權條款。

---

🚀 **快速部署**: 執行 `./deploy.sh` 立即部署到 Google Cloud Run！
🎵 **產品展示**: 專業商品設備，波形純淨、失真度低、磁場強度足！