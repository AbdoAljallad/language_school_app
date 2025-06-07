"""
Teacher Dashboard View
-------------------
This module contains the TeacherDashboardView class, which implements the teacher dashboard
functionality for the Language School Management System.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QTextEdit, 
    QPushButton, QDialogButtonBox, QListWidgetItem, QWidget
)
from PyQt5.QtCore import Qt, pyqtSlot, QDate, pyqtSignal

from app.ui.generated.teacher_dashboard_ui import Ui_TeacherDashboard
from app.views.dashboard_view import BaseDashboardView
from app.models.user_model import User
from app.models.course_model import Course
from app.utils.database import execute_query, get_connection, database


class TeacherDashboardView(BaseDashboardView):
    """Teacher dashboard view class."""
    
    # Define signal as class variable
    profile_updated = pyqtSignal()
    
    """
    Teacher dashboard view class.
    
    This class implements the teacher dashboard functionality, including:
    - Course management
    - Lesson management
    - Student management
    - Attendance tracking
    - Grading
    - Messaging
    """
    
    def __init__(self, user, parent=None):
        """Initialize the teacher dashboard view."""
        # Initialize base class first  
        super().__init__(user, parent)
        self.ui = Ui_TeacherDashboard()
        self.ui.setupUi(self)
        
        # Set welcome message
        self.ui.welcomeLabel.setText(f"Welcome, {self.user.first_name} {self.user.last_name}")
        
        # Connect signals and slots
        self.ui.logoutButton.clicked.connect(self.handle_logout)
        self.ui.actionLogout.triggered.connect(self.handle_logout)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionRefresh.triggered.connect(self.refresh_data)
        
        # Connect profile signals
        self.ui.profileButton.clicked.connect(self.open_profile_dialog)
        self.ui.actionProfile.triggered.connect(self.open_profile_dialog)
        self.profile_updated.connect(self.on_profile_updated)
        
        # Connect tab-specific signals and slots
        
        # Courses tab
        # Note: Using studentSearchInput for search functionality as courseSearchInput doesn't exist
        # self.ui.courseSearchInput.textChanged.connect(self.filter_courses)
        # self.ui.courseLanguageFilterComboBox.currentIndexChanged.connect(self.filter_courses)
        # self.ui.courseLevelFilterComboBox.currentIndexChanged.connect(self.filter_courses)
        
        # Lessons tab
        self.ui.courseFilterComboBox.currentIndexChanged.connect(self.filter_lessons)
        self.ui.addLessonButton.clicked.connect(self.add_lesson)
        
        # Students tab
        self.ui.studentSearchInput.textChanged.connect(self.filter_students)
        self.ui.studentCourseFilterComboBox.currentIndexChanged.connect(self.filter_students)
        
        # Attendance tab
        self.ui.attendanceCourseFilterComboBox.currentIndexChanged.connect(self.filter_attendance)
        self.ui.attendanceDateEdit.dateChanged.connect(self.filter_attendance)
        self.ui.saveAttendanceButton.clicked.connect(self.save_attendance)
        
        # Grades tab
        self.ui.gradesCourseFilterComboBox.currentIndexChanged.connect(self.filter_grades)
        self.ui.gradesTypeFilterComboBox.currentIndexChanged.connect(self.filter_grades)
        self.ui.saveGradesButton.clicked.connect(self.save_grades)
        
        # Messages tab
        self.ui.chatsList.currentItemChanged.connect(self.load_messages)
        self.ui.sendMessageButton.clicked.connect(self.send_message)
        self.ui.newChatButton.clicked.connect(self.new_chat)
        
        # Set current date for attendance
        self.ui.attendanceDateEdit.setDate(QDate.currentDate())
        
        # Initialize data
        self.refresh_data()
        
        # Show status message
        self.ui.statusbar.showMessage("Ready")
        
    def refresh_data(self):
        """Refresh all data in the dashboard."""
        self.load_courses()
        self.load_course_filter_combos()
        self.load_lessons()
        self.load_students()
        self.load_attendance()
        self.load_grades()
        self.load_chats()
        
    def load_courses(self):
        """Load courses taught by the teacher into the courses table."""
        # Clear the table
        self.ui.coursesTable.setRowCount(0)
        
        # Initialize search text and filters
        search_text = ""  # No search text input in current UI
        language_filter = None
        level_filter = None
        
        # Get courses taught by the teacher
        db = database()
        query = """
            SELECT id, name, language, level, description, price, active
            FROM courses
            WHERE teacher_id = %s
        """
        params = (self.user.user_id,)
        
        # Apply filters
        where_clauses = ["teacher_id = %s"]
        
        if language_filter:
            where_clauses.append("language = %s")
            params = params + (language_filter,)
            
        if level_filter:
            where_clauses.append("level = %s")
            params = params + (level_filter,)
            
        query = "SELECT id, name, language, level, description, price, active FROM courses WHERE " + " AND ".join(where_clauses)
        
        courses = db.fetch_all(query, params)
        
        # Populate the table
        row = 0
        for course in courses:
            # Apply search filter
            if search_text and not (
                search_text in course["name"].lower() or  # name
                search_text in course["description"].lower()     # description
            ):
                continue
                
            self.ui.coursesTable.insertRow(row)
            
            # Add course data
            self.ui.coursesTable.setItem(row, 0, QTableWidgetItem(str(course["id"])))
            self.ui.coursesTable.setItem(row, 1, QTableWidgetItem(course["name"]))
            self.ui.coursesTable.setItem(row, 2, QTableWidgetItem(course["language"]))
            self.ui.coursesTable.setItem(row, 3, QTableWidgetItem(course["level"]))
            self.ui.coursesTable.setItem(row, 4, QTableWidgetItem(course["description"]))
            self.ui.coursesTable.setItem(row, 5, QTableWidgetItem(f"${course['price']:.2f}"))
            self.ui.coursesTable.setItem(row, 6, QTableWidgetItem("Yes" if course["active"] else "No"))
            
            # Get student count
            query = """
                SELECT COUNT(*) FROM student_courses
                WHERE course_id = %s AND active = 1
            """
            params = (course["id"],)
            result = db.fetch_one(query, params)
            student_count = result["COUNT(*)"] if result else 0
            
            self.ui.coursesTable.setItem(row, 7, QTableWidgetItem(str(student_count)))
            
            # Add action buttons
            view_button = QPushButton("View Details")
            view_button.setProperty("course_id", course["id"])
            view_button.clicked.connect(lambda checked, cid=course["id"]: self.view_course_details(cid))
            
            # Create a widget to hold the buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(view_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.ui.coursesTable.setCellWidget(row, 8, actions_widget)
            
            row += 1
            
        # Resize columns to content
        self.ui.coursesTable.resizeColumnsToContents()
        
    def filter_courses(self):
        """Filter courses based on search text and filters."""
        self.load_courses()
        
    def view_course_details(self, course_id):
        """View details of a course."""
        # Get course data
        db = database()
        query = """
            SELECT name, language, level, description, price, active
            FROM courses
            WHERE id = %s
        """
        params = (course_id,)
        course = db.fetch_one(query, params)
        
        if not course:
            QMessageBox.warning(self, "Error", "Course not found.")
            return
            
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Course Details: {course['name']}")
        dialog.setMinimumWidth(500)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add course details
        details_layout = QVBoxLayout()
        
        # Course name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setMinimumWidth(100)
        name_value = QLabel(course['name'])
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_value)
        details_layout.addLayout(name_layout)
        
        # Language
        language_layout = QHBoxLayout()
        language_label = QLabel("Language:")
        language_label.setMinimumWidth(100)
        language_value = QLabel(course['language'])
        language_layout.addWidget(language_label)
        language_layout.addWidget(language_value)
        details_layout.addLayout(language_layout)
        
        # Level
        level_layout = QHBoxLayout()
        level_label = QLabel("Level:")
        level_label.setMinimumWidth(100)
        level_value = QLabel(course['level'])
        level_layout.addWidget(level_label)
        level_layout.addWidget(level_value)
        details_layout.addLayout(level_layout)
        
        # Description
        description_layout = QHBoxLayout()
        description_label = QLabel("Description:")
        description_label.setMinimumWidth(100)
        description_value = QLabel(course['description'])
        description_value.setWordWrap(True)
        description_layout.addWidget(description_label)
        description_layout.addWidget(description_value)
        details_layout.addLayout(description_layout)
        
        # Price
        price_layout = QHBoxLayout()
        price_label = QLabel("Price:")
        price_label.setMinimumWidth(100)
        price_value = QLabel(f"${course['price']:.2f}")
        price_layout.addWidget(price_label)
        price_layout.addWidget(price_value)
        details_layout.addLayout(price_layout)
        
        # Active
        active_layout = QHBoxLayout()
        active_label = QLabel("Active:")
        active_label.setMinimumWidth(100)
        active_value = QLabel("Yes" if course['active'] else "No")
        active_layout.addWidget(active_label)
        active_layout.addWidget(active_value)
        details_layout.addLayout(active_layout)
        
        layout.addLayout(details_layout)
        
        # Add student list
        students_label = QLabel("Enrolled Students:")
        layout.addWidget(students_label)
        
        # Get enrolled students
        query = """
            SELECT u.id, u.first_name, u.last_name, u.email, sc.enrollment_date
            FROM users u
            JOIN student_courses sc ON u.id = sc.student_id
            WHERE sc.course_id = %s AND sc.active = 1
            ORDER BY u.last_name, u.first_name
        """
        params = (course_id,)
        students = db.fetch_all(query, params)
        
        # Create table for students
        from PyQt5.QtWidgets import QTableWidget
        students_table = QTableWidget()
        students_table.setColumnCount(4)
        students_table.setHorizontalHeaderLabels(["Name", "Email", "Enrollment Date", "Actions"])
        
        # Populate table
        for row, student in enumerate(students):
            students_table.insertRow(row)
            
            # Add student data
            students_table.setItem(row, 0, QTableWidgetItem(f"{student["first_name"]} {student["last_name"]}"))
            students_table.setItem(row, 1, QTableWidgetItem(student[3]))
            students_table.setItem(row, 2, QTableWidgetItem(student[4]))
            
            # Add action button
            message_button = QPushButton("Message")
            message_button.setProperty("student_id", student["id"])
            message_button.clicked.connect(lambda checked, sid=student["id"], sname=f"{student["first_name"]} {student["last_name"]}": self.message_student(sid, sname))
            
            # Create a widget to hold the button
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(message_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            students_table.setCellWidget(row, 3, actions_widget)
            
        # Resize columns to content
        students_table.resizeColumnsToContents()
        
        layout.addWidget(students_table)
        
        # Add close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.reject)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        # Show dialog
        dialog.exec_()
        
    def load_course_filter_combos(self):
        """Load course filter combo boxes with the teacher's courses."""
        # Get courses taught by the teacher
        db = database()
        query = """
            SELECT id, name
            FROM courses
            WHERE teacher_id = %s AND active = 1
            ORDER BY name
        """
        params = (self.user.user_id,)
        courses = db.fetch_all(query, params)
        
        # Clear and repopulate combo boxes
        for combo in [
            self.ui.courseFilterComboBox,
            self.ui.studentCourseFilterComboBox,
            self.ui.attendanceCourseFilterComboBox,
            self.ui.gradesCourseFilterComboBox
        ]:
            combo.clear()
            combo.addItem("All Courses", -1)
            for course in courses:
                combo.addItem(course["name"], course["id"])
                
    def load_lessons(self):
        """Load lessons for the selected course."""
        # Clear the table
        self.ui.lessonsTable.setRowCount(0)
        
        # Get selected course ID (or -1 for all courses)
        course_id = self.ui.courseFilterComboBox.currentData()
        
        # Get courses taught by the teacher
        db = database()
        query = """
            SELECT id, name
            FROM courses
            WHERE teacher_id = %s AND active = 1
        """
        params = (self.user.user_id,)
        
        if course_id != -1:
            query += " AND id = %s"
            params = params + (course_id,)
            
        courses = db.fetch_all(query, params)
        
        # Placeholder implementation - in a real app, this would query the database for lessons
        # For now, we'll just show some sample data
        row = 0
        for course in courses:
            # Add rows for lessons
            for i in range(1, 6):
                self.ui.lessonsTable.insertRow(row)
                
                # Add lesson data
                self.ui.lessonsTable.setItem(row, 0, QTableWidgetItem(str(i)))
                self.ui.lessonsTable.setItem(row, 1, QTableWidgetItem(course["name"]))
                self.ui.lessonsTable.setItem(row, 2, QTableWidgetItem(f"Lesson {i}"))
                self.ui.lessonsTable.setItem(row, 3, QTableWidgetItem(f"Description for Lesson {i}"))
                
                # Date is 1 week apart for each lesson
                import datetime
                date = datetime.date.today() + datetime.timedelta(days=7*i)
                self.ui.lessonsTable.setItem(row, 4, QTableWidgetItem(date.isoformat()))
                
                # Add edit and delete buttons
                edit_button = QPushButton("Edit")
                edit_button.setProperty("lesson_id", i)
                edit_button.setProperty("course_id", course["id"])
                edit_button.clicked.connect(lambda checked, lid=i, cid=course["id"]: self.edit_lesson(lid, cid))
                
                delete_button = QPushButton("Delete")
                delete_button.setProperty("lesson_id", i)
                delete_button.setProperty("course_id", course["id"])
                delete_button.clicked.connect(lambda checked, lid=i, cid=course["id"]: self.delete_lesson(lid, cid))
                
                # Create a widget to hold the buttons
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.addWidget(edit_button)
                actions_layout.addWidget(delete_button)
                actions_layout.setContentsMargins(0, 0, 0, 0)
                
                self.ui.lessonsTable.setCellWidget(row, 5, actions_widget)
                
                row += 1
                
        # Resize columns to content
        self.ui.lessonsTable.resizeColumnsToContents()
        
    def filter_lessons(self):
        """Filter lessons based on selected course."""
        self.load_lessons()
        
    def add_lesson(self):
        """Open dialog to add a new lesson."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Lesson")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Course
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_combo = QComboBox()
        
        # Get courses taught by the teacher
        db = database()
        query = """
            SELECT id, name
            FROM courses
            WHERE teacher_id = %s AND active = 1
            ORDER BY name
        """
        params = (self.user.user_id,)
        courses = db.fetch_all(query, params)
        
        for course in courses:
            course_combo.addItem(course["name"], course["id"])
            
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_combo)
        form_layout.addLayout(course_layout)
        
        # Lesson title
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        title_input = QLineEdit()
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_input)
        form_layout.addLayout(title_layout)
        
        # Description
        description_layout = QVBoxLayout()
        description_label = QLabel("Description:")
        description_input = QTextEdit()
        description_input.setMaximumHeight(100)
        description_layout.addWidget(description_label)
        description_layout.addWidget(description_input)
        form_layout.addLayout(description_layout)
        
        # Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        date_input = QDateEdit()
        date_input.setDate(QDate.currentDate().addDays(7))  # Default to 1 week from now
        date_input.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(date_input)
        form_layout.addLayout(date_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get form values
            course_id = course_combo.currentData()
            title = title_input.text().strip()
            description = description_input.toPlainText().strip()
            date = date_input.date().toString("yyyy-MM-dd")
            
            # Validate form
            if not title or not description:
                QMessageBox.warning(self, "Validation Error", "Title and description are required.")
                return
                
            # In a real app, this would add a new lesson to the database
            # For now, we'll just show a success message
            QMessageBox.information(self, "Add Lesson", f"Lesson '{title}' added successfully.")
            
            # Refresh lessons table
            self.load_lessons()
            
    def edit_lesson(self, lesson_id, course_id):
        """Open dialog to edit a lesson."""
        # In a real app, this would get the lesson data from the database
        # For now, we'll just use placeholder data
        lesson_title = f"Lesson {lesson_id}"
        lesson_description = f"Description for Lesson {lesson_id}"
        lesson_date = QDate.currentDate().addDays(7 * lesson_id)
        
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Lesson")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Course (read-only)
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_input = QLineEdit()
        
        # Get course name
        db = database()
        query = "SELECT name FROM courses WHERE id = %s"
        params = (course_id,)
        course = db.fetch_one(query, params)
        
        if course:
            course_input.setText(course["name"])
            
        course_input.setReadOnly(True)
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_input)
        form_layout.addLayout(course_layout)
        
        # Lesson title
        title_layout = QHBoxLayout()
        title_label = QLabel("Title:")
        title_input = QLineEdit()
        title_input.setText(lesson_title)
        title_layout.addWidget(title_label)
        title_layout.addWidget(title_input)
        form_layout.addLayout(title_layout)
        
        # Description
        description_layout = QVBoxLayout()
        description_label = QLabel("Description:")
        description_input = QTextEdit()
        description_input.setMaximumHeight(100)
        description_input.setText(lesson_description)
        description_layout.addWidget(description_label)
        description_layout.addWidget(description_input)
        form_layout.addLayout(description_layout)
        
        # Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        date_input = QDateEdit()
        date_input.setDate(lesson_date)
        date_input.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(date_input)
        form_layout.addLayout(date_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get form values
            title = title_input.text().strip()
            description = description_input.toPlainText().strip()
            date = date_input.date().toString("yyyy-MM-dd")
            
            # Validate form
            if not title or not description:
                QMessageBox.warning(self, "Validation Error", "Title and description are required.")
                return
                
            # In a real app, this would update the lesson in the database
            # For now, we'll just show a success message
            QMessageBox.information(self, "Edit Lesson", f"Lesson '{title}' updated successfully.")
            
            # Refresh lessons table
            self.load_lessons()
            
    def delete_lesson(self, lesson_id, course_id):
        """Delete a lesson."""
        # In a real app, this would get the lesson data from the database
        # For now, we'll just use placeholder data
        lesson_title = f"Lesson {lesson_id}"
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete lesson '{lesson_title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # In a real app, this would delete the lesson from the database
            # For now, we'll just show a success message
            QMessageBox.information(self, "Delete Lesson", f"Lesson '{lesson_title}' deleted successfully.")
            
            # Refresh lessons table
            self.load_lessons()
            
    def load_students(self):
        """Load students for the selected course."""
        # Clear the table
        self.ui.studentsTable.setRowCount(0)
        
        # Get search text and selected course ID (or -1 for all courses)
        search_text = self.ui.studentSearchInput.text().lower()
        course_id = self.ui.studentCourseFilterComboBox.currentData()
        
        # Get students enrolled in the teacher's courses
        db = database()
        query = """
            SELECT u.id, u.first_name, u.last_name, u.email, c.id AS course_id, c.name AS course_name
            FROM users u
            JOIN student_courses sc ON u.id = sc.student_id
            JOIN courses c ON sc.course_id = c.id
            WHERE c.teacher_id = %s AND sc.active = 1
        """
        params = (self.user.user_id,)
        
        if course_id != -1:
            query += " AND c.id = %s"
            params = params + (course_id,)
            
        query += " ORDER BY u.last_name, u.first_name"
        
        students = db.fetch_all(query, params)
        
        # Populate the table
        row = 0
        for student in students:
            # Apply search filter
            if search_text and not (
                search_text in student["first_name"].lower() or  # first_name
                search_text in student["last_name"].lower() or  # last_name
                search_text in student["email"].lower()     # email
            ):
                continue
                
            self.ui.studentsTable.insertRow(row)
            
            # Add student data
            self.ui.studentsTable.setItem(row, 0, QTableWidgetItem(str(student["id"])))
            self.ui.studentsTable.setItem(row, 1, QTableWidgetItem(f"{student['first_name']} {student['last_name']}"))
            self.ui.studentsTable.setItem(row, 2, QTableWidgetItem(student["email"]))
            self.ui.studentsTable.setItem(row, 3, QTableWidgetItem(student["course_name"]))
            
            # Get progress (placeholder implementation)
            # In a real app, this would query the database for completed lessons/exercises
            progress = "50%"
            self.ui.studentsTable.setItem(row, 4, QTableWidgetItem(progress))
            
            # Get attendance (placeholder implementation)
            # In a real app, this would query the database for attendance records
            attendance = "80%"
            self.ui.studentsTable.setItem(row, 5, QTableWidgetItem(attendance))
            
            # Get average grade (placeholder implementation)
            # In a real app, this would query the database for grades
            grade = "85%"
            self.ui.studentsTable.setItem(row, 6, QTableWidgetItem(grade))
            
            # Add action buttons
            view_button = QPushButton("View Details")
            view_button.setProperty("student_id", student["id"])
            view_button.setProperty("course_id", student["course_id"])
            view_button.clicked.connect(lambda checked, sid=student["id"], cid=student["course_id"]: self.view_student_details(sid, cid))
            
            message_button = QPushButton("Message")
            message_button.setProperty("student_id", student["id"])
            message_button.clicked.connect(lambda checked, sid=student["id"], sname=f"{student['first_name']} {student['last_name']}": self.message_student(sid, sname))
            
            # Create a widget to hold the buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(view_button)
            actions_layout.addWidget(message_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.ui.studentsTable.setCellWidget(row, 7, actions_widget)
            
            row += 1
            
        # Resize columns to content
        self.ui.studentsTable.resizeColumnsToContents()
        
    def filter_students(self):
        """Filter students based on search text and selected course."""
        self.load_students()
        
    def view_student_details(self, student_id, course_id):
        """View details of a student."""
        # Get student data
        db = database()
        query = """
            SELECT first_name, last_name, email
            FROM users
            WHERE id = %s
        """
        params = (student_id,)
        student = db.fetch_one(query, params)
        
        if not student:
            QMessageBox.warning(self, "Error", "Student not found.")
            return
            
        # Get course data
        query = """
            SELECT name
            FROM courses
            WHERE id = %s
        """
        params = (course_id,)
        course = db.fetch_one(query, params)
        
        if not course:
            QMessageBox.warning(self, "Error", "Course not found.")
            return
            
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Student Details: {student['first_name']} {student['last_name']}")
        dialog.setMinimumWidth(600)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add student details
        details_layout = QVBoxLayout()
        
        # Student name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_label.setMinimumWidth(100)
        name_value = QLabel(f"{student['first_name']} {student['last_name']}")
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_value)
        details_layout.addLayout(name_layout)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_label.setMinimumWidth(100)
        email_value = QLabel(student['email'])
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_value)
        details_layout.addLayout(email_layout)
        
        # Course
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_label.setMinimumWidth(100)
        course_value = QLabel(course['name'])
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_value)
        details_layout.addLayout(course_layout)
        
        layout.addLayout(details_layout)
        
        # Add tabs for different sections
        from PyQt5.QtWidgets import QTabWidget
        tabs = QTabWidget()
        
        # Attendance tab
        attendance_widget = QWidget()
        attendance_layout = QVBoxLayout(attendance_widget)
        
        # Create table for attendance
        from PyQt5.QtWidgets import QTableWidget
        attendance_table = QTableWidget()
        attendance_table.setColumnCount(3)
        attendance_table.setHorizontalHeaderLabels(["Date", "Status", "Notes"])
        
        # Placeholder implementation - in a real app, this would query the database for attendance records
        # For now, we'll just show some sample data
        for row in range(5):
            attendance_table.insertRow(row)
            
            # Date is 1 week apart for each record
            import datetime
            date = datetime.date.today() - datetime.timedelta(days=7*row)
            attendance_table.setItem(row, 0, QTableWidgetItem(date.isoformat()))
            
            # Status is random
            import random
            status = random.choice(["Present", "Absent", "Late"])
            attendance_table.setItem(row, 1, QTableWidgetItem(status))
            
            # Notes
            if status == "Absent":
                notes = "Excused absence - doctor's appointment"
            elif status == "Late":
                notes = "15 minutes late"
            else:
                notes = ""
                
            attendance_table.setItem(row, 2, QTableWidgetItem(notes))
            
        # Resize columns to content
        attendance_table.resizeColumnsToContents()
        
        attendance_layout.addWidget(attendance_table)
        tabs.addTab(attendance_widget, "Attendance")
        
        # Grades tab
        grades_widget = QWidget()
        grades_layout = QVBoxLayout(grades_widget)
        
        # Create table for grades
        grades_table = QTableWidget()
        grades_table.setColumnCount(4)
        grades_table.setHorizontalHeaderLabels(["Type", "Title", "Date", "Grade"])
        
        # Placeholder implementation - in a real app, this would query the database for grades
        # For now, we'll just show some sample data
        for row in range(5):
            grades_table.insertRow(row)
            
            # Type alternates between Exercise and Test
            type_text = "Exercise" if row % 2 == 0 else "Test"
            grades_table.setItem(row, 0, QTableWidgetItem(type_text))
            
            # Title
            title = f"{type_text} {row + 1}"
            grades_table.setItem(row, 1, QTableWidgetItem(title))
            
            # Date is 1 week apart for each record
            import datetime
            date = datetime.date.today() - datetime.timedelta(days=7*row)
            grades_table.setItem(row, 2, QTableWidgetItem(date.isoformat()))
            
            # Grade is random between 70 and 100
            import random
            grade = random.randint(70, 100)
            grades_table.setItem(row, 3, QTableWidgetItem(f"{grade}%"))
            
        # Resize columns to content
        grades_table.resizeColumnsToContents()
        
        grades_layout.addWidget(grades_table)
        tabs.addTab(grades_widget, "Grades")
        
        # Progress tab
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        
        # Create table for progress
        progress_table = QTableWidget()
        progress_table.setColumnCount(4)
        progress_table.setHorizontalHeaderLabels(["Lesson", "Status", "Completion Date", "Grade"])
        
        # Placeholder implementation - in a real app, this would query the database for progress
        # For now, we'll just show some sample data
        for row in range(5):
            progress_table.insertRow(row)
            
            # Lesson
            progress_table.setItem(row, 0, QTableWidgetItem(f"Lesson {row + 1}"))
            
            # Status depends on lesson number
            if row < 2:
                status = "Completed"
            elif row == 2:
                status = "In Progress"
            else:
                status = "Not Started"
                
            progress_table.setItem(row, 1, QTableWidgetItem(status))
            
            # Completion date
            if status == "Completed":
                import datetime
                date = datetime.date.today() - datetime.timedelta(days=7*(2-row))
                progress_table.setItem(row, 2, QTableWidgetItem(date.isoformat()))
            else:
                progress_table.setItem(row, 2, QTableWidgetItem(""))
                
            # Grade
            if status == "Completed":
                import random
                grade = random.randint(70, 100)
                progress_table.setItem(row, 3, QTableWidgetItem(f"{grade}%"))
            else:
                progress_table.setItem(row, 3, QTableWidgetItem(""))
                
        # Resize columns to content
        progress_table.resizeColumnsToContents()
        
        progress_layout.addWidget(progress_table)
        tabs.addTab(progress_widget, "Progress")
        
        layout.addWidget(tabs)
        
        # Add close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.reject)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        # Show dialog
        dialog.exec_()
        
    def message_student(self, student_id, student_name):
        """Open dialog to send a message to a student."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Message to {student_name}")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Message
        message_label = QLabel("Message:")
        message_input = QTextEdit()
        form_layout.addWidget(message_label)
        form_layout.addWidget(message_input)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Send")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get form values
            message = message_input.toPlainText().strip()
            
            # Validate form
            if not message:
                QMessageBox.warning(self, "Validation Error", "Message is required.")
                return
                
            # In a real app, this would send a message to the student
            # For now, we'll just show a success message
            QMessageBox.information(self, "Send Message", f"Message sent to {student_name} successfully.")
            
            # Refresh chats
            self.load_chats()
            
    def load_attendance(self):
        """Load attendance for the selected course and date."""
        # Clear the table
        self.ui.attendanceTable.setRowCount(0)
        
        # Get selected course ID (or -1 for all courses)
        course_id = self.ui.attendanceCourseFilterComboBox.currentData()
        
        # Get selected date
        selected_date = self.ui.attendanceDateEdit.date().toString("yyyy-MM-dd")
        
        # Get students enrolled in the selected course
        db = database()
        query = """
            SELECT u.id, u.first_name, u.last_name
            FROM users u
            JOIN student_courses sc ON u.id = sc.student_id
            JOIN courses c ON sc.course_id = c.id
            WHERE c.teacher_id = %s AND sc.active = 1
        """
        params = (self.user.user_id,)
        
        if course_id != -1:
            query += " AND c.id = %s"
            params = params + (course_id,)
            
        query += " ORDER BY u.last_name, u.first_name"
        
        students = db.fetch_all(query, params)
        
        # Populate the table
        for row, student in enumerate(students):
            self.ui.attendanceTable.insertRow(row)
            
            # Add student data
            self.ui.attendanceTable.setItem(row, 0, QTableWidgetItem(str(student["id"])))
            self.ui.attendanceTable.setItem(row, 1, QTableWidgetItem(f"{student['first_name']} {student['last_name']}"))
            
            # Get attendance status (placeholder implementation)
            # In a real app, this would query the database for attendance records
            import random
            status = random.choice(["Present", "Absent", "Late"])
            
            # Add status combo box
            status_combo = QComboBox()
            status_combo.addItem("Present")
            status_combo.addItem("Absent")
            status_combo.addItem("Late")
            
            # Set current status
            status_index = status_combo.findText(status)
            if status_index >= 0:
                status_combo.setCurrentIndex(status_index)
                
            self.ui.attendanceTable.setCellWidget(row, 2, status_combo)
            
            # Add notes input
            notes_input = QLineEdit()
            
            # Set notes (placeholder implementation)
            if status == "Absent":
                notes_input.setText("Excused absence - doctor's appointment")
            elif status == "Late":
                notes_input.setText("15 minutes late")
                
            self.ui.attendanceTable.setCellWidget(row, 3, notes_input)
            
        # Resize columns to content
        self.ui.attendanceTable.resizeColumnsToContents()
        
    def filter_attendance(self):
        """Filter attendance based on selected course and date."""
        self.load_attendance()
        
    def save_attendance(self):
        """Save attendance records."""
        # Get selected date
        selected_date = self.ui.attendanceDateEdit.date().toString("yyyy-MM-dd")
        
        # Get attendance records from the table
        records = []
        for row in range(self.ui.attendanceTable.rowCount()):
            student_id = self.ui.attendanceTable.item(row, 0).text()
            status_combo = self.ui.attendanceTable.cellWidget(row, 2)
            status = status_combo.currentText()
            notes_input = self.ui.attendanceTable.cellWidget(row, 3)
            notes = notes_input.text()
            
            records.append({
                "student_id": student_id,
                "status": status,
                "notes": notes
            })
            
        # In a real app, this would save the attendance records to the database
        # For now, we'll just show a success message
        QMessageBox.information(self, "Save Attendance", f"Attendance records for {selected_date} saved successfully.")
        
    def load_grades(self):
        """Load grades for the selected course and type."""
        # Clear the table
        self.ui.gradesTable.setRowCount(0)
        
        # Get selected course ID (or -1 for all courses)
        course_id = self.ui.gradesCourseFilterComboBox.currentData()
        
        # Get selected type
        type_index = self.ui.gradesTypeFilterComboBox.currentIndex()
        grade_type = None
        if type_index == 1:
            grade_type = "Exercise"
        elif type_index == 2:
            grade_type = "Test"
            
        # Get students enrolled in the selected course
        db = database()
        query = """
            SELECT u.id, u.first_name, u.last_name, c.id, c.name
            FROM users u
            JOIN student_courses sc ON u.id = sc.student_id
            JOIN courses c ON sc.course_id = c.id
            WHERE c.teacher_id = %s AND sc.active = 1
        """
        params = (self.user.user_id,)
        
        if course_id != -1:
            query += " AND c.id = %s"
            params = params + (course_id,)
            
        query += " ORDER BY u.last_name, u.first_name"
        
        students = db.fetch_all(query, params)
        
        # Populate the table
        row = 0
        for student in students:
            # Add rows for exercises
            if grade_type is None or grade_type == "Exercise":
                for i in range(1, 4):
                    self.ui.gradesTable.insertRow(row)
                    
                    # Add grade data
                    self.ui.gradesTable.setItem(row, 0, QTableWidgetItem(str(student["id"])))
                    self.ui.gradesTable.setItem(row, 1, QTableWidgetItem(f"{student['first_name']} {student['last_name']}"))
                    self.ui.gradesTable.setItem(row, 2, QTableWidgetItem(student["name"]))
                    self.ui.gradesTable.setItem(row, 3, QTableWidgetItem("Exercise"))
                    self.ui.gradesTable.setItem(row, 4, QTableWidgetItem(f"Exercise {i}"))
                    
                    # Add grade input
                    grade_input = QLineEdit()
                    
                    # Set grade (placeholder implementation)
                    import random
                    grade = random.randint(70, 100)
                    grade_input.setText(str(grade))
                    
                    self.ui.gradesTable.setCellWidget(row, 5, grade_input)
                    
                    # Add feedback input
                    feedback_input = QLineEdit()
                    
                    # Set feedback (placeholder implementation)
                    feedback = "Good work, but needs more practice with grammar."
                    feedback_input.setText(feedback)
                    
                    self.ui.gradesTable.setCellWidget(row, 6, feedback_input)
                    
                    row += 1
                    
            # Add rows for tests
            if grade_type is None or grade_type == "Test":
                for i in range(1, 3):
                    self.ui.gradesTable.insertRow(row)
                    
                    # Add grade data
                    self.ui.gradesTable.setItem(row, 0, QTableWidgetItem(str(student["id"])))
                    self.ui.gradesTable.setItem(row, 1, QTableWidgetItem(f"{student['first_name']} {student['last_name']}"))
                    self.ui.gradesTable.setItem(row, 2, QTableWidgetItem(student["name"]))
                    self.ui.gradesTable.setItem(row, 3, QTableWidgetItem("Test"))
                    
                    if i == 1:
                        test_name = "Midterm Exam"
                    else:
                        test_name = "Final Exam"
                        
                    self.ui.gradesTable.setItem(row, 4, QTableWidgetItem(test_name))
                    
                    # Add grade input
                    grade_input = QLineEdit()
                    
                    # Set grade (placeholder implementation)
                    import random
                    grade = random.randint(70, 100)
                    grade_input.setText(str(grade))
                    
                    self.ui.gradesTable.setCellWidget(row, 5, grade_input)
                    
                    # Add feedback input
                    feedback_input = QLineEdit()
                    
                    # Set feedback (placeholder implementation)
                    feedback = "Excellent performance on the written section."
                    feedback_input.setText(feedback)
                    
                    self.ui.gradesTable.setCellWidget(row, 6, feedback_input)
                    
                    row += 1
                    
        # Resize columns to content
        self.ui.gradesTable.resizeColumnsToContents()
        
    def filter_grades(self):
        """Filter grades based on selected course and type."""
        self.load_grades()
        
    def save_grades(self):
        """Save grade records."""
        # Get grade records from the table
        records = []
        for row in range(self.ui.gradesTable.rowCount()):
            student_id = self.ui.gradesTable.item(row, 0).text()
            student_name = self.ui.gradesTable.item(row, 1).text()
            course_name = self.ui.gradesTable.item(row, 2).text()
            grade_type = self.ui.gradesTable.item(row, 3).text()
            item_name = self.ui.gradesTable.item(row, 4).text()
            grade_input = self.ui.gradesTable.cellWidget(row, 5)
            grade = grade_input.text()
            feedback_input = self.ui.gradesTable.cellWidget(row, 6)
            feedback = feedback_input.text()
            
            records.append({
                "student_id": student_id,
                "student_name": student_name,
                "course_name": course_name,
                "grade_type": grade_type,
                "item_name": item_name,
                "grade": grade,
                "feedback": feedback
            })
            
        # In a real app, this would save the grade records to the database
        # For now, we'll just show a success message
        QMessageBox.information(self, "Save Grades", "Grade records saved successfully.")
        
    def load_chats(self):
        """Load chats for the teacher."""
        # Clear the list
        self.ui.chatsList.clear()
        
        # Get students in the teacher's courses
        db = database()
        query = """
            SELECT DISTINCT u.id, u.first_name, u.last_name
            FROM users u
            JOIN student_courses sc ON u.id = sc.student_id
            JOIN courses c ON sc.course_id = c.id
            WHERE c.teacher_id = %s AND sc.active = 1
            ORDER BY u.last_name, u.first_name
        """
        params = (self.user.user_id,)
        students = db.fetch_all(query, params)
        
        # Add students to the list
        for student in students:
            item = QListWidgetItem(f"{student["first_name"]} {student["last_name"]} (Student)")
            item.setData(Qt.UserRole, student["id"])
            self.ui.chatsList.addItem(item)
            
        # Add admin to the list
        admin_item = QListWidgetItem("Admin")
        admin_item.setData(Qt.UserRole, 1)  # Admin ID
        self.ui.chatsList.addItem(admin_item)
        
    def load_messages(self, current_item, previous_item):
        """Load messages for the selected chat."""
        if not current_item:
            return
            
        # Clear the list
        self.ui.messagesList.clear()
        
        # Get selected user ID
        user_id = current_item.data(Qt.UserRole)
        
        # Placeholder implementation - in a real app, this would query the database for messages
        # For now, we'll just show some sample data
        
        # Add sample messages
        messages = [
            {"sender_id": user_id, "text": "Hello, teacher!", "timestamp": "2023-05-01 10:00:00"},
            {"sender_id": self.user.user_id, "text": "Hi! How can I help you?", "timestamp": "2023-05-01 10:05:00"},
            {"sender_id": user_id, "text": "I have a question about the homework.", "timestamp": "2023-05-01 10:10:00"},
            {"sender_id": self.user.user_id, "text": "Sure, what's your question?", "timestamp": "2023-05-01 10:15:00"},
            {"sender_id": user_id, "text": "I'm having trouble with exercise 3.", "timestamp": "2023-05-01 10:20:00"}
        ]
        
        for message in messages:
            if message["sender_id"] == self.user.user_id:
                prefix = "You: "
                alignment = Qt.AlignRight
            else:
                prefix = f"{current_item.text().split(' (')[0]}: "
                alignment = Qt.AlignLeft
                
            item = QListWidgetItem(f"{prefix}{message['text']}")
            item.setTextAlignment(alignment)
            self.ui.messagesList.addItem(item)
            
        # Scroll to bottom
        self.ui.messagesList.scrollToBottom()
        
    def send_message(self):
        """Send a message in the current chat."""
        # Get message text
        message_text = self.ui.messageInput.text().strip()
        
        if not message_text:
            return
            
        # Get current chat
        current_item = self.ui.chatsList.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Chat Selected", "Please select a chat to send a message.")
            return
            
        # In a real app, this would save the message to the database
        # For now, we'll just add it to the list
        
        # Add message to list
        item = QListWidgetItem(f"You: {message_text}")
        item.setTextAlignment(Qt.AlignRight)
        self.ui.messagesList.addItem(item)
        
        # Clear input
        self.ui.messageInput.clear()
        
        # Scroll to bottom
        self.ui.messagesList.scrollToBottom()
        
        # Show status message
        self.ui.statusbar.showMessage("Message sent.")
        
    def new_chat(self):
        """Open dialog to start a new chat."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("New Chat")
        dialog.setMinimumWidth(300)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # User selection
        user_label = QLabel("Select User:")
        user_combo = QComboBox()
        
        # Get students in the teacher's courses
        db = database()
        query = """
            SELECT DISTINCT u.id, u.first_name, u.last_name
            FROM users u
            JOIN student_courses sc ON u.id = sc.student_id
            JOIN courses c ON sc.course_id = c.id
            WHERE c.teacher_id = %s AND sc.active = 1
            ORDER BY u.last_name, u.first_name
        """
        params = (self.user.user_id,)
        students = db.fetch_all(query, params)
        
        # Add students to the combo box
        for student in students:
            user_combo.addItem(f"{student["first_name"]} {student["last_name"]} (Student)", student["id"])
            
        # Add admin to the combo box
        user_combo.addItem("Admin", 1)
        
        layout.addWidget(user_label)
        layout.addWidget(user_combo)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get selected user
            user_id = user_combo.currentData()
            user_name = user_combo.currentText()
            
            # In a real app, this would create a new chat in the database
            # For now, we'll just add it to the list if it doesn't exist
            
            # Check if chat already exists
            for i in range(self.ui.chatsList.count()):
                item = self.ui.chatsList.item(i)
                if item.data(Qt.UserRole) == user_id:
                    # Select existing chat
                    self.ui.chatsList.setCurrentItem(item)
                    return
                    
            # Add new chat
            item = QListWidgetItem(user_name)
            item.setData(Qt.UserRole, user_id)
            self.ui.chatsList.addItem(item)
            self.ui.chatsList.setCurrentItem(item)
            
        # Show status message
        self.ui.statusbar.showMessage(f"New chat started with {user_name}.")
        
    def on_profile_updated(self):
        """Handle profile update events."""
        self.ui.welcomeLabel.setText(f"Welcome, {self.user.first_name} {self.user.last_name}")
        self.ui.statusbar.showMessage("Profile updated successfully")

    def open_profile_dialog(self):
        """Open dialog to edit user profile."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Profile")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # First name
        first_name_layout = QHBoxLayout()
        first_name_label = QLabel("First Name:")
        first_name_input = QLineEdit()
        first_name_input.setText(self.user.first_name)
        first_name_layout.addWidget(first_name_label)
        first_name_layout.addWidget(first_name_input)
        form_layout.addLayout(first_name_layout)
        
        # Last name
        last_name_layout = QHBoxLayout()
        last_name_label = QLabel("Last Name:")
        last_name_input = QLineEdit()
        last_name_input.setText(self.user.last_name)
        last_name_layout.addWidget(last_name_label)
        last_name_layout.addWidget(last_name_input)
        form_layout.addLayout(last_name_layout)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_input = QLineEdit()
        email_input.setText(self.user.email)
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_input)
        form_layout.addLayout(email_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("New Password:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Leave empty to keep current password")
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_input)
        form_layout.addLayout(password_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # Get form values and validate
            first_name = first_name_input.text().strip()
            last_name = last_name_input.text().strip()
            email = email_input.text().strip()
            new_password = password_input.text().strip()
            
            if not first_name or not last_name or not email:
                QMessageBox.warning(self, "Validation Error", "First name, last name and email are required.")
                return
            
            try:
                db = database()
                cursor = db.cursor()
                
                # Separate queries for with/without password update
                if new_password:
                    query = """
                        UPDATE users 
                        SET first_name = %s,
                            last_name = %s,
                            email = %s,
                            password = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """
                    params = (first_name, last_name, email, new_password, self.user.user_id)
                else:
                    query = """
                        UPDATE users 
                        SET first_name = %s,
                            last_name = %s,
                            email = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """
                    params = (first_name, last_name, email, self.user.user_id)
                
                cursor.execute(query, params)
                db.commit()
                
                # Update local user object
                self.user.first_name = first_name
                self.user.last_name = last_name
                self.user.email = email
                if new_password:
                    self.user.password = new_password
                
                self.profile_updated.emit()
                QMessageBox.information(self, "Success", "Profile updated successfully")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update profile: {str(e)}")
            finally:
                cursor.close()
                db.close()