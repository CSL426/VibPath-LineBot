# Static Assets

這個目錄包含 LINE Bot 和未來網頁應用的靜態資源。

## 目錄結構

```
static/
├── images/           # 一般圖片資源
│   ├── weather/      # 天氣相關圖片
│   ├── icons/        # 圖標
│   └── backgrounds/  # 背景圖片
├── rich_menu/        # Rich Menu 圖片
│   ├── main_menu.png
│   ├── weather_menu.png
│   └── simple_menu.png
└── README.md
```

## Rich Menu 圖片規格

- **尺寸**: 2500x1686 pixels
- **格式**: PNG 或 JPG
- **大小**: 最大 1MB
- **色彩**: RGB

### 推薦設計工具

- Adobe Photoshop
- Canva
- Figma
- LINE Official Account Manager (內建編輯器)

## 圖片使用指南

### Flex Message 圖片
- 建議比例: 20:13 (例如: 1024x640)
- 格式: PNG, JPG
- 使用 HTTPS URL

### Hero Image
- 尺寸: 1024x640 pixels 或更大
- 保持 20:13 比例
- 高品質，清晰度佳

### Icon Images
- 尺寸: 64x64 或 128x128 pixels
- 格式: PNG (支援透明背景)
- 簡潔明瞭的設計

## 圖片最佳化

1. **壓縮**: 使用工具如 TinyPNG 減小檔案大小
2. **格式**: JPG 適合照片，PNG 適合圖標
3. **CDN**: 考慮使用 CDN 加速圖片載入
4. **響應式**: 提供不同尺寸適應各種裝置

## 注意事項

- 確保圖片版權清楚
- 避免使用受版權保護的素材
- 定期清理未使用的圖片
- 使用有意義的檔案名稱