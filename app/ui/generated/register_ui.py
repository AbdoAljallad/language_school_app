"""
Generated Python code for registration UI
--------------------------------------
This file contains the Python code generated from register.ui file.
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        RegisterWindow.setObjectName("RegisterWindow")
        RegisterWindow.resize(400, 600)
        RegisterWindow.setMinimumSize(QtCore.QSize(400, 600))
        RegisterWindow.setStyleSheet("QMainWindow {\n"
"    background-color: #f5f5f5;\n"
"}\n"
"QLabel#titleLabel {\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"}\n"
"QLabel#subtitleLabel {\n"
"    font-size: 16px;\n"
"    color: #7f8c8d;\n"
"}\n"
"QLabel {\n"
"    font-size: 14px;\n"
"    color: #2c3e50;\n"
"}\n"
"QLineEdit, QComboBox {\n"
"    padding: 8px;\n"
"    border: 1px solid #bdc3c7;\n"
"    border-radius: 4px;\n"
"    background-color: white;\n"
"    min-height: 20px;\n"
"}\n"
"QLineEdit:focus, QComboBox:focus {\n"
"    border: 1px solid #3498db;\n"
"}\n"
"QPushButton {\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 10px 20px;\n"
"    font-size: 14px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #1f6aa5;\n"
"}\n"
"QPushButton#loginButton {\n"
"    background-color: transparent;\n"
"    color: #3498db;\n"
"    text-decoration: underline;\n"
"    padding: 0;\n"
"}\n"
"QPushButton#loginButton:hover {\n"
"    color: #2980b9;\n"
"}\n"
"QLabel#errorLabel {\n"
"    color: #e74c3c;\n"
"    font-weight: bold;\n"
"}\n"
"QLabel#versionLabel {\n"
"    color: #7f8c8d;\n"
"    font-size: 12px;\n"
"}")
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
        RegisterWindow.setWindowTitle(_translate("RegisterWindow", "Language School - Register"))
        self.titleLabel.setText(_translate("RegisterWindow", "Language School"))
        self.subtitleLabel.setText(_translate("RegisterWindow", "Create a new account"))
        self.fullNameLabel.setText(_translate("RegisterWindow", "Full Name:"))
        self.fullNameInput.setPlaceholderText(_translate("RegisterWindow", "Enter your full name"))
        self.usernameLabel.setText(_translate("RegisterWindow", "Username:"))
        self.usernameInput.setPlaceholderText(_translate("RegisterWindow", "Choose a username"))
        self.emailLabel.setText(_translate("RegisterWindow", "Email:"))
        self.emailInput.setPlaceholderText(_translate("RegisterWindow", "Enter your email address"))
        self.passwordLabel.setText(_translate("RegisterWindow", "Password:"))
        self.passwordInput.setPlaceholderText(_translate("RegisterWindow", "Choose a password"))
        self.confirmPasswordLabel.setText(_translate("RegisterWindow", "Confirm Password:"))
        self.confirmPasswordInput.setPlaceholderText(_translate("RegisterWindow", "Confirm your password"))
        self.userTypeLabel.setText(_translate("RegisterWindow", "I am a:"))
        self.userTypeComboBox.setItemText(0, _translate("RegisterWindow", "Student"))
        self.userTypeComboBox.setItemText(1, _translate("RegisterWindow", "Teacher"))
        self.registerButton.setText(_translate("RegisterWindow", "Register"))
        self.loginPromptLabel.setText(_translate("RegisterWindow", "Already have an account?"))
        self.loginButton.setText(_translate("RegisterWindow", "Login"))
        self.versionLabel.setText(_translate("RegisterWindow", "Version 1.0.0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegisterWindow = QtWidgets.QMainWindow()
    ui = Ui_RegisterWindow()
    ui.setupUi(RegisterWindow)
    RegisterWindow.show()
    sys.exit(app.exec_())