from app.utils.database import execute_query

class Schedule:
    """Schedule model for course schedules."""
    
    def __init__(self, schedule_id=None, course_id=None, day_of_week=None, 
                 start_time=None, end_time=None, room=None):
        self.schedule_id = schedule_id
        self.course_id = course_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.room = room

    @staticmethod
    def get_schedules(course_id=None, day=None):
        """Get schedules with optional filtering."""
        query = """
            SELECT s.id, s.course_id, c.name AS course_name, 
                   s.day_of_week, s.start_time, s.end_time, s.room,
                   u.first_name, u.last_name
            FROM schedules s
            JOIN courses c ON s.course_id = c.id
            JOIN users u ON c.teacher_id = u.id
            WHERE 1=1
        """
        params = []
        
        if course_id:
            query += " AND s.course_id = %s"
            params.append(course_id)
            
        if day:
            query += " AND s.day_of_week = %s"
            params.append(day)
            
        query += " ORDER BY s.day_of_week, s.start_time"
        
        return execute_query(query, tuple(params), fetch=True)

    def save(self):
        """Save or update schedule."""
        if self.schedule_id:
            query = """
                UPDATE schedules 
                SET course_id = %s, day_of_week = %s,
                    start_time = %s, end_time = %s, room = %s
                WHERE id = %s
            """
            params = (self.course_id, self.day_of_week, self.start_time,
                     self.end_time, self.room, self.schedule_id)
        else:
            query = """
                INSERT INTO schedules 
                (course_id, day_of_week, start_time, end_time, room)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (self.course_id, self.day_of_week, self.start_time,
                     self.end_time, self.room)
            
        return execute_query(query, params, commit=True)

    @staticmethod
    def delete(schedule_id):
        """Delete a schedule."""
        query = "DELETE FROM schedules WHERE id = %s"
        return execute_query(query, (schedule_id,), commit=True)
