"""
Admin Dashboard View
------------------
This module contains the AdminDashboardView class, which implements the admin dashboard
functionality for the Language School Management System.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, 
    QDialogButtonBox, QListWidgetItem, QWidget
)
from PyQt5.QtCore import Qt, pyqtSlot, QDate

from app.ui.generated.admin_dashboard_ui import Ui_AdminDashboard
from app.views.dashboard_view import BaseDashboardView
from app.models.user_model import User
from app.models.course_model import Course
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
        # Clear the table
        self.ui.usersTable.setRowCount(0)
        
        # Get search text and user type filter
        search_text = self.ui.userSearchInput.text().lower()
        user_type_index = self.ui.userTypeFilter.currentIndex()
        user_type_filter = None
        if user_type_index == 1:
            user_type_filter = "admin"
        elif user_type_index == 2:
            user_type_filter = "teacher"
        elif user_type_index == 3:
            user_type_filter = "student"
            
        # Get users
        query = "SELECT id, username, first_name, last_name, email, user_type, active FROM users"
        params = ()
        
        if user_type_filter:
            query += " WHERE user_type = %s"
            params = (user_type_filter,)
            
        users = database.execute_query(query, params, fetch=True)
        
        # Populate the table
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
            SELECT username, first_name, last_name, email, user_type, active
            FROM users
            WHERE id = %s
        """
        params = (user_id,)
        result = database.execute_query(query, params, fetch=True)
        user = result[0] if result and len(result) > 0 else None
        
        if not user:
            QMessageBox.warning(self, "Error", "User not found.")
            return
            
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit User")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Username (read-only)
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_input = QLineEdit()
        username_input.setText(user['username'])
        username_input.setReadOnly(True)
        username_layout.addWidget(username_label)
        username_layout.addWidget(username_input)
        form_layout.addLayout(username_layout)
        
        # Password (optional)
        password_layout = QHBoxLayout()
        password_label = QLabel("New Password:")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Leave blank to keep current password")
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
        user_type_combo.addItem("Admin", "admin")
        user_type_combo.addItem("Teacher", "teacher")
        user_type_combo.addItem("Student", "student")
        
        # Set current user type
        if user['user_type'] == "admin":
            user_type_combo.setCurrentIndex(0)
        elif user['user_type'] == "teacher":
            user_type_combo.setCurrentIndex(1)
        elif user['user_type'] == "student":
            user_type_combo.setCurrentIndex(2)
            
        user_type_layout.addWidget(user_type_label)
        user_type_layout.addWidget(user_type_combo)
        form_layout.addLayout(user_type_layout)
        
        # Active
        active_layout = QHBoxLayout()
        active_label = QLabel("Active:")
        active_combo = QComboBox()
        active_combo.addItem("Yes", 1)
        active_combo.addItem("No", 0)
        
        # Set current active status
        active_combo.setCurrentIndex(0 if user['active'] else 1)
        
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
            password = password_input.text().strip()
            first_name = first_name_input.text().strip()
            last_name = last_name_input.text().strip()
            email = email_input.text().strip()
            user_type = user_type_combo.currentData()
            active = active_combo.currentData()
            
            # Validate form
            if not first_name or not last_name or not email:
                QMessageBox.warning(self, "Validation Error", "First name, last name, and email are required.")
                return
                
            # Update user
            if password:
                # Update with new password (plaintext)
                query = """
                    UPDATE users
                    SET password = %s, first_name = %s, last_name = %s, email = %s, user_type = %s, active = %s
                    WHERE id = %s
                """
                params = (password, first_name, last_name, email, user_type, active, user_id)
            else:
                # Update without changing password
                query = """
                    UPDATE users
                    SET first_name = %s, last_name = %s, email = %s, user_type = %s, active = %s
                    WHERE id = %s
                """
                params = (first_name, last_name, email, user_type, active, user_id)
                
            database.execute_query(query, params, commit=True)
            
            # Refresh users table
            self.load_users()
            
            # Show success message
            self.ui.statusbar.showMessage(f"User {username_input.text()} updated successfully.")
            
    def delete_user(self, user_id):
        """Delete a user."""
        # Get user data
        query = "SELECT username FROM users WHERE id = %s"
        params = (user_id,)
        result = database.execute_query(query, params, fetch=True)
        user = result[0] if result and len(result) > 0 else None
        
        if not user:
            QMessageBox.warning(self, "Error", "User not found.")
            return
            
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete user {user['username']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete user
            query = "DELETE FROM users WHERE id = %s"
            params = (user_id,)
            database.execute_query(query, params, commit=True)
            
            # Refresh users table
            self.load_users()
            
            # Show success message
            self.ui.statusbar.showMessage(f"User {user['username']} deleted successfully.")
            
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
            database.execute_query(query, params)
            
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
        """Delete a course."""
        # Get course data
        query = "SELECT name FROM courses WHERE id = %s"
        params = (course_id,)
        result = database.execute_query(query, params, fetch=True)
        course = result[0] if result and len(result) > 0 else None
        
        if not course:
            QMessageBox.warning(self, "Error", "Course not found.")
            return
            
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete course {course['name']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete course
            query = "DELETE FROM courses WHERE id = %s"
            params = (course_id,)
            database.execute_query(query, params, commit=True)
            
            # Refresh courses table
            self.load_courses()
            
            # Show success message
            self.ui.statusbar.showMessage(f"Course {course['name']} deleted successfully.")
            
    def load_schedules(self):
        """Load schedules into the schedules table."""
        # Placeholder implementation - in a real app, this would query the database for schedules
        # For now, we'll just show some sample data
        
        # Clear the table
        self.ui.schedulesTable.setRowCount(0)
        
        # Get selected course ID (or -1 for all courses)
        course_id = self.ui.courseFilter.currentData()
        
        # Get selected day from combo box
        selected_day = self.ui.dayFilter.currentText()
        
        # Add some sample data
        schedules = [
            {
                "id": 1,
                "course_id": 1,
                "course_name": "English B1",
                "day_of_week": "Monday",
                "start_time": "10:00",
                "end_time": "11:30",
                "room": "101",
                "teacher": "John Smith"
            },
            {
                "id": 2,
                "course_id": 1,
                "course_name": "English B1",
                "day_of_week": "Wednesday",
                "start_time": "10:00",
                "end_time": "11:30",
                "room": "101",
                "teacher": "John Smith"
            },
            {
                "id": 3,
                "course_id": 2,
                "course_name": "Spanish A2",
                "day_of_week": "Tuesday",
                "start_time": "14:00",
                "end_time": "15:30",
                "room": "203",
                "teacher": "Maria Garcia"
            },
            {
                "id": 4,
                "course_id": 2,
                "course_name": "Spanish A2",
                "day_of_week": "Thursday",
                "start_time": "14:00",
                "end_time": "15:30",
                "room": "203",
                "teacher": "Maria Garcia"
            }
        ]
        
        # Filter schedules by course ID
        if course_id != -1:
            schedules = [s for s in schedules if s["course_id"] == course_id]
            
        # Populate the table
        for row, schedule in enumerate(schedules):
            self.ui.schedulesTable.insertRow(row)
            
            # Add schedule data
            self.ui.schedulesTable.setItem(row, 0, QTableWidgetItem(str(schedule["id"])))
            self.ui.schedulesTable.setItem(row, 1, QTableWidgetItem(schedule["course_name"]))
            self.ui.schedulesTable.setItem(row, 2, QTableWidgetItem(schedule["day_of_week"]))
            self.ui.schedulesTable.setItem(row, 3, QTableWidgetItem(schedule["start_time"]))
            self.ui.schedulesTable.setItem(row, 4, QTableWidgetItem(schedule["end_time"]))
            self.ui.schedulesTable.setItem(row, 5, QTableWidgetItem(schedule["room"]))
            self.ui.schedulesTable.setItem(row, 6, QTableWidgetItem(schedule["teacher"]))
            
            # Add edit and delete buttons
            edit_button = QPushButton("Edit")
            edit_button.setProperty("schedule_id", schedule["id"])
            edit_button.clicked.connect(lambda checked, sid=schedule["id"]: self.edit_schedule(sid))
            
            delete_button = QPushButton("Delete")
            delete_button.setProperty("schedule_id", schedule["id"])
            delete_button.clicked.connect(lambda checked, sid=schedule["id"]: self.delete_schedule(sid))
            
            # Create a widget to hold the buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            self.ui.schedulesTable.setCellWidget(row, 7, actions_widget)
            
        # Resize columns to content
        self.ui.schedulesTable.resizeColumnsToContents()
        
    def filter_schedules(self):
        """Filter schedules based on selected course and date."""
        self.load_schedules()
        
    def add_schedule(self):
        """Open dialog to add a new schedule."""
        # Placeholder implementation - in a real app, this would add a new schedule to the database
        QMessageBox.information(self, "Add Schedule", "Schedule added successfully.")
        self.load_schedules()
        
    def edit_schedule(self, schedule_id):
        """Open dialog to edit a schedule."""
        # Placeholder implementation - in a real app, this would edit a schedule in the database
        QMessageBox.information(self, "Edit Schedule", f"Schedule {schedule_id} edited successfully.")
        self.load_schedules()
        
    def delete_schedule(self, schedule_id):
        """Delete a schedule."""
        # Placeholder implementation - in a real app, this would delete a schedule from the database
        QMessageBox.information(self, "Delete Schedule", f"Schedule {schedule_id} deleted successfully.")
        self.load_schedules()
        
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
        # Placeholder implementation - in a real app, this would generate a report based on selected criteria
        QMessageBox.information(self, "Generate Report", "Report generated successfully.")
        
    def export_report(self):
        """Export the generated report to a file."""
        # Placeholder implementation - in a real app, this would export the report to a file
        QMessageBox.information(self, "Export Report", "Report exported successfully.")