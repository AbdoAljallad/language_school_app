"""
Admin Dashboard View
------------------
This module contains the AdminDashboardView class, which implements the admin dashboard
functionality for the Language School Management System.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, 
    QDialogButtonBox, QListWidgetItem, QWidget, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSlot, QDate, pyqtSignal
from datetime import datetime

from app.ui.generated.admin_dashboard_ui import Ui_AdminDashboard
from app.views.dashboard_view import BaseDashboardView
from app.models.user_model import User
from app.models.course_model import Course
from app.models.schedule_model import Schedule
from app.models.report_model import Report  # Add this import
from app.utils import database
from app.utils.crypto import hash_password  # Will use plaintext instead of hashing



class AdminDashboardView(BaseDashboardView):
    """
    Admin dashboard view class.
    
    This class implements the admin dashboard functionality, including:
    - User management (add, edit, delete users)
    - Course management (add, edit, delete courses)
    - Schedule management
    - Payment management
    - Report generation
    """
    
    # Add profile_updated signal
    profile_updated = pyqtSignal()
    
    def __init__(self, user, parent=None):
        """
        Initialize the admin dashboard view.
        
        Args:
            user (User): The authenticated admin user
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(user, parent)
        self.ui = Ui_AdminDashboard()
        self.ui.setupUi(self)
        
        # Set welcome message
        self.ui.welcomeLabel.setText(f"Welcome, {self.user.first_name} {self.user.last_name}")
        
        # Set default dates to current date
        current_date = QDate.currentDate()
        self.ui.startDateEdit.setDate(current_date)
        self.ui.endDateEdit.setDate(current_date)

        # Connect signals and slots
        self.ui.logoutButton.clicked.connect(self.handle_logout)
        self.ui.actionLogout.triggered.connect(self.handle_logout)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionRefresh.triggered.connect(self.refresh_data)
        
        # Connect tab-specific signals and slots
        
        # Users tab
        self.ui.userSearchInput.textChanged.connect(self.filter_users)
        self.ui.userTypeFilter.currentIndexChanged.connect(self.filter_users)
        self.ui.addUserButton.clicked.connect(self.add_user)
        
        # Courses tab
        self.ui.courseSearchInput.textChanged.connect(self.filter_courses)
        self.ui.languageFilter.currentIndexChanged.connect(self.filter_courses)
        self.ui.levelFilter.currentIndexChanged.connect(self.filter_courses)
        self.ui.addCourseButton.clicked.connect(self.add_course)
        
        # Schedules tab
        self.ui.courseFilter.currentIndexChanged.connect(self.filter_schedules)
        self.ui.dayFilter.currentIndexChanged.connect(self.filter_schedules)  # Changed to use QComboBox signal
        self.ui.addScheduleButton.clicked.connect(self.add_schedule)
        
        # Payments tab
        self.ui.paymentSearchInput.textChanged.connect(self.filter_payments)
        self.ui.paymentStatusFilter.currentIndexChanged.connect(self.filter_payments)
        self.ui.addPaymentButton.clicked.connect(self.add_payment)
        
        # Reports tab
        self.ui.generateReportButton.clicked.connect(self.generate_report)
        self.ui.exportReportButton.clicked.connect(self.export_report)
        
        # Connect profile signals
        self.ui.profileButton.clicked.connect(self.open_profile_dialog)
        self.ui.actionProfile.triggered.connect(self.open_profile_dialog)
        self.profile_updated.connect(self.on_profile_updated)
        
        # Initialize data
        self.refresh_data()
        
        # Show status message
        self.ui.statusbar.showMessage("Ready")
        
    def refresh_data(self):
        """Refresh all data in the dashboard."""
        self.load_users()
        self.load_courses()
        self.load_schedules()
        self.load_payments()
        
    def load_users(self):
        """Load users into the users table."""
        # Get users with proper columns
        query = """
            SELECT u.id, u.username, u.first_name, u.last_name, 
                   u.email, u.user_type, u.active 
            FROM users u
        """
        if self.ui.userTypeFilter.currentIndex() > 0:
            query += " WHERE u.user_type = %s"
            params = (self.ui.userTypeFilter.currentText().lower(),)
        else:
            params = ()

        users = database.execute_query(query, params, fetch=True)
        
        # Clear and populate table
        self.ui.usersTable.setRowCount(0)
        
        search_text = self.ui.userSearchInput.text().lower()
        row = 0
        for user in users:
            # Apply search filter
            if search_text and not (
                search_text in user['username'].lower() or
                search_text in user['first_name'].lower() or
                search_text in user['last_name'].lower() or
                search_text in user['email'].lower()
            ):
                continue
                
            self.ui.usersTable.insertRow(row)
            
            # Add user data
            self.ui.usersTable.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.ui.usersTable.setItem(row, 1, QTableWidgetItem(user['username']))
            self.ui.usersTable.setItem(row, 2, QTableWidgetItem(user['first_name']))
            self.ui.usersTable.setItem(row, 3, QTableWidgetItem(user['last_name']))
            self.ui.usersTable.setItem(row, 4, QTableWidgetItem(user['email']))
            self.ui.usersTable.setItem(row, 5, QTableWidgetItem(user['user_type']))
            self.ui.usersTable.setItem(row, 6, QTableWidgetItem("Yes" if user['active'] else "No"))
            
            # Add edit and delete buttons
            edit_button = QPushButton("Edit")
            edit_button.setProperty("user_id", user['id'])
            edit_button.clicked.connect(lambda checked, uid=user['id']: self.edit_user(uid))
            
            delete_button = QPushButton("Delete")
            delete_button.setProperty("user_id", user['id'])
            delete_button.clicked.connect(lambda checked, uid=user['id']: self.delete_user(uid))
            
            # Create a widget to hold the buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.ui.usersTable.setCellWidget(row, 7, actions_widget)
            
            row += 1
            
        # Resize columns to content
        self.ui.usersTable.resizeColumnsToContents()
        
    def filter_users(self):
        """Filter users based on search text and user type filter."""
        self.load_users()
        
    def add_user(self):
        """Open dialog to add a new user."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add User")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Username
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_input = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_input)
        form_layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_input)
        form_layout.addLayout(password_layout)
        
        # First name
        first_name_layout = QHBoxLayout()
        first_name_label = QLabel("First Name:")
        first_name_input = QLineEdit()
        first_name_layout.addWidget(first_name_label)
        first_name_layout.addWidget(first_name_input)
        form_layout.addLayout(first_name_layout)
        
        # Last name
        last_name_layout = QHBoxLayout()
        last_name_label = QLabel("Last Name:")
        last_name_input = QLineEdit()
        last_name_layout.addWidget(last_name_label)
        last_name_layout.addWidget(last_name_input)
        form_layout.addLayout(last_name_layout)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_input)
        form_layout.addLayout(email_layout)
        
        # User type
        user_type_layout = QHBoxLayout()
        user_type_label = QLabel("User Type:")
        user_type_combo = QComboBox()
        user_type_combo.addItem("Admin", "admin")
        user_type_combo.addItem("Teacher", "teacher")
        user_type_combo.addItem("Student", "student")
        user_type_layout.addWidget(user_type_label)
        user_type_layout.addWidget(user_type_combo)
        form_layout.addLayout(user_type_layout)
        
        # Active
        active_layout = QHBoxLayout()
        active_label = QLabel("Active:")
        active_combo = QComboBox()
        active_combo.addItem("Yes", 1)
        active_combo.addItem("No", 0)
        active_layout.addWidget(active_label)
        active_layout.addWidget(active_combo)
        form_layout.addLayout(active_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get form values
            username = username_input.text().strip()
            password = password_input.text().strip()
            first_name = first_name_input.text().strip()
            last_name = last_name_input.text().strip()
            email = email_input.text().strip()
            user_type = user_type_combo.currentData()
            active = active_combo.currentData()
            
            # Validate form
            if not username or not password or not first_name or not last_name or not email:
                QMessageBox.warning(self, "Validation Error", "All fields are required.")
                return
                
            # Check if username already exists
            query = "SELECT COUNT(*) FROM users WHERE username = %s"
            params = (username,)
            result = database.execute_query(query, params, fetch=True)
            if result and len(result) > 0 and result[0].get('COUNT(*)', 0) > 0:
                QMessageBox.warning(self, "Validation Error", "Username already exists.")
                return
                
            # Create user - store password in plaintext
            query = """
                INSERT INTO users (username, password, first_name, last_name, email, user_type, active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (username, password, first_name, last_name, email, user_type, active)
            database.execute_query(query, params, commit=True)
            
            # Refresh users table
            self.load_users()
            
            # Show success message
            self.ui.statusbar.showMessage(f"User {username} added successfully.")
            
    def edit_user(self, user_id):
        """Open dialog to edit a user."""
        # Get user data
        query = """
            SELECT username, password, first_name, last_name, email, user_type, active
            FROM users WHERE id = %s
        """
        result = database.execute_query(query, (user_id,), fetch=True)
        if not result:
            QMessageBox.warning(self, "Error", "User not found.")
            return

        user = result[0]
        
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        form_layout = QVBoxLayout()
        
        # Username (readonly)
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_input = QLineEdit()
        username_input.setText(user['username'])
        username_input.setReadOnly(True)
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_input)
        form_layout.addLayout(username_layout)

        # New Password field
        password_layout = QHBoxLayout()
        password_label = QLabel("New Password:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Leave empty to keep current password")
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_input)
        form_layout.addLayout(password_layout)
        
        # First name
        first_name_layout = QHBoxLayout()
        first_name_label = QLabel("First Name:")
        first_name_input = QLineEdit()
        first_name_input.setText(user['first_name'])
        first_name_layout.addWidget(first_name_label)
        first_name_layout.addWidget(first_name_input)
        form_layout.addLayout(first_name_layout)
        
        # Last name
        last_name_layout = QHBoxLayout()
        last_name_label = QLabel("Last Name:")
        last_name_input = QLineEdit()
        last_name_input.setText(user['last_name'])
        last_name_layout.addWidget(last_name_label)
        last_name_layout.addWidget(last_name_input)
        form_layout.addLayout(last_name_layout)
        
        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_input = QLineEdit()
        email_input.setText(user['email'])
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_input)
        form_layout.addLayout(email_layout)
        
        # User type
        user_type_layout = QHBoxLayout()
        user_type_label = QLabel("User Type:")
        user_type_combo = QComboBox()
        user_type_combo.addItems(['admin', 'teacher', 'student'])
        user_type_combo.setCurrentText(user['user_type'])
        user_type_layout.addWidget(user_type_label)
        user_type_layout.addWidget(user_type_combo)
        form_layout.addLayout(user_type_layout)
        
        # Active status
        active_layout = QHBoxLayout()
        active_label = QLabel("Active:")
        active_combo = QComboBox()
        active_combo.addItems(['Yes', 'No'])
        active_combo.setCurrentText('Yes' if user['active'] else 'No')
        active_layout.addWidget(active_label)
        active_layout.addWidget(active_combo)
        form_layout.addLayout(active_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # Start building the query
            query = "UPDATE users SET"
            params = []

            # Add regular fields
            params.extend([
                first_name_input.text(),
                last_name_input.text(),
                email_input.text(),
                user_type_combo.currentText(),
                1 if active_combo.currentText() == 'Yes' else 0
            ])

            # Build the SET part of the query
            set_clauses = [
                "first_name = %s",
                "last_name = %s", 
                "email = %s",
                "user_type = %s",
                "active = %s"
            ]

            # Add password update if provided
            new_password = password_input.text().strip()
            if new_password:
                set_clauses.append("password = %s")
                params.append(new_password)

            # Complete the query
            query += " " + ", ".join(set_clauses)
            query += ", updated_at = CURRENT_TIMESTAMP WHERE id = %s"
            params.append(user_id)

            # Execute update
            try:
                database.execute_query(query, params, commit=True)
                self.load_users()
                QMessageBox.information(self, "Success", "User updated successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update user: {str(e)}")

    def delete_user(self, user_id):
        """Delete a user from the system."""
        query = "SELECT username FROM users WHERE id = %s"
        result = database.execute_query(query, (user_id,), fetch=True)
        
        if not result:
            QMessageBox.warning(self, "Error", "User not found")
            return
            
        user = result[0]
        
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete user {user['username']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # First delete related records
            delete_queries = [
                ("DELETE FROM student_courses WHERE student_id = %s", (user_id,)),
                ("DELETE FROM student_lesson_progress WHERE student_id = %s", (user_id,)),
                ("DELETE FROM student_exercise_submissions WHERE student_id = %s", (user_id,)),
                ("DELETE FROM attendance WHERE student_id = %s", (user_id,)),
                ("DELETE FROM payments WHERE student_id = %s", (user_id,)),
                ("DELETE FROM chat_messages WHERE sender_id = %s", (user_id,)),
                ("DELETE FROM chats WHERE user1_id = %s OR user2_id = %s", (user_id, user_id)),  # Fixed: pass user_id twice
                ("DELETE FROM notifications WHERE user_id = %s", (user_id,)),
                ("DELETE FROM users WHERE id = %s", (user_id,))
            ]
            
            # Execute all deletes in a transaction
            try:
                db = database.get_connection()
                cursor = db.cursor()
                
                for query, params in delete_queries:  # Updated to use query and params pairs
                    cursor.execute(query, params)
                    
                db.commit()
                self.load_users()  # Refresh table
                QMessageBox.information(self, "Success", "User deleted successfully")
                
            except Exception as e:
                db.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete user: {str(e)}")
            finally:
                cursor.close()
                db.close()

    def load_courses(self):
        """Load courses into the courses table."""
        # Clear the table
        self.ui.coursesTable.setRowCount(0)
        
        # Get search text and filters
        search_text = self.ui.courseSearchInput.text().lower()
        language_index = self.ui.languageFilter.currentIndex()
        language_filter = self.ui.languageFilter.currentText() if language_index > 0 else None
        level_index = self.ui.levelFilter.currentIndex()
        level_filter = self.ui.levelFilter.currentText() if level_index > 0 else None
        
        # Get courses
        query = """
            SELECT c.id, c.name, c.language, c.level, c.description, c.price, c.active,
                   u.first_name, u.last_name
            FROM courses c
            JOIN users u ON c.teacher_id = u.id
        """
        params = ()
        
        # Apply filters
        where_clauses = []
        
        if language_filter:
            where_clauses.append("c.language = %s")
            params = params + (language_filter,)
            
        if level_filter:
            where_clauses.append("c.level = %s")
            params = params + (level_filter,)
            
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
            
        courses = database.execute_query(query, params, fetch=True)
        
        # Populate the table
        row = 0
        for course in courses:
            # Apply search filter
            if search_text and not (
                search_text in course['name'].lower() or
                search_text in course['description'].lower()
            ):
                continue
                
            self.ui.coursesTable.insertRow(row)
            
            # Add course data
            self.ui.coursesTable.setItem(row, 0, QTableWidgetItem(str(course['id'])))
            self.ui.coursesTable.setItem(row, 1, QTableWidgetItem(course['name']))
            self.ui.coursesTable.setItem(row, 2, QTableWidgetItem(course['language']))
            self.ui.coursesTable.setItem(row, 3, QTableWidgetItem(course['level']))
            self.ui.coursesTable.setItem(row, 4, QTableWidgetItem(f"{course['first_name']} {course['last_name']}"))
            self.ui.coursesTable.setItem(row, 5, QTableWidgetItem(f"${course['price']:.2f}"))
            self.ui.coursesTable.setItem(row, 6, QTableWidgetItem("Yes" if course['active'] else "No"))
            
            # Add edit and delete buttons
            edit_button = QPushButton("Edit")
            edit_button.setProperty("course_id", course['id'])
            edit_button.clicked.connect(lambda checked, cid=course['id']: self.edit_course(cid))
            
            delete_button = QPushButton("Delete")
            delete_button.setProperty("course_id", course['id'])
            delete_button.clicked.connect(lambda checked, cid=course['id']: self.delete_course(cid))
            
            # Create a widget to hold the buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.ui.coursesTable.setCellWidget(row, 7, actions_widget)
            
            row += 1
            
        # Resize columns to content
        self.ui.coursesTable.resizeColumnsToContents()
        
    def filter_courses(self):
        """Filter courses based on search text and filters."""
        self.load_courses()
        
    def add_course(self):
        """Open dialog to add a new course."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Course")
        dialog.setMinimumWidth(500)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Course name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)
        form_layout.addLayout(name_layout)
        
        # Language
        language_layout = QHBoxLayout()
        language_label = QLabel("Language:")
        language_combo = QComboBox()
        language_combo.addItem("English")
        language_combo.addItem("Spanish")
        language_combo.addItem("French")
        language_combo.addItem("German")
        language_combo.addItem("Italian")
        language_combo.addItem("Russian")
        language_combo.addItem("Chinese")
        language_combo.addItem("Japanese")
        language_layout.addWidget(language_label)
        language_layout.addWidget(language_combo)
        form_layout.addLayout(language_layout)
        
        # Level
        level_layout = QHBoxLayout()
        level_label = QLabel("Level:")
        level_combo = QComboBox()
        level_combo.addItem("A1")
        level_combo.addItem("A2")
        level_combo.addItem("B1")
        level_combo.addItem("B2")
        level_combo.addItem("C1")
        level_combo.addItem("C2")
        level_layout.addWidget(level_label)
        level_layout.addWidget(level_combo)
        form_layout.addLayout(level_layout)
        
        # Description
        description_layout = QVBoxLayout()
        description_label = QLabel("Description:")
        description_input = QLineEdit()
        description_layout.addWidget(description_label)
        description_layout.addWidget(description_input)
        form_layout.addLayout(description_layout)
        
        # Price
        price_layout = QHBoxLayout()
        price_label = QLabel("Price:")
        price_input = QLineEdit()
        price_input.setPlaceholderText("0.00")
        price_layout.addWidget(price_label)
        price_layout.addWidget(price_input)
        form_layout.addLayout(price_layout)
        
        # Teacher
        teacher_layout = QHBoxLayout()
        teacher_label = QLabel("Teacher:")
        teacher_combo = QComboBox()
        
        # Get teachers
        query = """
            SELECT id, first_name, last_name
            FROM users
            WHERE user_type = 'teacher' AND active = 1
            ORDER BY last_name, first_name
        """
        teachers = database.execute_query(query, fetch=True)
        
        for teacher in teachers:
            teacher_combo.addItem(f"{teacher['first_name']} {teacher['last_name']}", teacher['id'])
            
        teacher_layout.addWidget(teacher_label)
        teacher_layout.addWidget(teacher_combo)
        form_layout.addLayout(teacher_layout)
        
        # Active
        active_layout = QHBoxLayout()
        active_label = QLabel("Active:")
        active_combo = QComboBox()
        active_combo.addItem("Yes", 1)
        active_combo.addItem("No", 0)
        active_layout.addWidget(active_label)
        active_layout.addWidget(active_combo)
        form_layout.addLayout(active_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get form values
            name = name_input.text().strip()
            language = language_combo.currentText()
            level = level_combo.currentText()
            description = description_input.text().strip()
            
            # Validate price
            try:
                price = float(price_input.text().strip())
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Price must be a valid number.")
                return
                
            teacher_id = teacher_combo.currentData()
            active = active_combo.currentData()
            
            # Validate form
            if not name or not description:
                QMessageBox.warning(self, "Validation Error", "Name and description are required.")
                return
                
            # Create course
            query = """
                INSERT INTO courses (name, language, level, description, price, teacher_id, active)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (name, language, level, description, price, teacher_id, active)
            database.execute_query(query, params, commit=True)
            
            # Refresh courses table
            self.load_courses()
            
            # Show success message
            self.ui.statusbar.showMessage(f"Course {name} added successfully.")
            
    def edit_course(self, course_id):
        """Open dialog to edit a course."""
        # Get course data
        query = """
            SELECT name, language, level, description, price, teacher_id, active
            FROM courses
            WHERE id = %s
        """
        params = (course_id,)
        result = database.execute_query(query, params, fetch=True)
        course = result[0] if result and len(result) > 0 else None
        
        if not course:
            QMessageBox.warning(self, "Error", "Course not found.")
            return
            
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Course")
        dialog.setMinimumWidth(500)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Course name
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        name_input = QLineEdit()
        name_input.setText(course['name'])
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)
        form_layout.addLayout(name_layout)
        
        # Language
        language_layout = QHBoxLayout()
        language_label = QLabel("Language:")
        language_combo = QComboBox()
        language_combo.addItem("English")
        language_combo.addItem("Spanish")
        language_combo.addItem("French")
        language_combo.addItem("German")
        language_combo.addItem("Italian")
        language_combo.addItem("Russian")
        language_combo.addItem("Chinese")
        language_combo.addItem("Japanese")
        
        # Set current language
        language_index = language_combo.findText(course['language'])
        if language_index >= 0:
            language_combo.setCurrentIndex(language_index)
            
        language_layout.addWidget(language_label)
        language_layout.addWidget(language_combo)
        form_layout.addLayout(language_layout)
        
        # Level
        level_layout = QHBoxLayout()
        level_label = QLabel("Level:")
        level_combo = QComboBox()
        level_combo.addItem("A1")
        level_combo.addItem("A2")
        level_combo.addItem("B1")
        level_combo.addItem("B2")
        level_combo.addItem("C1")
        level_combo.addItem("C2")
        
        # Set current level
        level_index = level_combo.findText(course['level'])
        if level_index >= 0:
            level_combo.setCurrentIndex(level_index)
            
        level_layout.addWidget(level_label)
        level_layout.addWidget(level_combo)
        form_layout.addLayout(level_layout)
        
        # Description
        description_layout = QVBoxLayout()
        description_label = QLabel("Description:")
        description_input = QLineEdit()
        description_input.setText(course['description'])
        description_layout.addWidget(description_label)
        description_layout.addWidget(description_input)
        form_layout.addLayout(description_layout)
        
        # Price
        price_layout = QHBoxLayout()
        price_label = QLabel("Price:")
        price_input = QLineEdit()
        price_input.setText(str(course['price']))
        price_layout.addWidget(price_label)
        price_layout.addWidget(price_input)
        form_layout.addLayout(price_layout)
        
        # Teacher
        teacher_layout = QHBoxLayout()
        teacher_label = QLabel("Teacher:")
        teacher_combo = QComboBox()
        
        # Get teachers
        query = """
            SELECT id, first_name, last_name
            FROM users
            WHERE user_type = 'teacher' AND active = 1
            ORDER BY last_name, first_name
        """
        teachers = database.execute_query(query, fetch=True)
        
        for teacher in teachers:
            teacher_combo.addItem(f"{teacher['first_name']} {teacher['last_name']}", teacher['id'])
            
        # Set current teacher
        for i in range(teacher_combo.count()):
            if teacher_combo.itemData(i) == course['teacher_id']:
                teacher_combo.setCurrentIndex(i)
                break
                
        teacher_layout.addWidget(teacher_label)
        teacher_layout.addWidget(teacher_combo)
        form_layout.addLayout(teacher_layout)
        
        # Active
        active_layout = QHBoxLayout()
        active_label = QLabel("Active:")
        active_combo = QComboBox()
        active_combo.addItem("Yes", 1)
        active_combo.addItem("No", 0)
        
        # Set current active status
        active_combo.setCurrentIndex(0 if course['active'] else 1)
        
        active_layout.addWidget(active_label)
        active_layout.addWidget(active_combo)
        form_layout.addLayout(active_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get form values
            name = name_input.text().strip()
            language = language_combo.currentText()
            level = level_combo.currentText()
            description = description_input.text().strip()
            
            # Validate price
            try:
                price = float(price_input.text().strip())
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Price must be a valid number.")
                return
                
            teacher_id = teacher_combo.currentData()
            active = active_combo.currentData()
            
            # Validate form
            if not name or not description:
                QMessageBox.warning(self, "Validation Error", "Name and description are required.")
                return
                
            # Update course
            query = """
                UPDATE courses
                SET name = %s, language = %s, level = %s, description = %s, price = %s, teacher_id = %s, active = %s
                WHERE id = %s
            """
            params = (name, language, level, description, price, teacher_id, active, course_id)
            database.execute_query(query, params, commit=True)
            
            # Refresh courses table
            self.load_courses()
            
            # Show success message
            self.ui.statusbar.showMessage(f"Course {name} updated successfully.")
            
    def delete_course(self, course_id):
        """Delete a course and all related records."""
        # Get course data
        query = "SELECT name FROM courses WHERE id = %s"
        params = (course_id,)
        result = database.execute_query(query, params, fetch=True)
        course = result[0] if result and len(result) > 0 else None
        
        if not course:
            QMessageBox.warning(self, "Error", "Course not found.")
            return
            
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete course {course['name']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete course and related records in a transaction
            delete_queries = [
                ("DELETE FROM student_courses WHERE course_id = %s", (course_id,)),
                ("DELETE FROM schedules WHERE course_id = %s", (course_id,)),
                ("DELETE FROM lessons WHERE course_id = %s", (course_id,)),
                ("DELETE FROM courses WHERE id = %s", (course_id,))
            ]
            
            try:
                db = database.get_connection()
                cursor = db.cursor()
                
                for query, params in delete_queries:
                    cursor.execute(query, params)
                    
                db.commit()
                self.load_courses()
                self.ui.statusbar.showMessage(f"Course {course['name']} deleted successfully.")
                
            except Exception as e:
                db.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete course: {str(e)}")
            finally:
                cursor.close()
                db.close()

    def load_schedules(self):
        """Load schedules into the schedules table."""
        # Clear the table
        self.ui.schedulesTable.setRowCount(0)
        
        # Get selected course ID and day
        course_id = self.ui.courseFilter.currentData()
        day = self.ui.dayFilter.currentText()
        if day == "All Days":
            day = None
        
        # Get schedules from database
        schedules = Schedule.get_schedules(
            course_id=course_id if course_id != -1 else None,
            day=day
        )
        
        # Populate the table
        for row, schedule in enumerate(schedules):
            self.ui.schedulesTable.insertRow(row)
            
            # Add schedule data
            self.ui.schedulesTable.setItem(row, 0, QTableWidgetItem(str(schedule['id'])))
            self.ui.schedulesTable.setItem(row, 1, QTableWidgetItem(schedule['course_name']))
            self.ui.schedulesTable.setItem(row, 2, QTableWidgetItem(schedule['day_of_week']))
            self.ui.schedulesTable.setItem(row, 3, QTableWidgetItem(str(schedule['start_time'])))
            self.ui.schedulesTable.setItem(row, 4, QTableWidgetItem(str(schedule['end_time'])))
            self.ui.schedulesTable.setItem(row, 5, QTableWidgetItem(schedule['room']))
            self.ui.schedulesTable.setItem(row, 6, QTableWidgetItem(
                f"{schedule['first_name']} {schedule['last_name']}"
            ))
            
            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda x, s=schedule['id']: self.edit_schedule(s))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda x, s=schedule['id']: self.delete_schedule(s))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.ui.schedulesTable.setCellWidget(row, 7, actions_widget)
            
        # Resize columns to content
        self.ui.schedulesTable.resizeColumnsToContents()
        
    def filter_schedules(self):
        """Filter schedules based on selected course and date."""
        self.load_schedules()
        
    def add_schedule(self):
        """Open dialog to add a new schedule."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Schedule")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        form_layout = QVBoxLayout()
        
        # Course selection
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_combo = QComboBox()
        
        # Get active courses
        query = """
            SELECT id, name FROM courses 
            WHERE active = 1 
            ORDER BY name
        """
        courses = database.execute_query(query, fetch=True)
        
        for course in courses:
            course_combo.addItem(course['name'], course['id'])
            
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_combo)
        form_layout.addLayout(course_layout)
        
        # Day selection
        day_layout = QHBoxLayout()
        day_label = QLabel("Day:")
        day_combo = QComboBox()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        day_combo.addItems(days)
        day_layout.addWidget(day_label)
        day_layout.addWidget(day_combo)
        form_layout.addLayout(day_layout)
        
        # Time selection
        time_layout = QHBoxLayout()
        start_label = QLabel("Time:")
        start_time = QLineEdit()
        start_time.setPlaceholderText("HH:MM")
        end_time = QLineEdit()
        end_time.setPlaceholderText("HH:MM")
        time_layout.addWidget(start_label)
        time_layout.addWidget(start_time)
        time_layout.addWidget(QLabel("to"))
        time_layout.addWidget(end_time)
        form_layout.addLayout(time_layout)
        
        # Room
        room_layout = QHBoxLayout()
        room_label = QLabel("Room:")
        room_input = QLineEdit()
        room_layout.addWidget(room_label)
        room_layout.addWidget(room_input)
        form_layout.addLayout(room_layout)
        
        layout.addLayout(form_layout)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            schedule = Schedule(
                course_id=course_combo.currentData(),
                day_of_week=day_combo.currentText(),
                start_time=start_time.text(),
                end_time=end_time.text(),
                room=room_input.text()
            )
            
            if schedule.save():
                self.load_schedules()
                QMessageBox.information(self, "Success", "Schedule added successfully")
            else:
                QMessageBox.critical(self, "Error", "Failed to add schedule")

    def edit_schedule(self, schedule_id):
        """Open dialog to edit a schedule."""
        # Get schedule data
        query = """
            SELECT s.*, c.name as course_name 
            FROM schedules s
            JOIN courses c ON s.course_id = c.id
            WHERE s.id = %s
        """
        result = database.execute_query(query, (schedule_id,), fetch=True)
        if not result:
            QMessageBox.warning(self, "Error", "Schedule not found")
            return
            
        schedule = result[0]
        
        # Create edit dialog (similar to add dialog but populated)
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit Schedule - {schedule['course_name']}")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        form_layout = QVBoxLayout()
        
        # Course selection (readonly)
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_input = QLineEdit()
        course_input.setText(schedule['course_name'])
        course_input.setReadOnly(True)
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_input)
        form_layout.addLayout(course_layout)

        # Day selection
        day_layout = QHBoxLayout()
        day_label = QLabel("Day:")
        day_combo = QComboBox()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        day_combo.addItems(days)
        day_combo.setCurrentText(schedule['day_of_week'])
        day_layout.addWidget(day_label)
        day_layout.addWidget(day_combo)
        form_layout.addLayout(day_layout)
        
        # Time selection
        time_layout = QHBoxLayout()
        start_label = QLabel("Time:")
        start_time = QLineEdit()
        start_time.setPlaceholderText("HH:MM")
        start_time.setText(schedule['start_time'])
        end_time = QLineEdit()
        end_time.setPlaceholderText("HH:MM")
        end_time.setText(schedule['end_time'])
        time_layout.addWidget(start_label)
        time_layout.addWidget(start_time)
        time_layout.addWidget(QLabel("to"))
        time_layout.addWidget(end_time)
        form_layout.addLayout(time_layout)
        
        # Room
        room_layout = QHBoxLayout()
        room_label = QLabel("Room:")
        room_input = QLineEdit()
        room_input.setText(schedule['room'])
        room_layout.addWidget(room_label)
        room_layout.addWidget(room_input)
        form_layout.addLayout(room_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            # Update schedule data
            schedule.day_of_week = day_combo.currentText()
            schedule.start_time = start_time.text()
            schedule.end_time = end_time.text()
            schedule.room = room_input.text()
            
            if schedule.save():
                self.load_schedules()
                QMessageBox.information(self, "Success", "Schedule updated successfully")
            else:
                QMessageBox.critical(self, "Error", "Failed to update schedule")

    def delete_schedule(self, schedule_id):
        """Delete a schedule."""
        if Schedule.delete(schedule_id):
            self.load_schedules()
            QMessageBox.information(self, "Success", "Schedule deleted successfully")
        else:
            QMessageBox.critical(self, "Error", "Failed to delete schedule")

    def load_payments(self):
        """Load payments into the payments table."""
        # Placeholder implementation - in a real app, this would query the database for payments
        # For now, we'll just show some sample data
        
        # Clear the table
        self.ui.paymentsTable.setRowCount(0)
        
        # Get search text and status filter
        search_text = self.ui.paymentSearchInput.text().lower()
        status_index = self.ui.paymentStatusFilter.currentIndex()
        status_filter = self.ui.paymentStatusFilter.currentText() if status_index > 0 else None
        
        # Add some sample data
        payments = [
            {
                "id": 1,
                "student": "Alice Johnson",
                "course": "English B1",
                "amount": 500.00,
                "date": "2023-01-15",
                "status": "Paid",
                "method": "Credit Card"
            },
            {
                "id": 2,
                "student": "Bob Smith",
                "course": "Spanish A2",
                "amount": 450.00,
                "date": "2023-02-15",
                "status": "Paid",
                "method": "Bank Transfer"
            },
            {
                "id": 3,
                "student": "Charlie Brown",
                "course": "French A1",
                "amount": 400.00,
                "date": None,
                "status": "Pending",
                "method": None
            },
            {
                "id": 4,
                "student": "David Wilson",
                "course": "German B2",
                "amount": 550.00,
                "date": None,
                "status": "Overdue",
                "method": None
            }
        ]
        
        # Filter payments by status
        if status_filter and status_filter != "All Status":
            payments = [p for p in payments if p["status"] == status_filter]
            
        # Filter payments by search text
        if search_text:
            payments = [p for p in payments if (
                search_text in p["student"].lower() or
                search_text in p["course"].lower()
            )]
            
        # Populate the table
        for row, payment in enumerate(payments):
            self.ui.paymentsTable.insertRow(row)
            
            # Add payment data
            self.ui.paymentsTable.setItem(row, 0, QTableWidgetItem(str(payment["id"])))
            self.ui.paymentsTable.setItem(row, 1, QTableWidgetItem(payment["student"]))
            self.ui.paymentsTable.setItem(row, 2, QTableWidgetItem(payment["course"]))
            self.ui.paymentsTable.setItem(row, 3, QTableWidgetItem(f"${payment['amount']:.2f}"))
            self.ui.paymentsTable.setItem(row, 4, QTableWidgetItem(payment["date"] if payment["date"] else ""))
            self.ui.paymentsTable.setItem(row, 5, QTableWidgetItem(payment["status"]))
            self.ui.paymentsTable.setItem(row, 6, QTableWidgetItem(payment["method"] if payment["method"] else ""))
            
            # Add edit and delete buttons
            edit_button = QPushButton("Edit")
            edit_button.setProperty("payment_id", payment["id"])
            edit_button.clicked.connect(lambda checked, pid=payment["id"]: self.edit_payment(pid))
            
            delete_button = QPushButton("Delete")
            delete_button.setProperty("payment_id", payment["id"])
            delete_button.clicked.connect(lambda checked, pid=payment["id"]: self.delete_payment(pid))
            
            # Create a widget to hold the buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.ui.paymentsTable.setCellWidget(row, 7, actions_widget)
            
        # Resize columns to content
        self.ui.paymentsTable.resizeColumnsToContents()
        
    def filter_payments(self):
        """Filter payments based on search text and status filter."""
        self.load_payments()
        
    def add_payment(self):
        """Open dialog to add a new payment."""
        # Placeholder implementation - in a real app, this would add a new payment to the database
        QMessageBox.information(self, "Add Payment", "Payment added successfully.")
        self.load_payments()
        
    def edit_payment(self, payment_id):
        """Open dialog to edit a payment."""
        # Placeholder implementation - in a real app, this would edit a payment in the database
        QMessageBox.information(self, "Edit Payment", f"Payment {payment_id} edited successfully.")
        self.load_payments()
        
    def delete_payment(self, payment_id):
        """Delete a payment."""
        # Placeholder implementation - in a real app, this would delete a payment from the database
        QMessageBox.information(self, "Delete Payment", f"Payment {payment_id} deleted successfully.")
        self.load_payments()
        
    def generate_report(self):
        """Generate a report based on selected criteria."""
        try:
            # Clear existing data
            self.ui.reportsTable.setRowCount(0)
            self.ui.reportsTable.setColumnCount(0)
            self.ui.exportReportButton.setEnabled(False)
            
            # Get report parameters
            report_type = self.ui.reportTypeComboBox.currentText().lower().replace(' ', '_')
            start_date = self.ui.startDateEdit.date().toString('yyyy-MM-dd')
            end_date = self.ui.endDateEdit.date().toString('yyyy-MM-dd')
            
            # Generate report
            data = Report.generate_report(report_type, start_date, end_date)
            
            if not data:
                self.ui.statusbar.showMessage("No data available for the selected criteria")
                return
            
            # Set up table
            self.ui.reportsTable.setColumnCount(len(data[0].keys()))
            self.ui.reportsTable.setHorizontalHeaderLabels(data[0].keys())
            
            # Populate data
            empty_report = True
            for row, record in enumerate(data):
                if any(v for v in record.values() if v not in (None, '', 0)):
                    empty_report = False
                self.ui.reportsTable.insertRow(row)
                for col, (key, value) in enumerate(record.items()):
                    display_value = str(value) if value not in (None, '') else '-'
                    item = QTableWidgetItem(display_value)
                    if isinstance(value, (int, float)):
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.ui.reportsTable.setItem(row, col, item)
            
            # Enable export if we have data
            self.ui.exportReportButton.setEnabled(not empty_report)
            
            # Format table
            self.ui.reportsTable.resizeColumnsToContents()
            self.ui.reportsTable.resizeRowsToContents()
            
            # Show status
            if not empty_report:
                self.ui.statusbar.showMessage(f"Report generated successfully - {len(data)} records found")
            else:
                self.ui.statusbar.showMessage("No data available for the selected criteria")
            
        except Exception as e:
            self.ui.statusbar.showMessage(f"Error generating report: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")

    def export_report(self):
        """Export the generated report to a file."""
        try:
            # Check if we have data to export
            if self.ui.reportsTable.rowCount() == 0:
                QMessageBox.warning(self, "Export Report", "No data to export")
                return
                
            # Get file name from save dialog
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Export Report",
                "",
                "CSV Files (*.csv)"  # Removed Excel option for now
            )
            
            if not file_name:
                return
                
            # Ensure file has .csv extension
            if not file_name.endswith('.csv'):
                file_name += '.csv'
                
            # Get report data from table
            data = []
            headers = [
                self.ui.reportsTable.horizontalHeaderItem(col).text() 
                for col in range(self.ui.reportsTable.columnCount())
            ]
                      
            for row in range(self.ui.reportsTable.rowCount()):
                record = {}
                for col in range(self.ui.reportsTable.columnCount()):
                    key = headers[col]
                    value = self.ui.reportsTable.item(row, col).text()
                    # Convert back to numbers if possible
                    try:
                        if '.' in value:
                            value = float(value.replace('$', '').replace(',', ''))
                        elif value.isdigit():
                            value = int(value)
                    except:
                        pass
                    record[key] = value
                data.append(record)
                
            if Report.export_to_csv(data, file_name):
                QMessageBox.information(self, "Success", f"Report exported to {file_name}")
            else:
                QMessageBox.warning(self, "Error", "Failed to export report")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export report: {str(e)}")

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
                db = database.get_connection()
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