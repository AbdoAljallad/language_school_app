from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class RegisterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel("Create Account")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Form fields
        self.username_input = self._create_input("Username", "Choose a username")
        self.email_input = self._create_input("Email", "Enter your email")
        self.full_name_input = self._create_input("Full Name", "Enter your full name")
        self.password_input = self._create_input("Password", "Choose a password", True)
        self.confirm_password_input = self._create_input("Confirm Password", "Confirm your password", True)

        # User type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("I am a:")
        self.user_type = QComboBox()
        self.user_type.addItems(["Student", "Teacher"])
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.user_type)
        layout.addLayout(type_layout)

        # Error label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label)

        # Register button
        self.register_btn = QPushButton("Register")
        self.register_btn.setMinimumHeight(40)
        layout.addWidget(self.register_btn)

        # Login link
        login_layout = QHBoxLayout()
        login_layout.addStretch()
        login_layout.addWidget(QLabel("Already have an account?"))
        self.login_btn = QPushButton("Login")
        self.login_btn.setFlat(True)
        login_layout.addWidget(self.login_btn)
        login_layout.addStretch()
        layout.addLayout(login_layout)

        self._apply_styles()

    def _create_input(self, label_text, placeholder, is_password=False):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(label)
        layout.addWidget(input_field)
        self.layout().addLayout(layout)
        return input_field

    def _apply_styles(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton[flat="true"] {
                background: transparent;
                color: #007bff;
            }
            QPushButton[flat="true"]:hover {
                color: #0056b3;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
