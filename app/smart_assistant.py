"""
Smart AI Assistant - Professional Edition v3.0
Advanced context-aware chatbot with intelligent features
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
import re

from app.models import User, Schedule, Exam, Activity, ChatHistory


class SmartAssistant:
    """Intelligent assistant with context awareness and proactive features"""

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.context_memory = []
        self.max_context_memory = 10

    def analyze_intent(self, message: str) -> Dict[str, Any]:
        """
        Intelligent intent detection with confidence scoring
        Returns: {
            'intent': str,
            'confidence': float,
            'entities': dict,
            'context_needed': bool
        }
        """
        message_lower = message.lower().strip()

        # Intent patterns with priority
        intent_patterns = {
            'add_schedule': {
                'patterns': [
                    r'(thêm|tạo|đăng ký).*?(lịch học|môn học|lớp)',
                    r'học.*?(môn|lớp|thứ)',
                ],
                'keywords': ['thêm', 'tạo', 'lịch học', 'môn học', 'đăng ký'],
                'priority': 10
            },
            'add_exam': {
                'patterns': [
                    r'(thêm|tạo).*?(lịch thi|thi|kiểm tra)',
                    r'thi.*?(môn|ngày)',
                ],
                'keywords': ['thêm', 'lịch thi', 'thi', 'kiểm tra', 'kỳ thi'],
                'priority': 10
            },
            'view_schedule': {
                'patterns': [
                    r'(xem|lịch|show).*?(học|hôm nay|tuần|ngày)',
                    r'hôm nay.*?học',
                ],
                'keywords': ['lịch', 'hôm nay', 'tuần này', 'xem'],
                'priority': 9
            },
            'view_exams': {
                'patterns': [
                    r'(xem|lịch).*?(thi|kiểm tra)',
                    r'(thi|kiểm tra).*?sắp tới',
                ],
                'keywords': ['lịch thi', 'thi sắp tới', 'kỳ thi'],
                'priority': 9
            },
            'recommendation': {
                'patterns': [
                    r'(tư vấn|gợi ý|nên).*?(học|ôn)',
                    r'(khi nào|thời gian).*?(học|ôn)',
                ],
                'keywords': ['tư vấn', 'gợi ý', 'nên học', 'khi nào'],
                'priority': 8
            },
            'rest_prediction': {
                'patterns': [
                    r'(nghỉ|休息|break|休み)',
                    r'(khi nào|thời gian).*?nghỉ',
                ],
                'keywords': ['nghỉ ngơi', 'break', 'thư giãn'],
                'priority': 8
            },
            'analytics': {
                'patterns': [
                    r'(phân tích|thống kê|báo cáo)',
                    r'thói quen.*?học',
                ],
                'keywords': ['phân tích', 'thống kê', 'báo cáo', 'hiệu quả'],
                'priority': 7
            },
            'delete': {
                'patterns': [
                    r'(xóa|hủy|bỏ).*?(lịch|môn)',
                ],
                'keywords': ['xóa', 'hủy', 'bỏ'],
                'priority': 10
            },
            'help': {
                'patterns': [
                    r'(trợ giúp|help|hướng dẫn|guide)',
                ],
                'keywords': ['help', 'trợ giúp', 'hướng dẫn'],
                'priority': 5
            },
            'greeting': {
                'patterns': [
                    r'^(xin chào|chào|hello|hi|hey).*?$',
                ],
                'keywords': ['xin chào', 'chào', 'hello', 'hi'],
                'priority': 3
            },
            'thanks': {
                'patterns': [
                    r'(cảm ơn|cám ơn|thank|thanks)',
                ],
                'keywords': ['cảm ơn', 'thanks', 'thank you'],
                'priority': 3
            },
            'general': {
                'patterns': [],
                'keywords': [],
                'priority': 1
            }
        }

        best_match = {'intent': 'general', 'confidence': 0.0, 'priority': 0}

        for intent, config in intent_patterns.items():
            score = 0

            # Pattern matching
            for pattern in config['patterns']:
                if re.search(pattern, message_lower):
                    score += 0.4
                    break

            # Keyword matching
            keyword_matches = sum(1 for kw in config['keywords'] if kw in message_lower)
            score += (keyword_matches / max(len(config['keywords']), 1)) * 0.4

            # Length penalty (longer messages are more likely to be general questions)
            if len(message.split()) > 20 and intent == 'general':
                score += 0.3

            # Priority boost
            score += config['priority'] * 0.02

            if score > best_match['confidence']:
                best_match = {
                    'intent': intent,
                    'confidence': score,
                    'priority': config['priority']
                }

        # Extract entities based on intent
        entities = self._extract_entities(message, best_match['intent'])

        return {
            'intent': best_match['intent'],
            'confidence': min(best_match['confidence'], 1.0),
            'entities': entities,
            'context_needed': best_match['confidence'] < 0.5
        }

    def _extract_entities(self, message: str, intent: str) -> Dict[str, Any]:
        """Extract relevant entities from message based on intent"""
        entities = {}
        message_lower = message.lower()

        # Time entities
        time_patterns = {
            'time': r'(\d{1,2}[h:]\d{0,2}|\d{1,2}\s*giờ)',
            'day': r'(thứ\s*\d|t\d|chủ\s*nhật)',
            'date': r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|ngày\s*\d{1,2})',
        }

        for entity_type, pattern in time_patterns.items():
            match = re.search(pattern, message_lower)
            if match:
                entities[entity_type] = match.group(0)

        # Subject entity
        subject_match = re.search(r'(toán|lý|hóa|sinh|văn|sử|địa|anh|tin|thể dục|âm nhạc|mỹ thuật)', message_lower)
        if subject_match:
            entities['subject'] = subject_match.group(0).title()

        return entities

    def get_proactive_suggestions(self) -> List[str]:
        """
        Generate proactive suggestions based on user's schedule and patterns
        """
        suggestions = []
        now = datetime.now()

        # Check for upcoming exams
        upcoming_exams = self.db.query(Exam).filter(
            Exam.user_id == self.user_id,
            Exam.exam_date.between(now, now + timedelta(days=7))
        ).all()

        if upcoming_exams:
            for exam in upcoming_exams:
                days_until = (exam.exam_date - now).days
                if days_until <= 3:
                    suggestions.append(f"⚠️ Bạn có kỳ thi {exam.subject} trong {days_until} ngày nữa. Đã ôn tập chưa?")

        # Check for missing schedule today
        today = now.weekday()
        today_schedule = self.db.query(Schedule).filter(
            Schedule.user_id == self.user_id,
            Schedule.day_of_week == today
        ).all()

        if not today_schedule and now.hour < 12:
            suggestions.append("💡 Hôm nay bạn chưa có lịch học. Muốn thêm lịch học không?")

        # Study streak tracking
        recent_activities = self.db.query(Activity).filter(
            Activity.user_id == self.user_id,
            Activity.timestamp >= now - timedelta(days=7)
        ).count()

        if recent_activities == 0:
            suggestions.append("📚 Bạn chưa có hoạt động học tập nào trong tuần này. Hãy bắt đầu học nhé!")

        return suggestions

    def get_smart_schedule_recommendation(self) -> str:
        """
        Intelligent schedule recommendation based on patterns and performance
        """
        # Analyze best study times
        activities = self.db.query(Activity).filter(
            Activity.user_id == self.user_id
        ).all()

        if not activities:
            return """
