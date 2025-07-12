# 部署說明

## 概述

本文件提供完整的系統部署指南，包含本地開發環境設置、生產環境部署和容器化部署等多種部署方式。

## 系統需求

### 硬體需求
- **記憶體**：最少 2GB RAM（建議 4GB+）
- **儲存空間**：最少 10GB 可用空間
- **處理器**：x64 架構，雙核心以上

### 軟體需求
- **作業系統**：Ubuntu 20.04+, CentOS 8+, macOS 10.15+, Windows 10+
- **Python**：3.9+
- **PostgreSQL**：13+
- **Redis**：6+（選用）
- **Node.js**：16+（用於前端資源編譯）

## 本地開發環境部署

### 1. 環境準備

#### 安裝 Python 和虛擬環境
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-dev

# CentOS/RHEL
sudo dnf install python39 python39-devel

# macOS (使用 Homebrew)
brew install python@3.9

# Windows
# 從 python.org 下載並安裝 Python 3.9+
```

#### 創建虛擬環境
```bash
python3.9 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

### 2. 資料庫設置

#### 安裝 PostgreSQL
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo dnf install postgresql postgresql-server postgresql-contrib

# macOS
brew install postgresql

# Windows
# 從 postgresql.org 下載並安裝
```

#### 創建資料庫
```bash
# 切換到 postgres 用戶
sudo -u postgres psql

# 在 PostgreSQL 命令列中執行
CREATE DATABASE playms_homework;
CREATE USER playms_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE playms_homework TO playms_user;
\q
```

### 3. 專案設置

#### 複製專案
```bash
git clone <repository-url>
cd playms_homework
```

#### 安裝 Python 依賴
```bash
pip install -r requirements/local.txt
```

#### 環境變數設置
創建 `.env` 檔案：
```bash
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://playms_user:your_password@localhost:5432/playms_homework
REDIS_URL=redis://localhost:6379/0

# AI 服務設定
OPENAI_API_KEY=your-openai-api-key
AI_MODEL=gpt-3.5-turbo
```

#### 資料庫遷移
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 創建超級用戶
```bash
python manage.py createsuperuser
```

#### 收集靜態檔案
```bash
python manage.py collectstatic
```

### 4. 啟動服務

#### 啟動 Django 開發伺服器
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 啟動 Redis（如果使用）
```bash
redis-server
```

### 5. 驗證部署
訪問 `http://localhost:8000` 確認系統正常運行。

## 生產環境部署

### 1. 伺服器準備

#### 系統更新
```bash
sudo apt update && sudo apt upgrade -y
```

#### 安裝必要軟體
```bash
sudo apt install -y python3.9 python3.9-venv python3.9-dev \
    postgresql postgresql-contrib redis-server \
    nginx supervisor git curl
```

### 2. 專案部署

#### 創建部署用戶
```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
su - deploy
```

#### 部署專案
```bash
cd /var/www
sudo mkdir playms_homework
sudo chown deploy:deploy playms_homework
git clone <repository-url> playms_homework
cd playms_homework
```

#### 設置虛擬環境
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements/production.txt
```

#### 生產環境設定
```bash
# /var/www/playms_homework/.env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://playms_user:secure_password@localhost:5432/playms_homework
REDIS_URL=redis://localhost:6379/0

# Security settings
SECURE_SSL_REDIRECT=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
```

#### 資料庫設置
```bash
sudo -u postgres createdb playms_homework
sudo -u postgres createuser playms_user
sudo -u postgres psql -c "ALTER USER playms_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE playms_homework TO playms_user;"

# 執行遷移
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3. Web 伺服器設置

#### Nginx 設定
```nginx
# /etc/nginx/sites-available/playms_homework
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 4G;

    access_log /var/log/nginx/playms_homework.access.log;
    error_log /var/log/nginx/playms_homework.error.log;

    location /static/ {
        alias /var/www/playms_homework/staticfiles/;
    }

    location /media/ {
        alias /var/www/playms_homework/media/;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

#### 啟用網站
```bash
sudo ln -s /etc/nginx/sites-available/playms_homework /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. 應用伺服器設置

#### Gunicorn 設定
```bash
# /var/www/playms_homework/gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 2
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
```

