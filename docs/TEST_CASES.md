# 測試用例文件

## 概述

本文件包含系統主要業務邏輯的測試用例，涵蓋用戶對話管理、AI 互動、權限控制等核心功能。

## 測試架構

### 測試分類
- **單元測試**：測試個別模組和函數
- **整合測試**：測試模組間的交互
- **API 測試**：測試 REST API 端點
- **權限測試**：測試存取控制

### 測試工具
- **Django TestCase**：Django 內建測試框架
- **DRF APITestCase**：REST Framework 測試工具
- **Mock**：模擬外部服務
- **Factory Boy**：測試資料生成

## 單元測試

### 1. 對話模型測試

#### 測試目標
驗證 Conversation 模型的基本功能和業務規則。

#### 測試用例

```python
class ConversationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_conversation_creation(self):
        """測試對話創建"""
        conversation = Conversation.objects.create(
            user=self.user,
            status='active'
        )
        self.assertEqual(conversation.user, self.user)
        self.assertEqual(conversation.status, 'active')
        self.assertIsNotNone(conversation.created_at)
        self.assertIsNotNone(conversation.updated_at)
    
    def test_conversation_status_change(self):
        """測試對話狀態變更"""
        conversation = Conversation.objects.create(
            user=self.user,
            status='active'
        )
        
        # 測試關閉對話
        conversation.status = 'closed'
        conversation.save()
        self.assertEqual(conversation.status, 'closed')
        
        # 測試重新開啟對話
        conversation.status = 'active'
        conversation.save()
        self.assertEqual(conversation.status, 'active')
    
    def test_conversation_user_relationship(self):
        """測試對話與用戶的關聯"""
        conversation = Conversation.objects.create(
            user=self.user,
            status='active'
        )
        
        # 測試正向查詢
        self.assertEqual(conversation.user.username, 'testuser')
        
        # 測試反向查詢
        user_conversations = self.user.conversations.all()
        self.assertIn(conversation, user_conversations)
```

### 2. 訊息模型測試

#### 測試用例

```python
class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.conversation = Conversation.objects.create(
            user=self.user,
            status='active'
        )
    
    def test_message_creation(self):
        """測試訊息創建"""
        message = Message.objects.create(
            conversation=self.conversation,
            sender='user',
            content='Hello, AI!'
        )
        
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.sender, 'user')
        self.assertEqual(message.content, 'Hello, AI!')
        self.assertIsNotNone(message.timestamp)
    
    def test_message_conversation_relationship(self):
        """測試訊息與對話的關聯"""
        user_message = Message.objects.create(
            conversation=self.conversation,
            sender='user',
            content='Hello'
        )
        
        ai_message = Message.objects.create(
            conversation=self.conversation,
            sender='ai',
            content='Hi there!'
        )
        
        # 測試對話包含正確的訊息
        messages = self.conversation.messages.all()
        self.assertEqual(messages.count(), 2)
        self.assertIn(user_message, messages)
        self.assertIn(ai_message, messages)
    
    def test_message_ordering(self):
        """測試訊息排序"""
        message1 = Message.objects.create(
            conversation=self.conversation,
            sender='user',
            content='First message'
        )
        
        message2 = Message.objects.create(
            conversation=self.conversation,
            sender='ai',
            content='Second message'
        )
        
        messages = Message.objects.filter(
            conversation=self.conversation
        ).order_by('timestamp')
        
        self.assertEqual(list(messages), [message1, message2])
```

### 3. 業務邏輯服務測試

#### 測試用例

