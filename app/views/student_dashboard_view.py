"""
Student Dashboard View
-------------------
This module contains the StudentDashboardView class, which implements the student dashboard
functionality for the Language School Management System.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QDateEdit, 
    QTextEdit, QPushButton, QDialogButtonBox, QListWidgetItem, QProgressBar, QWidget, QTableWidget
)
from PyQt5.QtCore import Qt, pyqtSlot, QDate, pyqtSignal

from app.ui.generated.student_dashboard_ui import Ui_StudentDashboard
from app.views.base_dashboard_view import BaseDashboardView
from app.models.user_model import User
from app.models.course_model import Course
from app.utils.database import execute_query, get_connection
from datetime import datetime, timedelta  # Fixed import to include timedelta


class StudentDashboardView(BaseDashboardView):
    """
    Student dashboard view class.
    
    This class implements the student dashboard functionality, including:
    - Viewing enrolled courses
    - Viewing schedule
    - Accessing lessons and exercises
    - Viewing grades
    - Messaging with teachers and other students
    - Managing payments
    """
    
    # Define signal as class variable 
    profile_updated = pyqtSignal()
    # Signal for when user logs out
    logout_requested = pyqtSignal()

    def __init__(self, user, parent=None):
        """Initialize the student dashboard view."""
        # Initialize base class first
        super().__init__(user, parent)
        self.ui = Ui_StudentDashboard()
        self.ui.setupUi(self)
        
        # Set welcome message
        self.ui.welcomeLabel.setText(f"Welcome, {self.user.first_name} {self.user.last_name}")
        
        # Connect signals and slots - fixed logout signal connection
        self.ui.logoutButton.clicked.connect(self.handle_logout)
        self.ui.actionLogout.triggered.connect(self.handle_logout)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionRefresh.triggered.connect(self.refresh_data)
        
        # Connect profile signals
        self.ui.profileButton.clicked.connect(self.open_profile_dialog)
        self.ui.actionEditProfile.triggered.connect(self.open_profile_dialog)
        self.profile_updated.connect(self.on_profile_updated)
        
        # Connect dashboard buttons
        self.ui.viewCoursesButton.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))
        self.ui.viewScheduleButton.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))
        self.ui.viewExercisesButton.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(3))
        self.ui.viewMessagesButton.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(5))
        
        # Connect tab-specific signals and slots
        self.ui.browseCatalogButton.clicked.connect(self.browse_catalog)
        self.ui.exportScheduleButton.clicked.connect(self.export_schedule)
        self.ui.exportGradesButton.clicked.connect(self.export_grades)
        self.ui.sendMessageButton.clicked.connect(self.send_message)
        self.ui.newChatButton.clicked.connect(self.new_chat)
        self.ui.makePaymentButton.clicked.connect(self.make_payment)
        
        # Connect filter signals
        self.ui.courseSearchInput.textChanged.connect(self.filter_courses)
        self.ui.courseFilterComboBox.currentIndexChanged.connect(self.filter_courses)
        self.ui.scheduleFilterComboBox.currentIndexChanged.connect(self.filter_schedule)
        self.ui.scheduleDateEdit.dateChanged.connect(self.filter_schedule)
        self.ui.lessonsCourseFilterComboBox.currentIndexChanged.connect(self.filter_lessons)
        self.ui.lessonsStatusFilterComboBox.currentIndexChanged.connect(self.filter_lessons)
        self.ui.gradesCourseFilterComboBox.currentIndexChanged.connect(self.filter_grades)
        self.ui.gradesTypeFilterComboBox.currentIndexChanged.connect(self.filter_grades)
        self.ui.paymentsStatusFilterComboBox.currentIndexChanged.connect(self.filter_payments)
        self.ui.chatsList.currentItemChanged.connect(self.load_messages)
        
        # Set current date for schedule
        self.ui.scheduleDateEdit.setDate(QDate.currentDate())
        
        # Initialize data
        self.refresh_data()
        
        # Show status message
        self.ui.statusLabel.setText("Ready")
        
    def refresh_data(self):
        """Refresh all data in the dashboard."""
        self.load_dashboard_stats()
        self.load_course_progress()
        self.load_recent_activity()
        self.load_courses()
        self.load_course_filter_combos()
        self.load_schedule()
        self.load_lessons()
        self.load_grades()
        self.load_payments()
        self.load_chats()
        
    def load_dashboard_stats(self):
        """Load dashboard statistics."""
        try:
            # Get enrolled courses count
            query = "SELECT COUNT(*) as count FROM student_courses WHERE student_id = %s AND active = 1"
            params = (self.user.user_id,)
            result = execute_query(query, params=params, fetch=True)
            enrolled_count = result[0]['count'] if isinstance(result[0], dict) else result[0][0]
            self.ui.enrolledCoursesCountLabel.setText(str(enrolled_count))

            # Get total scheduled lessons count for all enrolled courses
            query = """
                SELECT COUNT(*) as count
                FROM schedules s
                JOIN student_courses sc ON s.course_id = sc.course_id
                WHERE sc.student_id = %s 
                AND sc.active = 1
            """
            result = execute_query(query, params=params, fetch=True)
            upcoming_count = result[0]['count'] if isinstance(result[0], dict) else result[0][0]
            self.ui.upcomingLessonsCountLabel.setText(str(upcoming_count))

            # Get pending exercises count
            query = """
                SELECT COUNT(*) as count 
                FROM exercises e
                JOIN lessons l ON e.lesson_id = l.id
                JOIN student_courses sc ON l.course_id = sc.course_id
                LEFT JOIN student_exercise_submissions ses 
                    ON e.id = ses.exercise_id AND ses.student_id = sc.student_id
                WHERE sc.student_id = %s AND sc.active = 1
                AND (ses.status IS NULL OR ses.status = 'not_submitted')
                AND e.due_date >= CURRENT_DATE
            """
            result = execute_query(query, params=params, fetch=True)
            pending_count = result[0]['count'] if isinstance(result[0], dict) else result[0][0]
            self.ui.pendingExercisesCountLabel.setText(str(pending_count))

            # Get unread messages count
            query = """
                SELECT COUNT(*) as count
                FROM chat_messages cm
                JOIN chats c ON cm.chat_id = c.id
                WHERE (c.user1_id = %s OR c.user2_id = %s)
                AND cm.sender_id != %s 
                AND cm.read_status = 0
            """
            params = (self.user.user_id, self.user.user_id, self.user.user_id)
            result = execute_query(query, params=params, fetch=True)
            unread_count = result[0]['count'] if isinstance(result[0], dict) else result[0][0]
            self.ui.unreadMessagesCountLabel.setText(str(unread_count))

        except Exception as e:
            print(f"Error loading dashboard stats: {str(e)}")
            # Set default values on error
            self.ui.enrolledCoursesCountLabel.setText("0")
            self.ui.upcomingLessonsCountLabel.setText("0")
            self.ui.pendingExercisesCountLabel.setText("0") 
            self.ui.unreadMessagesCountLabel.setText("0")
    
    def load_course_progress(self):
        """Load course progress bars."""
        # Get enrolled courses
        query = """
            SELECT c.id, c.name, c.language, c.level 
            FROM courses c
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = %s AND sc.active = 1
            ORDER BY c.name
        """
        params = (self.user.user_id,)
        courses = execute_query(query, params=params, fetch=True)
        
        # Clear existing progress bars
        for i in reversed(range(self.ui.verticalLayout_11.count())):
            item = self.ui.verticalLayout_11.itemAt(i)
            if isinstance(item, QHBoxLayout):
                # Remove all widgets from the layout
                while item.count():
                    child = item.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                # Remove the layout itself
                self.ui.verticalLayout_11.removeItem(item)
        
        # Add progress bars for each course
        for i, course in enumerate(courses[:3]):  # Show up to 3 courses
            # Handle both dictionary and tuple results
            if isinstance(course, dict):
                course_name = course['name']
                course_lang = course['language']
                course_level = course['level']
            else:
                # Assuming tuple order: id, name, language, level
                course_name = course[1]
                course_lang = course[2] 
                course_level = course[3]
            
            # Create layout for this course
            layout = QHBoxLayout()
            
            # Add course label with consistent access
            label = QLabel(f"{course_name} ({course_lang} {course_level}):")
            layout.addWidget(label)
            
            # Add progress bar
            progress_bar = QProgressBar()
            
            # Calculate progress (placeholder implementation)
            if i == 0:
                progress = 75
            elif i == 1:
                progress = 45
            else:
                progress = 20
                
            progress_bar.setValue(progress)
            layout.addWidget(progress_bar)
            
            # Add layout to main layout
            self.ui.verticalLayout_11.addLayout(layout)
            
    def load_recent_activity(self):
        """Load recent activity list."""
        # Clear the list
        self.ui.recentActivityList.clear()
        
        # Placeholder implementation - in a real app, this would query the database for recent activity
        # For now, we'll just show some sample data
        activities = [
            "You completed Lesson 5 in English B1 - Yesterday",
            "You received a grade of 92% on Test 2 in Spanish A2 - 2 days ago",
            "You submitted Exercise 3 in French A1 - 3 days ago",
            "You enrolled in French A1 - 1 week ago"
        ]
        
        for activity in activities:
            self.ui.recentActivityList.addItem(activity)
            
    def load_courses(self):
        """Load enrolled courses into the courses table."""
        # Clear the table
        self.ui.coursesTable.setRowCount(0)
        
        # Get search text and language filter
        search_text = self.ui.courseSearchInput.text().lower()
        language_index = self.ui.courseFilterComboBox.currentIndex()
        language_filter = self.ui.courseFilterComboBox.currentText() if language_index > 0 else None
        
        # Get enrolled courses
        query = """
            SELECT c.id, c.name, c.language, c.level, u.first_name, u.last_name
            FROM courses c
            JOIN student_courses sc ON c.id = sc.course_id
            JOIN users u ON c.teacher_id = u.id
            WHERE sc.student_id = %s AND sc.active = 1
        """
        params = (self.user.user_id,)
        courses = execute_query(query, params=params, fetch=True)
        
        # Populate the table
        row = 0
        for course in courses:
            # Handle both dictionary and tuple results
            if isinstance(course, dict):
                course_id = course['id']
                course_name = course['name']
                course_lang = course['language']
                course_level = course['level']
                teacher_fname = course['first_name']
                teacher_lname = course['last_name']
            else:
                # Assuming tuple order: id, name, language, level, first_name, last_name
                course_id = course[0]
                course_name = course[1]
                course_lang = course[2]
                course_level = course[3]
                teacher_fname = course[4]
                teacher_lname = course[5]
            
            # Apply filters
            if search_text and search_text not in course_name.lower():
                continue
                
            if language_filter and course_lang != language_filter:
                continue
                
            self.ui.coursesTable.insertRow(row)
            
            # Add course data with consistent access
            self.ui.coursesTable.setItem(row, 0, QTableWidgetItem(str(course_id)))
            self.ui.coursesTable.setItem(row, 1, QTableWidgetItem(course_name))
            self.ui.coursesTable.setItem(row, 2, QTableWidgetItem(course_lang))
            self.ui.coursesTable.setItem(row, 3, QTableWidgetItem(course_level))
            self.ui.coursesTable.setItem(row, 4, QTableWidgetItem(f"{teacher_fname} {teacher_lname}"))
            
            # Calculate progress (placeholder implementation)
            progress = "50%"
            self.ui.coursesTable.setItem(row, 5, QTableWidgetItem(progress))
            
            # Add action buttons
            actions_item = QTableWidgetItem("View Details | View Lessons")
            self.ui.coursesTable.setItem(row, 6, actions_item)
            
            row += 1
            
        # Resize columns to content
        self.ui.coursesTable.resizeColumnsToContents()
        
    def filter_courses(self):
        """Filter courses based on search text and language filter."""
        self.load_courses()
        
    def browse_catalog(self):
        """Open dialog to browse course catalog."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Course Catalog")
        dialog.setMinimumSize(800, 500)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add filter controls
        filter_layout = QHBoxLayout()
        
        # Search input
        search_label = QLabel("Search:")
        search_input = QLineEdit()
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(search_input)
        
        # Language filter
        language_label = QLabel("Language:")
        language_combo = QComboBox()
        language_combo.addItem("All Languages")
        language_combo.addItem("English")
        language_combo.addItem("Spanish")
        language_combo.addItem("French")
        language_combo.addItem("German")
        filter_layout.addWidget(language_label)
        filter_layout.addWidget(language_combo)
        
        # Level filter
        level_label = QLabel("Level:")
        level_combo = QComboBox()
        level_combo.addItem("All Levels")
        level_combo.addItem("A1")
        level_combo.addItem("A2")
        level_combo.addItem("B1")
        level_combo.addItem("B2")
        level_combo.addItem("C1")
        level_combo.addItem("C2")
        filter_layout.addWidget(level_label)
        filter_layout.addWidget(level_combo)
        
        layout.addLayout(filter_layout)
        
        # Add table for courses
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(["ID", "Name", "Language", "Level", "Teacher", "Schedule", "Actions"])
        layout.addWidget(table)
        
        # Add close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.reject)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        # Function to load courses
        def load_catalog_courses():
            # Clear the table
            table.setRowCount(0)
            
            # Get search text and filters
            search_text = search_input.text().lower()
            language_index = language_combo.currentIndex()
            language_filter = language_combo.currentText() if language_index > 0 else None
            level_index = level_combo.currentIndex()
            level_filter = level_combo.currentText() if level_index > 0 else None
            
            # Get all courses
            query = """
                SELECT c.id, c.name, c.language, c.level, u.first_name, u.last_name
                FROM courses c
                JOIN users u ON c.teacher_id = u.id 
                WHERE c.active = 1
            """
            courses = execute_query(query, fetch=True)
            
            # Populate the table
            row = 0
            for course in courses:
                # Apply filters
                if search_text and search_text not in course['name'].lower():
                    continue
                    
                if language_filter and language_filter != "All Languages" and course['language'] != language_filter:
                    continue
                    
                if level_filter and level_filter != "All Levels" and course['level'] != level_filter:
                    continue
                    
                # Check if already enrolled
                query = """
                    SELECT COUNT(*) as count FROM student_courses 
                    WHERE student_id = %s AND course_id = %s AND active = 1
                """
                params = (self.user.user_id, course['id'])
                result = execute_query(query, params=params, fetch=True)
                already_enrolled = result[0]['count'] > 0 if result else False
                
                if already_enrolled:
                    continue  # Skip courses the student is already enrolled in
                    
                table.insertRow(row)
                
                # Add course data
                table.setItem(row, 0, QTableWidgetItem(str(course['id'])))
                table.setItem(row, 1, QTableWidgetItem(course['name']))
                table.setItem(row, 2, QTableWidgetItem(course['language']))
                table.setItem(row, 3, QTableWidgetItem(course['level']))
                table.setItem(row, 4, QTableWidgetItem(f"{course['first_name']} {course['last_name']}"))
                
                # Get schedule (placeholder implementation)
                schedule = "Mon, Wed, Fri 10:00-11:30"
                table.setItem(row, 5, QTableWidgetItem(schedule))
                
                # Add enroll button
                enroll_button = QPushButton("Enroll")
                enroll_button.setProperty("course_id", course['id'])
                enroll_button.clicked.connect(lambda checked, cid=course['id'], cname=course['name']: enroll_in_course(cid, cname))
                table.setCellWidget(row, 6, enroll_button)
                
                row += 1
                
            # Resize columns to content
            table.resizeColumnsToContents()
            
        # Function to enroll in a course
        def enroll_in_course(course_id, course_name):
            """Enroll in a course."""
            try:
                db = get_connection()
                cursor = db.cursor(dictionary=True)
                
                cursor.execute("START TRANSACTION")
                
                # Check enrollment limit
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM student_courses 
                    WHERE student_id = %s AND active = 1
                """, (self.user.user_id,))
                
                result = cursor.fetchone()
                if result and result['count'] >= 5:
                    db.rollback()
                    QMessageBox.warning(self, "Error",
                        "You cannot enroll in more than 5 courses")
                    return False

                # Check if already enrolled
                cursor.execute("""
                    SELECT id FROM student_courses
                    WHERE student_id = %s AND course_id = %s AND active = 1
                """, (self.user.user_id, course_id))
                
                if cursor.fetchone():
                    db.rollback() 
                    QMessageBox.warning(self, "Error",
                        "You are already enrolled in this course")
                    return False
                    
                # Check course capacity
                cursor.execute("""
                    SELECT c.max_students, COUNT(sc.id) as enrolled
                    FROM courses c
                    LEFT JOIN student_courses sc ON c.id = sc.course_id 
                    WHERE c.id = %s
                    GROUP BY c.id
                """, (course_id,))
                
                result = cursor.fetchone()
                if not result:
                    db.rollback()
                    QMessageBox.warning(self, "Error", "Course not found")
                    return False
                    
                if result['enrolled'] >= result['max_students']:
                    db.rollback()
                    QMessageBox.warning(self, "Error", "Course is full")
                    return False
                    
                # Enroll student
                cursor.execute("""
                    INSERT INTO student_courses 
                    (student_id, course_id, enrollment_date, active)
                    VALUES (%s, %s, CURRENT_DATE, 1)
                """, (self.user.user_id, course_id))
                
                db.commit()
                QMessageBox.information(self, "Success", 
                    f"Successfully enrolled in {course_name}")
                return True
                
            except Exception as e:
                if 'db' in locals():
                    db.rollback()
                QMessageBox.critical(self, "Error", str(e))
                return False
                
            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'db' in locals():
                    db.close()

        # Connect filter signals
        search_input.textChanged.connect(load_catalog_courses)
        language_combo.currentIndexChanged.connect(load_catalog_courses)
        level_combo.currentIndexChanged.connect(load_catalog_courses)
        
        # Load initial courses
        load_catalog_courses()
        
        # Show dialog
        dialog.exec_()
        
    def load_course_filter_combos(self):
        """Load course filter combo boxes with the student's courses."""
        # Get enrolled courses
        query = """
            SELECT c.id, c.name
            FROM courses c
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = %s AND sc.active = 1
            ORDER BY c.name
        """
        params = (self.user.user_id,)
        courses = execute_query(query, params=params, fetch=True)
        
        # Clear and repopulate combo boxes
        for combo in [
            self.ui.scheduleFilterComboBox,
            self.ui.lessonsCourseFilterComboBox,
            self.ui.gradesCourseFilterComboBox
        ]:
            combo.clear()
            combo.addItem("All Courses", -1)
            for course in courses:
                # Handle both dictionary and tuple results
                if isinstance(course, dict):
                    course_id = course['id']
                    course_name = course['name']
                else:
                    # Assuming tuple order: id, name
                    course_id = course[0]
                    course_name = course[1]
                combo.addItem(course_name, course_id)
                
    def load_schedule(self):
        """Load schedule for the selected course and date."""
        # Clear the table
        self.ui.scheduleTable.setRowCount(0)
        
        # Get selected course ID (or -1 for all courses)
        course_id = self.ui.scheduleFilterComboBox.currentData()
        
        # Get selected date
        selected_date = self.ui.scheduleDateEdit.date().toString("yyyy-MM-dd")
        
        # Get enrolled courses
        query = """
            SELECT c.id, c.name
            FROM courses c
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = %s AND sc.active = 1
        """
        params = (self.user.user_id,)
        
        if course_id != -1:
            query += " AND c.id = %s"
            params = params + (course_id,)
            
        courses = execute_query(query, params=params, fetch=True)
        
        # Populate table with schedule data
        row = 0
        for course in courses:
            # Handle both dictionary and tuple results
            if isinstance(course, dict):
                course_name = course['name']
            else:
                course_name = course[1]
                
            # Add a row for each schedule
            self.ui.scheduleTable.insertRow(row)
            
            # Add schedule data
            self.ui.scheduleTable.setItem(row, 0, QTableWidgetItem(selected_date))
            self.ui.scheduleTable.setItem(row, 1, QTableWidgetItem("10:00-11:30"))
            self.ui.scheduleTable.setItem(row, 2, QTableWidgetItem(course_name))
            self.ui.scheduleTable.setItem(row, 3, QTableWidgetItem("Introduction to Grammar"))
            self.ui.scheduleTable.setItem(row, 4, QTableWidgetItem("John Smith"))
            self.ui.scheduleTable.setItem(row, 5, QTableWidgetItem("Room 101"))
            
            row += 1
            
            # Add another row for a different time
            self.ui.scheduleTable.insertRow(row)
            
            # Add schedule data
            self.ui.scheduleTable.setItem(row, 0, QTableWidgetItem(selected_date))
            self.ui.scheduleTable.setItem(row, 1, QTableWidgetItem("14:00-15:30"))
            self.ui.scheduleTable.setItem(row, 2, QTableWidgetItem(course_name))
            self.ui.scheduleTable.setItem(row, 3, QTableWidgetItem("Conversation Practice"))
            self.ui.scheduleTable.setItem(row, 4, QTableWidgetItem("Jane Doe"))
            self.ui.scheduleTable.setItem(row, 5, QTableWidgetItem("Room 203"))
            
            row += 1
            
        # Resize columns to content
        self.ui.scheduleTable.resizeColumnsToContents()
        
    def filter_schedule(self):
        """Filter schedule based on selected course and date."""
        self.load_schedule()
        
    def export_schedule(self):
        """Export schedule to a CSV file."""
        try:
            # Get current schedule data from table
            rows = []
            for row in range(self.ui.scheduleTable.rowCount()):
                row_data = []
                for col in range(self.ui.scheduleTable.columnCount()):
                    item = self.ui.scheduleTable.item(row, col)
                    row_data.append(item.text() if item else "")
                rows.append(row_data)

            if not rows:
                QMessageBox.warning(self, "Export Schedule", "No schedule data to export.")
                return

            # Create CSV content
            header = ["Date", "Time", "Course", "Topic", "Teacher", "Room"] 
            csv_content = ",".join(header) + "\n"
            for row in rows:
                csv_content += ",".join(f'"{cell}"' for cell in row) + "\n"

            # Get save location from user
            from PyQt5.QtWidgets import QFileDialog
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Export Schedule",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )

            if filename:
                # Add .csv extension if not present
                if not filename.lower().endswith('.csv'):
                    filename += '.csv'

                # Save file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(csv_content)

                QMessageBox.information(
                    self,
                    "Export Schedule",
                    f"Schedule exported successfully to {filename}"
                )

        except Exception as e:
            QMessageBox.critical(
                self, 
                "Export Error",
                f"Failed to export schedule: {str(e)}"
            )
        
    def load_lessons(self):
        """Load lessons and exercises for the selected course and status."""
        # Clear the table
        self.ui.lessonsTable.setRowCount(0)
        
        # Get selected course ID (or -1 for all courses)
        course_id = self.ui.lessonsCourseFilterComboBox.currentData()
        
        # Get selected status
        status_index = self.ui.lessonsStatusFilterComboBox.currentIndex()
        status_filter = self.ui.lessonsStatusFilterComboBox.currentText() if status_index > 0 else None
        
        # Get enrolled courses
        query = """
            SELECT c.id, c.name
            FROM courses c
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = %s AND sc.active = 1
        """
        params = (self.user.user_id,)
        
        if course_id != -1:
            query += " AND c.id = %s"
            params = params + (course_id,)
            
        courses = execute_query(query, params=params, fetch=True)
        
        # Placeholder implementation - in a real app, this would query the database for lessons and exercises
        row = 0
        for course in courses:
            # Handle both dictionary and tuple results
            if isinstance(course, dict):
                course_name = course['name']
            else:
                course_name = course[1]
                
            # Add rows for lessons
            for i in range(1, 6):
                # Determine status based on lesson number
                if i <= 2:
                    status = "Completed"
                elif i == 3:
                    status = "In Progress"
                else:
                    status = "Not Started"
                    
                # Apply status filter if selected
                if status_filter and status != status_filter:
                    continue
                    
                self.ui.lessonsTable.insertRow(row)
                
                # Add lesson data with consistent access
                self.ui.lessonsTable.setItem(row, 0, QTableWidgetItem(f"L{i}"))
                self.ui.lessonsTable.setItem(row, 1, QTableWidgetItem(course_name))
                self.ui.lessonsTable.setItem(row, 2, QTableWidgetItem(f"Lesson {i}"))
                self.ui.lessonsTable.setItem(row, 3, QTableWidgetItem("Lesson"))
                
                # Due date is 1 week from now for each lesson
                due_date = datetime.now().date() + timedelta(days=7*i)  # Fixed timedelta usage
                self.ui.lessonsTable.setItem(row, 4, QTableWidgetItem(due_date.isoformat()))
                
                self.ui.lessonsTable.setItem(row, 5, QTableWidgetItem(status))
                
                # Add action buttons (view, start/continue)
                if status == "Not Started":
                    actions = "View | Start"
                elif status == "In Progress":
                    actions = "View | Continue"
                else:
                    actions = "View | Review"
                    
                self.ui.lessonsTable.setItem(row, 6, QTableWidgetItem(actions))
                
                row += 1
                
            # Add rows for exercises
            for i in range(1, 4):
                # Determine status based on exercise number
                if i <= 1:
                    status = "Completed"
                elif i == 2:
                    status = "In Progress"
                else:
                    status = "Not Started"
                    
                # Apply status filter if selected
                if status_filter and status != status_filter:
                    continue
                    
                self.ui.lessonsTable.insertRow(row)
                
                # Add exercise data
                self.ui.lessonsTable.setItem(row, 0, QTableWidgetItem(f"E{i}"))
                self.ui.lessonsTable.setItem(row, 1, QTableWidgetItem(course_name))
                self.ui.lessonsTable.setItem(row, 2, QTableWidgetItem(f"Exercise {i}"))
                self.ui.lessonsTable.setItem(row, 3, QTableWidgetItem("Exercise"))
                
                # Due date is 3 days from now for each exercise
                due_date = datetime.now().date() + timedelta(days=3*i)
                self.ui.lessonsTable.setItem(row, 4, QTableWidgetItem(due_date.isoformat()))
                
                self.ui.lessonsTable.setItem(row, 5, QTableWidgetItem(status))
                
                # Add action buttons (view, start/continue)
                if status == "Not Started":
                    actions = "View | Start"
                elif status == "In Progress":
                    actions = "View | Continue"
                else:
                    actions = "View | Review"
                    
                self.ui.lessonsTable.setItem(row, 6, QTableWidgetItem(actions))
                
                row += 1
                
        # Resize columns to content
        self.ui.lessonsTable.resizeColumnsToContents()
        
    def filter_lessons(self):
        """Filter lessons based on selected course and status."""
        self.load_lessons()
        
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
            
        # Get enrolled courses
        query = """
            SELECT c.id, c.name
            FROM courses c
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = %s AND sc.active = 1
        """
        params = (self.user.user_id,)
        
        if course_id != -1:
            query += " AND c.id = %s"
            params = params + (course_id,)
            
        courses = execute_query(query, params=params, fetch=True)
        
        # Placeholder implementation - in a real app, this would query the database for grades
        # For now, we'll just show some sample data
        row = 0
        for course in courses:
            # Handle both dictionary and tuple results
            if isinstance(course, dict):
                course_name = course['name']
            else:
                course_name = course[1]
                
            # Add exercise grades
            if grade_type is None or grade_type == "Exercise":
                for i in range(1, 4):
                    self.ui.gradesTable.insertRow(row)
                    
                    # Add grade data with consistent access
                    self.ui.gradesTable.setItem(row, 0, QTableWidgetItem(f"E{i}"))
                    self.ui.gradesTable.setItem(row, 1, QTableWidgetItem(course_name))
                    self.ui.gradesTable.setItem(row, 2, QTableWidgetItem("Exercise"))
                    self.ui.gradesTable.setItem(row, 3, QTableWidgetItem(f"Exercise {i}"))
                    
                    # Date is 1 week ago for each exercise
                    date = datetime.now().date() - timedelta(days=7*i)  # Fixed timedelta usage
                    self.ui.gradesTable.setItem(row, 4, QTableWidgetItem(date.isoformat()))
                    
                    # Grade is random between 70 and 100
                    grade = 70 + (i * 10)
                    self.ui.gradesTable.setItem(row, 5, QTableWidgetItem(f"{grade}%"))
                    
                    # Feedback
                    feedback = "Good work, but needs more practice with grammar."
                    self.ui.gradesTable.setItem(row, 6, QTableWidgetItem(feedback))
                    
                    row += 1
                    
            # Add test grades
            if grade_type is None or grade_type == "Test":
                for i in range(1, 3):
                    self.ui.gradesTable.insertRow(row)
                    
                    # Add grade data with consistent access
                    self.ui.gradesTable.setItem(row, 0, QTableWidgetItem(f"T{i}"))
                    self.ui.gradesTable.setItem(row, 1, QTableWidgetItem(course_name))
                    self.ui.gradesTable.setItem(row, 2, QTableWidgetItem("Test"))
                    
                    if i == 1:
                        test_name = "Midterm Exam"
                    else:
                        test_name = "Final Exam"
                        
                    self.ui.gradesTable.setItem(row, 3, QTableWidgetItem(test_name))
                    
                    # Date is 2 weeks ago for each test
                    date = datetime.now().date() - timedelta(days=14*i)  # Fixed timedelta usage
                    self.ui.gradesTable.setItem(row, 4, QTableWidgetItem(date.isoformat()))
                    
                    # Grade is random between 80 and 100
                    grade = 80 + (i * 10)
                    self.ui.gradesTable.setItem(row, 5, QTableWidgetItem(f"{grade}%"))
                    
                    # Feedback
                    feedback = "Excellent performance on the written section."
                    self.ui.gradesTable.setItem(row, 6, QTableWidgetItem(feedback))
                    
                    row += 1
                    
        # Resize columns to content
        self.ui.gradesTable.resizeColumnsToContents()
        
    def filter_grades(self):
        """Filter grades based on selected course and type."""
        self.load_grades()
        
    def export_grades(self):
        """Export grades to a CSV file."""
        try:
            # Get current grades data from table
            rows = []
            for row in range(self.ui.gradesTable.rowCount()):
                row_data = []
                for col in range(self.ui.gradesTable.columnCount()):
                    item = self.ui.gradesTable.item(row, col)
                    row_data.append(item.text() if item else "")
                rows.append(row_data)

            if not rows:
                QMessageBox.warning(self, "Export Grades", "No grade data to export.")
                return

            # Create CSV content
            header = ["ID", "Course", "Type", "Name", "Date", "Grade", "Feedback"]
            csv_content = ",".join(header) + "\n"
            for row in rows:
                csv_content += ",".join(f'"{cell}"' for cell in row) + "\n"

            # Get save location from user 
            from PyQt5.QtWidgets import QFileDialog
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Export Grades",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )

            if filename:
                # Add .csv extension if not present
                if not filename.lower().endswith('.csv'):
                    filename += '.csv'

                # Save file
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(csv_content)

                QMessageBox.information(
                    self,
                    "Export Grades",
                    f"Grades exported successfully to {filename}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error", 
                f"Failed to export grades: {str(e)}"
            )
        
    def load_payments(self):
        """Load payments for the student."""
        # Clear the table
        self.ui.paymentsTable.setRowCount(0)
        
        # Get selected status
        status_index = self.ui.paymentsStatusFilterComboBox.currentIndex()
        status_filter = self.ui.paymentsStatusFilterComboBox.currentText() if status_index > 0 else None
        
        # Placeholder implementation - in a real app, this would query the database for payments
        # For now, we'll just show some sample data
        payments = [
            {
                "id": 1,
                "date": "2023-01-15",
                "description": "Tuition for English B1",
                "amount": 500.00,
                "status": "Paid",
                "due_date": "2023-01-10"
            },
            {
                "id": 2,
                "date": "2023-02-15",
                "description": "Tuition for Spanish A2",
                "amount": 450.00,
                "status": "Paid",
                "due_date": "2023-02-10"
            },
            {
                "id": 3,
                "date": None,
                "description": "Tuition for French A1",
                "amount": 400.00,
                "status": "Pending",
                "due_date": "2023-03-10"
            },
            {
                "id": 4,
                "date": None,
                "description": "Late fee",
                "amount": 25.00,
                "status": "Overdue",
                "due_date": "2023-02-28"
            }
        ]
        
        # Filter payments by status
        if status_filter and status_filter != "All Status":
            payments = [p for p in payments if p["status"] == status_filter]
            
        # Populate the table
        for row, payment in enumerate(payments):
            self.ui.paymentsTable.insertRow(row)
            
            # Add payment data
            self.ui.paymentsTable.setItem(row, 0, QTableWidgetItem(str(payment["id"])))
            self.ui.paymentsTable.setItem(row, 1, QTableWidgetItem(payment["date"] if payment["date"] else ""))
            self.ui.paymentsTable.setItem(row, 2, QTableWidgetItem(payment["description"]))
            self.ui.paymentsTable.setItem(row, 3, QTableWidgetItem(f"${payment['amount']:.2f}"))
            self.ui.paymentsTable.setItem(row, 4, QTableWidgetItem(payment["status"]))
            self.ui.paymentsTable.setItem(row, 5, QTableWidgetItem(payment["due_date"]))
            
            # Add action button
            if payment["status"] == "Pending" or payment["status"] == "Overdue":
                actions = "Pay Now"
            else:
                actions = "View Receipt"
                
            self.ui.paymentsTable.setItem(row, 6, QTableWidgetItem(actions))
            
        # Resize columns to content
        self.ui.paymentsTable.resizeColumnsToContents()
        
    def filter_payments(self):
        """Filter payments based on selected status."""
        self.load_payments()
        
    def make_payment(self):
        """Open dialog to make a payment."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Make Payment")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Payment selection
        payment_layout = QHBoxLayout()
        payment_label = QLabel("Payment:")
        payment_combo = QComboBox()
        
        # Populate payment combo with pending/overdue payments
        payment_combo.addItem("Tuition for French A1 - $400.00", 3)
        payment_combo.addItem("Late fee - $25.00", 4)
        
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(payment_combo)
        layout.addLayout(payment_layout)
        
        # Payment method
        method_layout = QHBoxLayout()
        method_label = QLabel("Payment Method:")
        method_combo = QComboBox()
        method_combo.addItem("Credit Card")
        method_combo.addItem("Bank Transfer")
        method_combo.addItem("PayPal")
        
        method_layout.addWidget(method_label)
        method_layout.addWidget(method_combo)
        layout.addLayout(method_layout)
        
        # Credit card details (shown only when credit card is selected)
        card_details_widget = QWidget()
        card_details_layout = QVBoxLayout(card_details_widget)
        
        # Card number
        card_number_layout = QHBoxLayout()
        card_number_label = QLabel("Card Number:")
        card_number_input = QLineEdit()
        card_number_input.setPlaceholderText("1234 5678 9012 3456")
        card_number_layout.addWidget(card_number_label)
        card_number_layout.addWidget(card_number_input)
        card_details_layout.addLayout(card_number_layout)
        
        # Expiration date and CVV
        card_exp_cvv_layout = QHBoxLayout()
        
        # Expiration date
        card_exp_layout = QHBoxLayout()
        card_exp_label = QLabel("Expiration:")
        card_exp_month = QComboBox()
        for month in range(1, 13):
            card_exp_month.addItem(f"{month:02d}")
        card_exp_year = QComboBox()
        for year in range(datetime.now().year, datetime.now().year + 10):
            card_exp_year.addItem(str(year))
        card_exp_layout.addWidget(card_exp_label)
        card_exp_layout.addWidget(card_exp_month)
        card_exp_layout.addWidget(card_exp_year)
        card_exp_cvv_layout.addLayout(card_exp_layout)
        
        # CVV
        card_cvv_layout = QHBoxLayout()
        card_cvv_label = QLabel("CVV:")
        card_cvv_input = QLineEdit()
        card_cvv_input.setMaxLength(4)
        card_cvv_input.setFixedWidth(60)
        card_cvv_layout.addWidget(card_cvv_label)
        card_cvv_layout.addWidget(card_cvv_input)
        card_exp_cvv_layout.addLayout(card_cvv_layout)
        
        card_details_layout.addLayout(card_exp_cvv_layout)
        
        # Add card details to main layout
        layout.addWidget(card_details_widget)
        
        # Show/hide card details based on payment method
        def toggle_card_details():
            card_details_widget.setVisible(method_combo.currentText() == "Credit Card")
            
        method_combo.currentIndexChanged.connect(toggle_card_details)
        toggle_card_details()  # Initial state
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Pay Now")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Process payment (placeholder implementation)
            QMessageBox.information(
                self,
                "Payment Successful",
                "Your payment has been processed successfully."
            )
            
            # Refresh payments
            self.load_payments()
            
    def load_chats(self):
        """Load chats for the student."""
        # Clear the list
        self.ui.chatsList.clear()
        
        # Get teachers
        query = """
            SELECT u.id, u.first_name, u.last_name
            FROM users u
            JOIN courses c ON u.id = c.teacher_id
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = %s AND sc.active = 1
            GROUP BY u.id
        """
        params = (self.user.user_id,)
        teachers = execute_query(query, params=params, fetch=True)
        
        for teacher in teachers:
            # Handle both dictionary and tuple results
            if isinstance(teacher, dict):
                teacher_id = teacher['id']
                teacher_fname = teacher['first_name']
                teacher_lname = teacher['last_name']
            else:
                # Assuming tuple order: id, first_name, last_name
                teacher_id = teacher[0]
                teacher_fname = teacher[1]
                teacher_lname = teacher[2]
            
            # Create chat item with consistent access
            item = QListWidgetItem(f"{teacher_fname} {teacher_lname} (Teacher)")
            item.setData(Qt.UserRole, teacher_id)
            self.ui.chatsList.addItem(item)
            
        # Add admin chat
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
        # Remove duplicate code and undefined admin_item
        
        # Add sample messages
        messages = [
            {"sender_id": user_id, "text": "Hello, student!", "timestamp": "2023-05-01 10:00:00"},
            {"sender_id": self.user.user_id, "text": "Hi! I have a question about the homework.", "timestamp": "2023-05-01 10:05:00"},
            {"sender_id": user_id, "text": "Sure, what's your question?", "timestamp": "2023-05-01 10:10:00"},
            {"sender_id": self.user.user_id, "text": "I'm having trouble with exercise 3.", "timestamp": "2023-05-01 10:15:00"},
            {"sender_id": user_id, "text": "Let me explain it to you...", "timestamp": "2023-05-01 10:20:00"}
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
        self.ui.statusLabel.setText("Message sent.")
        
    def new_chat(self):
        """Open dialog to start a new chat."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("New Chat")
        dialog.setMinimumWidth(300)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # User selection
        user_layout = QHBoxLayout()
        user_label = QLabel("User:")
        user_combo = QComboBox()
        
        # Populate user combo with teachers and admin
        # In a real app, this would query the database for users
        user_combo.addItem("Admin", 1)
        user_combo.addItem("John Smith (Teacher)", 2)
        user_combo.addItem("Jane Doe (Teacher)", 3)
        
        user_layout.addWidget(user_label)
        user_layout.addWidget(user_combo)
        layout.addLayout(user_layout)
        
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
            
            # Check if chat already exists
            for i in range(self.ui.chatsList.count()):
                item = self.ui.chatsList.item(i)
                if item.data(Qt.UserRole) == user_id:
                    # Select existing chat
                    self.ui.chatsList.setCurrentItem(item)
                    return
                    
            # Create new chat
            item = QListWidgetItem(user_name)
            item.setData(Qt.UserRole, user_id)
            self.ui.chatsList.addItem(item)
            self.ui.chatsList.setCurrentItem(item)
            
            # Show status message
            self.ui.statusLabel.setText(f"New chat with {user_name} created.")
            
    def on_profile_updated(self):
        """Handle profile update events."""
        self.ui.welcomeLabel.setText(f"Welcome, {self.user.first_name} {self.user.last_name}")
        self.ui.statusLabel.setText("Profile updated successfully")

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
                db = get_connection()  # Use get_connection instead of undefined database()
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
                if 'cursor' in locals():
                    cursor.close()
                if 'db' in locals():
                    db.close()
                
    def handle_logout(self):
        """Handle user logout."""
        reply = QMessageBox.question(self, 'Confirm Logout',
                                   'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Emit logout signal
            self.logout_requested.emit()
            # Close the dashboard window
            self.close()