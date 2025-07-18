# 系統架構圖

## 概述

本文件提供系統架構的視覺化表示，幫助開發者和維護人員快速理解系統的整體結構、組件關係和資料流向。

## 整體系統架構

### 高層架構圖

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Frontend Layer                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Chat UI    │  │  Settings   │  │  Dashboard  │  │  Admin Interface    │ │
│  │             │  │  Modal      │  │             │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                  HTTP/HTTPS
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API Gateway                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                         Django REST Framework                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Presentation Layer                            │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌──────────────────────┐   │   │
│  │  │ Conversation  │  │  Chat Setting │  │ Admin Management     │   │   │
│  │  │ ViewSet       │  │  ViewSet      │  │ ViewSet              │   │   │
│  │  └───────────────┘  └───────────────┘  └──────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Business Logic Layer                          │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌──────────────────────┐   │   │
│  │  │ Conversation  │  │  AI Response  │  │ Validation &         │   │   │
│  │  │ Service       │  │  Service      │  │ Permission Service   │   │   │
│  │  └───────────────┘  └───────────────┘  └──────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Data Access Layer                             │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌──────────────────────┐   │   │
│  │  │ Conversation  │  │  Message      │  │ AI Service           │   │   │
│  │  │ Repository    │  │  Repository   │  │ Proxy                │   │   │
│  │  └───────────────┘  └───────────────┘  └──────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                              ┌───────┴───────┐
                              │               │
┌─────────────────────────────▼┐         ┌────▼──────────────────────────┐
│        Database              │         │     External Services         │
│                              │         │                               │
│  ┌─────────────────────────┐ │         │  ┌─────────────────────────┐  │
│  │      PostgreSQL         │ │         │  │      OpenAI API         │  │
│  │                         │ │         │  │                         │  │
│  │ ┌─────────────────────┐ │ │         │  │ ┌─────────────────────┐ │  │
│  │ │    Conversations    │ │ │         │  │ │   GPT-3.5/GPT-4     │ │  │
│  │ │    Messages         │ │ │         │  │ │   Text Generation   │ │  │
│  │ │    Users            │ │ │         │  │ └─────────────────────┘ │  │
│  │ │    ChatSettings     │ │ │         │  └─────────────────────────┘  │
│  │ └─────────────────────┘ │ │         └──────────────────────────────┘
│  └─────────────────────────┘ │
└──────────────────────────────┘
```

## 三層架構詳細圖

### 表現層 (Presentation Layer)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Presentation Layer                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │  User API       │    │  Admin API      │    │  Authentication         │  │
│  │                 │    │                 │    │                         │  │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────────────┐ │  │
│  │ │Conversation │ │    │ │Conversation │ │    │ │ Token Auth          │ │  │
│  │ │ViewSet      │ │    │ │Management   │ │    │ │ Session Auth        │ │  │
│  │ └─────────────┘ │    │ │ViewSet      │ │    │ │ Permission Control  │ │  │
│  │                 │    │ └─────────────┘ │    │ └─────────────────────┘ │  │
│  │ ┌─────────────┐ │    │                 │    └─────────────────────────┘  │
│  │ │ChatSetting  │ │    │ ┌─────────────┐ │                                │
│  │ │ViewSet      │ │    │ │User         │ │                                │
│  │ └─────────────┘ │    │ │Management   │ │                                │
│  │                 │    │ │ViewSet      │ │                                │
│  └─────────────────┘    │ └─────────────┘ │                                │
│                         └─────────────────┘                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Serializers                                 │   │
│  │                                                                     │   │
│  │  ConversationSerializer  │  MessageSerializer  │  ChatSettingSerializer │
│  │  UserMessageSerializer   │  AdminStatsSerializer                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
```

