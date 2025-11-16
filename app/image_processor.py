"""
AI Vision Image Processor - Professional Edition
Process images with Gemini Vision to extract schedule information
"""
import base64
from pathlib import Path
from typing import Dict, Any, Optional
import google.generativeai as genai
import os
from datetime import datetime
import re


class ImageProcessor:
    """Process images using Gemini Vision API to extract schedule data"""

    def __init__(self):
        """Initialize Gemini Vision API"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        # Use Gemini Pro Vision model
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_schedule_image(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """
        Analyze image containing schedule information

        Returns:
            {
                'success': bool,
                'type': 'schedule' | 'exam' | 'mixed' | 'unknown',
                'extracted_data': {
                    'schedules': [...],
                    'exams': [...]
                },
                'raw_text': str,
                'confidence': float
            }
        """
        try:
            # Create prompt for schedule extraction
            prompt = """
Phân tích hình ảnh này và trích xuất thông tin lịch học, lịch thi.

**Hãy trích xuất:**
1. **Lịch học** (Class Schedule):
   - Tên môn học
   - Thứ trong tuần (Thứ 2-7, Chủ nhật)
   - Thời gian bắt đầu
   - Thời gian kết thúc
   - Địa điểm (nếu có)

2. **Lịch thi** (Exam Schedule):
   - Tên môn thi
   - Ngày thi (DD/MM/YYYY)
   - Giờ thi
   - Địa điểm thi (nếu có)
   - Ghi chú (nếu có)

**Format trả về (JSON):**
```json
{
    "type": "schedule" hoặc "exam" hoặc "mixed",
    "schedules": [
        {
            "subject": "Tên môn",
            "day_of_week": "Thứ 2" (hoặc số 0-6),
            "start_time": "HH:MM",
            "end_time": "HH:MM",
            "location": "Phòng/Địa điểm"
        }
    ],
    "exams": [
        {
            "subject": "Tên môn",
            "exam_date": "DD/MM/YYYY",
            "exam_time": "HH:MM",
            "location": "Phòng thi",
            "notes": "Ghi chú"
        }
    ],
    "confidence": 0.0-1.0
}
```

