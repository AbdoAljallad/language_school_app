"""
Register View
------------
Handles the registration screen and user creation logic.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
import re

from app.ui.register_ui import RegisterUI
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
        self.ui = RegisterUI()
        self.setCentralWidget(self.ui)
        
        # Window settings
        self.setWindowTitle("Language School - Register")
        self.setMinimumSize(400, 600)
        
        # Connect signals
        self.ui.register_btn.clicked.connect(self.handle_register)
        self.ui.login_btn.clicked.connect(self.show_login.emit)

    def handle_register(self):
        """
        Handle the register button click or Enter key press.
        """
        # Clear any previous error message
        self.ui.error_label.clear()
        
        # Get the form data
        username = self.ui.username_input.text().strip()
        email = self.ui.email_input.text().strip()
        full_name = self.ui.full_name_input.text().strip()
        password = self.ui.password_input.text()
        confirm_password = self.ui.confirm_password_input.text()
        user_type = self.ui.user_type.currentText().lower()

        # Validate input
        if not self._validate_input(username, email, full_name, password, confirm_password):
            return

        # Create the user with combined full name
        user = User.create(
            username=username,
            password=password,
            email=email,  
            full_name=full_name,
            user_type=user_type
        )

        if user:
            QMessageBox.information(
                self,
                "Success",
                "Account created successfully! You can now log in."
            )
            # Emit signal to show login view
            self.registration_successful.emit()
            self.show_login.emit()
        else:
            # Show error message
            self.ui.error_label.setText("Failed to create account. Username may be taken.")

    def _validate_input(self, username, email, full_name, password, confirm_password):
        """Validate all input fields."""
        if not username or len(username) < 3:
            self.ui.error_label.setText("Username must be at least 3 characters")
            return False

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.ui.error_label.setText("Please enter a valid email address")
            return False

        if not full_name or len(full_name.split()) < 2:
            self.ui.error_label.setText("Please enter your full name (first and last name)")
            return False

        if len(password) < 6:
            self.ui.error_label.setText("Password must be at least 6 characters")
            return False

        if password != confirm_password:
            self.ui.error_label.setText("Passwords do not match")
            return False

        return True