```python
class ConversationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.service = ConversationService()
    
    def test_create_conversation(self):
        """測試創建對話服務"""
        conversation = self.service.create_conversation(self.user.id)
        
        self.assertIsNotNone(conversation)
        self.assertEqual(conversation.user, self.user)
        self.assertEqual(conversation.status, 'active')
    
    def test_close_conversation(self):
        """測試關閉對話服務"""
        conversation = self.service.create_conversation(self.user.id)
        conversation_id = conversation.id
        
        closed_conversation = self.service.close_conversation(conversation_id)
        
        self.assertIsNotNone(closed_conversation)
        self.assertEqual(closed_conversation.status, 'closed')
    
    def test_reopen_conversation(self):
        """測試重新開啟對話服務"""
        conversation = self.service.create_conversation(self.user.id)
        self.service.close_conversation(conversation.id)
        
        reopened_conversation = self.service.reopen_conversation(conversation.id)
        
        self.assertIsNotNone(reopened_conversation)
        self.assertEqual(reopened_conversation.status, 'active')
    
    @patch('conversations.proxies.ai_proxy.AIProxy.generate_response')
    def test_generate_ai_response(self, mock_ai_response):
        """測試 AI 回應生成服務"""
        mock_ai_response.return_value = "Hello! How can I help you?"
        
        conversation = self.service.create_conversation(self.user.id)
        user_message = "Hello, AI!"
        
        ai_message = self.service.generate_ai_response(
            user_id=self.user.id,
            conversation_id=conversation.id,
            user_message=user_message
        )
        
        self.assertIsNotNone(ai_message)
        self.assertEqual(ai_message.sender, 'ai')
        self.assertEqual(ai_message.content, "Hello! How can I help you?")
        
        # 驗證用戶訊息也被保存
        messages = Message.objects.filter(conversation=conversation)
        self.assertEqual(messages.count(), 2)
        
        user_msg = messages.filter(sender='user').first()
        self.assertEqual(user_msg.content, user_message)
```

## API 測試

### 1. 對話 API 測試

#### 測試用例

```python
class ConversationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_list_conversations(self):
        """測試獲取對話列表 API"""
        # 創建測試對話
        Conversation.objects.create(user=self.user, status='active')
        Conversation.objects.create(user=self.user, status='closed')
        
        url = '/api/conversations/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_create_conversation(self):
        """測試創建對話 API"""
        url = '/api/conversations/'
        response = self.client.post(url, {})
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['status'], 'active')
    
    def test_close_conversation(self):
        """測試關閉對話 API"""
        conversation = Conversation.objects.create(
            user=self.user, 
            status='active'
        )
        
        url = f'/api/conversations/{conversation.id}/close/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'closed')
    
    def test_send_message(self):
        """測試發送訊息 API"""
        conversation = Conversation.objects.create(
            user=self.user, 
            status='active'
        )
        
        url = f'/api/conversations/{conversation.id}/send_message/'
        data = {'message': 'Hello, AI!'}
        
        with patch('conversations.proxies.ai_proxy.AIProxy.generate_response') as mock_ai:
            mock_ai.return_value = "Hello! How can I help you?"
            response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_message', response.data)
        self.assertIn('ai_message', response.data)
    
    def test_unauthorized_access(self):
        """測試未授權存取"""
        self.client.credentials()  # 清除認證
        
        url = '/api/conversations/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 401)
```

### 2. 管理員 API 測試

#### 測試用例

```python
class AdminAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.user_token = Token.objects.create(user=self.regular_user)
    
    def test_admin_list_all_conversations(self):
        """測試管理員獲取所有對話"""
        # 創建不同用戶的對話
        Conversation.objects.create(user=self.admin_user, status='active')
        Conversation.objects.create(user=self.regular_user, status='active')
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        
        url = '/api/admin/conversations/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    def test_regular_user_cannot_access_admin_api(self):
        """測試一般用戶無法存取管理員 API"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        
        url = '/api/admin/conversations/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 403)
    
    def test_admin_filter_conversations_by_user(self):
        """測試管理員按用戶篩選對話"""
        Conversation.objects.create(user=self.admin_user, status='active')
        Conversation.objects.create(user=self.regular_user, status='active')
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        
        url = '/api/admin/conversations/?user=user'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user_username'], 'user')
```

## 整合測試

### 1. 完整對話流程測試

#### 測試用例

