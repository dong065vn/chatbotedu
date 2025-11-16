"""Gemini AI Integration for intelligent chatbot responses"""
import os
import google.generativeai as genai
from typing import Optional, Dict, Any
from datetime import datetime

class GeminiAI:
    """Gemini AI wrapper for chatbot intelligence"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini AI with API key"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please set it in .env file or environment variables."
            )

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # Use Gemini Pro model
        self.model = genai.GenerativeModel('gemini-pro')

        # System prompt for the chatbot
        self.system_prompt = """Bạn là trợ lý AI quản lý thời gian học tập thông minh cho sinh viên.

Vai trò của bạn:
- Giúp sinh viên quản lý lịch học, lịch thi hiệu quả
- Tư vấn thời gian học tập tối ưu
- Đề xuất thời gian nghỉ ngơi và ăn uống hợp lý
- Phân tích và cải thiện thói quen học tập
- Động viên và hỗ trợ tinh thần cho sinh viên

Phong cách giao tiếp:
- Thân thiện, nhiệt tình, dễ hiểu
- Sử dụng tiếng Việt tự nhiên
- Emoji phù hợp để tạo sự gần gũi
- Ngắn gọn, súc tích nhưng đầy đủ thông tin
- Luôn khích lệ và tích cực

Nguyên tắc:
- Ưu tiên sức khỏe và cân bằng trong học tập
- Không khuyến khích học quá sức
- Nhấn mạnh tầm quan trọng của nghỉ ngơi
- Cá nhân hóa theo nhu cầu từng sinh viên"""

    def generate_response(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate intelligent response using Gemini

        Args:
            user_message: User's message
            context: Additional context (schedule, exams, etc.)

        Returns:
            Generated response from Gemini
        """
        try:
            # Build the full prompt with context
            prompt = self._build_prompt(user_message, context)

            # Generate response
            response = self.model.generate_content(prompt)

            return response.text

        except Exception as e:
            print(f"Gemini AI Error: {str(e)}")
            return self._fallback_response(user_message)

    def _build_prompt(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build complete prompt with system prompt and context"""

        prompt_parts = [self.system_prompt, "\n\n"]

        # Add context if available
        if context:
            prompt_parts.append("THÔNG TIN HIỆN TẠI:\n")

            # Add schedule context
            if context.get('schedules'):
                prompt_parts.append("\nLịch học:\n")
                for schedule in context['schedules']:
                    prompt_parts.append(
                        f"- {schedule['subject']}: "
                        f"{schedule['day_of_week']}, "
                        f"{schedule['start_time']}-{schedule['end_time']}\n"
                    )

            # Add exam context
            if context.get('exams'):
                prompt_parts.append("\nLịch thi sắp tới:\n")
                for exam in context['exams']:
                    prompt_parts.append(
                        f"- {exam['subject']}: "
                        f"{exam['exam_date']}\n"
                    )

            # Add analysis context
            if context.get('study_analysis'):
                analysis = context['study_analysis']
                prompt_parts.append(
                    f"\nPhân tích học tập (7 ngày qua):\n"
                    f"- Thời gian học trung bình: {analysis.get('avg_study_per_day', 0)} phút/ngày\n"
                    f"- Tỷ lệ nghỉ/học: {analysis.get('study_rest_ratio', 0)}\n"
                )

            # Add current date/time
            now = datetime.now()
            prompt_parts.append(
                f"\nThời gian hiện tại: {now.strftime('%H:%M, %d/%m/%Y')}\n"
            )

            prompt_parts.append("\n---\n\n")

        # Add user message
        prompt_parts.append(f"SINH VIÊN HỎI: {user_message}\n\n")
        prompt_parts.append("TRẢ LỜI (ngắn gọn, thân thiện, có emoji phù hợp):")

        return "".join(prompt_parts)

    def _fallback_response(self, user_message: str) -> str:
        """Fallback response when Gemini fails"""
        return """Xin lỗi, tôi đang gặp chút vấn đề kỹ thuật.

Bạn có thể thử:
• "Lịch học hôm nay"
• "Lịch thi sắp tới"
• "Tư vấn thời gian học"
• "Khi nào nên nghỉ ngơi?"

Hoặc gõ "trợ giúp" để xem hướng dẫn đầy đủ."""

    def analyze_intent(self, message: str) -> Dict[str, Any]:
        """
        Analyze user intent using Gemini

        Returns dict with:
        - intent: Type of request (schedule, exam, advice, etc.)
        - confidence: Confidence score
        - entities: Extracted entities (subject, time, date, etc.)
        """
        try:
            prompt = f"""Phân tích ý định của câu hỏi sau:
"{message}"

Trả về JSON với format:
{{
    "intent": "schedule_add|schedule_view|exam_add|exam_view|advice_study|advice_rest|analysis|greeting|help|unknown",
    "confidence": 0.0-1.0,
    "entities": {{
        "subject": "tên môn học (nếu có)",
        "day": "thứ mấy (nếu có)",
        "time": "thời gian (nếu có)",
        "date": "ngày tháng (nếu có)"
    }}
}}

Chỉ trả về JSON, không giải thích."""

            response = self.model.generate_content(prompt)

            # Parse JSON response
            import json
            result = json.loads(response.text.strip())
            return result

        except Exception as e:
            print(f"Intent analysis error: {str(e)}")
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": {}
            }

    def personalized_advice(
        self,
        student_data: Dict[str, Any]
    ) -> str:
        """
        Generate personalized study advice based on student data
        """
        try:
            prompt = f"""Dựa trên dữ liệu sau của sinh viên, hãy đưa ra lời khuyên cá nhân hóa:

Thời gian học trung bình: {student_data.get('avg_study_hours', 0)} giờ/ngày
Số môn thi sắp tới: {student_data.get('upcoming_exams', 0)}
Tỷ lệ nghỉ/học: {student_data.get('rest_ratio', 0)}
Thói quen học: {student_data.get('study_pattern', 'chưa rõ')}

Hãy đưa ra 3-4 lời khuyên cụ thể, thiết thực để cải thiện hiệu quả học tập.
Sử dụng emoji phù hợp và giọng điệu thân thiện, khích lệ."""

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            print(f"Personalized advice error: {str(e)}")
            return "Hãy cố gắng duy trì thói quen học tập đều đặn và nhớ nghỉ ngơi hợp lý nhé! 💪"

# Global instance (optional)
_gemini_instance = None

def get_gemini_ai(api_key: Optional[str] = None) -> GeminiAI:
    """Get or create Gemini AI instance"""
    global _gemini_instance

    if _gemini_instance is None:
        _gemini_instance = GeminiAI(api_key)

    return _gemini_instance
