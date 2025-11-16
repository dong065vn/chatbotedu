# 🤖 Chatbot Quản lý Thời gian - Professional Edition v2.0

Chatbot AI thông minh sử dụng **Gemini AI** để giúp sinh viên quản lý thời gian học tập hiệu quả với giao diện chuyên nghiệp và hiện đại.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Tính năng nổi bật v2.0

### 🎨 Giao diện Professional
- **Dark/Light Mode**: Chuyển đổi chế độ tối/sáng với animation mượt mà
- **Modern Gradient UI**: Thiết kế gradient hiện đại, chuyên nghiệp
- **Responsive Design**: Hoạt động hoàn hảo trên mọi thiết bị
- **Smooth Animations**: Hơn 10+ hiệu ứng animation chuyên nghiệp
- **Glass Morphism**: Hiệu ứng kính mờ backdrop trendy

### 🚀 Tính năng mới
- **📊 Thống kê Real-time**: Theo dõi số tin nhắn, lịch học, lịch thi
- **💾 Xuất Chat History**: Lưu cuộc trò chuyện ra file TXT
- **😊 Emoji Picker**: Chọn emoji nhanh chóng cho tin nhắn
- **⚡ Quick Actions**: 4 nút action thường dùng nhất
- **🔔 Toast Notifications**: Thông báo đẹp mắt, thông minh
- **⌨️ Keyboard Shortcuts**: Phím tắt tiện lợi
- **🔄 Auto-save**: Tự động lưu lịch sử chat
- **🌐 Network Detection**: Phát hiện trạng thái mạng

### 🤖 AI Features
- **Gemini AI Integration**: Trò chuyện tự nhiên với AI thông minh
- **Context Awareness**: AI hiểu ngữ cảnh và lịch trình của bạn
- **Smart Recommendations**: Gợi ý thời gian học tập tối ưu
- **Pattern Analysis**: Phân tích thói quen học tập

### 📚 Quản lý Học tập
- ✅ Quản lý lịch học theo tuần
- ✅ Quản lý lịch thi và deadline
- ✅ Dự đoán thời gian nghỉ ngơi, ăn uống
- ✅ Tư vấn thời gian học hiệu quả
- ✅ Phân tích thói quen học tập
- ✅ Nhắc nhở thông minh

---

## 🎯 Demo

### Giao diện chính
```
┌─────────────────────────────────────────────────────────┐
│  🤖 Trợ lý AI Quản lý Thời gian        [🗑️] [💾] [☰]  │
│  ● Đang hoạt động                                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🤖  Xin chào! Tôi là trợ lý AI...                     │
│                                           14:30          │
│                                                          │
│                         👤  Thêm lịch học Toán...       │
│                                           14:31          │
│                                                          │
│  🤖  ✅ Đã thêm lịch học thành công!                   │
│      📚 Môn: Toán                                       │
│      📅 Thời gian: Thứ Hai, 08:00-10:00                │
│                                           14:31          │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  [🎤] ┃ Nhập tin nhắn... ┃ [😊] [➤]                    │
│  [📅 Lịch] [📝 Thi] [📊 Phân tích] [💡 Tư vấn]        │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Cài đặt & Sử dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package manager)
- Trình duyệt web hiện đại (Chrome, Firefox, Safari, Edge)

### Bước 1: Clone repository
```bash
git clone https://github.com/yourusername/chatbotedu.git
cd chatbotedu
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình Gemini API (Tùy chọn)
Tạo file `.env` và thêm API key:
```bash
cp .env.example .env
# Chỉnh sửa .env và thêm GEMINI_API_KEY của bạn
```

Để lấy API key miễn phí:
1. Truy cập https://makersuite.google.com/app/apikey
2. Tạo API key mới
3. Copy và paste vào file `.env`

### Bước 4: Chạy ứng dụng

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Hoặc chạy trực tiếp:**
```bash
python main.py
```

### Bước 5: Truy cập
Mở trình duyệt và truy cập:
```
http://localhost:8000
```

---

## 📖 Hướng dẫn sử dụng

### Quản lý Lịch học
```
"Thêm lịch học Toán vào thứ 2, 8h-10h"
"Thêm môn Lập trình vào thứ 4, 13h30-15h30, phòng A101"
"Lịch học hôm nay"
"Lịch học tuần này"
```

### Quản lý Lịch thi
```
"Thêm lịch thi Toán ngày 15/12/2024, 8h"
"Thêm thi Lập trình ngày 20/12, 13h30, phòng B201"
"Lịch thi sắp tới"
```

### Nhận Tư vấn
```
"Tư vấn thời gian học"
"Khi nào nên nghỉ ngơi?"
"Phân tích thói quen học tập"
```

### Chat với AI
```
"Làm sao để học hiệu quả hơn?"
"Tôi nên ưu tiên môn nào trước?"
"Giúp tôi lên kế hoạch ôn thi"
```

### Phím tắt
- `Ctrl + K`: Focus input
- `Ctrl + L`: Xóa chat
- `Ctrl + D`: Toggle dark mode
- `Enter`: Gửi tin nhắn
- `Escape`: Đóng emoji picker

---

## 🛠️ Công nghệ sử dụng

### Backend
- **FastAPI**: Web framework hiện đại, nhanh
- **SQLAlchemy**: ORM mạnh mẽ
- **SQLite**: Database nhẹ, không cần setup
- **Google Gemini AI**: Large Language Model thông minh
- **Python 3.8+**: Ngôn ngữ lập trình chính

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling với variables, animations
- **Vanilla JavaScript**: Pure JS, không framework
- **Responsive Design**: Mobile-first approach
- **Progressive Enhancement**: Hoạt động trên mọi browser