```python
class ConversationFlowTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_complete_conversation_flow(self):
        """測試完整對話流程"""
        # 1. 創建對話
        response = self.client.post('/api/conversations/', {})
        self.assertEqual(response.status_code, 201)
        conversation_id = response.data['id']
        
        # 2. 發送訊息
        with patch('conversations.proxies.ai_proxy.AIProxy.generate_response') as mock_ai:
            mock_ai.return_value = "Hello! How can I help you?"
            
            message_data = {'message': 'Hello, AI!'}
            response = self.client.post(
                f'/api/conversations/{conversation_id}/send_message/',
                message_data,
                format='json'
            )
            
            self.assertEqual(response.status_code, 200)
        
        # 3. 獲取對話訊息
        response = self.client.get(f'/api/conversations/{conversation_id}/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # 用戶訊息 + AI 回應
        
        # 4. 關閉對話
        response = self.client.post(f'/api/conversations/{conversation_id}/close/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'closed')
        
        # 5. 重新開啟對話
        response = self.client.post(f'/api/conversations/{conversation_id}/reopen/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'active')
```

## 效能測試

### 1. 負載測試

#### 測試用例

```python
class PerformanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_multiple_conversations_performance(self):
        """測試多對話負載效能"""
        import time
        
        start_time = time.time()
        
        # 創建多個對話
        conversation_ids = []
        for i in range(10):
            response = self.client.post('/api/conversations/', {})
            conversation_ids.append(response.data['id'])
        
        # 獲取對話列表
        response = self.client.get('/api/conversations/')
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)
        self.assertLess(execution_time, 5.0)  # 應在 5 秒內完成
    
    def test_message_pagination_performance(self):
        """測試訊息分頁效能"""
        conversation = Conversation.objects.create(
            user=self.user,
            status='active'
        )
        
        # 創建大量訊息
        for i in range(100):
            Message.objects.create(
                conversation=conversation,
                sender='user' if i % 2 == 0 else 'ai',
                content=f'Message {i}'
            )
        
        import time
        start_time = time.time()
        
        response = self.client.get(f'/api/conversations/{conversation.id}/messages/')
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(execution_time, 2.0)  # 應在 2 秒內完成
```

## 測試執行指南

### 執行所有測試
```bash
python manage.py test
```

### 執行特定應用程式測試
```bash
python manage.py test conversations
```

### 執行特定測試類別
```bash
python manage.py test conversations.tests.ConversationModelTest
```

### 執行特定測試方法
```bash
python manage.py test conversations.tests.ConversationModelTest.test_conversation_creation
```

### 生成測試覆蓋率報告
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # 生成 HTML 報告
```

## 測試資料管理

### 測試資料庫設定
```python
# settings/test.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
```

### 測試資料工廠
```python
# factories.py
import factory
from django.contrib.auth import get_user_model
from conversations.models import Conversation, Message

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

class ConversationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Conversation
    
    user = factory.SubFactory(UserFactory)
    status = 'active'

class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message
    
    conversation = factory.SubFactory(ConversationFactory)
    sender = 'user'
    content = factory.Faker('text', max_nb_chars=200)
```

## 持續整合

### GitHub Actions 設定
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements/test.txt
    
    - name: Run tests
      run: |
        python manage.py test
    
    - name: Generate coverage report
      run: |
        coverage run --source='.' manage.py test
        coverage xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
```

## 測試最佳實踐

### 1. 測試隔離
- 每個測試都應該獨立運行
- 使用 setUp 和 tearDown 方法管理測試狀態
- 避免測試間的相依性

### 2. 模擬外部服務
- 使用 Mock 模擬 AI 服務回應
- 避免在測試中呼叫真實的外部 API
- 確保測試的可重複性

### 3. 測試覆蓋率
- 目標達到 90% 以上的程式碼覆蓋率
- 重點測試核心業務邏輯
- 包含正常和異常情況的測試

### 4. 效能監控
- 設定合理的執行時間限制
- 監控資料庫查詢次數
- 測試大量資料情況下的效能表現
