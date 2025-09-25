"""
Admin Dashboard View
------------------
This module contains the AdminDashboardView class, which implements the admin dashboard
functionality for the Language School Management System.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, 
    QDialogButtonBox, QListWidgetItem, QWidget, QFileDialog, QTimeEdit
)
from PyQt5.QtCore import Qt, pyqtSlot, QDate, pyqtSignal, QTimer, QTime
from datetime import datetime
import datetime

from app.ui.generated.admin_dashboard_ui import Ui_AdminDashboard
from app.views.base_dashboard_view import BaseDashboardView
from app.models.user_model import User
from app.models.course_model import Course
from app.models.schedule_model import Schedule
from app.models.report_model import Report  # Add this import
from app.utils import database
from app.utils.crypto import hash_password  # Will use plaintext instead of hashing
from app.ui.common.messaging import attach_messaging



# Attempt to import real report generators; provide safe fallbacks if module is missing
try:
    from app.utils.report_generator import (
        generate_user_activity_report,
        generate_course_enrollment_report,
        generate_payment_summary_report,
    )
except Exception:
    # Fallback minimal implementations (write CSV) so IDE/linter/runtimes don't fail.
    def _write_csv(path, rows):
        import csv, os
        p = path
        if p.endswith(".xlsx"):
            p = p[:-5] + ".csv"
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        if not rows:
            with open(p, "w", newline="", encoding="utf-8") as f:
                f.write("no_data\n")
            return
        # rows expected as list of dicts
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if isinstance(rows, list) and isinstance(rows[0], dict):
                headers = list(rows[0].keys())
                writer.writerow(headers)
                for r in rows:
                    writer.writerow([r.get(h, "") for h in headers])
            else:
                # generic fallback
                for r in rows:
                    writer.writerow([str(r)])

    def generate_user_activity_report(path, data):
        _write_csv(path, data)

    def generate_course_enrollment_report(path, data):
        _write_csv(path, data)

    def generate_payment_summary_report(path, data):
        _write_csv(path, data)


class AdminDashboardView(BaseDashboardView):
    """
    Admin dashboard view class.
    """
    
    # Add profile_updated signal
    profile_updated = pyqtSignal()
    # Add explicit logout signal (MainWindow expects `logout`)
    logout = pyqtSignal()
    # keep legacy name as alias
    logout_requested = logout

    def __init__(self, user, parent=None):
        """Initialize the admin dashboard view."""
        super().__init__(user, parent)
        self.ui = Ui_AdminDashboard()
        self.ui.setupUi(self)

        # Ensure UI elements exist
        self._setup_missing_ui_elements()
        
        # Connect signals
        self._connect_signals()
        
        # Load initial data
        self.refresh_data()

    def _setup_missing_ui_elements(self):
        """Ensure all required UI elements exist"""
        # Use QLabel/ QPushButton imported at module top (avoid QtWidgets.* which isn't imported)
        if not hasattr(self.ui, 'welcomeLabel'):
            try:
                self.ui.welcomeLabel = QLabel(self)
                if hasattr(self.ui, 'headerLayout'):
                    self.ui.headerLayout.insertWidget(0, self.ui.welcomeLabel)
            except Exception:
                pass
            
        if not hasattr(self.ui, 'logoutButton'):
            try:
                self.ui.logoutButton = QPushButton("Logout", self)
                if hasattr(self.ui, 'headerLayout'):
                    self.ui.headerLayout.addWidget(self.ui.logoutButton)
            except Exception:
                pass
            
        if not hasattr(self.ui, 'profileButton'):
            try:
                self.ui.profileButton = QPushButton("Profile", self)
                if hasattr(self.ui, 'headerLayout'):
                    idx = max(0, self.ui.headerLayout.count()-1)
                    self.ui.headerLayout.insertWidget(idx, self.ui.profileButton)
            except Exception:
                pass

        # Set welcome message defensively
        try:
            first = getattr(self.user, "first_name", "") or ""
            last = getattr(self.user, "last_name", "") or ""
            name = f"{first} {last}".strip() or getattr(self.user, "username", "Admin")
            self.ui.welcomeLabel.setText(f"Welcome, {name}")
        except Exception:
            pass

    def _connect_signals(self):
        """Connect all signals to slots (ensure every clickable widget is connected)."""
        # Main header buttons
        try:
            self.ui.logoutButton.clicked.connect(self.handle_logout)
        except Exception:
            pass
        try:
            self.ui.profileButton.clicked.connect(self.open_profile_dialog)
        except Exception:
            pass

        # Menu actions
        try:
            self.ui.actionRefresh.triggered.connect(self.refresh_data)
        except Exception:
            pass
        try:
            self.ui.actionExit.triggered.connect(self.close)
        except Exception:
            pass

        # Users toolbar
        try:
            self.ui.userSearchInput.textChanged.connect(self.filter_users)
        except Exception:
            pass
        try:
            self.ui.userTypeFilter.currentIndexChanged.connect(self.filter_users)
        except Exception:
            pass
        try:
            self.ui.addUserButton.clicked.connect(self.on_add_user_clicked)
        except Exception:
            pass

        # Courses toolbar
        try:
            self.ui.courseSearchInput.textChanged.connect(self.filter_courses)
        except Exception:
            pass
        try:
            self.ui.languageFilter.currentIndexChanged.connect(self.filter_courses)
        except Exception:
            pass
        try:
            self.ui.levelFilter.currentIndexChanged.connect(self.filter_courses)
        except Exception:
            pass
        try:
            self.ui.addCourseButton.clicked.connect(self.on_add_course_clicked)
        except Exception:
            pass

        # Schedules toolbar
        try:
            self.ui.courseFilter.currentIndexChanged.connect(self.filter_schedules)
        except Exception:
            pass
        try:
            self.ui.dayFilter.currentIndexChanged.connect(self.filter_schedules)
        except Exception:
            pass
        try:
            self.ui.addScheduleButton.clicked.connect(self.on_add_schedule_clicked)
        except Exception:
            pass

        # Payments toolbar
        try:
            # search / status filter
            self.ui.paymentSearchInput.textChanged.connect(self.filter_payments)
        except Exception:
            pass
        try:
            self.ui.paymentStatusFilter.currentIndexChanged.connect(self.filter_payments)
        except Exception:
            pass
        try:
            self.ui.addPaymentButton.clicked.connect(self.on_add_payment_clicked)
        except Exception:
            pass

        # Reports
        try:
            self.ui.generateReportButton.clicked.connect(self.on_generate_report_clicked)
        except Exception:
            pass
        try:
            self.ui.exportReportButton.clicked.connect(self.on_export_report_clicked)
        except Exception:
            pass

        # Messaging: attach_messaging expects names chatsList/newChatButton; create aliases if UI uses different names
        try:
            # alias conversationsList -> chatsList for attach_messaging compatibility
            if hasattr(self.ui, "conversationsList") and not hasattr(self.ui, "chatsList"):
                self.ui.chatsList = self.ui.conversationsList
            # alias newConversationButton -> newChatButton
            if hasattr(self.ui, "newConversationButton") and not hasattr(self.ui, "newChatButton"):
                self.ui.newChatButton = self.ui.newConversationButton
            # if sendMessageButton/messageInput/messagesList exist, attach messaging
            if all(hasattr(self.ui, name) for name in ("chatsList", "messagesList", "messageInput", "sendMessageButton", "newChatButton")):
                try:
                    # provide a small getter for current user id to messaging helpers
                    attach_messaging(self.ui, lambda: getattr(self.user, "user_id", getattr(self.user, "id", None)))
                    # if UI exposes helper methods from attach_messaging, keep track
                    # optionally set current user for messaging
                    try:
                        if getattr(self, "user", None):
                            self.ui.set_current_user(getattr(self.user, "user_id", getattr(self.user, "id", None)))
                    except Exception:
                        pass
                except Exception:
                    pass
        except Exception:
            pass

        # Generic defensive connections (if widgets exist but were missed)
        try:
            # fallback connect for any button named refreshButton/exportButton etc.
            if hasattr(self.ui, "refreshButton"):
                self.ui.refreshButton.clicked.connect(self.refresh_data)
        except Exception:
            pass

    # Placeholder slots for buttons (minimal, delegate to real methods when available)
    def on_add_user_clicked(self):
        """Placeholder slot for Add User button."""
        print("Add User clicked")
        try:
            self.add_user()
        except Exception:
            pass

    def on_add_course_clicked(self):
        """Placeholder slot for Add Course button."""
        print("Add Course clicked")
        try:
            self.add_course()
        except Exception:
            pass

    def on_add_schedule_clicked(self):
        """Placeholder slot for Add Schedule button."""
        print("Add Schedule clicked")
        try:
            self.add_schedule()
        except Exception:
            pass

    def on_add_payment_clicked(self):
        """Placeholder slot for Add Payment button."""
        print("Add Payment clicked")
        try:
            self.add_payment()
        except Exception:
            pass

    def on_generate_report_clicked(self):
        """Placeholder slot for Generate Report button."""
        print("Generate Report clicked")
        try:
            self.generate_report()
        except Exception:
            pass

    def on_export_report_clicked(self):
        """Placeholder slot for Export Report button."""
        print("Export Report clicked")
        try:
            self.export_report()
        except Exception:
            pass

    def refresh_data(self):
        """Refresh all data in the dashboard."""
        self.load_users()
        self.load_courses()
        self.load_schedules()
        self.load_payments()
        # load messaging data
        try:
            self.load_conversations()
        except Exception:
            pass
        
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

        users = database.execute_query(query, params, fetch=True) or []  # normalize None -> []

        # Clear and populate table
        self.ui.usersTable.setRowCount(0)
        
        search_text = (self.ui.userSearchInput.text() or "").lower()
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
            query += ", ".join(set_clauses) + " WHERE id = %s"
            params.append(user_id)

            # Execute the update
            database.execute_query(query, params, commit=True)
            
            # Refresh users table
            self.load_users()
            
            # Show success message
            self.ui.statusbar.showMessage(f"User {user_id} updated successfully.")
            
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
            self, "Confirm Deletion",
            f"Are you sure you want to delete the user '{user['username']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete user - this will also delete related records due to foreign key constraints
            query = "DELETE FROM users WHERE id = %s"
            params = (user_id,)
            database.execute_query(query, params, commit=True)
            
            # Refresh users table
            self.load_users()
            
            # Show success message
            self.ui.statusbar.showMessage(f"User '{user['username']}' deleted successfully.")
            
    def load_courses(self):
        """Load courses into the courses table."""
        # Clear the table
        self.ui.coursesTable.setRowCount(0)
        
        # Get search text and filters
        search_text = (self.ui.courseSearchInput.text() or "").lower()
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
            
        courses = database.execute_query(query, params, fetch=True) or []  # normalize None -> []
        
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
        teachers = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
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
        teachers = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
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
            
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete the course '{course['name']}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete course - this will also delete related records due to foreign key constraints
            query = "DELETE FROM courses WHERE id = %s"
            params = (course_id,)
            database.execute_query(query, params, commit=True)
            
            # Refresh courses table
            self.load_courses()
            
            # Show success message
            self.ui.statusbar.showMessage(f"Course '{course['name']}' deleted successfully.")
            
    def load_schedules(self):
        """Load schedules into the schedules table."""
        # Clear the table
        try:
            self.ui.schedulesTable.setRowCount(0)
        except Exception:
            pass
        
        # Get selected course (defensive)
        try:
            course_id = self.ui.courseFilter.currentData()
        except Exception:
            course_id = None
        
        # Use columns that exist in DB: day_of_week and room
        query = """
            SELECT s.id,
                   s.day_of_week AS date,
                   s.start_time,
                   s.end_time,
                   s.room AS location,
                   '' AS notes,
                   c.name AS course_name,
                   u.first_name,
                   u.last_name
            FROM schedules s
            JOIN courses c ON s.course_id = c.id
            LEFT JOIN users u ON c.teacher_id = u.id
        """
        params = ()
        if course_id and course_id != -1:
            query += " WHERE s.course_id = %s"
            params = (course_id,)
        
        try:
            schedules = database.execute_query(query, params, fetch=True) or []
        except Exception:
            schedules = []
        
        # Populate the table safely
        row = 0
        for schedule in schedules:
            try:
                self.ui.schedulesTable.insertRow(row)
                # schedule['date'] is now day_of_week string (e.g. 'Monday')
                sid = schedule.get('id') if isinstance(schedule, dict) else schedule[0]
                day = schedule.get('date') if isinstance(schedule, dict) else schedule[1]
                start_val = schedule.get('start_time') if isinstance(schedule, dict) else schedule[2]
                end_val = schedule.get('end_time') if isinstance(schedule, dict) else schedule[3]
                location = schedule.get('location') if isinstance(schedule, dict) else schedule[4]
                notes = schedule.get('notes') if isinstance(schedule, dict) else schedule[5]
                course_name = schedule.get('course_name') if isinstance(schedule, dict) else schedule[6]
                first = schedule.get('first_name') if isinstance(schedule, dict) else schedule[7]
                last = schedule.get('last_name') if isinstance(schedule, dict) else (schedule[8] if len(schedule) > 8 else "")

                # Format start/end safely
                try:
                    start_str = start_val.strftime("%H:%M") if hasattr(start_val, "strftime") else str(start_val or "")
                except Exception:
                    start_str = str(start_val or "")
                try:
                    end_str = end_val.strftime("%H:%M") if hasattr(end_val, "strftime") else str(end_val or "")
                except Exception:
                    end_str = str(end_val or "")

                self.ui.schedulesTable.setItem(row, 0, QTableWidgetItem(str(sid)))
                # display day_of_week in "Date" column (keeps UI unchanged)
                self.ui.schedulesTable.setItem(row, 1, QTableWidgetItem(str(day or "")))
                self.ui.schedulesTable.setItem(row, 2, QTableWidgetItem(start_str))
                self.ui.schedulesTable.setItem(row, 3, QTableWidgetItem(end_str))
                self.ui.schedulesTable.setItem(row, 4, QTableWidgetItem(str(location or "")))
                self.ui.schedulesTable.setItem(row, 5, QTableWidgetItem(str(notes or "")))
                self.ui.schedulesTable.setItem(row, 6, QTableWidgetItem(str(course_name or "")))
                self.ui.schedulesTable.setItem(row, 7, QTableWidgetItem(f"{first or ''} {last or ''}".strip()))
                
                # Actions
                edit_button = QPushButton("Edit")
                edit_button.setProperty("schedule_id", sid)
                edit_button.clicked.connect(lambda checked, sid=sid: self.edit_schedule(sid))
                delete_button = QPushButton("Delete")
                delete_button.setProperty("schedule_id", sid)
                delete_button.clicked.connect(lambda checked, sid=sid: self.delete_schedule(sid))
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.addWidget(edit_button)
                actions_layout.addWidget(delete_button)
                actions_layout.setContentsMargins(0,0,0,0)
                try:
                    self.ui.schedulesTable.setCellWidget(row, 8 if self.ui.schedulesTable.columnCount() <= 8 else self.ui.schedulesTable.columnCount()-1, actions_widget)
                except Exception:
                    # best-effort
                    try:
                        self.ui.schedulesTable.setCellWidget(row, 7, actions_widget)
                    except Exception:
                        pass

                row += 1
            except Exception:
                continue

        try:
            self.ui.schedulesTable.resizeColumnsToContents()
        except Exception:
            pass

    def add_schedule(self):
        """Open dialog to add a new schedule."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Schedule")
        dialog.setMinimumWidth(500)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Day (choose weekday instead of specific date)
        day_layout = QHBoxLayout()
        day_label = QLabel("Day:")
        day_combo = QComboBox()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            day_combo.addItem(d, d)
        day_layout.addWidget(day_label)
        day_layout.addWidget(day_combo)
        form_layout.addLayout(day_layout)
        
        # Start time
        start_time_layout = QHBoxLayout()
        start_time_label = QLabel("Start Time:")
        start_time_input = QTimeEdit()
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(start_time_input)
        form_layout.addLayout(start_time_layout)
        
        # End time
        end_time_layout = QHBoxLayout()
        end_time_label = QLabel("End Time:")
        end_time_input = QTimeEdit()
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addWidget(end_time_input)
        form_layout.addLayout(end_time_layout)
        
        # Location
        location_layout = QHBoxLayout()
        location_label = QLabel("Room:")
        location_input = QLineEdit()
        location_layout.addWidget(location_label)
        location_layout.addWidget(location_input)
        form_layout.addLayout(location_layout)
        
        # Notes
        notes_layout = QVBoxLayout()
        notes_label = QLabel("Notes:")
        notes_input = QLineEdit()
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(notes_input)
        form_layout.addLayout(notes_layout)
        
        # Course
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_combo = QComboBox()
        
        # Get courses
        query = """
            SELECT id, name
            FROM courses
            WHERE active = 1
            ORDER BY name
        """
        courses = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
        for course in courses:
            course_combo.addItem(course['name'], course['id'])
            
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_combo)
        form_layout.addLayout(course_layout)
        
        # Teacher (optional, for admin)
        if self.user.user_type == 'admin':
            teacher_layout = QHBoxLayout()
            teacher_label = QLabel("Teacher:")
            teacher_combo = QComboBox()
            
            # Get active teachers
            query = """
                SELECT id, first_name, last_name
                FROM users
                WHERE user_type = 'teacher' AND active = 1
                ORDER BY last_name, first_name
            """
            teachers = database.execute_query(query, fetch=True) or []  # normalize None -> []
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
            day_of_week = day_combo.currentText()
            start_time = start_time_input.time().toString("HH:mm")
            end_time = end_time_input.time().toString("HH:mm")
            room = location_input.text().strip()  # UI had "location" -> use as room
            course_id = course_combo.currentData()
            # Validate minimal fields
            if not day_of_week or not start_time or not end_time or not room:
                QMessageBox.warning(self, "Validation Error", "Day, start time, end time, and room are required.")
                return

            # Insert using correct columns (course_id, day_of_week, start_time, end_time, room)
            query = """
                INSERT INTO schedules (course_id, day_of_week, start_time, end_time, room)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (course_id, day_of_week, start_time, end_time, room)
            database.execute_query(query, params, commit=True)
            self.load_schedules()
            self.ui.statusbar.showMessage("Schedule added successfully.")

    def edit_schedule(self, schedule_id):
        """Open dialog to edit a schedule."""
        # Get schedule data using schema columns
        query = """
            SELECT s.day_of_week AS date, s.start_time, s.end_time, s.room AS location, s.course_id, s.id
            FROM schedules s
            WHERE s.id = %s
        """
        result = database.execute_query(query, (schedule_id,), fetch=True) or []
        schedule = result[0] if result and len(result) > 0 else None
        
        if not schedule:
            QMessageBox.warning(self, "Error", "Schedule not found.")
            return

        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Schedule")
        dialog.setMinimumWidth(500)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Day (choose weekday instead of specific date)
        day_layout = QHBoxLayout()
        day_label = QLabel("Day:")
        day_combo = QComboBox()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            day_combo.addItem(d, d)
        # Set current day if available
        try:
            current_day = schedule.get('date') or ""
            idx = day_combo.findText(current_day)
            if idx >= 0:
                day_combo.setCurrentIndex(idx)
        except Exception:
            pass
        day_layout.addWidget(day_label)
        day_layout.addWidget(day_combo)
        form_layout.addLayout(day_layout)
        
        # Start time
        start_time_layout = QHBoxLayout()
        start_time_label = QLabel("Start Time:")
        start_time_input = QTimeEdit()
        try:
            start_time_input.setTime(QTime.fromString(schedule['start_time'], "HH:mm"))
        except Exception:
            pass
        start_time_layout.addWidget(start_time_label)
        start_time_layout.addWidget(start_time_input)
        form_layout.addLayout(start_time_layout)
        
        # End time
        end_time_layout = QHBoxLayout()
        end_time_label = QLabel("End Time:")
        end_time_input = QTimeEdit()
        try:
            end_time_input.setTime(QTime.fromString(schedule['end_time'], "HH:mm"))
        except Exception:
            pass
        end_time_layout.addWidget(end_time_label)
        end_time_layout.addWidget(end_time_input)
        form_layout.addLayout(end_time_layout)
        
        # Location
        location_layout = QHBoxLayout()
        location_label = QLabel("Location:")
        location_input = QLineEdit()
        location_input.setText(schedule.get('location') or "")
        location_layout.addWidget(location_label)
        location_layout.addWidget(location_input)
        form_layout.addLayout(location_layout)
        
        # Notes
        notes_layout = QVBoxLayout()
        notes_label = QLabel("Notes:")
        notes_input = QLineEdit()
        notes_input.setText(schedule.get('notes') or "")
        notes_layout.addWidget(notes_label)
        notes_layout.addWidget(notes_input)
        form_layout.addLayout(notes_layout)
        
        # Course
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_combo = QComboBox()
        
        # Get courses
        query = """
            SELECT id, name
            FROM courses
            WHERE active = 1
            ORDER BY name
        """
        courses = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
        for course in courses:
            course_combo.addItem(course['name'], course['id'])
            
        # Set current course
        try:
            idx = course_combo.findData(schedule['course_id'])
            if idx >= 0:
                course_combo.setCurrentIndex(idx)
        except Exception:
            pass
        
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_combo)
        form_layout.addLayout(course_layout)
        
        # Teacher (optional, for admin)
        if self.user.user_type == 'admin':
            teacher_layout = QHBoxLayout()
            teacher_label = QLabel("Teacher:")
            teacher_combo = QComboBox()
            
            # Get active teachers
            query = """
                SELECT id, first_name, last_name
                FROM users
                WHERE user_type = 'teacher' AND active = 1
                ORDER BY last_name, first_name
            """
            teachers = database.execute_query(query, fetch=True) or []  # normalize None -> []
            
            for teacher in teachers:
                teacher_combo.addItem(f"{teacher['first_name']} {teacher['last_name']}", teacher['id'])
                
            # Set current teacher (if applicable)
            try:
                tval = schedule.get('teacher_id')
                idx = teacher_combo.findData(tval)
                if idx >= 0:
                    teacher_combo.setCurrentIndex(idx)
            except Exception:
                pass
            
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
        active_combo.setCurrentIndex(0 if schedule.get('active') else 1)
        
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
            day_of_week = day_combo.currentText()
            start_time = start_time_input.time().toString("HH:mm")
            end_time = end_time_input.time().toString("HH:mm")
            room = location_input.text().strip()
            course_id = course_combo.currentData()

            if not day_of_week or not start_time or not end_time or not room:
                QMessageBox.warning(self, "Validation Error", "Day, start time, end time, and room are required.")
                return

            query = """
                UPDATE schedules
                SET day_of_week = %s, start_time = %s, end_time = %s, room = %s, course_id = %s
                WHERE id = %s
            """
            params = (day_of_week, start_time, end_time, room, course_id, schedule_id)
            database.execute_query(query, params, commit=True)
            self.load_schedules()
            self.ui.statusbar.showMessage("Schedule updated successfully.")
    
    def delete_schedule(self, schedule_id):
        """Delete a schedule."""
        # Get schedule data (day_of_week column aliased to 'date', room aliased to 'location')
        query = "SELECT id, day_of_week AS date, start_time, end_time, room AS location FROM schedules WHERE id = %s"
        params = (schedule_id,)
        result = database.execute_query(query, params, fetch=True)
        schedule = result[0] if result and len(result) > 0 else None
        
        if not schedule:
            QMessageBox.warning(self, "Error", "Schedule not found.")
            return
            
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete the schedule for {schedule['date']} {schedule['start_time']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Delete schedule
            query = "DELETE FROM schedules WHERE id = %s"
            params = (schedule_id,)
            database.execute_query(query, params, commit=True)
            
            # Refresh schedules table
            self.load_schedules()
            
            # Show success message
            self.ui.statusbar.showMessage("Schedule deleted successfully.")
            
    def load_payments(self):
        """Load payments into the payments table."""
        # Clear the table
        try:
            self.ui.paymentsTable.setRowCount(0)
        except Exception:
            pass

        query = """
            SELECT p.id, p.amount, p.payment_date AS date, p.status, u.first_name, u.last_name, c.name as course_name
            FROM payments p
            JOIN users u ON p.student_id = u.id
            JOIN courses c ON p.course_id = c.id
        """
        try:
            payments = database.execute_query(query, (), fetch=True) or []
        except Exception:
            payments = []

        row = 0
        for payment in payments:
            try:
                self.ui.paymentsTable.insertRow(row)
                # date may be datetime.date - format safely
                date_val = payment.get('date') if isinstance(payment, dict) else (payment[2] if len(payment) > 2 else None)
                try:
                    date_str = date_val.strftime("%Y-%m-%d") if hasattr(date_val, "strftime") else str(date_val or "")
                except Exception:
                    date_str = str(date_val or "")

                self.ui.paymentsTable.setItem(row, 0, QTableWidgetItem(str(payment['id'])))
                self.ui.paymentsTable.setItem(row, 1, QTableWidgetItem(f"${payment['amount']:.2f}"))
                self.ui.paymentsTable.setItem(row, 2, QTableWidgetItem(date_str))
                self.ui.paymentsTable.setItem(row, 3, QTableWidgetItem(payment['status']))
                self.ui.paymentsTable.setItem(row, 4, QTableWidgetItem(f"{payment['first_name']} {payment['last_name']}"))
                self.ui.paymentsTable.setItem(row, 5, QTableWidgetItem(payment['course_name']))

                edit_button = QPushButton("Edit")
                edit_button.setProperty("payment_id", payment['id'])
                edit_button.clicked.connect(lambda checked, pid=payment['id']: self.edit_payment(pid))
                delete_button = QPushButton("Delete")
                delete_button.setProperty("payment_id", payment['id'])
                delete_button.clicked.connect(lambda checked, pid=payment['id']: self.delete_payment(pid))
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.addWidget(edit_button)
                actions_layout.addWidget(delete_button)
                actions_layout.setContentsMargins(0,0,0,0)
                try:
                    self.ui.paymentsTable.setCellWidget(row, 6, actions_widget)
                except Exception:
                    pass

                row += 1
            except Exception:
                continue

        try:
            self.ui.paymentsTable.resizeColumnsToContents()
        except Exception:
            pass

    def add_payment(self):
        """Open dialog to add a new payment."""
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Payment")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Amount
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Amount:")
        amount_input = QLineEdit()
        amount_input.setPlaceholderText("0.00")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(amount_input)
        form_layout.addLayout(amount_layout)
        
        # Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_layout.addWidget(date_label)
        date_layout.addWidget(date_input)
        form_layout.addLayout(date_layout)
        
        # Status
        status_layout = QHBoxLayout()
        status_label = QLabel("Status:")
        status_combo = QComboBox()
        status_combo.addItem("Pending", "pending")
        status_combo.addItem("Completed", "completed")
        status_combo.addItem("Failed", "failed")
        status_layout.addWidget(status_label)
        status_layout.addWidget(status_combo)
        form_layout.addLayout(status_layout)
        
        # Student
        student_layout = QHBoxLayout()
        student_label = QLabel("Student:")
        student_combo = QComboBox()
        
        # Get students
        query = """
            SELECT id, first_name, last_name
            FROM users
            WHERE user_type = 'student' AND active = 1
            ORDER BY last_name, first_name
        """
        students = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
        for student in students:
            student_combo.addItem(f"{student['first_name']} {student['last_name']}", student['id'])
            
        student_layout.addWidget(student_label)
        student_layout.addWidget(student_combo)
        form_layout.addLayout(student_layout)
        
        # Course
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_combo = QComboBox()
        
        # Get courses
        query = """
            SELECT id, name
            FROM courses
            WHERE active = 1
            ORDER BY name
        """
        courses = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
        for course in courses:
            course_combo.addItem(course['name'], course['id'])
            
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_combo)
        form_layout.addLayout(course_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            amount = amount_input.text().strip()
            date_py = date_input.date().toPyDate()
            payment_date = date_py  # column is payment_date in DB
            status = status_combo.currentData()
            student_id = student_combo.currentData()
            course_id = course_combo.currentData()

            if not amount or not payment_date or not status or not student_id or not course_id:
                QMessageBox.warning(self, "Validation Error", "All fields are required.")
                return

            query = """
                INSERT INTO payments (amount, payment_date, status, student_id, course_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (amount, payment_date, status, student_id, course_id)
            database.execute_query(query, params, commit=True)
            self.load_payments()
            self.ui.statusbar.showMessage("Payment added successfully.")

    def edit_payment(self, payment_id):
        """Open dialog to edit a payment."""
        # Get payment data
        query = """
            SELECT amount, date, status, student_id, course_id
            FROM payments
            WHERE id = %s
        """
        result = database.execute_query(query, (payment_id,), fetch=True)
        payment = result[0] if result and len(result) > 0 else None
        
        if not payment:
            QMessageBox.warning(self, "Error", "Payment not found.")
            return
            
        # Create a dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Payment")
        dialog.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(dialog)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # Amount
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Amount:")
        amount_input = QLineEdit()
        amount_input.setText(str(payment['amount']))
        amount_input.setPlaceholderText("0.00")
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(amount_input)
        form_layout.addLayout(amount_layout)
        
        # Date
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        # Safely convert payment['date'] to QDate
        try:
            pd = payment.get('date')
            qd = self._str_to_qdate(pd)
            date_input.setDate(qd)
        except Exception:
            date_input.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(date_input)
        form_layout.addLayout(date_layout)
        
        # Status
        status_layout = QHBoxLayout()
        status_label = QLabel("Status:")
        status_combo = QComboBox()
        status_combo.addItem("Pending", "pending")
        status_combo.addItem("Completed", "completed")
        status_combo.addItem("Failed", "failed")
        status_combo.setCurrentText(payment['status'])
        status_layout.addWidget(status_label)
        status_layout.addWidget(status_combo)
        form_layout.addLayout(status_layout)
        
        # Student
        student_layout = QHBoxLayout()
        student_label = QLabel("Student:")
        student_combo = QComboBox()
        
        # Get students
        query = """
            SELECT id, first_name, last_name
            FROM users
            WHERE user_type = 'student' AND active = 1
            ORDER BY last_name, first_name
        """
        students = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
        for student in students:
            student_combo.addItem(f"{student['first_name']} {student['last_name']}", student['id'])
            
        # Set current student
        try:
            idx = student_combo.findData(payment['student_id'])
            if idx >= 0:
                student_combo.setCurrentIndex(idx)
        except Exception:
            pass
        
        student_layout.addWidget(student_label)
        student_layout.addWidget(student_combo)
        form_layout.addLayout(student_layout)
        
        # Course
        course_layout = QHBoxLayout()
        course_label = QLabel("Course:")
        course_combo = QComboBox()
        
        # Get courses
        query = """
            SELECT id, name
            FROM courses
            WHERE active = 1
            ORDER BY name
        """
        courses = database.execute_query(query, fetch=True) or []  # normalize None -> []
        
        for course in courses:
            course_combo.addItem(course['name'], course['id'])
            
        # Set current course
        try:
            idx = course_combo.findData(payment['course_id'])
            if idx >= 0:
                course_combo.setCurrentIndex(idx)
        except Exception:
            pass
        
        course_layout.addWidget(course_label)
        course_layout.addWidget(course_combo)
        form_layout.addLayout(course_layout)
        
        layout.addLayout(form_layout)
        
        # Add buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            amount = amount_input.text().strip()
            date_py = date_input.date().toPyDate()
            payment_date = date_py
            status = status_combo.currentData()
            student_id = student_combo.currentData()
            course_id = course_combo.currentData()

            if not amount or not payment_date or not status or not student_id or not course_id:
                QMessageBox.warning(self, "Validation Error", "All fields are required.")
                return

            query = """
                UPDATE payments
                SET amount = %s, payment_date = %s, status = %s, student_id = %s, course_id = %s
                WHERE id = %s
            """
            params = (amount, payment_date, status, student_id, course_id, payment_id)
            database.execute_query(query, params, commit=True)
            self.load_payments()
            self.ui.statusbar.showMessage("Payment updated successfully.")

    def generate_report(self):
        """Generate a report based on the selected criteria."""
        # Get selected criteria
        start_date = self.ui.startDateEdit.date().toPyDate()
        end_date = self.ui.endDateEdit.date().toPyDate()
        report_type = self.ui.reportTypeCombo.currentData()
        
        # Validate dates
        if not start_date or not end_date:
            QMessageBox.warning(self, "Validation Error", "Start date and end date are required.")
            return
            
        if start_date > end_date:
            QMessageBox.warning(self, "Validation Error", "Start date must be before end date.")
            return
            
        # Generate report
        try:
            if report_type == "user_activity":
                self.generate_user_activity_report(start_date, end_date)
            elif report_type == "course_enrollment":
                self.generate_course_enrollment_report(start_date, end_date)
            elif report_type == "payment_summary":
                self.generate_payment_summary_report(start_date, end_date)
            else:
                QMessageBox.warning(self, "Validation Error", "Invalid report type.")
                return
                
            QMessageBox.information(self, "Success", "Report generated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")
            
    def generate_user_activity_report(self, start_date, end_date):
        """Generate user activity report."""
        query = """
            SELECT u.id, u.username, u.first_name, u.last_name, u.email, 
                   COUNT(DISTINCT c.id) as courses_enrolled, 
                   COUNT(DISTINCT s.id) as schedules_created,
                   COUNT(DISTINCT p.id) as payments_made
            FROM users u
            LEFT JOIN courses c ON u.id = c.teacher_id
            LEFT JOIN schedules s ON u.id = s.course_id
            LEFT JOIN payments p ON u.id = p.student_id
            WHERE u.active = 1 AND u.user_type = 'student'
              AND p.payment_date BETWEEN %s AND %s
            GROUP BY u.id
            ORDER BY u.last_name, u.first_name
        """
        params = (start_date, end_date)
        report_data = database.execute_query(query, params, fetch=True) or []
        # ...existing code to generate report...
        report_file = f"user_activity_report_{start_date}_to_{end_date}.xlsx"
        from app.utils.report_generator import generate_user_activity_report
        generate_user_activity_report(report_file, report_data)

    def generate_course_enrollment_report(self, start_date, end_date):
        """Generate course enrollment report."""
        # Removed schedule date filtering because schedules store day_of_week; keep aggregated data
        query = """
            SELECT c.id, c.name, c.language, c.level, c.price, 
                   COUNT(s.id) as schedules_count, 
                   COUNT(DISTINCT sc.student_id) as students_enrolled
            FROM courses c
            LEFT JOIN schedules s ON c.id = s.course_id
            LEFT JOIN student_courses sc ON c.id = sc.course_id
            WHERE c.active = 1
            GROUP BY c.id
            ORDER BY c.name
        """
        report_data = database.execute_query(query, fetch=True) or []
        report_file = f"course_enrollment_report_{start_date}_to_{end_date}.xlsx"
        from app.utils.report_generator import generate_course_enrollment_report
        generate_course_enrollment_report(report_file, report_data)

    def generate_payment_summary_report(self, start_date, end_date):
        """Generate payment summary report."""
        query = """
            SELECT u.id, u.username, u.first_name, u.last_name, 
                   SUM(p.amount) as total_paid, 
                   COUNT(p.id) as payments_count
            FROM users u
            JOIN payments p ON u.id = p.student_id
            WHERE u.active = 1 AND p.payment_date BETWEEN %s AND %s
            GROUP BY u.id
            ORDER BY u.last_name, u.first_name
        """
        params = (start_date, end_date)
        report_data = database.execute_query(query, params, fetch=True) or []
        report_file = f"payment_summary_report_{start_date}_to_{end_date}.xlsx"
        from app.utils.report_generator import generate_payment_summary_report
        generate_payment_summary_report(report_file, report_data)

    def export_report(self):
        """Export the generated report to a file."""
        # TODO: Implement report export functionality
        QMessageBox.information(self, "Info", "Report export functionality is not yet implemented.")
    
    def handle_logout(self):
        """Handle logout button click."""
        try:
            if hasattr(self, '_messages_timer') and self._messages_timer.isActive():
                self._messages_timer.stop()
        except Exception:
            pass

        # Emit standardized logout signal
        try:
            self.logout.emit()
        except Exception:
            try:
                self.logout_requested.emit()
            except Exception:
                pass

        try:
            self.close()
        except Exception:
            pass

    def _poll_messages_and_conversations(self):
        """Poll for new messages and update conversations."""
        try:
            if hasattr(self.ui, 'populate_messages') and self._last_loaded_chat_id:
                self.ui.populate_messages(self._last_loaded_chat_id)
            if hasattr(self.ui, 'populate_chats'):
                self.ui.populate_chats()
        except Exception:
            pass  # Silent fail on polling errors

    # Add helper to convert various date representations to QDate
    def _str_to_qdate(self, date_val):
        """Convert str / datetime.date / datetime.datetime / QDate -> QDate (robust)."""
        # already a QDate
        if isinstance(date_val, QDate):
            return date_val
        # datetime.date or datetime.datetime
        try:
            import datetime as _dt_mod
            if isinstance(date_val, (_dt_mod.date, _dt_mod.datetime)):
                d = date_val if isinstance(date_val, _dt_mod.date) else date_val.date()
                return QDate(d.year, d.month, d.day)
        except Exception:
            pass
        # string parsing (try common ISO 'YYYY-MM-DD' or fromisoformat)
        if isinstance(date_val, str):
            s = date_val.strip()
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                try:
                    import datetime as _dt_mod
                    dt = _dt_mod.datetime.strptime(s, fmt).date()
                    return QDate(dt.year, dt.month, dt.day)
                except Exception:
                    continue
            # try fromisoformat on date
            try:
                import datetime as _dt_mod
                dt = _dt_mod.date.fromisoformat(s)
                return QDate(dt.year, dt.month, dt.day)
            except Exception:
                pass
        # fallback to today
        return QDate.currentDate()