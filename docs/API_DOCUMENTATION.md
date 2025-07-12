# API 文件

## 概述

本系統提供 RESTful API，支援用戶對話管理和管理員監控功能。所有 API 都需要身份驗證，管理員 API 需要額外的管理員權限。

## 認證

### 認證方式
系統支援兩種認證方式：
- **Token 認證**：適用於程式化存取
- **Session 認證**：適用於網頁瀏覽器

### 請求標頭
```http
Authorization: Token <your-token>
Content-Type: application/json
```

## 用戶 API 端點

### 對話管理

#### 1. 獲取對話列表
```http
GET /api/conversations/
```

**回應格式：**
```json
[
  {
    "id": 1,
    "user": 1,
    "user_username": "john_doe",
    "status": "active",
    "created_at": "2025-01-12T10:00:00Z",
    "updated_at": "2025-01-12T10:30:00Z",
    "messages": []
  }
]
```

#### 2. 創建新對話
```http
POST /api/conversations/
```

**請求內容：**
```json
{}
```

**回應格式：**
```json
{
  "id": 2,
  "user": 1,
  "user_username": "john_doe",
  "status": "active",
  "created_at": "2025-01-12T11:00:00Z",
  "updated_at": "2025-01-12T11:00:00Z",
  "messages": []
}
```

#### 3. 獲取特定對話
```http
GET /api/conversations/{id}/
```

**回應格式：**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "john_doe",
  "status": "active",
  "created_at": "2025-01-12T10:00:00Z",
  "updated_at": "2025-01-12T10:30:00Z",
  "messages": [
    {
      "id": 1,
      "sender": "user",
      "content": "Hello, AI!",
      "timestamp": "2025-01-12T10:15:00Z"
    },
    {
      "id": 2,
      "sender": "ai",
      "content": "Hello! How can I help you today?",
      "timestamp": "2025-01-12T10:15:30Z"
    }
  ]
}
```

#### 4. 關閉對話
```http
POST /api/conversations/{id}/close/
```

**回應格式：**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "john_doe",
  "status": "closed",
  "created_at": "2025-01-12T10:00:00Z",
  "updated_at": "2025-01-12T11:00:00Z",
  "messages": []
}
```

#### 5. 重新開啟對話
```http
POST /api/conversations/{id}/reopen/
```

