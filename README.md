# Chatbot Quản lý Thời gian Học tập

Chatbot AI với **Google Gemini** hỗ trợ sinh viên quản lý thời gian học tập hiệu quả.

## Tính năng

- 📚 **Quản lý lịch học**: Theo dõi lịch học theo tuần, tháng
- 📝 **Quản lý lịch thi**: Nhắc nhở và chuẩn bị cho các kỳ thi
- ⏰ **Tư vấn thời gian học**: Gợi ý thời gian học tập hiệu quả
- 🍽️ **Dự đoán thời gian nghỉ ngơi**: Tự động đề xuất thời gian nghỉ ngơi và ăn uống
- 🤖 **Gemini AI**: Chat tự nhiên với Gemini AI thông minh
- 💬 **Hiểu ngôn ngữ tự nhiên**: Tương tác linh hoạt, không cần câu lệnh cứng nhắc

## Cài đặt

### 1. Cài đặt dependencies

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình Gemini API (Bắt buộc cho AI features)

1. Lấy API key từ [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Tạo file `.env` từ `.env.example`:
   ```bash
   cp .env.example .env
   ```
3. Thêm API key vào file `.env`:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

> **Lưu ý**: Nếu không có API key, chatbot vẫn hoạt động nhưng sẽ sử dụng pattern matching thay vì AI thông minh.

## Chạy ứng dụng

### Cách 1: Sử dụng script tự động

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

### Cách 2: Chạy thủ công

```bash
python main.py
```

Mở trình duyệt tại: http://localhost:8000

## API Documentation

Swagger UI: http://localhost:8000/docs

## Cấu trúc dự án

```
chatbotedu/
├── main.py                 # FastAPI entry point
├── app/
│   ├── models.py          # Database models
│   ├── database.py        # Database setup
│   ├── chatbot.py         # Legacy chatbot (pattern matching)
│   ├── chatbot_v2.py      # Enhanced chatbot with Gemini
│   ├── gemini_ai.py       # Gemini AI integration
│   └── ai_engine.py       # AI recommendation algorithms
├── static/                # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md
```

## Sử dụng

1. Mở chat interface
2. Nhập lịch học và lịch thi của bạn
3. Chatbot sẽ tự động:
   - Phân tích lịch trình
   - Đề xuất thời gian học hiệu quả
   - Nhắc nhở trước kỳ thi
   - Gợi ý thời gian nghỉ ngơi và ăn uống

## Ví dụ câu lệnh

### Câu lệnh có cấu trúc (Pattern-based)
- "Thêm lịch học Toán vào thứ 2, 8h-10h"
- "Lịch học hôm nay"
- "Lịch thi sắp tới"
- "Khi nào nên nghỉ ngơi?"
- "Tư vấn thời gian học"
- "Phân tích thói quen học tập"

### Chat tự nhiên với Gemini AI
- "Tôi cảm thấy stress với việc học, làm sao đây?"
- "Làm thế nào để cải thiện điểm số môn Toán?"
- "Nên ôn thi Lập trình như thế nào cho hiệu quả?"
- "Tôi có nên thức khuya học không?"
- "Gợi ý lịch học cho tuần tới đi"

> **Với Gemini AI**, bạn có thể hỏi bất kỳ câu hỏi nào về học tập một cách tự nhiên!

## Công nghệ sử dụng

- **Backend**: FastAPI (Python 3.8+)
- **AI Engine**: Google Gemini Pro
- **Database**: SQLite + SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **NLP**: Pattern matching + Gemini AI

## Tính năng nâng cao với Gemini AI

Khi có API key, chatbot sẽ:
- ✅ Hiểu câu hỏi tự nhiên, không cần format cứng nhắc
- ✅ Tư vấn cá nhân hóa dựa trên lịch trình và thói quen
- ✅ Trả lời các câu hỏi về phương pháp học tập
- ✅ Động viên tinh thần và hỗ trợ tâm lý
- ✅ Phân tích và đưa ra gợi ý sáng tạo

## Lấy Gemini API Key

1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Đăng nhập bằng tài khoản Google
3. Click "Create API Key"
4. Copy API key và paste vào file `.env`

**Miễn phí**: Gemini API có free tier rất hào phóng cho việc học tập và phát triển!