**Lưu ý:**
- Nếu không thấy thông tin gì, trả về empty arrays
- Confidence: 1.0 = rất chắc chắn, 0.5 = trung bình, 0.0 = không chắc
- day_of_week: 0=Monday, 1=Tuesday, ..., 6=Sunday
- Chỉ trả về JSON, không giải thích thêm
"""

            # Upload image and generate content
            import PIL.Image
            from io import BytesIO

            image = PIL.Image.open(BytesIO(image_data))

            response = self.model.generate_content([prompt, image])

            # Extract JSON from response
            raw_text = response.text

            # Try to parse JSON from response
            import json

            # Remove markdown code blocks if present
            json_text = raw_text
            if '```json' in json_text:
                json_text = json_text.split('```json')[1].split('```')[0]
            elif '```' in json_text:
                json_text = json_text.split('```')[1].split('```')[0]

            json_text = json_text.strip()

            try:
                extracted_data = json.loads(json_text)
            except json.JSONDecodeError:
                # Fallback: try to extract structured data manually
                extracted_data = self._fallback_extraction(raw_text)

            return {
                'success': True,
                'type': extracted_data.get('type', 'unknown'),
                'extracted_data': extracted_data,
                'raw_text': raw_text,
                'confidence': extracted_data.get('confidence', 0.5)
            }

        except Exception as e:
            return {
                'success': False,
                'type': 'unknown',
                'extracted_data': {'schedules': [], 'exams': []},
                'raw_text': str(e),
                'confidence': 0.0,
                'error': str(e)
            }

    def _fallback_extraction(self, text: str) -> Dict[str, Any]:
        """Fallback method to extract data if JSON parsing fails"""
        return {
            'type': 'unknown',
            'schedules': [],
            'exams': [],
            'confidence': 0.0,
            'note': 'Failed to parse structured data. Raw text available.'
        }

    def process_and_format_response(self, analysis_result: Dict[str, Any]) -> str:
        """
        Format analysis result into user-friendly response
        """
        if not analysis_result['success']:
            return f"❌ **Lỗi xử lý ảnh:**\n{analysis_result.get('error', 'Unknown error')}"

        data = analysis_result['extracted_data']
        confidence = analysis_result['confidence']

        response = "📸 **KẾT QUẢ PHÂN TÍCH ẢNH**\n\n"

        # Add confidence indicator
        if confidence >= 0.8:
            response += "✅ Độ tin cậy: Cao\n\n"
        elif confidence >= 0.5:
            response += "⚠️ Độ tin cậy: Trung bình\n\n"
        else:
            response += "❓ Độ tin cậy: Thấp (vui lòng kiểm tra lại)\n\n"

        # Process schedules
        schedules = data.get('schedules', [])
        if schedules:
            response += "📚 **LỊCH HỌC ĐƯỢC PHÁT HIỆN:**\n\n"
            for idx, schedule in enumerate(schedules, 1):
                response += f"{idx}. **{schedule.get('subject', 'N/A')}**\n"
                response += f"   • Thứ: {schedule.get('day_of_week', 'N/A')}\n"
                response += f"   • Thời gian: {schedule.get('start_time', 'N/A')} - {schedule.get('end_time', 'N/A')}\n"
                if schedule.get('location'):
                    response += f"   • Địa điểm: {schedule['location']}\n"
                response += "\n"

        # Process exams
        exams = data.get('exams', [])
        if exams:
            response += "📝 **LỊCH THI ĐƯỢC PHÁT HIỆN:**\n\n"
            for idx, exam in enumerate(exams, 1):
                response += f"{idx}. **{exam.get('subject', 'N/A')}**\n"
                response += f"   • Ngày thi: {exam.get('exam_date', 'N/A')}\n"
                response += f"   • Giờ thi: {exam.get('exam_time', 'N/A')}\n"
                if exam.get('location'):
                    response += f"   • Địa điểm: {exam['location']}\n"
                if exam.get('notes'):
                    response += f"   • Ghi chú: {exam['notes']}\n"
                response += "\n"

        # If nothing found
        if not schedules and not exams:
            response += "⚠️ Không tìm thấy thông tin lịch học hoặc lịch thi trong ảnh.\n\n"
            response += "**Gợi ý:**\n"
            response += "• Đảm bảo ảnh rõ nét, không bị mờ\n"
            response += "• Ảnh chứa thông tin lịch học/thi bằng tiếng Việt hoặc tiếng Anh\n"
            response += "• Thử chụp lại với ánh sáng tốt hơn\n"
        else:
            response += "💡 **Hành động tiếp theo:**\n"
            response += "• Xem lại thông tin trên có chính xác không\n"
            response += "• Bạn có thể nói 'thêm tất cả lịch trên' để lưu vào hệ thống\n"
            response += "• Hoặc nói 'thêm lịch học số 1' để thêm từng cái\n"

        return response


class ImageUploadHandler:
    """Handle image uploads and storage"""

    def __init__(self, upload_dir: str = "uploads"):
        """Initialize upload handler"""
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

        # Allowed extensions
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

        # Max file size (10MB)
        self.max_file_size = 10 * 1024 * 1024

    def is_allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return Path(filename).suffix.lower() in self.allowed_extensions

    def save_upload(self, file_data: bytes, filename: str) -> Optional[str]:
        """
        Save uploaded file

        Returns:
            Path to saved file or None if failed
        """
        try:
            # Check file size
            if len(file_data) > self.max_file_size:
                raise ValueError(f"File too large. Max size: {self.max_file_size / 1024 / 1024}MB")

            # Check extension
            if not self.is_allowed_file(filename):
                raise ValueError(f"Invalid file type. Allowed: {self.allowed_extensions}")

            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{filename}"
            file_path = self.upload_dir / safe_filename

            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_data)

            return str(file_path)

        except Exception as e:
            print(f"Error saving file: {e}")
            return None

    def cleanup_old_files(self, days: int = 7):
        """Remove uploaded files older than specified days"""
        try:
            import time
            current_time = time.time()
            for file_path in self.upload_dir.glob('*'):
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > days * 86400:  # days to seconds
                        file_path.unlink()
        except Exception as e:
            print(f"Error cleaning up old files: {e}")
