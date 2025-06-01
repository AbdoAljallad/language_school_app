"""
Base Dashboard View
-----------------
Base class for all dashboard views.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal

from app.models.user_model import User


class BaseDashboardView(QMainWindow):
    """
    Base class for all dashboard views.
    """
    
    # Signal emitted when the user logs out
    logout = pyqtSignal()
    
    def __init__(self, user):
        """
        Initialize the base dashboard view.
        
        Args:
            user (User): The authenticated user.
        """
        super().__init__()
        
        # Store the user
        self.user = user
        
        # Set up common UI elements
        self._setup_common_ui()
    
    def _setup_common_ui(self):
        """
        Set up common UI elements for all dashboards.
        This method should be overridden by subclasses.
        """
        pass
    
    def handle_logout(self):
        """
        Handle the logout action.
        """
        # Confirm logout
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Emit the logout signal
            self.logout.emit()
            
            # Close the dashboard
            self.close()
    
    def closeEvent(self, event):
        """
        Handle the window close event.
        
        Args:
            event (QCloseEvent): The close event.
        """
        # Don't emit the logout signal here as it causes issues with window navigation
        # Users should explicitly use the logout button to log out
        
        # Accept the event
        event.accept()