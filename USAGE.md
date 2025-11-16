# Hướng dẫn sử dụng Chatbot Quản lý Thời gian

## Giới thiệu

Chatbot Quản lý Thời gian là một trợ lý AI thông minh giúp sinh viên:
- Quản lý lịch học và lịch thi hiệu quả
- Nhận tư vấn về thời gian học tập tối ưu
- Dự đoán thời gian nghỉ ngơi và ăn uống phù hợp
- Phân tích thói quen học tập cá nhân

## Cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package manager)

### Các bước cài đặt

1. **Clone repository hoặc tải mã nguồn**

2. **Tạo virtual environment** (khuyến nghị)
```bash
python -m venv venv
```

3. **Kích hoạt virtual environment**

Linux/Mac:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

4. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

### Khởi động server

```bash
python main.py
```

Hoặc sử dụng uvicorn trực tiếp:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Truy cập ứng dụng

Mở trình duyệt và truy cập:
```
http://localhost:8000
```

### API Documentation

FastAPI tự động tạo documentation tại:
```
http://localhost:8000/docs
```

## Hướng dẫn sử dụng

### 1. Quản lý lịch học

#### Thêm lịch học mới

**Format cơ bản:**
```
Thêm lịch học [Tên môn] vào [Thứ], [Giờ bắt đầu]-[Giờ kết thúc]
```

**Ví dụ:**
- `Thêm lịch học Toán vào thứ 2, 8h-10h`
- `Thêm môn Lập trình vào thứ 4, 13h30-15h30`
- `Thêm lịch học Tiếng Anh vào thứ 6, 7h-9h, phòng A101`

#### Xem lịch học

**Lịch hôm nay:**
```
Lịch học hôm nay
Lịch ngày hôm nay
```

**Lịch tuần này:**
```
Lịch học tuần này
Lịch học
```

### 2. Quản lý lịch thi

#### Thêm lịch thi

**Format:**
```
Thêm lịch thi [Tên môn] ngày [DD/MM/YYYY], [Giờ]
```

**Ví dụ:**
- `Thêm lịch thi Toán ngày 15/12/2024, 8h`
- `Thêm thi Lập trình ngày 20/12, 13h30, phòng B201`
- `Thêm lịch thi Vật lý ngày 25/12/2024, 14h`

#### Xem lịch thi

```
Lịch thi sắp tới
Lịch thi tuần này
Kỳ thi sắp tới
```

### 3. Nhận tư vấn thời gian học

#### Tư vấn thời gian học tối ưu

```
Tư vấn thời gian học
Nên học khi nào?
Thời gian học hiệu quả
```

**Chatbot sẽ cung cấp:**
- Danh sách các môn thi sắp tới và mức độ ưu tiên
- Khung giờ học hiệu quả nhất trong ngày
- Gợi ý số giờ học cho từng môn dựa trên thời gian thi

#### Khung giờ học hiệu quả

Chatbot sẽ gợi ý các khung giờ tối ưu:
- **06:00-08:00**: Đầu óc tỉnh táo - Phù hợp học các môn khó
- **09:00-11:00**: Khả năng tập trung tốt - Làm bài tập, thực hành
- **15:00-17:00**: Sau giấc ngủ trưa - Ôn tập, đọc tài liệu
- **20:00-22:00**: Buổi tối - Tổng hợp kiến thức, làm bài tập

### 4. Dự đoán thời gian nghỉ ngơi

#### Nhận gợi ý nghỉ ngơi

```
Khi nào nên nghỉ ngơi?
Thời gian nghỉ ngơi
Gợi ý thời gian break
```

**Chatbot sẽ phân tích:**
- Lịch học của bạn trong ngày
- Khoảng trống giữa các buổi học
- Thời gian ăn trưa và ăn tối phù hợp
- Thời lượng nghỉ ngơi hợp lý

**Các loại nghỉ ngơi được gợi ý:**
- 🍽️ **Bữa chính**: 60 phút (trưa 12:00-13:00, tối 18:30-19:30)
- ☕ **Nghỉ dài**: 30-60 phút (giữa các buổi học dài)
- 😌 **Nghỉ ngắn**: 15-20 phút (giữa các buổi học gần nhau)

### 5. Phân tích thói quen học tập

```
Phân tích thói quen học tập
Phân tích hiệu quả học tập
Thói quen của tôi
```

**Chatbot sẽ phân tích:**
- Tổng thời gian học trong 7 ngày qua
- Tổng thời gian nghỉ ngơi
- Trung bình thời gian học mỗi ngày
- Tỷ lệ nghỉ/học
- Đưa ra nhận xét và gợi ý cải thiện

