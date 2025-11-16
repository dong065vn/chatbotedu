"""Chatbot logic and natural language processing"""
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import User, Schedule, Exam, Activity, ChatHistory
from app.ai_engine import AIRecommendationEngine

class ChatBot:
    """Intelligent chatbot for schedule management"""

    def __init__(self, db: Session, user_id: int = None):
        self.db = db
        self.user_id = user_id or self._get_or_create_default_user()
        self.ai_engine = AIRecommendationEngine(db, self.user_id)

    def _get_or_create_default_user(self) -> int:
        """Get or create default user"""
        user = self.db.query(User).filter(User.username == "default").first()
        if not user:
            user = User(username="default")
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user.id

    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process user message and return appropriate response
        """
        message = message.lower().strip()

        # Save chat history
        response_text = ""

        try:
            # Pattern matching for different intents
            if self._match_pattern(message, ["xin chào", "hello", "hi", "chào"]):
                response_text = self._greet_user()

            elif self._match_pattern(message, ["thêm lịch học", "thêm môn học", "lịch học mới"]):
                response_text = self._handle_add_schedule(message)

            elif self._match_pattern(message, ["thêm lịch thi", "thêm thi", "kỳ thi"]):
                response_text = self._handle_add_exam(message)

            elif self._match_pattern(message, ["lịch học", "lịch tuần này", "lịch hôm nay", "lịch ngày"]):
                response_text = self._handle_get_schedule(message)

            elif self._match_pattern(message, ["lịch thi", "thi tuần này", "kỳ thi sắp tới"]):
                response_text = self._handle_get_exams(message)

            elif self._match_pattern(message, ["nghỉ ngơi", "khi nào nghỉ", "thời gian nghỉ", "break"]):
                response_text = self._handle_rest_prediction()

            elif self._match_pattern(message, ["tư vấn", "học khi nào", "thời gian học", "nên học"]):
                response_text = self._handle_study_recommendation(message)

            elif self._match_pattern(message, ["phân tích", "thói quen", "học tập", "hiệu quả"]):
                response_text = self._handle_study_analysis()

            elif self._match_pattern(message, ["trợ giúp", "help", "hướng dẫn"]):
                response_text = self._show_help()

            elif self._match_pattern(message, ["xóa lịch", "xóa môn", "hủy"]):
                response_text = self._handle_delete_schedule(message)

            else:
                response_text = self._handle_unknown(message)

            # Save to history
            chat_entry = ChatHistory(
                user_id=self.user_id,
                message=message,
                response=response_text
            )
            self.db.add(chat_entry)
            self.db.commit()

            return {
                "success": True,
                "response": response_text,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            error_msg = f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
            return {
                "success": False,
                "response": error_msg,
                "timestamp": datetime.now().isoformat()
            }

    def _match_pattern(self, message: str, patterns: list) -> bool:
        """Check if message matches any pattern"""
        return any(pattern in message for pattern in patterns)

    def _greet_user(self) -> str:
        """Greet the user"""
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Chào buổi sáng"
        elif hour < 18:
            greeting = "Chào buổi chiều"
        else:
            greeting = "Chào buổi tối"

        return f"""{greeting}! 👋

Tôi là trợ lý AI giúp bạn quản lý thời gian học tập.

Tôi có thể giúp bạn:
• Quản lý lịch học và lịch thi
• Tư vấn thời gian học hiệu quả
• Dự đoán thời gian nghỉ ngơi phù hợp
• Phân tích thói quen học tập

Hãy nói cho tôi biết bạn cần gì! Gõ "trợ giúp" để xem hướng dẫn."""

    def _handle_add_schedule(self, message: str) -> str:
        """Handle adding a new class schedule"""
        # Extract information using regex
        # Format: "Thêm lịch học [Subject] vào [Day], [Time]"

        # Try to extract subject
        subject_match = re.search(r'lịch học\s+([^vào]+)', message)
        if not subject_match:
            return """Để thêm lịch học, vui lòng cung cấp thông tin đầy đủ.

