"""
Course Model
-----------
Represents a course in the system and provides methods for course-related operations.
"""

from app.utils.database import execute_query, execute_transaction
import datetime
from typing import Any

class Course:
    """
    Course model representing a course in the system.
    """
    
    def __init__(self, course_id=None, course_name=None, description=None, 
                 language=None, level=None, price=None, duration_weeks=None, 
                 max_students=None, teacher_id=None, is_active=True):
        """
        Initialize a Course object.
        
        Args:
            course_id (int, optional): Course ID. Defaults to None.
            course_name (str, optional): Course name. Defaults to None.
            description (str, optional): Course description. Defaults to None.
            language (str, optional): Course language. Defaults to None.
            level (str, optional): Course level. Defaults to None.
            price (float, optional): Course price. Defaults to None.
            duration_weeks (int, optional): Course duration in weeks. Defaults to None.
            max_students (int, optional): Maximum number of students. Defaults to None.
            teacher_id (int, optional): Teacher ID. Defaults to None.
            is_active (bool, optional): Whether the course is active. Defaults to True.
        """
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.language = language
        self.level = level
        self.price = price
        self.duration_weeks = duration_weeks
        self.max_students = max_students
        self.teacher_id = teacher_id
        self.is_active = is_active
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Course object from a dictionary.
        
        Args:
            data (dict): Dictionary containing course data.
        
        Returns:
            Course: A Course object.
        """
        return cls(
            course_id=data.get('course_id'),
            course_name=data.get('course_name'),
            description=data.get('description'),
            language=data.get('language'),
            level=data.get('level'),
            price=data.get('price'),
            duration_weeks=data.get('duration_weeks'),
            max_students=data.get('max_students'),
            teacher_id=data.get('teacher_id'),
            is_active=data.get('is_active', True)
        )
    
    def to_dict(self):
        """
        Convert the Course object to a dictionary.
        
        Returns:
            dict: Dictionary representation of the Course object.
        """
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'description': self.description,
            'language': self.language,
            'level': self.level,
            'price': self.price,
            'duration_weeks': self.duration_weeks,
            'max_students': self.max_students,
            'teacher_id': self.teacher_id,
            'is_active': self.is_active
        }
    
    @staticmethod
    def get_by_id(course_id):
        """
        Get a course by ID.
        
        Args:
            course_id (int): Course ID.
        
        Returns:
            Course: Course object if found, None otherwise.
        """
        query = "SELECT * FROM courses WHERE course_id = %s"
        result = execute_query(query, (course_id,), fetch=True)
        
        if result and len(result) > 0:
            return Course.from_dict(result[0])
        return None
    
    @staticmethod
    def get_all(active_only=False):
        """
        Get all courses.
        
        Args:
            active_only (bool, optional): Whether to get only active courses. Defaults to False.
        
        Returns:
            list: List of Course objects.
        """
        if active_only:
            query = "SELECT * FROM courses WHERE is_active = 1"
        else:
            query = "SELECT * FROM courses"
        
        result = execute_query(query, fetch=True)
        
        if result:
            return [Course.from_dict(course_data) for course_data in result]
        return []
    
    @staticmethod
    def get_by_teacher(teacher_id, active_only=False):
        """
        Get courses by teacher ID.
        
        Args:
            teacher_id (int): Teacher ID.
            active_only (bool, optional): Whether to get only active courses. Defaults to False.
        
        Returns:
            list: List of Course objects.
        """
        if active_only:
            query = "SELECT * FROM courses WHERE teacher_id = %s AND is_active = 1"
        else:
            query = "SELECT * FROM courses WHERE teacher_id = %s"
        
        result = execute_query(query, (teacher_id,), fetch=True)
        
        if result:
            return [Course.from_dict(course_data) for course_data in result]
        return []
    
    @staticmethod
    def get_by_language(language, active_only=False):
        """
        Get courses by language.
        
        Args:
            language (str): Course language.
            active_only (bool, optional): Whether to get only active courses. Defaults to False.
        
        Returns:
            list: List of Course objects.
        """
        if active_only:
            query = "SELECT * FROM courses WHERE language = %s AND is_active = 1"
        else:
            query = "SELECT * FROM courses WHERE language = %s"
        
        result = execute_query(query, (language,), fetch=True)
        
        if result:
            return [Course.from_dict(course_data) for course_data in result]
        return []
    
    @staticmethod
    def get_by_level(level, active_only=False):
        """
        Get courses by level.
        
        Args:
            level (str): Course level.
            active_only (bool, optional): Whether to get only active courses. Defaults to False.
        
        Returns:
            list: List of Course objects.
        """
        if active_only:
            query = "SELECT * FROM courses WHERE level = %s AND is_active = 1"
        else:
            query = "SELECT * FROM courses WHERE level = %s"
        
        result = execute_query(query, (level,), fetch=True)
        
        if result:
            return [Course.from_dict(course_data) for course_data in result]
        return []
    
    def save(self):
        """
        Save the course to the database.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        if self.course_id:
            # Update existing course
            query = """
                UPDATE courses 
                SET course_name = %s, description = %s, language = %s, level = %s, 
                    price = %s, duration_weeks = %s, max_students = %s, 
                    teacher_id = %s, is_active = %s, updated_at = CURRENT_TIMESTAMP
                WHERE course_id = %s
            """
            params = (
                self.course_name, self.description, self.language, self.level,
                self.price, self.duration_weeks, self.max_students,
                self.teacher_id, self.is_active, self.course_id
            )
            result = execute_query(query, params, commit=True)
            return result is not None and result > 0
        else:
            # Insert new course
            query = """
                INSERT INTO courses 
                (course_name, description, language, level, price, 
                 duration_weeks, max_students, teacher_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.course_name, self.description, self.language, self.level,
                self.price, self.duration_weeks, self.max_students,
                self.teacher_id, self.is_active
            )
            result = execute_query(query, params, commit=True)
            
            if result is not None and result > 0:
                # Get the last inserted ID
                query = "SELECT LAST_INSERT_ID() as id"
                id_result = execute_query(query, fetch=True)
                
                if id_result and len(id_result) > 0:
                    self.course_id = id_result[0].get('id')
                    return True
            return False
    
    @staticmethod
    def create(course_name, language, level, price, duration_weeks, 
               description=None, max_students=None, teacher_id=None, is_active=True):
        """
        Create a new course.
        
        Args:
            course_name (str): Course name.
            language (str): Course language.
            level (str): Course level.
            price (float): Course price.
            duration_weeks (int): Course duration in weeks.
            description (str, optional): Course description. Defaults to None.
            max_students (int, optional): Maximum number of students. Defaults to None.
            teacher_id (int, optional): Teacher ID. Defaults to None.
            is_active (bool, optional): Whether the course is active. Defaults to True.
        
        Returns:
            Course: Course object if creation succeeds, None otherwise.
        """
        # Insert the new course
        query = """
            INSERT INTO courses 
            (course_name, description, language, level, price, 
             duration_weeks, max_students, teacher_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            course_name, description, language, level, price,
            duration_weeks, max_students, teacher_id, is_active
        )
        result = execute_query(query, params, commit=True)
        
        if result is not None and result > 0:
            # Get the last inserted ID
            query = "SELECT LAST_INSERT_ID() as id"
            id_result = execute_query(query, fetch=True)
            
            if id_result and len(id_result) > 0:
                course_id = id_result[0].get('id')
                return Course.get_by_id(course_id)
        return None
    
    def delete(self):
        """
        Delete the course.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        if not self.course_id:
            return False
        
        query = "DELETE FROM courses WHERE course_id = %s"
        result = execute_query(query, (self.course_id,), commit=True)
        
        return result is not None and result > 0
    
    def get_students(self):
        """
        Get the students enrolled in the course.
        
        Returns:
            list: List of student dictionaries.
        """
        if not self.course_id:
            return []
        
        query = """
            SELECT u.* FROM users u
            JOIN student_courses sc ON u.user_id = sc.student_id
            WHERE sc.course_id = %s
        """
        result = execute_query(query, (self.course_id,), fetch=True)
        
        return result if result else []
    
    def get_lessons(self):
        """
        Get the lessons in the course.
        
        Returns:
            list: List of lesson dictionaries.
        """
        if not self.course_id:
            return []
        
        query = "SELECT * FROM lessons WHERE course_id = %s ORDER BY order_num"
        result = execute_query(query, (self.course_id,), fetch=True)
        
        return result if result else []
    
    def get_schedules(self):
        """
        Get the schedules for the course.
        
        Returns:
            list: List of schedule dictionaries.
        """
        if not self.course_id:
            return []
        
        query = "SELECT * FROM schedules WHERE course_id = %s"
        result = execute_query(query, (self.course_id,), fetch=True)
        
        return result if result else []
    
    def enroll_student(self, student_id):
        """
        Enroll a student in the course.
        
        Args:
            student_id (int): Student ID.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        if not self.course_id:
            return False
        
        # Check if the student is already enrolled
        check_query = "SELECT * FROM student_courses WHERE student_id = %s AND course_id = %s"
        check_result = execute_query(check_query, (student_id, self.course_id), fetch=True)
        
        if check_result and len(check_result) > 0:
            return False  # Student already enrolled
        
        # Enroll the student
        query = """
            INSERT INTO student_courses 
            (student_id, course_id, enrollment_date, status)
            VALUES (%s, %s, CURRENT_TIMESTAMP, 'enrolled')
        """
        result = execute_query(query, (student_id, self.course_id), commit=True)
        
        return result is not None and result > 0
    
    def unenroll_student(self, student_id):
        """
        Unenroll a student from the course.
        
        Args:
            student_id (int): Student ID.
        
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        if not self.course_id:
            return False
        
        query = "DELETE FROM student_courses WHERE student_id = %s AND course_id = %s"
        result = execute_query(query, (student_id, self.course_id), commit=True)
        
        return result is not None and result > 0
    
    def add_lesson(self, lesson_name, description=None, content=None, order_num=None, duration_minutes=None):
        """
        Add a lesson to the course.
        
        Args:
            lesson_name (str): Lesson name.
            description (str, optional): Lesson description. Defaults to None.
            content (str, optional): Lesson content. Defaults to None.
            order_num (int, optional): Lesson order number. Defaults to None.
            duration_minutes (int, optional): Lesson duration in minutes. Defaults to None.
        
        Returns:
            dict: Lesson dictionary if creation succeeds, None otherwise.
        """
        if not self.course_id:
            return None
        
        # If order_num is not provided, set it to the next available number
        if order_num is None:
            query = "SELECT MAX(order_num) as max_order FROM lessons WHERE course_id = %s"
            result = execute_query(query, (self.course_id,), fetch=True)
            
            if result and len(result) > 0 and result[0].get('max_order') is not None:
                order_num = result[0].get('max_order') + 1
            else:
                order_num = 1
        
        # Insert the new lesson
        query = """
            INSERT INTO lessons 
            (course_id, lesson_name, description, content, order_num, duration_minutes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self.course_id, lesson_name, description, content, order_num, duration_minutes
        )
        result = execute_query(query, params, commit=True)
        
        if result is not None and result > 0:
            # Get the last inserted ID
            query = "SELECT LAST_INSERT_ID() as id"
            id_result = execute_query(query, fetch=True)
            
            if id_result and len(id_result) > 0:
                lesson_id = id_result[0].get('id')
                
                # Get the lesson
                query = "SELECT * FROM lessons WHERE lesson_id = %s"
                lesson_result = execute_query(query, (lesson_id,), fetch=True)
                
                if lesson_result and len(lesson_result) > 0:
                    return lesson_result[0]
        return None
    
    def add_schedule(self, day_of_week, start_time, end_time, room=None):
        """
        Add a schedule to the course.

        Args:
            day_of_week (str): Day of the week.
            start_time (str|datetime.time|datetime.timedelta): Start time.
            end_time (str|datetime.time|datetime.timedelta): End time.
            room (str, optional): Room. Defaults to None.

        Returns:
            dict: Schedule dictionary if creation succeeds, None otherwise.
        """
        if not self.course_id:
            return None

        def _time_to_str(t: Any) -> str:
            """Normalize time-like value to 'HH:MM:SS' string."""
            if t is None:
                return ""
            if isinstance(t, datetime.timedelta):
                secs = int(t.total_seconds())
                h = secs // 3600
                m = (secs % 3600) // 60
                s = secs % 60
                return f"{h:02d}:{m:02d}:{s:02d}"
            if isinstance(t, datetime.time):
                return t.strftime("%H:%M:%S")
            if isinstance(t, datetime.datetime):
                return t.time().strftime("%H:%M:%S")
            return str(t)

        def _to_seconds(ts: str) -> int:
            parts = ts.split(":")
            parts = [int(p) for p in parts]
            if len(parts) == 2:
                h, m = parts
                s = 0
            else:
                h, m, s = parts
            return h * 3600 + m * 60 + s

        # normalize times
        start_str = _time_to_str(start_time)
        end_str = _time_to_str(end_time)
        try:
            start_secs = _to_seconds(start_str)
            end_secs = _to_seconds(end_str)
        except Exception:
            raise ValueError("Invalid time format for start_time or end_time")

        if start_secs >= end_secs:
            raise ValueError("start_time must be earlier than end_time")

        # Normalize day_of_week and room for comparisons
        norm_day = str(day_of_week).strip().lower()
        norm_room = None if room is None else str(room).strip()
        room_key = norm_room if norm_room is not None else ""

        # Try parse numeric room for DB int column usage
        room_int = None
        if room_key != "":
            try:
                room_int = int(room_key)
            except Exception:
                room_int = None

        # --- validate room exists in rooms table (DB-level rooms list) ---
        if room_key != "":
            try:
                if room_int is not None:
                    room_check = execute_query("SELECT room_number FROM rooms WHERE room_number = %s", (room_int,), fetch=True)
                else:
                    room_check = execute_query("SELECT room_number FROM rooms WHERE CAST(room_number AS CHAR) = %s", (room_key,), fetch=True)

                if not room_check or len(room_check) == 0:
                    raise ValueError(f"Room '{room}' is not valid. Valid rooms are 101–150 and 201–250.")
            except ValueError:
                raise
            except Exception:
                # If DB/table missing, return explicit error so caller can surface it
                raise ValueError("Room validation failed (rooms table missing or DB error).")
        # --- end room validation ---

        # Ensure we have teacher_id (try DB if missing on object)
        teacher_id = self.teacher_id
        if not teacher_id and self.course_id:
            try:
                r = execute_query("SELECT teacher_id FROM courses WHERE course_id = %s", (self.course_id,), fetch=True)
                if r and len(r) > 0:
                    teacher_id = r[0].get('teacher_id')
            except Exception:
                teacher_id = None

        # Fetch all schedules for the same normalized day to perform robust checks in Python
        candidates = execute_query(
            "SELECT s.*, c.teacher_id as _teacher_id FROM schedules s LEFT JOIN courses c ON s.course_id = c.course_id WHERE LOWER(TRIM(s.day_of_week)) = %s",
            (norm_day,), fetch=True
        ) or []

        def _norm_room_val(v):
            if v is None:
                return ""
            return str(v).strip()

        for cand in candidates:
            try:
                cand_course = cand.get('course_id')
                cand_room = _norm_room_val(cand.get('room'))
                cand_start = _time_to_str(cand.get('start_time'))
                cand_end = _time_to_str(cand.get('end_time'))
                cand_start_secs = _to_seconds(cand_start)
                cand_end_secs = _to_seconds(cand_end)
            except Exception:
                # skip malformed row
                continue

            # Exact duplicate for same course (same start,end,room)
            if cand_course == self.course_id and cand_start_secs == start_secs and cand_end_secs == end_secs and cand_room == room_key:
                raise ValueError("An identical schedule already exists for this course.")

            # Room conflict: same room (empty/null treated same) and overlapping times
            if room_key != "" and cand_room == room_key:
                # overlap if not (candidate ends <= new start or candidate starts >= new end)
                if not (cand_end_secs <= start_secs or cand_start_secs >= end_secs):
                    raise ValueError(f"Room '{room}' is already booked on {day_of_week} at that time.")

            # Teacher conflict: candidate teacher matches and overlapping times
            cand_teacher = cand.get('_teacher_id') or cand.get('teacher_id')
            if teacher_id and cand_teacher and int(cand_teacher) == int(teacher_id):
                if not (cand_end_secs <= start_secs or cand_start_secs >= end_secs):
                    raise ValueError(f"Teacher (id={teacher_id}) has another class on {day_of_week} at that time.")

        # Insert the new schedule
        query = """
            INSERT INTO schedules 
            (course_id, day_of_week, start_time, end_time, room)
            VALUES (%s, %s, %s, %s, %s)
        """
        # Insert room as integer where possible
        insert_room = room_int if room_int is not None else (norm_room if norm_room != "" else None)
        params = (
            self.course_id, day_of_week, start_str, end_str, insert_room
        )
        try:
            result = execute_query(query, params, commit=True)
        except Exception as e:
            # Translate DB errors (FK, trigger SIGNAL, etc.) to ValueError with user-friendly messages
            msg = str(e)
            if "foreign key" in msg.lower() or "referential" in msg.lower():
                raise ValueError("Invalid room: room must be one of the defined rooms (101–150, 201–250).")
            if "Room conflict" in msg or "room conflict" in msg.lower():
                raise ValueError("Room conflict: another schedule uses this room at the same time.")
            if "Teacher conflict" in msg or "teacher conflict" in msg.lower():
                raise ValueError("Teacher conflict: teacher has another class at the same time.")
            # Fallback: raise generic schedule insertion error
            raise ValueError(f"Failed to add schedule: {msg}")

        if result is not None and result > 0:
            # Get the last inserted ID
            query = "SELECT LAST_INSERT_ID() as id"
            id_result = execute_query(query, fetch=True)

            if id_result and len(id_result) > 0:
                schedule_id = id_result[0].get('id')

                # Get the schedule
                query = "SELECT * FROM schedules WHERE schedule_id = %s"
                schedule_result = execute_query(query, (schedule_id,), fetch=True)

                if schedule_result and len(schedule_result) > 0:
                    return schedule_result[0]
        return None