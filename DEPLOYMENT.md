# 🚀 Hướng dẫn Deploy Chatbot

Hướng dẫn chi tiết cách deploy Chatbot Quản lý Thời gian lên các nền tảng phổ biến.

---

## 📋 Mục lục

1. [Deploy lên Render.com (Free)](#1-deploy-lên-rendercom-free)
2. [Deploy lên Railway.app (Free)](#2-deploy-lên-railwayapp-free)
3. [Deploy lên Vercel (Free)](#3-deploy-lên-vercel-free)
4. [Deploy lên Heroku](#4-deploy-lên-heroku)
5. [Deploy lên VPS/Server riêng](#5-deploy-lên-vpsserver-riêng)
6. [Deploy với Docker](#6-deploy-với-docker)
7. [Cấu hình Domain tùy chỉnh](#7-cấu-hình-domain-tùy-chỉnh)

---

## 1. Deploy lên Render.com (Free)

**✅ Ưu điểm:**
- Miễn phí hoàn toàn
- Tự động deploy từ GitHub
- Hỗ trợ Python/FastAPI tốt
- SSL certificate miễn phí
- Easy setup

**Bước 1: Chuẩn bị file cấu hình**

Tạo file `render.yaml`:
```yaml
services:
  - type: web
    name: chatbot-edu
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: GEMINI_API_KEY
        sync: false
```

**Bước 2: Push code lên GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/chatbotedu.git
git push -u origin main
```

**Bước 3: Deploy trên Render**
1. Truy cập https://render.com và đăng nhập
2. Click "New" → "Web Service"
3. Connect GitHub repository của bạn
4. Chọn repository `chatbotedu`
5. Cấu hình:
   - **Name**: chatbot-edu
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Thêm Environment Variable:
   - `GEMINI_API_KEY`: [Your API Key]
7. Click "Create Web Service"

**✅ Done!** App sẽ có URL: `https://chatbot-edu.onrender.com`

---

## 2. Deploy lên Railway.app (Free)

**✅ Ưu điểm:**
- $5 credit miễn phí mỗi tháng
- Deploy cực kỳ dễ dàng
- Tự động detect Python app
- CLI mạnh mẽ

**Bước 1: Cài Railway CLI**
```bash
# Windows (với npm)
npm install -g @railway/cli

# Mac
brew install railway

# Linux
curl -fsSL https://railway.app/install.sh | sh
```

**Bước 2: Login và Deploy**
```bash
# Login
railway login

# Khởi tạo project
railway init

# Link với project
railway link

# Add environment variables
railway variables set GEMINI_API_KEY=your_api_key_here

# Deploy
railway up
```

**Hoặc deploy từ GitHub:**
1. Truy cập https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Chọn repository
4. Thêm environment variables
5. Deploy tự động

**✅ Done!** Railway sẽ tự động generate URL

---

## 3. Deploy lên Vercel (Free)

**⚠️ Lưu ý:** Vercel chủ yếu cho serverless, cần chỉnh sửa code một chút

**Bước 1: Tạo file `vercel.json`**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

**Bước 2: Cài Vercel CLI**
```bash
npm install -g vercel
```

**Bước 3: Deploy**
```bash
vercel login
vercel

# Thêm environment variables
vercel env add GEMINI_API_KEY
```

---

## 4. Deploy lên Heroku

**Bước 1: Cài Heroku CLI**
```bash
# Windows
choco install heroku-cli

# Mac
brew install heroku/brew/heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh
```

**Bước 2: Tạo file `Procfile`**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Bước 3: Tạo file `runtime.txt`**
```
python-3.11.0
```

**Bước 4: Deploy**
```bash
# Login
heroku login

# Tạo app
heroku create chatbot-edu-app

# Set environment variables
heroku config:set GEMINI_API_KEY=your_api_key

# Push code
git push heroku main

# Mở app
heroku open
```

---

## 5. Deploy lên VPS/Server riêng

**Yêu cầu:**
- VPS Ubuntu 20.04+ (DigitalOcean, Linode, AWS EC2, etc.)
- Domain name (tùy chọn)

**Bước 1: SSH vào server**
```bash
ssh root@your_server_ip
```

**Bước 2: Cài đặt dependencies**
```bash
# Update system
apt update && apt upgrade -y

# Install Python
apt install python3 python3-pip python3-venv nginx -y

# Install supervisor
apt install supervisor -y
```

**Bước 3: Upload code**
```bash
# Clone từ GitHub
cd /var/www
git clone https://github.com/yourusername/chatbotedu.git
cd chatbotedu

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Bước 4: Cấu hình environment**
```bash
nano .env
# Thêm GEMINI_API_KEY=your_key
```

**Bước 5: Cấu hình Supervisor**
```bash
nano /etc/supervisor/conf.d/chatbot.conf
```

Nội dung:
```ini
[program:chatbot]
directory=/var/www/chatbotedu
command=/var/www/chatbotedu/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
stderr_logfile=/var/log/chatbot.err.log
stdout_logfile=/var/log/chatbot.out.log
user=www-data
```

**Bước 6: Cấu hình Nginx**
```bash
nano /etc/nginx/sites-available/chatbot
```

Nội dung:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/chatbotedu/static;
    }
}
```

**Bước 7: Enable và khởi động**
```bash
# Link config
ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/

# Test nginx config
nginx -t

# Restart services
supervisorctl reread
supervisorctl update
supervisorctl start chatbot
systemctl restart nginx
```

**Bước 8: Setup SSL với Let's Encrypt**
```bash
# Install certbot
apt install certbot python3-certbot-nginx -y

# Get certificate
certbot --nginx -d your_domain.com

# Auto-renewal
certbot renew --dry-run
```

**✅ Done!** Truy cập `https://your_domain.com`

---

## 6. Deploy với Docker

**Bước 1: Tạo `Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Bước 2: Tạo `docker-compose.yml`**
```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./chatbot.db:/app/chatbot.db
    restart: unless-stopped
```

**Bước 3: Tạo `.dockerignore`**
```
__pycache__
*.pyc
*.pyo
*.db
.env
.git
.gitignore
venv/
```

**Bước 4: Build và Run**
```bash
# Build image
docker build -t chatbot-edu .

# Run container
docker run -d -p 8000:8000 -e GEMINI_API_KEY=your_key chatbot-edu

# Hoặc dùng docker-compose
docker-compose up -d
```

**Deploy lên Docker Hub:**
```bash
# Tag image
docker tag chatbot-edu yourusername/chatbot-edu:latest

# Push
docker push yourusername/chatbot-edu:latest

# Pull và run trên server khác
docker pull yourusername/chatbot-edu:latest
docker run -d -p 8000:8000 yourusername/chatbot-edu:latest
```

---

## 7. Cấu hình Domain tùy chỉnh

### Với Render/Railway/Vercel:
1. Vào Settings → Custom Domain
2. Thêm domain của bạn (ví dụ: `chatbot.yourdomain.com`)
3. Cập nhật DNS records:
   ```
   Type: CNAME
   Name: chatbot
   Value: [platform-provided-url]
   ```

### Với VPS:
1. Point A record đến IP server:
   ```
   Type: A
   Name: @
   Value: your_server_ip
   ```
2. Cấu hình Nginx như bước 6
3. Setup SSL với certbot

---

## 🔒 Security Checklist

- [ ] Không commit file `.env` lên Git
- [ ] Sử dụng environment variables cho secrets
- [ ] Enable HTTPS/SSL
- [ ] Giới hạn rate limiting
- [ ] Setup firewall trên VPS
- [ ] Regular backup database
- [ ] Update dependencies thường xuyên
- [ ] Monitor logs và errors

---

## 📊 Monitoring & Logs

### Render:
- Xem logs trong dashboard
- Setup log streaming

### Railway:
```bash
railway logs
```

### VPS:
```bash
# View supervisor logs
tail -f /var/log/chatbot.out.log
tail -f /var/log/chatbot.err.log

# View nginx logs
tail -f /var/nginx/access.log
tail -f /var/nginx/error.log
```

### Docker:
```bash
docker logs -f container_name
```

---

## 💰 So sánh Chi phí

| Platform | Free Tier | Paid Plan | Phù hợp cho |
|----------|-----------|-----------|-------------|
| **Render** | ✅ 750h/month | $7/month | Học tập, demo |
| **Railway** | ✅ $5 credit/month | $5/month usage | MVP, prototype |
| **Vercel** | ✅ Unlimited | $20/month | Serverless apps |
| **Heroku** | ❌ (đã ngừng) | $7/month | N/A |
| **VPS** | ❌ | $5-50/month | Production |
| **Docker** | Depends on hosting | Varies | Flexible |

---

## 🎯 Khuyến nghị

### Cho học tập/demo:
→ **Render.com** hoặc **Railway.app** (Free tier)

### Cho MVP/Startup:
→ **Railway** hoặc **VPS** nhỏ ($5/month)

### Cho Production:
→ **VPS** với Docker hoặc **AWS/GCP**

---

## 🆘 Troubleshooting

### Lỗi "Failed building wheel for pydantic-core" trên Render:
**Nguyên nhân:** Pydantic version cũ yêu cầu build từ Rust source code, Render thiếu maturin/Rust compiler.

**Giải pháp:**
1. Upgrade pydantic lên phiên bản có pre-built wheels:
   ```txt
   pydantic==2.6.4
   pydantic-settings==2.2.1
   ```

2. Cập nhật `render.yaml` với build command tối ưu:
   ```yaml
   buildCommand: pip install --upgrade pip && pip install --only-binary :all: --no-build-isolation -r requirements.txt || pip install -r requirements.txt
   envVars:
     - key: PIP_NO_CACHE_DIR
       value: "1"
     - key: PIP_PREFER_BINARY
       value: "1"
   ```

3. Upgrade Python version trong `runtime.txt`:
   ```
   python-3.11.9
   ```

### Lỗi "Application Error" trên Render:
```bash
# Check logs trong dashboard
# Thường do thiếu environment variables hoặc lỗi dependencies
```

### Database không lưu trên Railway:
```bash
# Mount volume persistent
railway volume create
```

### Port đã được sử dụng:
```bash
# Kill process
lsof -ti:8000 | xargs kill -9

# Hoặc đổi port
uvicorn main:app --port 8001
```

---

## 📚 Resources

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Docker Docs](https://docs.docker.com)
- [Nginx Docs](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org)

---

## ✅ Quick Start - Khuyến nghị

**Cách nhanh nhất (5 phút):**

1. Push code lên GitHub
2. Đăng ký Render.com
3. New Web Service → Connect GitHub
4. Thêm GEMINI_API_KEY
5. Deploy!

```bash
# Hoặc dùng Railway CLI
railway login
railway init
railway up
```

---

**🎉 Chúc bạn deploy thành công!**

Nếu gặp vấn đề, hãy check logs và đọc documentation của platform bạn chọn.