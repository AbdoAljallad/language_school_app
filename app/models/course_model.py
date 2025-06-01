"""
Course Model
-----------
Represents a course in the system and provides methods for course-related operations.
"""

from app.utils.database import execute_query, execute_transaction

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
            start_time (str): Start time.
            end_time (str): End time.
            room (str, optional): Room. Defaults to None.
        
        Returns:
            dict: Schedule dictionary if creation succeeds, None otherwise.
        """
        if not self.course_id:
            return None
        
        # Insert the new schedule
        query = """
            INSERT INTO schedules 
            (course_id, day_of_week, start_time, end_time, room)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            self.course_id, day_of_week, start_time, end_time, room
        )
        result = execute_query(query, params, commit=True)
        
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