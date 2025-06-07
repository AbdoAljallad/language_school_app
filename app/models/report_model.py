"""
Report Model
-----------
This module provides functionality for generating and exporting reports.
"""

from app.utils.database import execute_query
import csv
from datetime import datetime

class Report:
    """Report model for generating various system reports."""
    
    @staticmethod
    def generate_report(report_type, start_date, end_date):
        """Generate report data based on type and date range."""
        try:
            if report_type == 'student_enrollment':
                query = """
                    SELECT 
                        c.name as 'Course Name',
                        c.language as Language,
                        c.level as Level,
                        COUNT(sc.student_id) as 'Total Students'
                    FROM courses c
                    LEFT JOIN student_courses sc ON c.id = sc.course_id
                    GROUP BY c.id, c.name, c.language, c.level
                    ORDER BY c.name
                """
                params = ()
            elif report_type == 'course_revenue':
                query = """
                    SELECT 
                        c.name as 'Course Name',
                        COUNT(DISTINCT sc.student_id) as 'Total Students',
                        COALESCE(SUM(p.amount), 0) as 'Revenue'
                    FROM courses c
                    LEFT JOIN student_courses sc ON c.id = sc.course_id
                    LEFT JOIN payments p ON sc.student_id = p.student_id
                    GROUP BY c.id, c.name
                    ORDER BY 'Revenue' DESC
                """
                params = ()
            elif report_type == 'teacher_performance':
                query = """
                    SELECT 
                        CONCAT(u.first_name, ' ', u.last_name) as 'Teacher Name',
                        COUNT(DISTINCT c.id) as 'Courses',
                        COUNT(DISTINCT sc.student_id) as 'Students'
                    FROM users u
                    LEFT JOIN courses c ON u.id = c.teacher_id
                    LEFT JOIN student_courses sc ON c.id = sc.course_id
                    WHERE u.user_type = 'teacher'
                    GROUP BY u.id, u.first_name, u.last_name
                """
                params = ()
            elif report_type == 'student_attendance':
                query = """
                    SELECT 
                        CONCAT(u.first_name, ' ', u.last_name) as 'Student Name',
                        c.name as 'Course Name',
                        COALESCE(COUNT(a.id), 0) as 'Classes Attended'
                    FROM users u
                    JOIN student_courses sc ON u.id = sc.student_id
                    JOIN courses c ON sc.course_id = c.id
                    LEFT JOIN attendance a ON u.id = a.student_id
                    WHERE u.user_type = 'student'
                    GROUP BY u.id, u.first_name, u.last_name, c.id, c.name
                """
                params = ()
            else:  # payment_history
                query = """
                    SELECT 
                        CONCAT(u.first_name, ' ', u.last_name) as 'Student Name',
                        c.name as 'Course Name',
                        COALESCE(p.amount, 0) as 'Amount',
                        COALESCE(p.status, 'Not Paid') as 'Status'
                    FROM users u
                    JOIN student_courses sc ON u.id = sc.student_id
                    JOIN courses c ON sc.course_id = c.id
                    LEFT JOIN payments p ON u.id = p.student_id AND c.id = p.course_id
                    WHERE u.user_type = 'student'
                """
                params = ()

            result = execute_query(query, params, fetch=True)
            
            if not result:
                # Return empty data structure with columns
                empty_data = {
                    'student_enrollment': {'Course Name': '-', 'Language': '-', 'Level': '-', 'Total Students': 0},
                    'course_revenue': {'Course Name': '-', 'Total Students': 0, 'Revenue': 0},
                    'teacher_performance': {'Teacher Name': '-', 'Courses': 0, 'Students': 0},
                    'student_attendance': {'Student Name': '-', 'Course Name': '-', 'Classes Attended': 0},
                    'payment_history': {'Student Name': '-', 'Course Name': '-', 'Amount': 0, 'Status': '-'}
                }
                return [empty_data.get(report_type, {'No Data': '-'})]
            
            return result

        except Exception as e:
            print(f"Error generating report: {str(e)}")
            return []

    @staticmethod
    def export_to_csv(data, filename):
        """Export report data to CSV file."""
        if not data:
            return False
            
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                return True
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
