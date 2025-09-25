"""
Base Dashboard View
-----------------
Base class for all dashboard views.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal

from app.models.user_model import User
from app.utils.database import execute_query, get_connection


class BaseDashboardView(QMainWindow):
    """Base class for all dashboard views."""
    
    # Add profile update signal
    profile_updated = pyqtSignal()
    
    def __init__(self, user, parent=None):
        """Initialize the base dashboard view."""
        super().__init__(parent)
        self.user = user

    def open_profile_dialog(self):
        """Open dialog to edit user profile."""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Edit Profile")
            dialog.setMinimumWidth(400)
            
            layout = QVBoxLayout(dialog)
            
            # Add personal info fields
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
            
            # Password change section
            password_group = QGroupBox("Change Password")
            password_layout = QVBoxLayout()
            
            current_pw_layout = QHBoxLayout()
            current_pw_label = QLabel("Current Password:")
            current_pw_input = QLineEdit()
            current_pw_input.setEchoMode(QLineEdit.Password)
            current_pw_layout.addWidget(current_pw_label)
            current_pw_layout.addWidget(current_pw_input)
            password_layout.addLayout(current_pw_layout)
            
            new_pw_layout = QHBoxLayout()
            new_pw_label = QLabel("New Password:")
            new_pw_input = QLineEdit()
            new_pw_input.setEchoMode(QLineEdit.Password)
            new_pw_layout.addWidget(new_pw_label)
            new_pw_layout.addWidget(new_pw_input)
            password_layout.addLayout(new_pw_layout)
            
            confirm_pw_layout = QHBoxLayout()
            confirm_pw_label = QLabel("Confirm Password:")
            confirm_pw_input = QLineEdit()
            confirm_pw_input.setEchoMode(QLineEdit.Password)
            confirm_pw_layout.addWidget(confirm_pw_label)
            confirm_pw_layout.addWidget(confirm_pw_input)
            password_layout.addLayout(confirm_pw_layout)
            
            password_group.setLayout(password_layout)
            
            layout.addLayout(form_layout)
            layout.addWidget(password_group)
            
            # Add buttons
            button_box = QDialogButtonBox(
                QDialogButtonBox.Save | QDialogButtonBox.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
            
            if dialog.exec_() == QDialog.Accepted:
                # Validate and save changes
                if self.save_profile_changes(
                    first_name=first_name_input.text().strip(),
                    last_name=last_name_input.text().strip(),
                    email=email_input.text().strip(),
                    current_password=current_pw_input.text(),
                    new_password=new_pw_input.text(),
                    confirm_password=confirm_pw_input.text()
                ):
                    self.profile_updated.emit()
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open profile dialog: {str(e)}")

    def save_profile_changes(self, **kwargs):
        """Save profile changes with validation and error handling."""
        try:
            if not kwargs.get('email') or '@' not in kwargs['email']:
                QMessageBox.warning(self, "Validation Error", "Please enter a valid email address.")
                return False
                
            # Check password change if attempted
            if kwargs.get('new_password'):
                if not kwargs.get('current_password'):
                    QMessageBox.warning(self, "Validation Error", "Please enter your current password.")
                    return False
                    
                if kwargs['new_password'] != kwargs.get('confirm_password'):
                    QMessageBox.warning(self, "Validation Error", "New passwords do not match.")
                    return False
                    
                # Verify current password
                query = "SELECT password FROM users WHERE id = %s"
                result = execute_query(query, (self.user.user_id,), fetch=True)
                if not result or result[0]['password'] != kwargs['current_password']:
                    QMessageBox.warning(self, "Validation Error", "Current password is incorrect.")
                    return False
                    
            # Build update query
            updates = []
            params = []
            
            for field in ['first_name', 'last_name', 'email']:
                if kwargs.get(field):
                    updates.append(f"{field} = %s")
                    params.append(kwargs[field])
                    
            if kwargs.get('new_password'):
                updates.append("password = %s")
                params.append(kwargs['new_password'])
                
            if not updates:
                return True
                
            # Add user_id to params
            params.append(self.user.user_id)
            
            # Update database
            query = f"""
                UPDATE users 
                SET {', '.join(updates)},
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            
            execute_query(query, params, commit=True)
            
            # Update local user object
            self.user.first_name = kwargs.get('first_name', self.user.first_name)
            self.user.last_name = kwargs.get('last_name', self.user.last_name)
            self.user.email = kwargs.get('email', self.user.email)
            
            QMessageBox.information(self, "Success", "Profile updated successfully")
            return True
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update profile: {str(e)}")
            return False

    def on_profile_updated(self):
        """Handle profile update events."""
        # Reload user data
        self.user = User.get_by_id(self.user.user_id)
        # Update UI elements
        if hasattr(self, 'ui') and hasattr(self.ui, 'welcomeLabel'):
            self.ui.welcomeLabel.setText(f"Welcome, {self.user.first_name} {self.user.last_name}")