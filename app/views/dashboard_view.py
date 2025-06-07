"""
Base Dashboard View
-----------------
This module contains the BaseDashboardView class, which serves as a base class for all dashboard views
in the Language School Management System.
"""

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal


class BaseDashboardView(QMainWindow):
    """
    Base dashboard view class.
    
    This class serves as a base class for all dashboard views (admin, teacher, student).
    It provides common functionality such as logout handling.
    """
    
    # Signal emitted when the user logs out
    logout = pyqtSignal()
    
    def __init__(self, user, parent=None):
        """
        Initialize the base dashboard view.
        
        Args:
            user (User): The authenticated user
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.user = user
        
    def setup_ui(self):
        """
        Set up the UI for the dashboard.
        
        This method should be overridden by subclasses to set up their specific UI.
        """
        pass
        
    def handle_logout(self):
        """
        Handle the logout action.
        
        This method is called when the user clicks the logout button or selects the logout action.
        It confirms the logout action and emits the logout signal.
        """
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.close()
            # Emit logout signal that MainWindow will handle
            self.logout.emit()
            
    def closeEvent(self, event):
        """
        Handle the close event.
        
        This method is called when the user closes the window. It emits the logout signal.
        
        Args:
            event (QCloseEvent): The close event
        """
        self.logout.emit()
        event.accept()