Ví dụ:
• "Thêm lịch học Toán vào thứ 2, 8h-10h"
• "Thêm môn Lập trình vào thứ 4, 13h30-15h30, phòng A101"

Format: Thêm lịch học [Môn học] vào [Thứ], [Giờ bắt đầu]-[Giờ kết thúc], [Phòng (tùy chọn)]"""

        subject = subject_match.group(1).strip()

        # Extract day of week
        day_map = {
            "thứ 2": 0, "thứ 3": 1, "thứ 4": 2, "thứ 5": 3,
            "thứ 6": 4, "thứ 7": 5, "chủ nhật": 6,
            "thứ hai": 0, "thứ ba": 1, "thứ tư": 2, "thứ năm": 3,
            "thứ sáu": 4, "thứ bảy": 5
        }

        day_of_week = None
        for day_text, day_num in day_map.items():
            if day_text in message:
                day_of_week = day_num
                break

        if day_of_week is None:
            return "Vui lòng chỉ rõ thứ mấy (ví dụ: thứ 2, thứ 3, ...)"

        # Extract time
        time_match = re.search(r'(\d{1,2}h?\d{0,2})\s*-\s*(\d{1,2}h?\d{0,2})', message)
        if not time_match:
            return "Vui lòng chỉ rõ thời gian (ví dụ: 8h-10h, 13h30-15h30)"

        start_time = self._parse_time(time_match.group(1))
        end_time = self._parse_time(time_match.group(2))

        # Extract location (optional)
        location_match = re.search(r'phòng\s+([A-Za-z0-9]+)', message)
        location = location_match.group(1) if location_match else None

        # Create schedule
        schedule = Schedule(
            user_id=self.user_id,
            subject=subject,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            location=location
        )

        self.db.add(schedule)
        self.db.commit()

        day_names = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        location_text = f" tại {location}" if location else ""

        return f"""✅ Đã thêm lịch học thành công!

📚 Môn: {subject}
📅 Thời gian: {day_names[day_of_week]}, {start_time} - {end_time}{location_text}

Gõ "lịch học" để xem toàn bộ lịch của bạn."""

    def _handle_add_exam(self, message: str) -> str:
        """Handle adding an exam"""
        # Format: "Thêm lịch thi [Subject] ngày [Date], [Time]"

        subject_match = re.search(r'thi\s+([^ngày]+)', message)
        if not subject_match:
            return """Để thêm lịch thi, vui lòng cung cấp thông tin đầy đủ.

Ví dụ:
• "Thêm lịch thi Toán ngày 15/12/2024, 8h"
• "Thêm thi Lập trình ngày 20/12, 13h30, phòng B201"

Format: Thêm lịch thi [Môn] ngày [DD/MM/YYYY], [Giờ], [Phòng (tùy chọn)]"""

        subject = subject_match.group(1).strip()

        # Extract date
        date_match = re.search(r'ngày\s+(\d{1,2})/(\d{1,2})(?:/(\d{4}))?', message)
        if not date_match:
            return "Vui lòng chỉ rõ ngày thi (ví dụ: ngày 15/12/2024)"

        day = int(date_match.group(1))
        month = int(date_match.group(2))
        year = int(date_match.group(3)) if date_match.group(3) else datetime.now().year

        # Extract time
        time_match = re.search(r'(\d{1,2}h\d{0,2})', message)
        if time_match:
            time_str = self._parse_time(time_match.group(1))
            hour, minute = map(int, time_str.split(':'))
        else:
            hour, minute = 8, 0

        exam_date = datetime(year, month, day, hour, minute)

        # Extract location
        location_match = re.search(r'phòng\s+([A-Za-z0-9]+)', message)
        location = location_match.group(1) if location_match else None

        # Create exam
        exam = Exam(
            user_id=self.user_id,
            subject=subject,
            exam_date=exam_date,
            location=location
        )

        self.db.add(exam)
        self.db.commit()

        location_text = f" tại {location}" if location else ""

        return f"""✅ Đã thêm lịch thi thành công!