### 6. Các lệnh hữu ích khác

#### Trợ giúp
```
Trợ giúp
Help
Hướng dẫn
```

#### Chào hỏi
```
Xin chào
Hello
Hi
Chào
```

## Ví dụ quy trình sử dụng hoàn chỉnh

### Tuần đầu tiên

1. **Nhập lịch học:**
```
Thêm lịch học Toán vào thứ 2, 8h-10h
Thêm lịch học Vật lý vào thứ 2, 13h-15h
Thêm lịch học Lập trình vào thứ 3, 8h-11h
Thêm lịch học Tiếng Anh vào thứ 4, 7h-9h
Thêm lịch học Hóa học vào thứ 5, 9h-11h
```

2. **Nhập lịch thi:**
```
Thêm lịch thi Toán ngày 20/12/2024, 8h
Thêm lịch thi Lập trình ngày 22/12/2024, 13h30
```

3. **Kiểm tra lịch hôm nay:**
```
Lịch học hôm nay
```

4. **Nhận gợi ý nghỉ ngơi:**
```
Khi nào nên nghỉ ngơi?
```

### Hàng ngày

1. **Kiểm tra lịch:**
```
Lịch học hôm nay
```

2. **Nhận tư vấn học tập:**
```
Tư vấn thời gian học
```

3. **Xem thời gian nghỉ ngơi:**
```
Khi nào nên nghỉ ngơi?
```

### Cuối tuần

1. **Phân tích hiệu quả:**
```
Phân tích thói quen học tập
```

2. **Kiểm tra lịch thi:**
```
Lịch thi sắp tới
```

## Tính năng nâng cao

### 1. AI Recommendations

Chatbot sử dụng thuật toán thông minh để:
- Phân tích khoảng trống trong lịch học
- Tự động đề xuất thời gian nghỉ ngơi hợp lý
- Tính toán độ ưu tiên ôn thi dựa trên ngày thi
- Đưa ra feedback về thói quen học tập

### 2. Smart Scheduling

- Tự động phát hiện xung đột thời gian
- Nhắc nhở trước kỳ thi (3 ngày, 7 ngày)
- Gợi ý thời gian ăn uống phù hợp với lịch học

### 3. Pattern Analysis

Chatbot theo dõi và phân tích:
- Tổng thời gian học mỗi ngày
- Tỷ lệ cân bằng giữa học và nghỉ
- Đưa ra cảnh báo nếu học quá nhiều hoặc quá ít

## Mẹo sử dụng hiệu quả

1. **Nhập đầy đủ lịch học**: Càng nhiều thông tin, chatbot càng đưa ra gợi ý chính xác

2. **Kiểm tra hàng ngày**: Hỏi "Lịch học hôm nay" mỗi sáng để chuẩn bị tốt

3. **Tuân theo gợi ý nghỉ ngơi**: Nghỉ ngơi đúng cách giúp học tập hiệu quả hơn

4. **Ôn thi sớm**: Thêm lịch thi ngay khi biết để nhận tư vấn ôn tập kịp thời

5. **Phân tích thường xuyên**: Kiểm tra thói quen học tập mỗi tuần để cải thiện

## Xử lý sự cố

### Lỗi kết nối
- Kiểm tra server có đang chạy không
- Đảm bảo port 8000 không bị chiếm dụng
- Thử khởi động lại server

### Lỗi database
- Xóa file `chatbot_schedule.db` và khởi động lại
- Database sẽ tự động được tạo lại

### Chatbot không hiểu
- Thử diễn đạt lại câu hỏi
- Xem ví dụ trong phần "Trợ giúp"
- Đảm bảo format đúng như hướng dẫn

## Liên hệ và đóng góp

- Báo lỗi: Tạo issue trên repository
- Đề xuất tính năng: Pull request hoặc issue
- Thắc mắc: Xem README.md hoặc documentation

## Cập nhật và bảo trì

### Cập nhật dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Backup dữ liệu
File database: `chatbot_schedule.db`

Sao lưu thường xuyên để tránh mất dữ liệu.

## Kế hoạch phát triển

Các tính năng sẽ được thêm vào:
- [ ] Export lịch ra file PDF/Excel
- [ ] Thông báo nhắc nhở qua email/SMS
- [ ] Tích hợp với Google Calendar
- [ ] Thống kê chi tiết hơn
- [ ] Chế độ nhóm (chia sẻ lịch với bạn bè)
- [ ] Mobile app
- [ ] Hỗ trợ nhiều ngôn ngữ

---

**Chúc bạn học tập hiệu quả với Chatbot Quản lý Thời gian! 📚✨**
