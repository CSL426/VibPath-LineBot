"""Test environment. Must load before any vibpath_bot import reads settings."""
import os

# 明確蓋掉本機 .env：測試不能連到正式的 MongoDB、決策 API 或 LINE
os.environ.update({
    "ChannelSecret": "test-channel-secret",
    "ChannelAccessToken": "test-channel-token",
    "GOOGLE_API_KEY": "test-google-key",
    "GOOGLE_API_KEY_FALLBACK": "",
    "GOOGLE_AI_MODEL": "gemini-test",
    "STATIC_BASE_URL": "https://csl426.github.io/VibPath-LineBot",
    "ADMIN_USER_IDS": "",
    "MONGODB_URI": "",
    "MONGODB_USERNAME": "",
    "MONGODB_PASSWORD": "",
    "MONGODB_CLUSTER": "",
    "DECISION_API_URL": "",
    "ADMIN_API_TOKEN": "test-admin-token",
})
