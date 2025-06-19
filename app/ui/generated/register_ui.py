"""
Generated Python code for registration UI
--------------------------------------
This file contains the Python code generated from register.ui file.
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(450, 650)  # Slightly larger window
        RegisterWindow.setMinimumSize(QtCore.QSize(450, 650))
        RegisterWindow.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel#titleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLabel#subtitleLabel {
                font-size: 16px;
                color: #7f8c8d;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                padding: 5px 0;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                min-height: 25px;
                font-size: 14px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QPushButton#registerButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                min-height: 45px;
            }
            QPushButton#registerButton:hover {
                background-color: #27ae60;
            }
            QPushButton#loginButton {
                background-color: transparent;
                color: #3498db;
                text-decoration: underline;
                border: none;
                font-size: 14px;
            }
            QPushButton#loginButton:hover {
                color: #2980b9;
            }
            QLabel#errorLabel {
                color: #e74c3c;
                font-weight: bold;
                padding: 5px;
            }
        """)
        self.centralwidget = QtWidgets.QWidget(RegisterWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        self.subtitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.subtitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitleLabel.setObjectName("subtitleLabel")
        self.verticalLayout.addWidget(self.subtitleLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.fullNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.fullNameLabel.setObjectName("fullNameLabel")
        self.verticalLayout.addWidget(self.fullNameLabel)
        self.fullNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.fullNameInput.setObjectName("fullNameInput")
        self.verticalLayout.addWidget(self.fullNameInput)
        self.usernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.usernameLabel.setObjectName("usernameLabel")
        self.verticalLayout.addWidget(self.usernameLabel)
        self.usernameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameInput.setObjectName("usernameInput")
        self.verticalLayout.addWidget(self.usernameInput)
        self.emailLabel = QtWidgets.QLabel(self.centralwidget)
        self.emailLabel.setObjectName("emailLabel")
        self.verticalLayout.addWidget(self.emailLabel)
        self.emailInput = QtWidgets.QLineEdit(self.centralwidget)
        self.emailInput.setObjectName("emailInput")
        self.verticalLayout.addWidget(self.emailInput)
        self.passwordLabel = QtWidgets.QLabel(self.centralwidget)
        self.passwordLabel.setObjectName("passwordLabel")
        self.verticalLayout.addWidget(self.passwordLabel)
        self.passwordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordInput.setObjectName("passwordInput")
        self.verticalLayout.addWidget(self.passwordInput)
        self.confirmPasswordLabel = QtWidgets.QLabel(self.centralwidget)
        self.confirmPasswordLabel.setObjectName("confirmPasswordLabel")
        self.verticalLayout.addWidget(self.confirmPasswordLabel)
        self.confirmPasswordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.confirmPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPasswordInput.setObjectName("confirmPasswordInput")
        self.verticalLayout.addWidget(self.confirmPasswordInput)
        self.userTypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.userTypeLabel.setObjectName("userTypeLabel")
        self.verticalLayout.addWidget(self.userTypeLabel)
        self.userTypeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.userTypeComboBox.setObjectName("userTypeComboBox")
        self.userTypeComboBox.addItem("")
        self.userTypeComboBox.addItem("")
        self.verticalLayout.addWidget(self.userTypeComboBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.errorLabel = QtWidgets.QLabel(self.centralwidget)
        self.errorLabel.setText("")
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorLabel.setObjectName("errorLabel")
        self.verticalLayout.addWidget(self.errorLabel)
        self.registerButton = QtWidgets.QPushButton(self.centralwidget)
        self.registerButton.setObjectName("registerButton")
        self.verticalLayout.addWidget(self.registerButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loginPromptLabel = QtWidgets.QLabel(self.centralwidget)
        self.loginPromptLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.loginPromptLabel.setObjectName("loginPromptLabel")
        self.horizontalLayout.addWidget(self.loginPromptLabel)
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setObjectName("loginButton")
        self.horizontalLayout.addWidget(self.loginButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.versionLabel = QtWidgets.QLabel(self.centralwidget)
        self.versionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.verticalLayout.addWidget(self.versionLabel)
        RegisterWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegisterWindow)
        QtCore.QMetaObject.connectSlotsByName(RegisterWindow)

    def retranslateUi(self, RegisterWindow):
        _translate = QtCore.QCoreApplication.translate
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", "Language School - Create Account"))
        self.titleLabel.setText(_translate("RegisterWindow", "Language School"))
        self.subtitleLabel.setText(_translate("RegisterWindow", "Join our learning community"))
        self.fullNameLabel.setText(_translate("RegisterWindow", "Full Name:"))
        self.fullNameInput.setPlaceholderText(_translate("RegisterWindow", "Enter your full name"))
        self.usernameLabel.setText(_translate("RegisterWindow", "Username:"))
        self.usernameInput.setPlaceholderText(_translate("RegisterWindow", "Choose a username (min. 3 characters)"))
        self.emailLabel.setText(_translate("RegisterWindow", "Email:"))
        self.emailInput.setPlaceholderText(_translate("RegisterWindow", "Enter your email address"))
        self.passwordLabel.setText(_translate("RegisterWindow", "Password:"))
        self.passwordInput.setPlaceholderText(_translate("RegisterWindow", "Choose a password (min. 6 characters)"))
        self.confirmPasswordLabel.setText(_translate("RegisterWindow", "Confirm Password:"))
        self.confirmPasswordInput.setPlaceholderText(_translate("RegisterWindow", "Confirm your password"))
        self.userTypeLabel.setText(_translate("RegisterWindow", "I want to:"))
        self.userTypeComboBox.setItemText(0, _translate("RegisterWindow", "Learn a language (Student)"))
        self.userTypeComboBox.setItemText(1, _translate("RegisterWindow", "Teach a language (Teacher)"))
        self.registerButton.setText(_translate("RegisterWindow", "Create Account"))
        self.loginPromptLabel.setText(_translate("RegisterWindow", "Already have an account?"))
        self.loginButton.setText(_translate("RegisterWindow", "Sign In"))
        self.versionLabel.setText(_translate("RegisterWindow", "Version 1.0.0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegisterWindow = QtWidgets.QMainWindow()
    ui = Ui_RegisterWindow()
    ui.setupUi(RegisterWindow)
    RegisterWindow.show()
    sys.exit(app.exec_())