#### Supervisor 設定
```ini
# /etc/supervisor/conf.d/playms_homework.conf
[program:playms_homework]
command=/var/www/playms_homework/venv/bin/gunicorn config.wsgi:application -c /var/www/playms_homework/gunicorn.conf.py
directory=/var/www/playms_homework
user=deploy
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/playms_homework.log
```

#### 啟動服務
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start playms_homework
sudo supervisorctl status
```

### 5. SSL 憑證設置

#### 使用 Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### 自動續約
```bash
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

## Docker 容器化部署

### 1. Docker 設置

#### 安裝 Docker
```bash
# Ubuntu
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# 安裝 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Docker 檔案

#### Dockerfile
```dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安裝系統依賴
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 依賴
COPY requirements/production.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案檔案
COPY . /app/

# 收集靜態檔案
RUN python manage.py collectstatic --noinput

# 建立非 root 用戶
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: playms_homework
      POSTGRES_USER: playms_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DEBUG=False
      - DATABASE_URL=postgres://playms_user:secure_password@db:5432/playms_homework
      - REDIS_URL=redis://redis:6379/0

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

### 3. 部署執行

#### 建構和啟動
```bash
docker-compose build
docker-compose up -d
```

#### 資料庫遷移
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

#### 檢查狀態
```bash
docker-compose ps
docker-compose logs web
```

## 監控與維護

### 1. 日誌管理

#### 設定日誌輪替
```bash
# /etc/logrotate.d/playms_homework
/var/log/supervisor/playms_homework.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 deploy deploy
    postrotate
        supervisorctl restart playms_homework
    endscript
}
```

### 2. 備份策略

#### 資料庫備份腳本
```bash
#!/bin/bash
# /usr/local/bin/backup_db.sh

BACKUP_DIR="/var/backups/playms_homework"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

pg_dump -h localhost -U playms_user playms_homework > $BACKUP_FILE

# 壓縮備份檔案
gzip $BACKUP_FILE

# 刪除 30 天前的備份
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

echo "Database backup completed: $BACKUP_FILE.gz"
```

#### 自動備份
```bash
sudo crontab -e
# 每日凌晨 2 點備份
0 2 * * * /usr/local/bin/backup_db.sh
```

### 3. 效能監控

#### 系統監控
```bash
# 安裝監控工具
sudo apt install htop iotop nethogs

# 檢查系統資源
htop
iotop
nethogs
```

#### 應用程式監控
```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/playms_homework/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 故障排除

### 常見問題

#### 1. 資料庫連線問題
```bash
# 檢查 PostgreSQL 狀態
sudo systemctl status postgresql

# 檢查連線設定
sudo -u postgres psql -c "\l"

# 重啟資料庫
sudo systemctl restart postgresql
```

#### 2. 靜態檔案載入問題
```bash
# 重新收集靜態檔案
python manage.py collectstatic --clear --noinput

# 檢查 Nginx 設定
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. 記憶體不足
```bash
# 檢查記憶體使用
free -h
ps aux --sort=-%mem | head

# 重啟應用服務
sudo supervisorctl restart playms_homework
```

### 4. 權限問題
```bash
# 修正檔案權限
sudo chown -R deploy:deploy /var/www/playms_homework
sudo chmod -R 755 /var/www/playms_homework
```

## 更新部署

### 1. 程式碼更新
```bash
cd /var/www/playms_homework
git pull origin main
source venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart playms_homework
```

### 2. 零停機部署
```bash
# 使用藍綠部署策略
./scripts/deploy.sh
```

## 安全建議

### 1. 伺服器加固
- 定期更新系統套件
- 設定防火牆規則
- 停用不必要的服務
- 使用強密碼和 SSH 金鑰

### 2. 應用安全
- 定期更新 Django 和依賴套件
- 設定適當的 CORS 政策
- 啟用 HTTPS
- 實施速率限制

### 3. 資料安全
- 定期備份資料庫
- 加密敏感資料
- 設定存取控制
- 監控異常活動

這份部署說明提供了完整的部署流程，從本地開發到生產環境的各種部署方式，確保系統能夠穩定運行。
