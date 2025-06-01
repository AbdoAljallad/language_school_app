"""
Login View
---------
Handles the login screen and authentication logic.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

from app.ui.generated.login_ui import Ui_LoginWindow
from app.models.user_model import User
from app.views.admin_dashboard_view import AdminDashboardView
from app.views.teacher_dashboard_view import TeacherDashboardView
from app.views.student_dashboard_view import StudentDashboardView
from app.views.register_view import RegisterView
from app.utils.database import initialize_database


class LoginView(QMainWindow):
    """
    Login view that handles user authentication.
    """
    
    # Signal emitted when a user successfully logs in
    login_successful = pyqtSignal(User)
    
    def __init__(self):
        """
        Initialize the login view.
        """
        super().__init__()
        
        # Set up the UI
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        
        # Connect signals and slots
        self.ui.loginButton.clicked.connect(self.handle_login)
        self.ui.passwordInput.returnPressed.connect(self.handle_login)
        
        # Add register link
        self._add_register_link()
        
        # Initialize the database
        self._initialize_database()
        
        # Create register view (but don't show it yet)
        self.register_view = None
    def _add_register_link(self):
        """
        Add a link to the registration page.
        """
        # Create horizontal layout below the login button
        register_layout = QHBoxLayout()
        
        # Create a label
        register_prompt = QLabel("Don't have an account?")
        register_layout.addWidget(register_prompt)
        
        # Create a button styled as a link
        register_button = QPushButton("Register")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3498db;
                text-decoration: underline;
                border: none;
                padding: 0;
            }
            QPushButton:hover {
                color: #2980b9;
            }
        """)
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.clicked.connect(self.handle_register)
        register_layout.addWidget(register_button)
        
        # Add the layout to the main layout
        self.ui.verticalLayout.addLayout(register_layout)
    
    def handle_register(self):
        """
        Show the registration form.
        """
        # Create the registration view if it doesn't exist
        if not self.register_view:
            self.register_view = RegisterView()
            # Connect signals
            self.register_view.show_login.connect(self.show)
            self.register_view.registration_successful.connect(self.on_registration_successful)
        
        # Hide the login window and show the registration window
        self.hide()
        self.register_view.show()
    
    def on_registration_successful(self):
        """
        Handle successful registration.
        """
        # Show a success message when returning to login
        self.ui.errorLabel.setStyleSheet("color: green;")
        self.ui.errorLabel.setText("Registration successful! You can now log in.")
    def _initialize_database(self):
        """
        Initialize the database if it doesn't exist.
        """
        success = initialize_database()
        if not success:
            QMessageBox.critical(
                self,
                "Database Error",
                "Failed to initialize the database. The application may not function correctly."
            )
    
    def handle_login(self):
        """
        Handle the login button click or Enter key press.
        """
        # Clear any previous error message
        self.ui.errorLabel.setText("")
        
        # Get the username and password
        username = self.ui.usernameInput.text().strip()
        password = self.ui.passwordInput.text()
        
        # Validate input
        if not username:
            self.ui.errorLabel.setText("Please enter a username")
            self.ui.usernameInput.setFocus()
            return
        
        if not password:
            self.ui.errorLabel.setText("Please enter a password")
            self.ui.passwordInput.setFocus()
            return
        
        # Authenticate the user
        user = User.authenticate(username, password)
        
        if user:
            # Emit the login_successful signal
            self.login_successful.emit(user)
            
            # Open the appropriate dashboard based on user type
            self._open_dashboard(user)
        else:
            # Show error message
            self.ui.errorLabel.setText("Invalid username or password")
            self.ui.passwordInput.clear()
            self.ui.passwordInput.setFocus()
    
    def _open_dashboard(self, user):
        """
        Open the appropriate dashboard based on user type.
        
        Args:
            user (User): The authenticated user.
        """
        # Hide the login window
        self.hide()
        
        # Create and show the appropriate dashboard
        if user.user_type == 'admin':
            dashboard = AdminDashboardView(user)
        elif user.user_type == 'teacher':
            dashboard = TeacherDashboardView(user)
        elif user.user_type == 'student':
            dashboard = StudentDashboardView(user)
        else:
            # This should never happen, but just in case
            QMessageBox.critical(
                self,
                "Error",
                f"Unknown user type: {user.user_type}"
            )
            self.show()
            return
        
        # Connect the logout signal to show the login window again
        dashboard.logout.connect(self.show)
        
        # Show the dashboard
        dashboard.show()