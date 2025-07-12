# 系統架構文件

## 概述

本系統是一個基於 Django REST Framework 的 AI 對話管理系統，採用三層架構設計，提供用戶與 AI 對話的完整功能，並包含管理員監控介面。

## 整體架構

### 三層架構設計

```
┌─────────────────────────────────────────────────────────────┐
│                    表現層 (Presentation Layer)                │
├─────────────────────────────────────────────────────────────┤
│                   業務邏輯層 (Business Logic Layer)            │
├─────────────────────────────────────────────────────────────┤
│                   資料存取層 (Data Access Layer)              │
└─────────────────────────────────────────────────────────────┘
```

#### 1. 表現層 (Presentation Layer)
負責處理 HTTP 請求和回應，提供 API 端點給前端使用。

**主要組件：**
- `presentation/conversation_views.py` - 對話相關的 API 視圖
- `presentation/conversation_management_views.py` - 管理員專用的對話管理 API
- `presentation/chat_setting_views.py` - 聊天設定 API
- `presentation/user_views.py` - 用戶管理 API
- `presentation/serializers.py` - 資料序列化器

#### 2. 業務邏輯層 (Business Logic Layer)
包含核心業務邏輯，處理對話管理、訊息處理等核心功能。

**主要組件：**
- `business_logic/services.py` - 對話管理服務
- `business_logic/ai_service.py` - AI 服務整合
- `business_logic/validators.py` - 業務規則驗證

#### 3. 資料存取層 (Data Access Layer)
負責資料庫操作和外部服務整合。

**主要組件：**
- `repositories/conversation_repository.py` - 對話資料存取
- `repositories/message_repository.py` - 訊息資料存取
- `proxies/ai_proxy.py` - AI 服務代理

## 模組交互關係

### 核心模組

#### 1. Conversations 模組
- **功能**：管理用戶對話、訊息記錄
- **交互對象**：Users 模組、AI 服務
- **主要職責**：
  - 對話生命週期管理
  - 訊息存儲和檢索
  - 對話狀態控制

#### 2. Users 模組
- **功能**：用戶認證、權限管理
- **交互對象**：Conversations 模組
- **主要職責**：
  - 用戶註冊和登入
  - 權限控制
  - 用戶設定管理

#### 3. Admin 管理系統
- **功能**：系統監控和管理
- **交互對象**：所有模組
- **主要職責**：
  - 對話監控
  - 用戶管理
  - 系統統計

## 資料模型

### 核心實體

#### Conversation (對話)
```python
- id: 主鍵
- user: 用戶外鍵
- status: 對話狀態 (active/closed)
- created_at: 建立時間
- updated_at: 最後更新時間
```

#### Message (訊息)
```python
- id: 主鍵
- conversation: 對話外鍵
- sender: 發送者 (user/ai)
- content: 訊息內容
- timestamp: 發送時間
```

#### ChatSetting (聊天設定)
```python
- id: 主鍵
- user: 用戶外鍵
- ai_model: AI 模型選擇
- temperature: 溫度參數
- max_tokens: 最大回應長度
```

## 安全性設計

### 認證與授權
- 使用 Django REST Framework 的 Token 認證
- 基於角色的存取控制 (RBAC)
- 管理員功能需要 `is_staff=True` 權限

### 資料保護
- 用戶只能存取自己的對話記錄
- 管理員可以存取所有對話記錄
- 敏感資料加密存儲

## 擴展性考量

### 水平擴展
- 無狀態設計，支援多實例部署
- 資料庫讀寫分離
- 快取機制優化效能

### 功能擴展
- 插件化 AI 服務整合
- 多語言支援
- 自定義對話模板

## 技術棧

### 後端
- **框架**：Django 4.x + Django REST Framework
- **資料庫**：PostgreSQL
- **快取**：Redis
- **任務佇列**：Celery

### 前端
- **框架**：原生 JavaScript + HTML/CSS
- **UI 庫**：Bootstrap 5
- **HTTP 客戶端**：Fetch API

### 基礎設施
- **容器化**：Docker
- **反向代理**：Nginx
- **監控**：Django Debug Toolbar (開發環境)

## 部署架構

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Nginx     │    │   Django    │    │ PostgreSQL  │
│ (反向代理)   │───→│   應用伺服器  │───→│   資料庫     │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │    Redis    │
                   │   (快取)     │
                   └─────────────┘
```

## 監控與維護

### 日誌記錄
- 應用程式日誌
- 存取日誌
- 錯誤日誌

### 效能監控
- 回應時間監控
- 資料庫查詢優化
- 記憶體使用監控

### 備份策略
- 資料庫定期備份
- 設定檔版本控制
- 災難恢復計劃