📊 **Gợi ý học tập thông minh:**

Dựa trên nghiên cứu khoa học, đây là khung giờ tốt nhất để học:
• **6:00 - 8:00 sáng**: Trí nhớ và tập trung cao nhất
• **10:00 - 12:00 trưa**: Tư duy logic và phân tích tốt
• **16:00 - 18:00 chiều**: Phù hợp ôn tập và thực hành
• **20:00 - 22:00 tối**: Củng cố kiến thức đã học

💡 **Tip**: Học 25 phút, nghỉ 5 phút (Pomodoro Technique)
"""

        # Analyze activity patterns
        hour_distribution = {}
        for activity in activities:
            hour = activity.timestamp.hour
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1

        best_hours = sorted(hour_distribution.items(), key=lambda x: x[1], reverse=True)[:3]

        recommendation = "📊 **Phân tích thói quen học tập của bạn:**\n\n"
        recommendation += "Các khung giờ bạn học tập hiệu quả nhất:\n"

        for hour, count in best_hours:
            recommendation += f"• **{hour}:00 - {hour+1}:00**: {count} hoạt động\n"

        recommendation += "\n💡 **Gợi ý**: Hãy sắp xếp các môn khó vào khung giờ này để đạt hiệu quả tốt nhất!"

        return recommendation

    def get_rest_prediction(self) -> str:
        """
        Predict optimal rest times based on schedule density
        """
        now = datetime.now()
        today = now.weekday()

        # Get today's schedule
        schedules = self.db.query(Schedule).filter(
            Schedule.user_id == self.user_id,
            Schedule.day_of_week == today
        ).order_by(Schedule.start_time).all()

        if not schedules:
            return """
😌 **Thời gian nghỉ ngơi hôm nay:**

Bạn không có lịch học hôm nay - hoàn toàn tự do!

