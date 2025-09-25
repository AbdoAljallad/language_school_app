from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QMenuBar, QMenu, QAction


class Ui_AdminDashboard(object):
    def setupUi(self, AdminDashboard):
        """Setup the admin dashboard UI."""
        AdminDashboard.setObjectName("AdminDashboard")
        AdminDashboard.resize(1200, 800)

        # Add unified stylesheet to match other dashboards (same colors / button styles)
        AdminDashboard.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QLabel#welcomeLabel { font-size: 16px; font-weight: bold; color: #2c3e50; }
            QTabWidget::pane { border: 1px solid #bdc3c7; background-color: white; }
            QTabBar::tab { background-color: #ecf0f1; border: 1px solid #bdc3c7; padding: 8px 12px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: white; border-bottom-color: white; }
            QTabBar::tab:hover { background-color: #d6dbdf; }
            QTableWidget { border: 1px solid #bdc3c7; gridline-color: #ecf0f1; selection-background-color: #3498db; selection-color: white; background-color: white; }
            QHeaderView::section { background-color: #ecf0f1; border: 1px solid #bdc3c7; padding: 4px; }
            QPushButton { background-color: #3498db; color: white; border: none; border-radius: 4px; padding: 8px 14px; }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1f6aa5; }
            QPushButton#logoutButton { background-color: #e74c3c; }
            QPushButton#logoutButton:hover { background-color: #c0392b; }
            QLineEdit, QComboBox, QDateEdit, QTimeEdit { padding: 6px; border: 1px solid #bdc3c7; border-radius: 4px; background-color: white; }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus { border: 1px solid #3498db; }
        """)

        # Create central widget
        self.centralwidget = QtWidgets.QWidget(AdminDashboard)
        AdminDashboard.setCentralWidget(self.centralwidget)

        # Create main layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Create header layout
        self.headerLayout = QtWidgets.QHBoxLayout()

        # Welcome label
        self.welcomeLabel = QtWidgets.QLabel(self.centralwidget)
        self.headerLayout.addWidget(self.welcomeLabel)

        # Add stretch to push buttons to the right
        self.headerLayout.addStretch()

        # Profile button
        self.profileButton = QtWidgets.QPushButton("Profile", self.centralwidget)
        self.headerLayout.addWidget(self.profileButton)

        # Logout button
        self.logoutButton = QtWidgets.QPushButton("Logout", self.centralwidget)
        self.headerLayout.addWidget(self.logoutButton)

        self.mainLayout.addLayout(self.headerLayout)

        # Create menu bar
        self.menubar = QtWidgets.QMenuBar(AdminDashboard)
        AdminDashboard.setMenuBar(self.menubar)

        # Create File menu and actions
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle("File")
        self.menubar.addAction(self.menuFile.menuAction())

        self.actionRefresh = QtWidgets.QAction(AdminDashboard)
        self.actionRefresh.setText("Refresh")
        self.menuFile.addAction(self.actionRefresh)

        self.actionExit = QtWidgets.QAction(AdminDashboard)
        self.actionExit.setText("Exit")
        self.menuFile.addAction(self.actionExit)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(AdminDashboard)
        AdminDashboard.setStatusBar(self.statusbar)

        # -----------------------
        # Create tab widget + tabs
        # -----------------------
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Users tab
        self.usersTab = QtWidgets.QWidget()
        self.usersTab.setObjectName("usersTab")
        self.usersLayout = QtWidgets.QVBoxLayout(self.usersTab)

        # Users toolbar (search + type filter + add button)
        self.usersToolbar = QtWidgets.QHBoxLayout()
        self.userSearchInput = QtWidgets.QLineEdit(self.usersTab)
        self.userSearchInput.setObjectName("userSearchInput")
        self.userSearchInput.setPlaceholderText("Search users...")
        self.usersToolbar.addWidget(self.userSearchInput)

        self.userTypeFilter = QtWidgets.QComboBox(self.usersTab)
        self.userTypeFilter.setObjectName("userTypeFilter")
        self.userTypeFilter.addItem("All Types", "")
        self.userTypeFilter.addItem("Admin", "admin")
        self.userTypeFilter.addItem("Teacher", "teacher")
        self.userTypeFilter.addItem("Student", "student")
        self.usersToolbar.addWidget(self.userTypeFilter)

        self.addUserButton = QtWidgets.QPushButton("Add User", self.usersTab)
        self.addUserButton.setObjectName("addUserButton")
        self.usersToolbar.addWidget(self.addUserButton)

        self.usersLayout.addLayout(self.usersToolbar)

        # Users table
        self.usersTable = QtWidgets.QTableWidget(self.usersTab)
        self.usersTable.setObjectName("usersTable")
        self.usersLayout.addWidget(self.usersTable)
        self.tabWidget.addTab(self.usersTab, "Users")

        # Courses tab
        self.coursesTab = QtWidgets.QWidget()
        self.coursesTab.setObjectName("coursesTab")
        self.coursesLayout = QtWidgets.QVBoxLayout(self.coursesTab)

        # Courses toolbar (search + language + level + add)
        self.coursesToolbar = QtWidgets.QHBoxLayout()
        self.courseSearchInput = QtWidgets.QLineEdit(self.coursesTab)
        self.courseSearchInput.setObjectName("courseSearchInput")
        self.courseSearchInput.setPlaceholderText("Search courses...")
        self.coursesToolbar.addWidget(self.courseSearchInput)

        self.languageFilter = QtWidgets.QComboBox(self.coursesTab)
        self.languageFilter.setObjectName("languageFilter")
        self.languageFilter.addItem("All Languages", "")
        self.languageFilter.addItem("English", "English")
        self.languageFilter.addItem("Spanish", "Spanish")
        self.languageFilter.addItem("French", "French")
        self.coursesToolbar.addWidget(self.languageFilter)

        self.levelFilter = QtWidgets.QComboBox(self.coursesTab)
        self.levelFilter.setObjectName("levelFilter")
        self.levelFilter.addItem("All Levels", "")
        self.levelFilter.addItem("A1", "A1")
        self.levelFilter.addItem("A2", "A2")
        self.levelFilter.addItem("B1", "B1")
        self.levelFilter.addItem("B2", "B2")
        self.levelFilter.addItem("C1", "C1")
        self.levelFilter.addItem("C2", "C2")
        self.coursesToolbar.addWidget(self.levelFilter)

        self.addCourseButton = QtWidgets.QPushButton("Add Course", self.coursesTab)
        self.addCourseButton.setObjectName("addCourseButton")
        self.coursesToolbar.addWidget(self.addCourseButton)

        self.coursesLayout.addLayout(self.coursesToolbar)

        # Courses table
        self.coursesTable = QtWidgets.QTableWidget(self.coursesTab)
        self.coursesTable.setObjectName("coursesTable")
        self.coursesLayout.addWidget(self.coursesTable)
        self.tabWidget.addTab(self.coursesTab, "Courses")

        # Schedules tab
        self.schedulesTab = QtWidgets.QWidget()
        self.schedulesTab.setObjectName("schedulesTab")
        self.schedulesLayout = QtWidgets.QVBoxLayout(self.schedulesTab)

        # Schedules toolbar (course filter + day filter + add)
        self.schedulesToolbar = QtWidgets.QHBoxLayout()
        self.courseFilter = QtWidgets.QComboBox(self.schedulesTab)
        self.courseFilter.setObjectName("courseFilter")
        self.courseFilter.addItem("All Courses", -1)
        self.schedulesToolbar.addWidget(self.courseFilter)

        self.dayFilter = QtWidgets.QComboBox(self.schedulesTab)
        self.dayFilter.setObjectName("dayFilter")
        self.dayFilter.addItem("All Days", "")
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            self.dayFilter.addItem(d, d)
        self.schedulesToolbar.addWidget(self.dayFilter)

        self.addScheduleButton = QtWidgets.QPushButton("Add Schedule", self.schedulesTab)
        self.addScheduleButton.setObjectName("addScheduleButton")
        self.schedulesToolbar.addWidget(self.addScheduleButton)

        self.schedulesLayout.addLayout(self.schedulesToolbar)

        # Schedules table
        self.schedulesTable = QtWidgets.QTableWidget(self.schedulesTab)
        self.schedulesTable.setObjectName("schedulesTable")
        self.schedulesLayout.addWidget(self.schedulesTable)
        self.tabWidget.addTab(self.schedulesTab, "Schedules")

        # Payments tab
        self.paymentsTab = QtWidgets.QWidget()
        self.paymentsTab.setObjectName("paymentsTab")
        self.paymentsLayout = QtWidgets.QVBoxLayout(self.paymentsTab)

        # Payments toolbar (search + status + add) - keep names expected by view
        self.paymentsToolbar = QtWidgets.QHBoxLayout()
        self.paymentSearchInput = QtWidgets.QLineEdit(self.paymentsTab)
        self.paymentSearchInput.setObjectName("paymentSearchInput")
        self.paymentSearchInput.setPlaceholderText("Search payments...")
        self.paymentsToolbar.addWidget(self.paymentSearchInput)
        self.paymentStatusFilter = QtWidgets.QComboBox(self.paymentsTab)
        self.paymentStatusFilter.setObjectName("paymentStatusFilter")
        self.paymentStatusFilter.addItem("All Status")
        self.paymentsToolbar.addWidget(self.paymentStatusFilter)
        self.addPaymentButton = QtWidgets.QPushButton("Add Payment", self.paymentsTab)
        self.addPaymentButton.setObjectName("addPaymentButton")
        self.paymentsToolbar.addWidget(self.addPaymentButton)
        self.paymentsLayout.addLayout(self.paymentsToolbar)

        # Payments table
        self.paymentsTable = QtWidgets.QTableWidget(self.paymentsTab)
        self.paymentsTable.setObjectName("paymentsTable")
        self.paymentsLayout.addWidget(self.paymentsTable)
        self.tabWidget.addTab(self.paymentsTab, "Payments")

        # -----------------------
        # Reports tab (kept as before)
        # -----------------------
        self.reportsTab = QtWidgets.QWidget()
        self.reportsTab.setObjectName("reportsTab")
        self.reportsLayout = QtWidgets.QVBoxLayout(self.reportsTab)

        self.reportsToolbar = QtWidgets.QHBoxLayout()
        self.startDateEdit = QtWidgets.QDateEdit(self.reportsTab)
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setObjectName("startDateEdit")
        self.reportsToolbar.addWidget(self.startDateEdit)
        self.endDateEdit = QtWidgets.QDateEdit(self.reportsTab)
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.setObjectName("endDateEdit")
        self.reportsToolbar.addWidget(self.endDateEdit)
        self.reportTypeCombo = QtWidgets.QComboBox(self.reportsTab)
        self.reportTypeCombo.setObjectName("reportTypeCombo")
        self.reportTypeCombo.addItem("User Activity", "user_activity")
        self.reportTypeCombo.addItem("Course Enrollment", "course_enrollment")
        self.reportTypeCombo.addItem("Payment Summary", "payment_summary")
        self.reportsToolbar.addWidget(self.reportTypeCombo)
        self.generateReportButton = QtWidgets.QPushButton("Generate Report", self.reportsTab)
        self.generateReportButton.setObjectName("generateReportButton")
        self.reportsToolbar.addWidget(self.generateReportButton)
        self.exportReportButton = QtWidgets.QPushButton("Export", self.reportsTab)
        self.exportReportButton.setObjectName("exportReportButton")
        self.reportsToolbar.addWidget(self.exportReportButton)
        self.reportsLayout.addLayout(self.reportsToolbar)
        # Add an empty table for reports (optional)
        self.reportsTable = QtWidgets.QTableWidget(self.reportsTab)
        self.reportsTable.setObjectName("reportsTable")
        self.reportsLayout.addWidget(self.reportsTable)
        self.tabWidget.addTab(self.reportsTab, "Reports")

        # -----------------------
        # Messages tab (kept as before)
        # -----------------------
        self.messagesTab = QtWidgets.QWidget()
        self.messagesTab.setObjectName("messagesTab")
        self.messagesLayout = QtWidgets.QVBoxLayout(self.messagesTab)

        self.messageTopLayout = QtWidgets.QHBoxLayout()
        self.messageSearchInput = QtWidgets.QLineEdit(self.messagesTab)
        self.messageSearchInput.setObjectName("messageSearchInput")
        self.messageSearchInput.setPlaceholderText("Search conversations...")
        self.messageTopLayout.addWidget(self.messageSearchInput)
        self.newConversationButton = QtWidgets.QPushButton("New Conversation", self.messagesTab)
        self.newConversationButton.setObjectName("newConversationButton")
        self.messageTopLayout.addWidget(self.newConversationButton)
        self.messagesLayout.addLayout(self.messageTopLayout)

        self.messagesSplitter = QtWidgets.QSplitter(self.messagesTab)
        self.messagesSplitter.setOrientation(QtCore.Qt.Horizontal)
        # Conversations list
        self.conversationsList = QtWidgets.QListWidget(self.messagesSplitter)
        self.conversationsList.setObjectName("conversationsList")
        # Messages list
        self.messagesList = QtWidgets.QListWidget(self.messagesSplitter)
        self.messagesList.setObjectName("messagesList")
        self.messagesLayout.addWidget(self.messagesSplitter)

        self.messageInputLayout = QtWidgets.QHBoxLayout()
        self.messageInput = QtWidgets.QLineEdit(self.messagesTab)
        self.messageInput.setObjectName("messageInput")
        self.messageInput.setPlaceholderText("Type a message...")
        self.messageInputLayout.addWidget(self.messageInput)
        self.sendMessageButton = QtWidgets.QPushButton("Send", self.messagesTab)
        self.sendMessageButton.setObjectName("sendMessageButton")
        self.messageInputLayout.addWidget(self.sendMessageButton)
        self.messagesLayout.addLayout(self.messageInputLayout)

        self.tabWidget.addTab(self.messagesTab, "Messages")

        # Add the tab widget to the main layout
        self.mainLayout.addWidget(self.tabWidget)

        # Finalize
        self.retranslateUi(AdminDashboard)
        QtCore.QMetaObject.connectSlotsByName(AdminDashboard)

    def retranslateUi(self, AdminDashboard):
        _translate = QtCore.QCoreApplication.translate
        AdminDashboard.setWindowTitle(_translate("AdminDashboard", "Language School - Admin Dashboard"))
        self.welcomeLabel.setText(_translate("AdminDashboard", "Welcome, Admin"))
        self.profileButton.setText(_translate("AdminDashboard", "Profile"))
        self.logoutButton.setText(_translate("AdminDashboard", "Logout"))
        self.menuFile.setTitle(_translate("AdminDashboard", "File"))
        self.actionRefresh.setText(_translate("AdminDashboard", "Refresh"))
        self.actionExit.setText(_translate("AdminDashboard", "Exit"))

        # Set headers for each table (tables are created in setupUi)
        def set_table_headers(table, headers):
            table.setRowCount(0)
            table.setColumnCount(len(headers))
            for i, header in enumerate(headers):
                item = QtWidgets.QTableWidgetItem(header)
                table.setHorizontalHeaderItem(i, item)

        set_table_headers(self.usersTable, ["ID", "Username", "First", "Last", "Email", "Type", "Active", "Actions"])
        set_table_headers(self.coursesTable, ["ID", "Name", "Language", "Level", "Teacher", "Price", "Active", "Actions"])
        set_table_headers(self.schedulesTable, ["ID", "Date", "Start", "End", "Room", "Notes", "Course", "Teacher", "Actions"])
        set_table_headers(self.paymentsTable, ["ID", "Amount", "Date", "Status", "Student", "Course", "Actions"])

        # Reports tab texts
        self.generateReportButton.setText(_translate("AdminDashboard", "Generate Report"))
        self.exportReportButton.setText(_translate("AdminDashboard", "Export"))