📝 Môn: {subject}
📅 Ngày thi: {exam_date.strftime('%d/%m/%Y %H:%M')}{location_text}

Tôi sẽ nhắc nhở bạn khi gần đến ngày thi!"""

    def _handle_get_schedule(self, message: str) -> str:
        """Get schedule for today or this week"""
        if "hôm nay" in message or "ngày" in message:
            summary = self.ai_engine.get_daily_schedule_summary()

            if not summary['classes'] and not summary['exams']:
                return f"""📅 Lịch {summary['day_of_week']}, {summary['date']}

Bạn không có lịch học hay thi hôm nay.
Đây là thời gian tốt để tự học hoặc nghỉ ngơi! 😊"""

            response = f"""📅 Lịch {summary['day_of_week']}, {summary['date']}\n\n"""

            if summary['classes']:
                response += "📚 Lịch học:\n"
                for cls in summary['classes']:
                    response += f"  • {cls['subject']}: {cls['time']}"
                    if cls['location'] != "Chưa cập nhật":
                        response += f" - {cls['location']}"
                    response += "\n"

            if summary['exams']:
                response += "\n📝 Lịch thi:\n"
                for exam in summary['exams']:
                    response += f"  • {exam['subject']}: {exam['time']}"
                    if exam['location'] != "Chưa cập nhật":
                        response += f" - {exam['location']}"
                    response += "\n"

            return response

        else:  # Week schedule
            schedules = self.db.query(Schedule).filter(
                Schedule.user_id == self.user_id
            ).order_by(Schedule.day_of_week, Schedule.start_time).all()

            if not schedules:
                return """Bạn chưa có lịch học nào.

Thêm lịch học bằng cách:
"Thêm lịch học [Môn] vào [Thứ], [Giờ]"