### Features
- **Dark/Light Mode**: CSS variables với localStorage
- **LocalStorage API**: Lưu chat history và preferences
- **Fetch API**: Async communication với backend
- **CSS Animations**: Smooth transitions và effects
- **Toast Notifications**: Custom notification system

---

## 📁 Cấu trúc Project

```
chatbotedu/
├── app/
│   ├── __init__.py
│   ├── ai_engine.py          # AI recommendation engine
│   ├── chatbot_v2.py          # Main chatbot logic với Gemini
│   ├── database.py            # Database configuration
│   ├── gemini_ai.py           # Gemini API integration
│   └── models.py              # SQLAlchemy models
├── static/
│   ├── index.html             # UI với modern design
│   ├── style.css              # Professional styles v2.0
│   └── script.js              # Enhanced JavaScript v2.0
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── FEATURES.md                # Detailed features documentation
├── GEMINI_SETUP.md            # Gemini API setup guide
├── main.py                    # FastAPI application entry
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── run.bat                    # Windows run script
├── run.sh                     # Linux/Mac run script
└── USAGE.md                   # Detailed usage guide
```

---

## 🎨 Screenshots

### Light Mode
![Light Mode](docs/screenshots/light-mode.png)

### Dark Mode
![Dark Mode](docs/screenshots/dark-mode.png)

### Mobile View
![Mobile](docs/screenshots/mobile.png)

---

## 🔧 API Endpoints

### Chat API
```http
POST /api/chat
Content-Type: application/json

{
    "message": "Lịch học hôm nay",
    "user_id": 1
}
```

### Health Check
```http
GET /api/health
```

### User Info
```http
GET /api/user/{user_id}
```

---

## 📊 Database Schema

### Users
- `id`: Integer (Primary Key)
- `username`: String
- `created_at`: DateTime

### Schedules
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key)
- `subject`: String
- `day_of_week`: Integer (0-6)
- `start_time`: String
- `end_time`: String
- `location`: String (Optional)

### Exams
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key)
- `subject`: String
- `exam_date`: DateTime
- `location`: String (Optional)

### Activities
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key)
- `activity_type`: String
- `start_time`: DateTime
- `end_time`: DateTime
- `description`: String

### ChatHistory
- `id`: Integer (Primary Key)
- `user_id`: Integer (Foreign Key)
- `message`: Text
- `response`: Text
- `timestamp`: DateTime

---

## 🤝 Đóng góp

Chúng tôi rất hoan nghênh mọi đóng góp!

### Cách đóng góp:
1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

### Báo lỗi:
- Mở issue với label "bug"
- Mô tả chi tiết lỗi và cách tái tạo
- Attach screenshots nếu có

### Đề xuất tính năng:
- Mở issue với label "enhancement"
- Mô tả tính năng và lý do cần thiết
- Thảo luận với community

---

## 📝 Changelog

### v2.0.0 (2024-11-16) - Professional Edition
#### ✨ New Features
- Dark/Light mode toggle với smooth transition
- Real-time statistics dashboard
- Chat export functionality (TXT format)
- Emoji picker với 12+ emojis
- Quick action buttons
- Toast notification system
- Keyboard shortcuts (Ctrl+K, Ctrl+L, Ctrl+D)
- Auto-save chat history
- Network status detection
- Voice input button (placeholder)

#### 🎨 UI/UX Improvements
- Complete redesign với modern gradient
- Glass morphism effects
- Smooth animations throughout
- Improved responsive design
- Enhanced chat interface với shadows
- Better mobile experience
- Professional color scheme
- Accessibility improvements

#### 🚀 Performance
- Optimized CSS animations
- Efficient DOM manipulation
- Debounced scroll events
- Lazy loading support
- Faster load time

#### 🔧 Technical
- Migrated to CSS variables
- Added LocalStorage API usage
- Improved error handling
- Better code organization
- Enhanced security measures

### v1.0.0 (Initial Release)
- Basic chat functionality
- Schedule management
- Exam tracking
- AI recommendations với Gemini
- Simple UI

---

## 🔮 Roadmap

### v2.1 (Coming Soon)
- [ ] Voice input với Speech-to-Text
- [ ] Search functionality trong chat
- [ ] File attachments
- [ ] Multi-language support (EN, VI)
- [ ] Advanced analytics dashboard

### v2.2
- [ ] Calendar view integration
- [ ] Push notifications
- [ ] Chat templates
- [ ] Custom themes
- [ ] Share chat functionality

### v3.0
- [ ] Progressive Web App (PWA)
- [ ] Offline mode
- [ ] Sync across devices
- [ ] Team collaboration
- [ ] Advanced AI features

---

## 🐛 Known Issues

- Voice input chưa được implement (placeholder only)
- Stats count cần integrate với backend API
- IE11 không được support

---

## 📄 License

MIT License - Free to use and modify

Copyright (c) 2024 ChatbotEdu Team

---

## 👥 Team

**Development Team:**
- Lead Developer: [Your Name]
- UI/UX Designer: [Designer Name]
- AI Integration: [AI Developer Name]

---

## 📞 Support

- 📧 Email: support@chatbotedu.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/chatbotedu/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/chatbotedu/discussions)
- 📚 Docs: [Documentation](https://docs.chatbotedu.com)

---

## 🙏 Acknowledgments

- Google Gemini AI Team
- FastAPI Community
- Open Source Contributors
- All Beta Testers

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/chatbotedu&type=Date)](https://star-history.com/#yourusername/chatbotedu&Date)

---

**Made with ❤️ in Vietnam 🇻🇳**

**Powered by Gemini AI 🤖**

---

## 📸 More Screenshots

Xem thêm screenshots trong folder [docs/screenshots](docs/screenshots/)

---

**[⬆ Back to top](#-chatbot-quản-lý-thời-gian---professional-edition-v20)**
