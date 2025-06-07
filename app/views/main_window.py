"""
Main Window
----------
This module contains the MainWindow class, which serves as the main window for the
Language School Management System application.
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from app.views.login_view import LoginView
from app.views.admin_dashboard_view import AdminDashboardView
from app.views.teacher_dashboard_view import TeacherDashboardView
from app.views.student_dashboard_view import StudentDashboardView


class MainWindow(QMainWindow):
    """
    Main window class.
    
    This class serves as the main window for the application. It manages the stacked widget
    that contains the login view and dashboard views, and handles switching between views
    based on user authentication and logout events.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the main window.
        
        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        # Set window properties
        self.setWindowTitle("Language School Management System")
        self.setMinimumSize(1024, 768)
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create login view
        self.login_view = LoginView()
        self.stacked_widget.addWidget(self.login_view)
        
        # Connect login view signals
        self.login_view.login_successful.connect(self.handle_login)
        
        # Initialize dashboard views to None
        self.admin_dashboard = None
        self.teacher_dashboard = None
        self.student_dashboard = None
        
        # Show login view
        self.stacked_widget.setCurrentWidget(self.login_view)
        
    def handle_login(self, user):
        """
        Handle successful login.
        
        This method is called when a user successfully logs in. It creates the appropriate
        dashboard view based on the user type and shows it.
        
        Args:
            user (User): The authenticated user
        """
        # Create dashboard view based on user type
        if user.user_type == "admin":
            if not self.admin_dashboard:
                self.admin_dashboard = AdminDashboardView(user)
                self.admin_dashboard.logout.connect(self.handle_logout)
                self.stacked_widget.addWidget(self.admin_dashboard)
            else:
                # Update user in existing dashboard
                self.admin_dashboard.user = user
                # Refresh dashboard data
                self.admin_dashboard.refresh_data()
                
            # Show admin dashboard
            self.stacked_widget.setCurrentWidget(self.admin_dashboard)
            
        elif user.user_type == "teacher":
            if not self.teacher_dashboard:
                self.teacher_dashboard = TeacherDashboardView(user)
                self.teacher_dashboard.logout.connect(self.handle_logout)
                self.stacked_widget.addWidget(self.teacher_dashboard)
            else:
                # Update user in existing dashboard
                self.teacher_dashboard.user = user
                # Refresh dashboard data
                self.teacher_dashboard.refresh_data()
                
            # Show teacher dashboard
            self.stacked_widget.setCurrentWidget(self.teacher_dashboard)
            
        elif user.user_type == "student":
            if not self.student_dashboard:
                self.student_dashboard = StudentDashboardView(user)
                self.student_dashboard.logout_requested.connect(self.handle_logout)  # Fixed signal name
                self.stacked_widget.addWidget(self.student_dashboard)
            else:
                # Update user in existing dashboard
                self.student_dashboard.user = user
                # Refresh dashboard data
                self.student_dashboard.refresh_data()
                
            # Show student dashboard
            self.stacked_widget.setCurrentWidget(self.student_dashboard)
            
    def handle_logout(self):
        """
        Handle logout.
        
        This method is called when a user logs out. It shows the login view.
        """
        # Show login view
        self.stacked_widget.setCurrentWidget(self.login_view)
        
        # Clear login form
        self.login_view.ui.usernameInput.clear()
        self.login_view.ui.passwordInput.clear()
        self.login_view.ui.errorLabel.clear()
        
        # Set focus to username input
        self.login_view.ui.usernameInput.setFocus()