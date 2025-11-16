# Hướng dẫn cấu hình Gemini AI

## Tổng quan

Chatbot sử dụng Google Gemini Pro API để cung cấp khả năng chat thông minh, hiểu ngôn ngữ tự nhiên và tư vấn cá nhân hóa.

## Lấy API Key

### Bước 1: Truy cập Google AI Studio

Mở trình duyệt và truy cập: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

### Bước 2: Đăng nhập

Đăng nhập bằng tài khoản Google của bạn.

### Bước 3: Tạo API Key

1. Click vào nút "**Create API Key**"
2. Chọn project (hoặc tạo project mới)
3. API key sẽ được tạo và hiển thị

### Bước 4: Copy API Key

Copy toàn bộ API key (dạng: `AIzaSy...`)

## Cấu hình trong dự án

### Cách 1: Sử dụng file .env (Khuyến nghị)

1. Tạo file `.env` trong thư mục gốc của dự án:
   ```bash
   cp .env.example .env
   ```

2. Mở file `.env` và thêm API key:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

3. Lưu file

### Cách 2: Sử dụng biến môi trường hệ thống

**Linux/Mac:**
```bash
export GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

## Kiểm tra cấu hình

### Kiểm tra trong code

Chạy server và xem log khi khởi động:

```bash
python main.py
```

Nếu thành công, bạn sẽ thấy:
```
✅ Database initialized successfully
🤖 Gemini AI: ENABLED
🚀 Chatbot server is running!
```

Nếu không có API key:
```
✅ Database initialized successfully
⚠️  Gemini AI: DISABLED (No API key found)
   Set GEMINI_API_KEY in .env to enable AI features
🚀 Chatbot server is running!
```

### Kiểm tra qua API

Truy cập: http://localhost:8000/api/health

Response sẽ có:
```json
{
  "status": "healthy",
  "service": "Chatbot Quản lý Thời gian",
  "version": "2.0.0",
  "gemini_enabled": true
}
```

## Tính năng khi có Gemini AI

### 1. Chat tự nhiên

**Không có Gemini:**
- User: "Tôi stress quá"
- Bot: "Xin lỗi, tôi chưa hiểu yêu cầu của bạn..."

**Có Gemini:**
- User: "Tôi stress quá"
- Bot: "Mình hiểu bạn đang cảm thấy áp lực. Hãy thử nghỉ ngơi 15-20 phút, đi dạo hoặc nghe nhạc thư giãn. Stress kéo dài sẽ ảnh hưởng đến hiệu quả học tập. Bạn có muốn mình phân tích lịch học để tìm thời gian nghỉ ngơi hợp lý không? 😊"

### 2. Tư vấn cá nhân hóa

Gemini phân tích:
- Lịch học hiện tại của bạn
- Lịch thi sắp tới
- Thói quen học tập (nếu có data)

Và đưa ra lời khuyên phù hợp với từng người.

### 3. Trả lời câu hỏi đa dạng

Bạn có thể hỏi về:
- Phương pháp học tập
- Quản lý thời gian
- Cách ôn thi hiệu quả
- Cân bằng giữa học và nghỉ
- Động lực học tập
- ...và nhiều hơn nữa!

## Giới hạn Free Tier

**Gemini API Free Tier:**
- 60 requests/phút
- 1,500 requests/ngày
- Hoàn toàn miễn phí!

Đối với chatbot cá nhân, giới hạn này quá đủ.

## Bảo mật API Key

### ⚠️ QUAN TRỌNG

**KHÔNG BAO GIỜ:**
- Commit API key vào Git
- Chia sẻ API key công khai
- Để API key trong source code

**NÊN:**
- Lưu trong file `.env` (đã có trong `.gitignore`)
- Sử dụng biến môi trường
- Giữ bí mật API key

### File .gitignore

Đảm bảo file `.gitignore` có dòng:
```
.env
.env.local
```

## Xử lý sự cố

### Lỗi: "GEMINI_API_KEY not found"

**Nguyên nhân:** Không tìm thấy API key

**Giải pháp:**
1. Kiểm tra file `.env` đã tồn tại chưa
2. Đảm bảo file `.env` có dòng `GEMINI_API_KEY=...`
3. Restart server sau khi thêm API key

### Lỗi: "API key not valid"

**Nguyên nhân:** API key sai hoặc đã bị thu hồi

**Giải pháp:**
1. Kiểm tra lại API key có đúng không
2. Tạo API key mới từ Google AI Studio
3. Đảm bảo không có khoảng trắng thừa

### Lỗi: "Quota exceeded"

**Nguyên nhân:** Vượt quá giới hạn free tier

**Giải pháp:**
1. Đợi reset (sau 1 phút hoặc 1 ngày)
2. Tạo project mới và API key mới
3. Chatbot vẫn hoạt động với pattern matching khi Gemini fail

### Chatbot không dùng Gemini

**Kiểm tra:**
1. API key đã được set chưa?
2. Server có log "Gemini AI: ENABLED" không?
3. Thử chat với câu không có trong pattern (VD: "Tôi buồn quá")

## Test Gemini Integration

### Test 1: Câu hỏi đơn giản

```
User: "Xin chào"
Bot: Sẽ trả lời bằng pattern matching (cố định)
```

### Test 2: Câu hỏi tự nhiên

```
User: "Làm sao để học tốt hơn?"
Bot: Gemini sẽ trả lời với lời khuyên chi tiết, cá nhân hóa
```

### Test 3: Câu hỏi có context

```
User: "Thêm lịch học Toán vào thứ 2, 8h-10h"
Bot: Thêm thành công

User: "Tôi nên ôn Toán khi nào?"
Bot: Gemini phân tích lịch và gợi ý thời gian ôn tập phù hợp
```

## Nâng cấp lên Paid Plan (Tùy chọn)

Nếu cần nhiều requests hơn, bạn có thể:
1. Truy cập Google Cloud Console
2. Enable billing
3. Chọn paid plan

Nhưng với chatbot cá nhân, free tier là quá đủ!

## Tài liệu tham khảo

- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/)
- [Pricing Information](https://ai.google.dev/pricing)

## Liên hệ hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. README.md
2. USAGE.md
3. GitHub Issues của dự án

---

**Chúc bạn sử dụng Gemini AI hiệu quả! 🚀**
