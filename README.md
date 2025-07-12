# AI 對話管理系統 (Playms Homework)

一個基於 Django REST Framework 的智能對話管理平台，提供用戶與 AI 的互動功能，並包含完整的管理監控介面。

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 目錄

- [專案概述](#專案概述)
- [主要功能](#主要功能)
- [技術架構](#技術架構)
- [文檔導覽](#文檔導覽)
- [快速開始](#快速開始)
- [開發指南](#開發指南)
- [部署說明](#部署說明)
- [API 使用](#api-使用)
- [測試](#測試)
- [貢獻指南](#貢獻指南)
- [授權](#授權)

## 🚀 專案概述

本專案是一個現代化的 AI 對話管理系統，採用三層架構設計，提供：

- **用戶介面**：直觀的聊天介面，支援即時對話
- **管理介面**：完整的系統監控和用戶管理功能
- **API 服務**：RESTful API 支援第三方整合
- **智能回應**：整合 OpenAI GPT 模型提供智能對話

### 核心價值

- 🎯 **專業架構**：採用三層架構確保代碼品質和可維護性
- 🔒 **安全可靠**：完整的身份驗證和權限控制系統
- 📊 **監控管理**：提供詳細的使用統計和管理功能
- 🔧 **易於擴展**：模組化設計支援功能擴展
- 📚 **完整文檔**：提供全面的開發和使用文檔

## ✨ 主要功能

### 用戶功能
- 🗨️ **智能對話**：與 AI 進行自然語言對話
- 📝 **對話管理**：創建、關閉、重新開啟對話
- ⚙️ **個人設定**：自定義 AI 模型參數
- 🔍 **對話搜尋**：快速找到歷史對話記錄
- 📤 **資料匯出**：支援多種格式的對話記錄匯出

### 管理功能
- 👥 **用戶管理**：監控所有用戶活動
- 📊 **統計分析**：詳細的使用統計和趨勢分析
- 🔐 **權限控制**：基於角色的存取控制
- 📋 **系統監控**：即時監控系統狀態和效能

## 🏗️ 技術架構

本專案採用**三層架構**設計：

```
┌─────────────────────────────────────────┐
│           表現層 (Presentation)          │  ← API 端點、序列化器
├─────────────────────────────────────────┤
│         業務邏輯層 (Business Logic)       │  ← 核心業務邏輯、服務
├─────────────────────────────────────────┤
│         資料存取層 (Data Access)         │  ← 資料庫操作、外部 API
└─────────────────────────────────────────┘
```

### 技術棧

- **後端框架**：Django 4.x + Django REST Framework
- **資料庫**：PostgreSQL
- **快取**：Redis
- **前端**：HTML5 + JavaScript + Bootstrap 5
- **AI 服務**：OpenAI GPT API
- **容器化**：Docker + Docker Compose
- **測試**：pytest + coverage

## 📚 文檔導覽

本專案提供完整的文檔系統，涵蓋開發、部署、使用的各個層面：

### 系統設計文檔
- 📋 **[系統架構文件](docs/SYSTEM_ARCHITECTURE.md)** - 詳細的三層架構設計說明
- 🔧 **[架構圖表](docs/ARCHITECTURE_DIAGRAMS.md)** - 視覺化的系統架構和資料流向圖

### 開發文檔
- 🔌 **[API 文件](docs/API_DOCUMENTATION.md)** - 完整的 RESTful API 說明
- 🧪 **[測試用例](docs/TEST_CASES.md)** - 全面的測試策略和用例

### 使用文檔
- 👥 **[使用說明](docs/USER_GUIDE.md)** - 詳細的用戶操作指南
- 🚀 **[部署指南](docs/DEPLOYMENT_GUIDE.md)** - 本地和生產環境部署說明

### 模組說明
- 💬 **[對話模組說明](playms_homework/conversations/README.md)** - 核心對話功能詳解
- 📊 **[實作總結](playms_homework/conversations/IMPLEMENTATION_SUMMARY.md)** - 開發重點和設計決策

## 🚀 快速開始

### 環境需求

- Python 3.9+
- PostgreSQL 13+
- Redis 6+ (選用)
- Node.js 16+ (用於前端資源編譯)

### 本地開發設置

1. **複製專案**
   ```bash
   git clone <repository-url>
   cd playms_homework
   ```

2. **建立虛擬環境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或 venv\Scripts\activate  # Windows
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements/local.txt
   ```

4. **環境變數設定**
   ```bash
   cp .env.example .env
   # 編輯 .env 檔案，設定資料庫和 API 金鑰
   ```

5. **資料庫設置**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **啟動服務**
   ```bash
   python manage.py runserver
   ```

訪問 `http://localhost:8000` 開始使用！

### Docker 快速部署

```bash
# 使用 Docker Compose 一鍵啟動
docker-compose up -d

# 執行資料庫遷移
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 💻 開發指南

### 專案結構

```
playms_homework/
├── config/                 # Django 設定檔
├── playms_homework/        # 主要應用程式
│   ├── conversations/      # 對話管理模組
│   │   ├── business_logic/ # 業務邏輯層
│   │   ├── presentation/   # 表現層 (API)
│   │   ├── repositories/   # 資料存取層
│   │   └── models/         # 資料模型
│   ├── users/             # 用戶管理模組
│   └── static/            # 靜態檔案
├── docs/                  # 專案文檔
├── requirements/          # 依賴套件
└── utility/              # 工具腳本
```

### 開發命令

```bash
# 執行測試
pytest

# 檢查程式碼品質
mypy playms_homework
ruff check .

# 測試覆蓋率
coverage run -m pytest
coverage html

# 建立新的資料庫遷移
python manage.py makemigrations

# 收集靜態檔案
python manage.py collectstatic
```

## 🌐 部署說明

詳細的部署指南請參考：**[部署指南](docs/DEPLOYMENT_GUIDE.md)**

### 支援的部署方式

- **本地開發**：Django 開發伺服器
- **生產環境**：Nginx + Gunicorn + PostgreSQL
- **容器化**：Docker + Docker Compose
- **雲端部署**：支援各大雲端平台

### 快速部署檢查清單

- [ ] 設定環境變數
- [ ] 設定資料庫連線
- [ ] 設定 AI API 金鑰
- [ ] 執行資料庫遷移
- [ ] 收集靜態檔案
- [ ] 設定 Web 伺服器
- [ ] 設定 SSL 憑證

## 🔌 API 使用

本專案提供完整的 RESTful API，詳細說明請參考：**[API 文件](docs/API_DOCUMENTATION.md)**

### 主要端點

```bash
# 對話管理
GET    /api/conversations/              # 獲取對話列表
POST   /api/conversations/              # 創建新對話
POST   /api/conversations/{id}/send_message/  # 發送訊息

# 管理員 API
GET    /api/admin/conversations/        # 獲取所有對話 (管理員)
GET    /api/admin/users/               # 獲取用戶列表 (管理員)
```

### API 使用範例

```javascript
// JavaScript 範例
const response = await fetch('/api/conversations/', {
    headers: {
        'Authorization': 'Token your-token-here',
        'Content-Type': 'application/json'
    }
});
const conversations = await response.json();
```

## 🧪 測試

完整的測試策略請參考：**[測試用例](docs/TEST_CASES.md)**

### 測試覆蓋範圍

- ✅ 單元測試：模型、服務、業務邏輯
- ✅ 整合測試：API 端點和資料流
- ✅ 權限測試：身份驗證和授權
- ✅ 效能測試：負載和回應時間

### 執行測試

```bash
# 執行所有測試
pytest

# 執行特定模組測試
pytest playms_homework/conversations/tests/

# 生成測試覆蓋率報告
coverage run -m pytest
coverage report
coverage html  # 產生 HTML 報告
```

## 🤝 貢獻指南

我們歡迎各種形式的貢獻！

### 如何貢獻

1. **Fork** 本專案
2. **建立功能分支** (`git checkout -b feature/amazing-feature`)
3. **提交變更** (`git commit -m 'Add some amazing feature'`)
4. **推送到分支** (`git push origin feature/amazing-feature`)
5. **開啟 Pull Request**

### 開發規範

- 遵循 PEP 8 Python 編碼規範
- 編寫單元測試覆蓋新功能
- 更新相關文檔
- 提交訊息使用中文或英文，描述清楚

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 📞 支援與聯繫

- **技術文檔**：查看 [docs/](docs/) 目錄下的詳細文檔
- **問題回報**：使用 GitHub Issues
- **功能建議**：歡迎提交 Pull Request

---

## 🔗 相關連結

- [Django 官方文檔](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [OpenAI API 文檔](https://platform.openai.com/docs)
- [PostgreSQL 文檔](https://www.postgresql.org/docs/)

**感謝使用 AI 對話管理系統！** 🚀