💡 **Gợi ý hoạt động:**
• Ôn tập các môn đã học
• Thư giãn, tập thể dục
• Chuẩn bị cho các buổi học sắp tới
• Đọc sách hoặc phát triển kỹ năng mới
"""

        response = "😌 **Lịch nghỉ ngơi được đề xuất:**\n\n"

        # Find gaps between classes
        rest_periods = []
        for i in range(len(schedules) - 1):
            end_time = datetime.strptime(schedules[i].end_time, "%H:%M").time()
            start_next = datetime.strptime(schedules[i+1].start_time, "%H:%M").time()

            end_datetime = datetime.combine(now.date(), end_time)
            start_next_datetime = datetime.combine(now.date(), start_next)

            gap = (start_next_datetime - end_datetime).total_seconds() / 60

            if gap >= 30:  # At least 30 min break
                rest_periods.append({
                    'start': schedules[i].end_time,
                    'end': schedules[i+1].start_time,
                    'duration': int(gap)
                })

        if rest_periods:
            for period in rest_periods:
                response += f"• **{period['start']} - {period['end']}** ({period['duration']} phút)\n"
        else:
            response += "⚠️ Lịch học hôm nay khá dày! Hãy cố gắng nghỉ ngơi 5-10 phút giữa các môn.\n"

        response += "\n💡 **Lời khuyên sức khỏe:**\n"
        response += "• Nghỉ 5-10 phút mỗi 50 phút học\n"
        response += "• Uống đủ nước (2-3 lít/ngày)\n"
        response += "• Vận động nhẹ nhàng\n"
        response += "• Ngủ đủ 7-8 tiếng/đêm"

        return response

    def get_performance_analytics(self) -> str:
        """
        Advanced analytics about study performance
        """
        now = datetime.now()

        # Get statistics
        total_schedules = self.db.query(Schedule).filter(
            Schedule.user_id == self.user_id
        ).count()

        total_exams = self.db.query(Exam).filter(
            Schedule.user_id == self.user_id
        ).count()

        activities_this_week = self.db.query(Activity).filter(
            Activity.user_id == self.user_id,
            Activity.timestamp >= now - timedelta(days=7)
        ).count()

        activities_last_week = self.db.query(Activity).filter(
            Activity.user_id == self.user_id,
            Activity.timestamp >= now - timedelta(days=14),
            Activity.timestamp < now - timedelta(days=7)
        ).count()

        # Calculate trend
        if activities_last_week > 0:
            trend = ((activities_this_week - activities_last_week) / activities_last_week) * 100
            trend_emoji = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
            trend_text = f"{trend_emoji} {abs(trend):.1f}% so với tuần trước"
        else:
            trend_text = "🆕 Mới bắt đầu theo dõi"

        response = f"""
📊 **BÁO CÁO HIỆU SUẤT HỌC TẬP**

**📚 Tổng quan:**
• Môn học đang theo dõi: {total_schedules}
• Kỳ thi đã đăng ký: {total_exams}
• Hoạt động tuần này: {activities_this_week}
• Xu hướng: {trend_text}

**⏱️ Phân tích thời gian:**
"""

        # Most studied subjects
        subject_stats = self.db.query(
            Schedule.subject,
            func.count(Schedule.id).label('count')
        ).filter(
            Schedule.user_id == self.user_id
        ).group_by(Schedule.subject).order_by(func.count(Schedule.id).desc()).limit(3).all()

        if subject_stats:
            response += "\n**🏆 Top 3 môn học nhiều nhất:**\n"
            for idx, (subject, count) in enumerate(subject_stats, 1):
                response += f"{idx}. {subject}: {count} buổi/tuần\n"

        # Upcoming exams
        upcoming = self.db.query(Exam).filter(
            Exam.user_id == self.user_id,
            Exam.exam_date >= now
        ).order_by(Exam.exam_date).limit(3).all()

        if upcoming:
            response += "\n**📝 Kỳ thi sắp tới:**\n"
            for exam in upcoming:
                days_left = (exam.exam_date - now).days
                response += f"• {exam.subject} - còn {days_left} ngày\n"

        response += "\n💡 **Đánh giá tổng thể:**\n"

        if activities_this_week >= 10:
            response += "✅ Xuất sắc! Bạn rất chăm chỉ."
        elif activities_this_week >= 5:
            response += "👍 Tốt! Hãy duy trì đà này."
        else:
            response += "💪 Hãy cố gắng hơn nữa!"

        return response

    def format_response(self, response: str, intent: str = None) -> str:
        """
        Format response with professional styling
        """
        # Add intent-specific emojis and formatting
        intent_emojis = {
            'add_schedule': '✅',
            'add_exam': '📝',
            'view_schedule': '📅',
            'view_exams': '🎯',
            'recommendation': '💡',
            'rest_prediction': '😌',
            'analytics': '📊',
            'help': '❓',
            'greeting': '👋',
            'thanks': '😊',
        }

        emoji = intent_emojis.get(intent, '🤖')

        # Add structured formatting if not already formatted
        if not any(marker in response for marker in ['**', '•', '---']):
            response = f"{emoji} {response}"

        return response
