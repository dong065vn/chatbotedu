"""AI Engine for smart recommendations and predictions"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import Schedule, Exam, Activity, User

class AIRecommendationEngine:
    """AI engine for time management recommendations"""

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def predict_rest_times(self, date: datetime = None) -> List[Dict[str, Any]]:
        """
        Dự đoán thời gian nghỉ ngơi dựa trên lịch học
        Predict rest times based on class schedule
        """
        if date is None:
            date = datetime.now()

        day_of_week = date.weekday()

        # Get schedules for the day
        schedules = self.db.query(Schedule).filter(
            Schedule.user_id == self.user_id,
            Schedule.day_of_week == day_of_week
        ).order_by(Schedule.start_time).all()

        rest_recommendations = []

        if not schedules:
            return [{
                "time": "09:00-12:00",
                "reason": "Không có lịch học, đây là thời gian tốt để tự học",
                "duration_minutes": 180,
                "type": "study"
            }]

        # Analyze gaps between classes
        for i in range(len(schedules) - 1):
            current_end = self._time_to_minutes(schedules[i].end_time)
            next_start = self._time_to_minutes(schedules[i + 1].start_time)
            gap = next_start - current_end

            if gap >= 30:  # Gap of at least 30 minutes
                rest_time = self._minutes_to_time(current_end + 5)

                if gap >= 90:
                    rest_recommendations.append({
                        "time": f"{rest_time}",
                        "reason": "Khoảng trống dài, nên nghỉ ngơi hoặc ăn nhẹ",
                        "duration_minutes": min(gap - 10, 60),
                        "type": "rest_or_meal"
                    })
                elif gap >= 45:
                    rest_recommendations.append({
                        "time": f"{rest_time}",
                        "reason": "Nghỉ ngơi ngắn giữa các buổi học",
                        "duration_minutes": 20,
                        "type": "short_rest"
                    })

        # Add lunch time if no class during 11:30-13:00
        lunch_overlap = any(
            self._time_overlap(s.start_time, s.end_time, "11:30", "13:00")
            for s in schedules
        )

        if not lunch_overlap:
            rest_recommendations.append({
                "time": "12:00-13:00",
                "reason": "Thời gian ăn trưa lý tưởng",
                "duration_minutes": 60,
                "type": "lunch"
            })

        # Add dinner time if no class during 18:00-19:30
        dinner_overlap = any(
            self._time_overlap(s.start_time, s.end_time, "18:00", "19:30")
            for s in schedules
        )

        if not dinner_overlap:
            rest_recommendations.append({
                "time": "18:30-19:30",
                "reason": "Thời gian ăn tối",
                "duration_minutes": 60,
                "type": "dinner"
            })

        return rest_recommendations

    def recommend_study_times(self, subject: str = None) -> List[Dict[str, Any]]:
        """
        Tư vấn thời gian học hiệu quả
        Recommend effective study times
        """
        recommendations = []

        # Get upcoming exams
        upcoming_exams = self.db.query(Exam).filter(
            Exam.user_id == self.user_id,
            Exam.exam_date >= datetime.now(),
            Exam.exam_date <= datetime.now() + timedelta(days=30)
        ).order_by(Exam.exam_date).all()

        for exam in upcoming_exams:
            days_until_exam = (exam.exam_date - datetime.now()).days

            if days_until_exam <= 3:
                priority = "cao"
                suggestion = f"Ôn tập tích cực {exam.subject} - còn {days_until_exam} ngày!"
                study_hours = 3
            elif days_until_exam <= 7:
                priority = "trung bình"
                suggestion = f"Bắt đầu ôn tập {exam.subject} - còn {days_until_exam} ngày"
                study_hours = 2
            else:
                priority = "thấp"
                suggestion = f"Lên kế hoạch ôn tập {exam.subject}"
                study_hours = 1

            recommendations.append({
                "subject": exam.subject,
                "priority": priority,
                "suggestion": suggestion,
                "recommended_hours_per_day": study_hours,
                "exam_date": exam.exam_date.strftime("%d/%m/%Y %H:%M"),
                "days_remaining": days_until_exam
            })

        # General study time recommendations
        optimal_times = [
            {
                "time_range": "06:00-08:00",
                "effectiveness": "Cao",
                "reason": "Đầu óc tỉnh táo sau khi ngủ dậy",
                "recommended_for": "Học các môn khó, ghi nhớ kiến thức mới"
            },
            {
                "time_range": "09:00-11:00",
                "effectiveness": "Cao",
                "reason": "Khả năng tập trung tốt",
                "recommended_for": "Làm bài tập, thực hành"
            },
            {
                "time_range": "15:00-17:00",
                "effectiveness": "Trung bình",
                "reason": "Sau giấc ngủ trưa",
                "recommended_for": "Ôn tập, đọc tài liệu"
            },
            {
                "time_range": "20:00-22:00",
                "effectiveness": "Trung bình",
                "reason": "Thời gian tự học buổi tối",
                "recommended_for": "Tổng hợp kiến thức, làm bài tập"
            }
        ]

        return {
            "exam_priorities": recommendations,
            "optimal_study_times": optimal_times
        }

    def analyze_study_patterns(self) -> Dict[str, Any]:
        """
        Phân tích thói quen học tập
        Analyze study patterns
        """
        # Get activities from last 7 days
        week_ago = datetime.now() - timedelta(days=7)
        activities = self.db.query(Activity).filter(
            Activity.user_id == self.user_id,
            Activity.created_at >= week_ago
        ).all()

        study_time = sum(
            a.duration for a in activities
            if a.activity_type == "study" and a.duration
        ) or 0

        rest_time = sum(
            a.duration for a in activities
            if a.activity_type == "rest" and a.duration
        ) or 0

        avg_study_per_day = study_time / 7

        # Recommendations based on patterns
        feedback = []

        if avg_study_per_day < 120:  # Less than 2 hours per day
            feedback.append({
                "type": "warning",
                "message": "Thời gian học tập còn ít. Nên tăng lên ít nhất 3-4 giờ/ngày."
            })
        elif avg_study_per_day > 480:  # More than 8 hours per day
            feedback.append({
                "type": "warning",
                "message": "Học quá nhiều có thể gây mệt mỏi. Hãy cân bằng với nghỉ ngơi."
            })
        else:
            feedback.append({
                "type": "success",
                "message": "Thời gian học tập hợp lý!"
            })

        if study_time > 0 and rest_time / study_time < 0.2:
            feedback.append({
                "type": "warning",
                "message": "Bạn cần nghỉ ngơi nhiều hơn. Tỷ lệ lý tưởng là 20-30 phút nghỉ/2h học."
            })

        return {
            "total_study_minutes": study_time,
            "total_rest_minutes": rest_time,
            "average_study_per_day": round(avg_study_per_day, 1),
            "study_rest_ratio": round(rest_time / study_time, 2) if study_time > 0 else 0,
            "feedback": feedback
        }

    def get_daily_schedule_summary(self, date: datetime = None) -> Dict[str, Any]:
        """
        Tóm tắt lịch trình trong ngày
        Get daily schedule summary
        """
        if date is None:
            date = datetime.now()

        day_of_week = date.weekday()
        day_names = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]

        # Get schedules
        schedules = self.db.query(Schedule).filter(
            Schedule.user_id == self.user_id,
            Schedule.day_of_week == day_of_week
        ).order_by(Schedule.start_time).all()

        # Get exams today
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        exams = self.db.query(Exam).filter(
            Exam.user_id == self.user_id,
            Exam.exam_date >= start_of_day,
            Exam.exam_date < end_of_day
        ).all()

        schedule_list = [
            {
                "subject": s.subject,
                "time": f"{s.start_time} - {s.end_time}",
                "location": s.location or "Chưa cập nhật"
            }
            for s in schedules
        ]

        exam_list = [
            {
                "subject": e.subject,
                "time": e.exam_date.strftime("%H:%M"),
                "location": e.location or "Chưa cập nhật"
            }
            for e in exams
        ]

        return {
            "date": date.strftime("%d/%m/%Y"),
            "day_of_week": day_names[day_of_week],
            "classes": schedule_list,
            "exams": exam_list,
            "total_classes": len(schedule_list),
            "has_exams": len(exam_list) > 0
        }

    # Helper methods
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert HH:MM to minutes since midnight"""
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes

    def _minutes_to_time(self, minutes: int) -> str:
        """Convert minutes since midnight to HH:MM"""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"

    def _time_overlap(self, start1: str, end1: str, start2: str, end2: str) -> bool:
        """Check if two time ranges overlap"""
        s1 = self._time_to_minutes(start1)
        e1 = self._time_to_minutes(end1)
        s2 = self._time_to_minutes(start2)
        e2 = self._time_to_minutes(end2)

        return not (e1 <= s2 or e2 <= s1)