### 業務邏輯層 (Business Logic Layer)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Business Logic Layer                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Core Services                               │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │   │
│  │  │ Conversation    │    │ AI Response     │    │ Validation      │ │   │
│  │  │ Service         │    │ Service         │    │ Service         │ │   │
│  │  │                 │    │                 │    │                 │ │   │
│  │  │ • Create        │    │ • Generate      │    │ • User Auth     │ │   │
│  │  │ • Close         │    │ • Process       │    │ • Permissions   │ │   │
│  │  │ • Reopen        │    │ • Format        │    │ • Input Valid   │ │   │
│  │  │ • Get Messages  │    │ • Error Handle  │    │ • Rate Limit    │ │   │
│  │  └─────────────────┘    │ • Token Manage  │    │ • Security      │ │   │
│  │                         └─────────────────┘    └─────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Business Rules                              │   │
│  │                                                                     │   │
│  │  • User can only access their own conversations                    │   │
│  │  • Admin can access all conversations                              │   │
│  │  • Conversations must have valid status (active/closed)            │   │
│  │  • Messages must belong to existing conversations                  │   │
│  │  • AI responses are generated asynchronously                       │   │
│  │  • Settings are user-specific and validated                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
```

### 資料存取層 (Data Access Layer)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Data Access Layer                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Repositories                                │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │   │
│  │  │ Conversation    │    │ Message         │    │ User            │ │   │
│  │  │ Repository      │    │ Repository      │    │ Repository      │ │   │
│  │  │                 │    │                 │    │                 │ │   │
│  │  │ • CRUD Ops      │    │ • CRUD Ops      │    │ • CRUD Ops      │ │   │
│  │  │ • Filter/Search │    │ • Filter/Search │    │ • Auth Methods  │ │   │
│  │  │ • Status Mgmt   │    │ • Pagination    │    │ • Profile Mgmt  │ │   │
│  │  └─────────────────┘    │ • Ordering      │    └─────────────────┘ │   │
│  │                         └─────────────────┘                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        External Proxies                           │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │   │
│  │  │ AI Service      │    │ Cache Service   │    │ File Storage    │ │   │
│  │  │ Proxy           │    │ Proxy           │    │ Proxy           │ │   │
│  │  │                 │    │                 │    │                 │ │   │
│  │  │ • OpenAI API    │    │ • Redis Cache   │    │ • Static Files  │ │   │
│  │  │ • Response      │    │ • Session Store │    │ • Media Files   │ │   │
│  │  │ • Error Handle  │    │ • Rate Limiting │    │ • Backup Store  │ │   │
│  │  │ • Retry Logic   │    │ • Performance   │    │ • CDN Support   │ │   │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 資料模型關係圖

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Data Model Relationships                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │      User       │                                                        │
│  │─────────────────│                                                        │
│  │ id (PK)         │                                                        │
│  │ username        │                                                        │
│  │ email           │                                                        │
│  │ is_staff        │                                                        │
│  │ date_joined     │                                                        │
│  └─────────────────┘                                                        │
│           │                                                                 │
│           │ 1:N                                                             │
│           ▼                                                                 │
│  ┌─────────────────┐                    ┌─────────────────┐                │
│  │  Conversation   │                    │  ChatSetting    │                │
│  │─────────────────│                    │─────────────────│                │
│  │ id (PK)         │                    │ id (PK)         │                │
│  │ user_id (FK)    │◄─────────────────► │ user_id (FK)    │                │
│  │ status          │         1:1        │ ai_model        │                │
│  │ created_at      │                    │ temperature     │                │
│  │ updated_at      │                    │ max_tokens      │                │
│  └─────────────────┘                    └─────────────────┘                │
│           │                                                                 │
│           │ 1:N                                                             │
│           ▼                                                                 │
│  ┌─────────────────┐                                                        │
│  │     Message     │                                                        │
│  │─────────────────│                                                        │
│  │ id (PK)         │                                                        │
│  │ conversation_id │                                                        │
│  │ sender          │                                                        │
│  │ content         │                                                        │
│  │ timestamp       │                                                        │
│  └─────────────────┘                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## API 路由架構圖

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              API Route Architecture                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        User APIs                                   │   │
│  │                                                                     │   │
│  │  /api/conversations/                                                │   │
│  │  ├── GET     → List user conversations                              │   │
│  │  ├── POST    → Create new conversation                              │   │
│  │  └── /{id}/                                                         │   │
│  │      ├── GET    → Get conversation details                          │   │
│  │      ├── POST   → /close/     → Close conversation                  │   │
│  │      ├── POST   → /reopen/    → Reopen conversation                 │   │
│  │      ├── GET    → /messages/  → Get conversation messages           │   │
│  │      └── POST   → /send_message/ → Send message and get AI response │   │
│  │                                                                     │   │
│  │  /api/chat-setting/                                                 │   │
│  │  ├── GET     → Get user settings                                    │   │
│  │  ├── POST    → Create user settings                                 │   │
│  │  └── PUT     → Update user settings                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Admin APIs                                  │   │
│  │                                                                     │   │
│  │  /api/admin/conversations/                                          │   │
│  │  ├── GET     → List all conversations (with filters)               │   │
│  │  └── /{id}/                                                         │   │
│  │      ├── GET    → Get any conversation details                      │   │
│  │      ├── POST   → /close/    → Admin close conversation             │   │
│  │      ├── POST   → /reopen/   → Admin reopen conversation            │   │
│  │      └── GET    → /stats/    → Get conversation statistics          │   │
│  │                                                                     │   │
│  │  /api/admin/users/                                                  │   │
│  │  ├── GET     → List all users                                       │   │
│  │  └── /{id}/                                                         │   │
│  │      ├── GET    → Get user details                                  │   │
│  │      └── GET    → /conversations/ → Get user conversations          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Web Pages                                   │   │
│  │                                                                     │   │
│  │  /chat/          → Main chat interface                              │   │
│  │  /setting/       → User settings page                               │   │
│  │  /manage/        → Admin management interface                       │   │
│  │  /admin/         → Django admin interface                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 部署架構圖

### 本地開發環境

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Local Development                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐                                                        │
│  │   Developer     │                                                        │
│  │   Machine       │                                                        │
│  │                 │                                                        │
│  │ ┌─────────────┐ │                                                        │
│  │ │   Browser   │ │                                                        │
│  │ └─────────────┘ │                                                        │
│  │        │        │                                                        │
│  │        │ :8000  │                                                        │
│  │        ▼        │                                                        │
│  │ ┌─────────────┐ │                                                        │
│  │ │   Django    │ │                                                        │
│  │ │ Dev Server  │ │                                                        │
│  │ └─────────────┘ │                                                        │
│  │        │        │                                                        │
│  │        ▼        │                                                        │
│  │ ┌─────────────┐ │                                                        │
│  │ │ PostgreSQL  │ │                                                        │
│  │ │  :5432      │ │                                                        │
│  │ └─────────────┘ │                                                        │
│  └─────────────────┘                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 生產環境部署

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Production Environment                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │     Internet    │    │   Load Balancer │    │      CDN/Static Files   │  │
│  │                 │    │                 │    │                         │  │
│  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────────────┐ │  │
│  │ │    Users    │ │───▶│ │    Nginx    │ │───▶│ │    Static Assets    │ │  │
│  │ └─────────────┘ │    │ │    :80/443  │ │    │ │    Media Files      │ │  │
│  └─────────────────┘    │ └─────────────┘ │    │ └─────────────────────┘ │  │
│                         └─────────────────┘    └─────────────────────────┘  │
│                                  │                                          │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Application Server                            │   │
│  │                                                                     │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐ │   │
│  │  │  Gunicorn   │    │  Gunicorn   │    │      Supervisor         │ │   │
│  │  │  Worker 1   │    │  Worker 2   │    │                         │ │   │
│  │  │  :8001      │    │  :8002      │    │ ┌─────────────────────┐ │ │   │
│  │  └─────────────┘    └─────────────┘    │ │  Process Monitor    │ │ │   │
│  │         │                   │          │ │  Log Management     │ │ │   │
│  │         └───────────────────┼──────────│ │  Auto Restart       │ │ │   │
│  │                             │          │ └─────────────────────┘ │ │   │
│  │                             ▼          └─────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                  │                                          │
│                                  ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          Data Layer                                │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │   │
│  │  │   PostgreSQL    │    │      Redis      │    │   File Storage  │ │   │
│  │  │   Database      │    │     Cache       │    │                 │ │   │
│  │  │                 │    │                 │    │ ┌─────────────┐ │ │   │
│  │  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ │   Backups   │ │ │   │
│  │  │ │Primary :5432│ │    │ │    :6379    │ │    │ │   Logs      │ │ │   │
│  │  │ └─────────────┘ │    │ └─────────────┘ │    │ │   Media     │ │ │   │
│  │  └─────────────────┘    └─────────────────┘    │ └─────────────┘ │ │   │
│  │                                                └─────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      External Services                             │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │   │
│  │  │   OpenAI API    │    │   Email Service │    │   Monitoring    │ │   │
│  │  │                 │    │                 │    │                 │ │   │
│  │  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │ │   │
│  │  │ │  GPT Models │ │    │ │   SMTP      │ │    │ │   Logs      │ │ │   │
│  │  │ │  API Keys   │ │    │ │   Sendgrid  │ │    │ │   Metrics   │ │ │   │
│  │  │ └─────────────┘ │    │ └─────────────┘ │    │ │   Alerts    │ │ │   │
│  │  └─────────────────┘    └─────────────────┘    │ └─────────────┘ │ │   │
│  │                                                └─────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Docker 容器化部署

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Docker Deployment                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         Docker Host                                │   │
│  │                                                                     │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │   │
│  │  │     nginx       │    │      web        │    │      db         │ │   │
│  │  │   Container     │    │   Container     │    │   Container     │ │   │
│  │  │                 │    │                 │    │                 │ │   │
│  │  │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │ │   │
│  │  │ │  Nginx      │ │    │ │   Django    │ │    │ │ PostgreSQL  │ │ │   │
│  │  │ │  :80/443    │ │───▶│ │  Gunicorn   │ │───▶│ │   :5432     │ │ │   │
│  │  │ │  Proxy      │ │    │ │   :8000     │ │    │ └─────────────┘ │ │   │
│  │  │ └─────────────┘ │    │ └─────────────┘ │    │                 │ │   │
│  │  └─────────────────┘    └─────────────────┘    │   Volume:       │ │   │
│  │                                  │              │   postgres_data │ │   │
│  │                                  ▼              └─────────────────┘ │   │
│  │  ┌─────────────────┐    ┌─────────────────┐                        │   │
│  │  │     redis       │    │    volumes      │                        │   │
│  │  │   Container     │    │                 │                        │   │
│  │  │                 │    │ ┌─────────────┐ │                        │   │
│  │  │ ┌─────────────┐ │    │ │static_volume│ │                        │   │
│  │  │ │    Redis    │ │    │ │media_volume │ │                        │   │
│  │  │ │    :6379    │ │    │ │log_volume   │ │                        │   │
│  │  │ └─────────────┘ │    │ └─────────────┘ │                        │   │
│  │  └─────────────────┘    └─────────────────┘                        │   │
│  │                                                                     │   │
│  │  ┌─────────────────────────────────────────────────────────────┐   │   │
│  │  │                    Docker Network                          │   │   │
│  │  │                 playms_homework_default                    │   │   │
│  │  └─────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 資料流向圖

### 用戶對話流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              User Conversation Flow                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐                                                            │
│  │    User     │                                                            │
│  │   Browser   │                                                            │
│  └─────────────┘                                                            │
│         │                                                                   │
│         │ 1. POST /api/conversations/{id}/send_message/                     │
│         ▼                                                                   │
│  ┌─────────────┐                                                            │
│  │   Django    │                                                            │
│  │ API Layer   │                                                            │
│  └─────────────┘                                                            │
│         │                                                                   │
│         │ 2. Validate & Authenticate                                        │
│         ▼                                                                   │
│  ┌─────────────┐                                                            │
│  │  Business   │                                                            │
│  │   Logic     │                                                            │
│  │  Service    │                                                            │
│  └─────────────┘                                                            │
│         │                                                                   │
│         │ 3. Save User Message                                              │
│         ▼                                                                   │
│  ┌─────────────┐    4. Call AI API    ┌─────────────┐                      │
│  │  Database   │◄──────────────────────│ AI Service  │                      │
│  │             │                       │   Proxy     │                      │
│  │             │                       └─────────────┘                      │
│  │             │                               │                            │
│  │             │                               │ 5. Generate Response       │
│  │             │                               ▼                            │
│  │             │    6. Save AI Message ┌─────────────┐                      │
│  │             │◄──────────────────────│  OpenAI     │                      │
│  └─────────────┘                       │    API      │                      │
│         │                              └─────────────┘                      │
│         │ 7. Return Both Messages                                           │
│         ▼                                                                   │
│  ┌─────────────┐                                                            │
│  │    User     │                                                            │
│  │   Browser   │                                                            │
│  └─────────────┘                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 管理員監控流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Admin Monitoring Flow                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐                                                            │
│  │   Admin     │                                                            │
│  │   User      │                                                            │
│  └─────────────┘                                                            │
│         │                                                                   │
│         │ 1. GET /api/admin/conversations/?filters                          │
│         ▼                                                                   │
│  ┌─────────────┐                                                            │
│  │   Admin     │                                                            │
│  │ API Layer   │                                                            │
│  └─────────────┘                                                            │
│         │                                                                   │
│         │ 2. Check Admin Permissions                                        │
│         ▼                                                                   │
│  ┌─────────────┐                                                            │
│  │  Admin      │                                                            │
│  │  Service    │                                                            │
│  └─────────────┘                                                            │
│         │                                                                   │
│         │ 3. Query All User Data                                            │
│         ▼                                                                   │
│  ┌─────────────┐                                                            │
│  │  Database   │                                                            │
│  │             │                                                            │
│  │ • Users     │                                                            │
│  │ • Convs     │                                                            │
│  │ • Messages  │                                                            │
│  │ • Stats     │                                                            │
│  └─────────────┘                                                            │
│         │                                                                   │
│         │ 4. Aggregate & Filter Data                                        │
│         ▼                                                                   │
│  ┌─────────────┐                                                            │
│  │   Admin     │                                                            │
│  │ Interface   │                                                            │
│  └─────────────┘                                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 安全架構圖

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Security Architecture                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Input Validation Layer                         │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐ │   │
│  │  │   CSRF      │  │    CORS     │  │         Rate Limiting       │ │   │
│  │  │ Protection  │  │ Protection  │  │                             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   Authentication Layer                             │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐ │   │
│  │  │    Token    │  │   Session   │  │      Password Policies      │ │   │
│  │  │    Auth     │  │    Auth     │  │                             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                   Authorization Layer                              │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐ │   │
│  │  │    User     │  │    Admin    │  │      Object Level           │ │   │
│  │  │ Permissions │  │ Permissions │  │      Permissions            │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Data Protection                               │   │
│  │                                                                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐ │   │
│  │  │ Data Access │  │   Audit     │  │        Encryption           │ │   │
│  │  │   Control   │  │   Logging   │  │                             │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

這些架構圖提供了系統各個層面的視覺化表示，幫助開發者、維護人員和利益相關者快速理解系統的結構、組件關係和資料流向。圖表涵蓋了從高層次的系統架構到具體的部署配置，為系統的開發、部署和維護提供了重要的參考資料。
