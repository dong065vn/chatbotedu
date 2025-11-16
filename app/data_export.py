"""
Professional Data Export/Import Module
Support for JSON, CSV, and backup/restore functionality
"""
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
from io import StringIO
from sqlalchemy.orm import Session

from app.models import User, Schedule, Exam, Activity, ChatHistory


class DataExporter:
    """Professional data export and import handler"""

    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id

    def export_all_data(self, format: str = 'json') -> str:
        """
        Export all user data in specified format
        Formats: 'json', 'csv'
        """
        if format == 'json':
            return self._export_json()
        elif format == 'csv':
            return self._export_csv()
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_json(self) -> str:
        """Export data as JSON"""
        data = {
            'export_date': datetime.now().isoformat(),
            'user_id': self.user_id,
            'version': '3.0',
            'schedules': self._get_schedules_data(),
            'exams': self._get_exams_data(),
            'activities': self._get_activities_data(),
            'chat_history': self._get_chat_history_data(),
            'statistics': self._get_statistics()
        }

        return json.dumps(data, ensure_ascii=False, indent=2)

    def _export_csv(self) -> Dict[str, str]:
        """Export data as multiple CSV files"""
        return {
            'schedules.csv': self._schedules_to_csv(),
            'exams.csv': self._exams_to_csv(),
            'activities.csv': self._activities_to_csv()
        }

    def _get_schedules_data(self) -> List[Dict]:
        """Get all schedules as dict list"""
        schedules = self.db.query(Schedule).filter(
            Schedule.user_id == self.user_id
        ).all()

        return [
            {
                'id': s.id,
                'subject': s.subject,
                'day_of_week': s.day_of_week,
                'start_time': s.start_time,
                'end_time': s.end_time,
                'location': s.location,
                'created_at': s.created_at.isoformat() if s.created_at else None
            }
            for s in schedules
        ]

    def _get_exams_data(self) -> List[Dict]:
        """Get all exams as dict list"""
        exams = self.db.query(Exam).filter(
            Exam.user_id == self.user_id
        ).all()

        return [
            {
                'id': e.id,
                'subject': e.subject,
                'exam_date': e.exam_date.isoformat(),
                'exam_time': e.exam_time,
                'location': e.location,
                'notes': e.notes,
                'created_at': e.created_at.isoformat() if e.created_at else None
            }
            for e in exams
        ]

    def _get_activities_data(self) -> List[Dict]:
        """Get all activities as dict list"""
        activities = self.db.query(Activity).filter(
            Activity.user_id == self.user_id
        ).all()

        return [
            {
                'id': a.id,
                'activity_type': a.activity_type,
                'description': a.description,
                'timestamp': a.timestamp.isoformat()
            }
            for a in activities
        ]

    def _get_chat_history_data(self) -> List[Dict]:
        """Get chat history (limited to last 100)"""
        history = self.db.query(ChatHistory).filter(
            ChatHistory.user_id == self.user_id
        ).order_by(ChatHistory.timestamp.desc()).limit(100).all()

        return [
            {
                'message': h.message,
                'response': h.response,
                'timestamp': h.timestamp.isoformat()
            }
            for h in reversed(history)  # Reverse to chronological order
        ]

    def _get_statistics(self) -> Dict[str, Any]:
        """Get summary statistics"""
        return {
            'total_schedules': self.db.query(Schedule).filter(
                Schedule.user_id == self.user_id
            ).count(),
            'total_exams': self.db.query(Exam).filter(
                Exam.user_id == self.user_id
            ).count(),
            'total_activities': self.db.query(Activity).filter(
                Activity.user_id == self.user_id
            ).count(),
            'total_conversations': self.db.query(ChatHistory).filter(
                ChatHistory.user_id == self.user_id
            ).count()
        }

    def _schedules_to_csv(self) -> str:
        """Convert schedules to CSV"""
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(['Subject', 'Day of Week', 'Start Time', 'End Time', 'Location'])

        # Data
        schedules = self.db.query(Schedule).filter(
            Schedule.user_id == self.user_id
        ).all()

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for s in schedules:
            writer.writerow([
                s.subject,
                day_names[s.day_of_week],
                s.start_time,
                s.end_time,
                s.location or ''
            ])

        return output.getvalue()

    def _exams_to_csv(self) -> str:
        """Convert exams to CSV"""
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(['Subject', 'Exam Date', 'Exam Time', 'Location', 'Notes'])

        # Data
        exams = self.db.query(Exam).filter(
            Exam.user_id == self.user_id
        ).all()

        for e in exams:
            writer.writerow([
                e.subject,
                e.exam_date.strftime('%Y-%m-%d'),
                e.exam_time,
                e.location or '',
                e.notes or ''
            ])

        return output.getvalue()

    def _activities_to_csv(self) -> str:
        """Convert activities to CSV"""
        output = StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(['Type', 'Description', 'Timestamp'])

        # Data
        activities = self.db.query(Activity).filter(
            Activity.user_id == self.user_id
        ).all()

        for a in activities:
            writer.writerow([
                a.activity_type,
                a.description,
                a.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])

        return output.getvalue()

    def import_from_json(self, json_data: str) -> Dict[str, Any]:
        """
        Import data from JSON
        Returns: {
            'success': bool,
            'imported': dict,
            'errors': list
        }
        """
        try:
            data = json.loads(json_data)
            imported = {'schedules': 0, 'exams': 0}
            errors = []

            # Import schedules
            if 'schedules' in data:
                for sched_data in data['schedules']:
                    try:
                        schedule = Schedule(
                            user_id=self.user_id,
                            subject=sched_data['subject'],
                            day_of_week=sched_data['day_of_week'],
                            start_time=sched_data['start_time'],
                            end_time=sched_data['end_time'],
                            location=sched_data.get('location')
                        )
                        self.db.add(schedule)
                        imported['schedules'] += 1
                    except Exception as e:
                        errors.append(f"Schedule import error: {str(e)}")

            # Import exams
            if 'exams' in data:
                for exam_data in data['exams']:
                    try:
                        exam = Exam(
                            user_id=self.user_id,
                            subject=exam_data['subject'],
                            exam_date=datetime.fromisoformat(exam_data['exam_date']),
                            exam_time=exam_data['exam_time'],
                            location=exam_data.get('location'),
                            notes=exam_data.get('notes')
                        )
                        self.db.add(exam)
                        imported['exams'] += 1
                    except Exception as e:
                        errors.append(f"Exam import error: {str(e)}")

            self.db.commit()

            return {
                'success': len(errors) == 0,
                'imported': imported,
                'errors': errors
            }

        except json.JSONDecodeError as e:
            return {
                'success': False,
                'imported': {},
                'errors': [f"Invalid JSON format: {str(e)}"]
            }
        except Exception as e:
            self.db.rollback()
            return {
                'success': False,
                'imported': {},
                'errors': [f"Import failed: {str(e)}"]
            }

    def create_backup(self) -> str:
        """Create a full backup of user data"""
        return self._export_json()

    def restore_from_backup(self, backup_data: str) -> Dict[str, Any]:
        """Restore data from backup"""
        # First, clear existing data (optional - be careful!)
        # Then import
        return self.import_from_json(backup_data)
