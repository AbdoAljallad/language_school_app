"""
Register View
------------
Handles the registration screen and user creation logic.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
import re

from app.ui.generated.register_ui import Ui_RegisterWindow
from app.models.user_model import User


class RegisterView(QMainWindow):
    """
    Register view that handles user registration.
    """
    
    # Signal emitted when a user successfully registers
    registration_successful = pyqtSignal()
    # Signal emitted when user wants to go back to login
    show_login = pyqtSignal()
    
    def __init__(self):
        """
        Initialize the register view.
        """
        super().__init__()
        
        # Set up the UI
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)
        
        # Connect signals and slots
        self.ui.registerButton.clicked.connect(self.handle_register)
        self.ui.loginButton.clicked.connect(self.handle_login_click)
        self.ui.confirmPasswordInput.returnPressed.connect(self.handle_register)
    
    def handle_register(self):
        """
        Handle the register button click or Enter key press.
        """
        # Clear any previous error message
        self.ui.errorLabel.setText("")
        
        # Get the form data
        full_name = self.ui.fullNameInput.text().strip()
        username = self.ui.usernameInput.text().strip()
        email = self.ui.emailInput.text().strip()
        password = self.ui.passwordInput.text()
        confirm_password = self.ui.confirmPasswordInput.text()
        user_type = "student" if self.ui.userTypeComboBox.currentIndex() == 0 else "teacher"
        
        # Validate input
        if not full_name:
            self.ui.errorLabel.setText("Please enter your full name")
            self.ui.fullNameInput.setFocus()
            return
        
        if not username:
            self.ui.errorLabel.setText("Please enter a username")
            self.ui.usernameInput.setFocus()
            return
        
        if not email:
            self.ui.errorLabel.setText("Please enter your email address")
            self.ui.emailInput.setFocus()
            return
        
        # Validate email format
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            self.ui.errorLabel.setText("Please enter a valid email address")
            self.ui.emailInput.setFocus()
            return
        
        if not password:
            self.ui.errorLabel.setText("Please enter a password")
            self.ui.passwordInput.setFocus()
            return
        
        if password != confirm_password:
            self.ui.errorLabel.setText("Passwords do not match")
            self.ui.confirmPasswordInput.setFocus()
            return
        
        # Check if username or email already exists
        if User.get_by_username(username):
            self.ui.errorLabel.setText("Username already exists")
            self.ui.usernameInput.setFocus()
            return
        
        if User.get_by_email(email):
            self.ui.errorLabel.setText("Email already exists")
            self.ui.emailInput.setFocus()
            return
        
        # Create the user
        user = User.create(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            user_type=user_type
        )
        
        if user:
            # Show success message
            QMessageBox.information(
                self,
                "Registration Successful",
                "Your account has been created successfully. You can now log in."
            )
            
            # Emit signal to show login view
            self.registration_successful.emit()
            self.show_login.emit()
            
            # Hide this window
            self.hide()
        else:
            # Show error message
            self.ui.errorLabel.setText("Failed to create account. Please try again.")
    
    def handle_login_click(self):
        """
        Handle the login button click.
        """
        # Emit signal to show login view
        self.show_login.emit()
        
        # Hide this window
        self.hide()