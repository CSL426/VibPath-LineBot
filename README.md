# VibPath 智能客服 LINE Bot

基於 Google ADK (Agent SDK) 和 Google Gemini 的智能客服 LINE Bot，專門提供天氣查詢服務並支援繁體中文對話。

## 🌟 功能特色

- 🌤️ **即時天氣查詢** - 使用 wttr.in API 提供全球城市天氣資訊
- 🤖 **智能對話** - 基於 Google Gemini 2.0 Flash 模型
- ⚡ **等待動畫** - 處理請求時顯示「正在輸入」動畫
- 🌐 **多語言支援** - 優化繁體中文回應
- 🔧 **模組化架構** - 清晰的工具和代理分離
- ☁️ **雲端部署** - 針對 Google Cloud Run 優化

## 🛠️ 技術架構

```
multi_tool_agent/
├── agent.py              # 中控台 (Control Center)
├── utils/
│   ├── weather_utils.py  # 天氣 API 工具
│   └── line_utils.py     # LINE Bot 工具 (等待動畫)
└── agents/               # 代理模組目錄
```

### 技術堆疊

- **Python 3.10** - 主要程式語言
- **FastAPI** - 高效能異步 Web 框架
- **LINE Messaging API** - LINE Bot 通訊
- **Google ADK** - AI 代理開發框架
- **Google Gemini 2.0 Flash** - 語言模型
- **wttr.in API** - 天氣數據來源
- **Docker** - 容器化部署
- **Google Cloud Run** - 雲端託管

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

# Service Name (可選)
SERVICE_NAME=my-linebot-service
```

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

## 🌤️ 使用方式

### 天氣查詢範例

向您的 LINE Bot 發送以下訊息：

- "台北天氣如何？"
- "東京明天會下雨嗎？"
- "高雄的天氣資訊"
- "London weather"

### 回應格式

```
🌤️ 台北, Taiwan 天氣資訊：
📊 天氣：Clear
🌡️ 溫度：25°C (77°F)
🌡️ 體感：27°C
💧 濕度：65%
🌬️ 風速：8 km/h (NE)
```

## 🔧 開發指南

### 添加新工具

1. 在 `multi_tool_agent/utils/` 建立新的工具模組
2. 在 `multi_tool_agent/agent.py` 中建立對應函數
3. 將函數加入 `tools` 列表

### 本地測試流程

```bash
# 1. 本地開發測試
docker-compose up --build

# 2. 確認功能正常後部署
./deploy.sh

# 3. 檢查部署狀態
gcloud run services describe SERVICE_NAME --region=asia-east1
```

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
- 建議在生產環境使用 Google Secret Manager
- LINE Bot Webhook 使用簽名驗證
- Cloud Run 服務預設使用 HTTPS

## 📈 擴展性

### 新增功能模組

1. **新增代理** - 在 `agents/` 目錄建立專門的代理
2. **新增工具** - 在 `utils/` 目錄建立工具函數
3. **API 整合** - 透過工具模組整合外部 API

### 效能優化

- Docker Layer Caching 減少建構時間
- Cloud Run 自動擴縮容
- 異步處理提升回應速度

## 🆘 故障排除

### 常見問題

1. **部署失敗** - 檢查環境變數是否正確設定
2. **Webhook 無回應** - 確認 LINE Bot 設定正確
3. **天氣查詢失敗** - 檢查網路連線和 API 可用性
4. **等待動畫不顯示** - 確認 LINE Bot API 實例正確設定

### 除錯指令

```bash
# 檢查服務狀態
curl https://your-service-url/health

# 檢查容器日誌
gcloud logs read "resource.type=cloud_run_revision"

# 測試本地部署
docker build -t test . && docker run -p 8080:8080 --env-file .env test
```

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個專案！

## 📄 授權

本專案採用 MIT 授權條款。

---

🚀 **快速部署**: 執行 `./deploy.sh` 立即部署到 Google Cloud Run！