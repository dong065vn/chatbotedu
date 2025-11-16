# Chatbot Quản lý Thời gian Học tập

Chatbot AI hỗ trợ sinh viên quản lý thời gian học tập hiệu quả.

## Tính năng

- 📚 **Quản lý lịch học**: Theo dõi lịch học theo tuần, tháng
- 📝 **Quản lý lịch thi**: Nhắc nhở và chuẩn bị cho các kỳ thi
- ⏰ **Tư vấn thời gian học**: Gợi ý thời gian học tập hiệu quả
- 🍽️ **Dự đoán thời gian nghỉ ngơi**: Tự động đề xuất thời gian nghỉ ngơi và ăn uống
- 🤖 **Chat AI thông minh**: Tương tác tự nhiên qua chat

## Cài đặt

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python main.py
```

Mở trình duyệt tại: http://localhost:8000

## API Documentation

Swagger UI: http://localhost:8000/docs

## Cấu trúc dự án

```
chatbotedu/
├── main.py                 # Entry point
├── app/
│   ├── models.py          # Database models
│   ├── database.py        # Database setup
│   ├── chatbot.py         # Chatbot logic
│   ├── scheduler.py       # Schedule management
│   └── ai_engine.py       # AI recommendation engine
├── static/                # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
└── requirements.txt
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

- "Thêm lịch học Toán vào thứ 2, 8h sáng"
- "Lịch thi của tôi tuần này?"
- "Khi nào tôi nên nghỉ ngơi?"
- "Tư vấn thời gian học cho môn Lập trình"