Ví dụ: "Thêm lịch học Toán vào thứ 2, 8h-10h" """

            day_names = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
            response = "📅 Lịch học tuần này:\n\n"

            current_day = -1
            for schedule in schedules:
                if schedule.day_of_week != current_day:
                    current_day = schedule.day_of_week
                    response += f"\n{day_names[current_day]}:\n"

                response += f"  • {schedule.subject}: {schedule.start_time}-{schedule.end_time}"
                if schedule.location:
                    response += f" - {schedule.location}"
                response += "\n"

            return response

    def _handle_get_exams(self, message: str) -> str:
        """Get upcoming exams"""
        exams = self.db.query(Exam).filter(
            Exam.user_id == self.user_id,
            Exam.exam_date >= datetime.now()
        ).order_by(Exam.exam_date).limit(10).all()

        if not exams:
            return "Bạn chưa có lịch thi nào được lên lịch."

        response = "📝 Lịch thi sắp tới:\n\n"

        for exam in exams:
            days_until = (exam.exam_date - datetime.now()).days
            urgency = "🔴" if days_until <= 3 else "🟡" if days_until <= 7 else "🟢"

            response += f"{urgency} {exam.subject}\n"
            response += f"   📅 {exam.exam_date.strftime('%d/%m/%Y %H:%M')}"
            if exam.location:
                response += f" - {exam.location}"
            response += f"\n   ⏰ Còn {days_until} ngày\n\n"

        return response

    def _handle_rest_prediction(self) -> str:
        """Predict rest and meal times"""
        predictions = self.ai_engine.predict_rest_times()

        if not predictions:
            return "Tôi không tìm thấy lịch học của bạn hôm nay để đưa ra gợi ý nghỉ ngơi."

        response = "🌟 Gợi ý thời gian nghỉ ngơi hôm nay:\n\n"

        for pred in predictions:
            if pred['type'] == 'lunch':
                icon = "🍽️"
            elif pred['type'] == 'dinner':
                icon = "🍲"
            elif pred['type'] == 'rest_or_meal':
                icon = "☕"
            else:
                icon = "😌"

            response += f"{icon} {pred['time']}\n"
            response += f"   {pred['reason']}\n"
            response += f"   ⏱️ Thời lượng: {pred['duration_minutes']} phút\n\n"

        return response

    def _handle_study_recommendation(self, message: str) -> str:
        """Provide study time recommendations"""
        recommendations = self.ai_engine.recommend_study_times()

        response = "📖 Tư vấn thời gian học tập:\n\n"

        # Exam priorities
        if recommendations['exam_priorities']:
            response += "🎯 Ưu tiên ôn thi:\n\n"
            for rec in recommendations['exam_priorities']:
                priority_icon = "🔴" if rec['priority'] == "cao" else "🟡" if rec['priority'] == "trung bình" else "🟢"
                response += f"{priority_icon} {rec['suggestion']}\n"
                response += f"   📅 Ngày thi: {rec['exam_date']}\n"
                response += f"   ⏰ Nên học: {rec['recommended_hours_per_day']} giờ/ngày\n\n"

        # Optimal study times
        response += "⭐ Khung giờ học hiệu quả:\n\n"
        for time in recommendations['optimal_study_times']:
            response += f"🕐 {time['time_range']} - {time['effectiveness']}\n"
            response += f"   ✓ {time['reason']}\n"
            response += f"   💡 Phù hợp: {time['recommended_for']}\n\n"

        return response

    def _handle_study_analysis(self) -> str:
        """Analyze study patterns"""
        analysis = self.ai_engine.analyze_study_patterns()

        response = "📊 Phân tích thói quen học tập (7 ngày qua):\n\n"

        response += f"⏱️ Tổng thời gian học: {analysis['total_study_minutes']} phút\n"
        response += f"😌 Tổng thời gian nghỉ: {analysis['total_rest_minutes']} phút\n"
        response += f"📈 Trung bình: {analysis['average_study_per_day']} phút/ngày\n"
        response += f"⚖️ Tỷ lệ nghỉ/học: {analysis['study_rest_ratio']}\n\n"

        if analysis['feedback']:
            response += "💬 Nhận xét:\n"
            for fb in analysis['feedback']:
                icon = "✅" if fb['type'] == "success" else "⚠️"
                response += f"{icon} {fb['message']}\n"

        return response

    def _handle_delete_schedule(self, message: str) -> str:
        """Handle deleting a schedule"""
        # This is a simplified version
        return """Để xóa lịch học, vui lòng cung cấp tên môn học.

Ví dụ: "Xóa lịch Toán"

(Tính năng này đang được phát triển)"""

    def _show_help(self) -> str:
        """Show help information"""
        return """📚 Hướng dẫn sử dụng Chatbot Quản lý Thời gian

🔹 Quản lý lịch học:
   • "Thêm lịch học Toán vào thứ 2, 8h-10h"
   • "Lịch học hôm nay"
   • "Lịch học tuần này"

🔹 Quản lý lịch thi:
   • "Thêm lịch thi Toán ngày 15/12/2024, 8h"
   • "Lịch thi sắp tới"

🔹 Tư vấn học tập:
   • "Tư vấn thời gian học"
   • "Khi nào nên nghỉ ngơi?"
   • "Phân tích thói quen học tập"

🔹 Khác:
   • "Trợ giúp" - Xem hướng dẫn này

Hãy thử nói chuyện với tôi một cách tự nhiên! 😊"""

    def _handle_unknown(self, message: str) -> str:
        """Handle unknown messages"""
        return """Xin lỗi, tôi chưa hiểu yêu cầu của bạn.

Gõ "trợ giúp" để xem hướng dẫn sử dụng.

Hoặc thử:
• "Thêm lịch học..."
• "Lịch thi sắp tới"
• "Tư vấn thời gian học"
• "Khi nào nên nghỉ ngơi?" """

    def _parse_time(self, time_str: str) -> str:
        """Parse time string to HH:MM format"""
        time_str = time_str.replace('h', ':')
        if ':' not in time_str:
            time_str += ':00'

        parts = time_str.split(':')
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 and parts[1] else 0

        return f"{hour:02d}:{minute:02d}"