**回應格式：**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "john_doe",
  "status": "active",
  "created_at": "2025-01-12T10:00:00Z",
  "updated_at": "2025-01-12T11:30:00Z",
  "messages": []
}
```

#### 6. 獲取對話訊息
```http
GET /api/conversations/{id}/messages/
```

**回應格式：**
```json
[
  {
    "id": 1,
    "sender": "user",
    "content": "Hello, AI!",
    "timestamp": "2025-01-12T10:15:00Z"
  },
  {
    "id": 2,
    "sender": "ai",
    "content": "Hello! How can I help you today?",
    "timestamp": "2025-01-12T10:15:30Z"
  }
]
```

#### 7. 發送訊息
```http
POST /api/conversations/{id}/send_message/
```

**請求內容：**
```json
{
  "message": "What is machine learning?"
}
```

**回應格式：**
```json
{
  "user_message": {
    "id": 3,
    "sender": "user",
    "content": "What is machine learning?",
    "timestamp": "2025-01-12T10:20:00Z"
  },
  "ai_message": {
    "id": 4,
    "sender": "ai",
    "content": "Machine learning is a subset of artificial intelligence...",
    "timestamp": "2025-01-12T10:20:15Z"
  }
}
```

### 聊天設定

#### 1. 獲取用戶設定
```http
GET /api/chat-setting/
```

**回應格式：**
```json
{
  "id": 1,
  "user": 1,
  "ai_model": "gpt-3.5-turbo",
  "temperature": 0.7,
  "max_tokens": 150
}
```

#### 2. 更新用戶設定
```http
PUT /api/chat-setting/{id}/
```

**請求內容：**
```json
{
  "ai_model": "gpt-4",
  "temperature": 0.8,
  "max_tokens": 200
}
```

**回應格式：**
```json
{
  "id": 1,
  "user": 1,
  "ai_model": "gpt-4",
  "temperature": 0.8,
  "max_tokens": 200
}
```

## 管理員 API 端點

### 對話管理（管理員專用）

#### 1. 獲取所有對話（管理員）
```http
GET /api/admin/conversations/
```

**查詢參數：**
- `user`: 按用戶名稱篩選
- `status`: 按狀態篩選（active/closed）
- `search`: 關鍵字搜索

**範例：**
```http
GET /api/admin/conversations/?user=john_doe&status=active&search=machine
```

**回應格式：**
```json
[
  {
    "id": 1,
    "user": 1,
    "user_username": "john_doe",
    "status": "active",
    "created_at": "2025-01-12T10:00:00Z",
    "updated_at": "2025-01-12T10:30:00Z",
    "messages": []
  }
]
```

#### 2. 獲取特定對話（管理員）
```http
GET /api/admin/conversations/{id}/
```

**回應格式：**
```json
{
  "id": 1,
  "user": 1,
  "user_username": "john_doe",
  "status": "active",
  "created_at": "2025-01-12T10:00:00Z",
  "updated_at": "2025-01-12T10:30:00Z",
  "messages": [
    {
      "id": 1,
      "sender": "user",
      "content": "Hello, AI!",
      "timestamp": "2025-01-12T10:15:00Z"
    }
  ]
}
```

#### 3. 管理員關閉對話
```http
POST /api/admin/conversations/{id}/close/
```

#### 4. 管理員重新開啟對話
```http
POST /api/admin/conversations/{id}/reopen/
```

#### 5. 獲取對話統計資訊
```http
GET /api/admin/conversations/{id}/stats/
```

**回應格式：**
```json
{
  "conversation_id": 1,
  "message_count": 10,
  "duration_minutes": 45,
  "user_messages": 5,
  "ai_messages": 5,
  "first_message_time": "2025-01-12T10:15:00Z",
  "last_message_time": "2025-01-12T11:00:00Z"
}
```

### 用戶管理（管理員專用）

#### 1. 獲取所有用戶
```http
GET /api/admin/users/
```

**回應格式：**
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_staff": false,
    "is_active": true,
    "date_joined": "2025-01-10T09:00:00Z",
    "conversation_count": 5,
    "total_messages": 50
  }
]
```

## 錯誤回應格式

### 標準錯誤格式
```json
{
  "detail": "Error message description"
}
```

### 驗證錯誤格式
```json
{
  "field_name": ["This field is required."],
  "another_field": ["Invalid value."]
}
```

## HTTP 狀態碼

- `200 OK`: 請求成功
- `201 Created`: 資源創建成功
- `400 Bad Request`: 請求格式錯誤或驗證失敗
- `401 Unauthorized`: 未授權存取
- `403 Forbidden`: 權限不足
- `404 Not Found`: 資源不存在
- `500 Internal Server Error`: 伺服器內部錯誤

## 使用範例

### JavaScript 範例

```javascript
// 獲取用戶對話列表
async function getConversations() {
    const response = await fetch('/api/conversations/', {
        headers: {
            'Authorization': 'Token ' + userToken,
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
}

// 發送訊息
async function sendMessage(conversationId, message) {
    const response = await fetch(`/api/conversations/${conversationId}/send_message/`, {
        method: 'POST',
        headers: {
            'Authorization': 'Token ' + userToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    });
    return await response.json();
}
```

### Python 範例

```python
import requests

# 設定標頭
headers = {
    'Authorization': 'Token your-token-here',
    'Content-Type': 'application/json'
}

# 獲取對話列表
response = requests.get('http://localhost:8000/api/conversations/', headers=headers)
conversations = response.json()

# 發送訊息
data = {'message': 'Hello, AI!'}
response = requests.post(
    f'http://localhost:8000/api/conversations/{conversation_id}/send_message/',
    headers=headers,
    json=data
)
result = response.json()
```

## 限制與配額

- **請求頻率限制**：每分鐘最多 60 次請求
- **訊息長度限制**：單次訊息最多 4000 個字符
- **對話數量限制**：每位用戶最多同時有 10 個活躍對話
- **檔案上傳**：目前不支援檔案上傳功能

## 版本控制

當前 API 版本：`v1`

API 變更將遵循語義化版本控制，主要變更會提前通知。
