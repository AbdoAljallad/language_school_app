from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdminDashboard(object):
    def setupUi(self, AdminDashboard):
        AdminDashboard.setObjectName("AdminDashboard")
        AdminDashboard.resize(1000, 700)
        AdminDashboard.setMinimumSize(QtCore.QSize(1000, 700))
        AdminDashboard.setStyleSheet("QMainWindow {\n"
"    background-color: #f5f5f5;\n"
"}\n"
"\n"
"QLabel#welcomeLabel {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #2c3e50;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #bdc3c7;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #ecf0f1;\n"
"    border: 1px solid #bdc3c7;\n"
"    padding: 8px 16px;\n"
"    margin-right: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: white;\n"
"    border-bottom-color: white;\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #d6dbdf;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #3498db;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 8px 16px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1f6dad;\n"
"}\n"
"\n"
"QPushButton#logoutButton {\n"
"    background-color: #e74c3c;\n"
"}\n"
"\n"
"QPushButton#logoutButton:hover {\n"
"    background-color: #c0392b;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    border: 1px solid #bdc3c7;\n"
"    gridline-color: #ecf0f1;\n"
"    selection-background-color: #3498db;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QTableWidget QHeaderView::section {\n"
"    background-color: #ecf0f1;\n"
"    padding: 4px;\n"
"    border: 1px solid #bdc3c7;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLineEdit, QComboBox, QSpinBox, QDateEdit {\n"
"    padding: 6px;\n"
"    border: 1px solid #bdc3c7;\n"
"    border-radius: 4px;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {\n"
"    border: 1px solid #3498db;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(AdminDashboard)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLayout = QtWidgets.QHBoxLayout()
        self.headerLayout.setObjectName("headerLayout")
        self.welcomeLabel = QtWidgets.QLabel(self.centralwidget)
        self.welcomeLabel.setObjectName("welcomeLabel")
        self.headerLayout.addWidget(self.welcomeLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.headerLayout.addItem(spacerItem)
        self.logoutButton = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../resources/icons/logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logoutButton.setIcon(icon)
        self.logoutButton.setObjectName("logoutButton")
        self.headerLayout.addWidget(self.logoutButton)
        # Add Profile button to header
        self.profileButton = QtWidgets.QPushButton(self.centralwidget)
        self.profileButton.setObjectName("profileButton")
        self.profileButton.setText("Profile")
        self.headerLayout.insertWidget(self.headerLayout.count()-1, self.profileButton)
        self.verticalLayout.addLayout(self.headerLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.usersTab = QtWidgets.QWidget()
        self.usersTab.setObjectName("usersTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.usersTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.usersToolbarLayout = QtWidgets.QHBoxLayout()
        self.usersToolbarLayout.setObjectName("usersToolbarLayout")
        self.userSearchInput = QtWidgets.QLineEdit(self.usersTab)
        self.userSearchInput.setObjectName("userSearchInput")
        self.usersToolbarLayout.addWidget(self.userSearchInput)
        self.userTypeFilter = QtWidgets.QComboBox(self.usersTab)
        self.userTypeFilter.setObjectName("userTypeFilter")
        self.userTypeFilter.addItem("")
        self.userTypeFilter.addItem("")
        self.userTypeFilter.addItem("")
        self.userTypeFilter.addItem("")
        self.usersToolbarLayout.addWidget(self.userTypeFilter)
        self.addUserButton = QtWidgets.QPushButton(self.usersTab)
        self.addUserButton.setObjectName("addUserButton")
        self.usersToolbarLayout.addWidget(self.addUserButton)
        self.verticalLayout_2.addLayout(self.usersToolbarLayout)
        self.usersTable = QtWidgets.QTableWidget(self.usersTab)
        self.usersTable.setObjectName("usersTable")
        self.usersTable.setColumnCount(8)
        headers = ["ID", "Username", "First Name", "Last Name", "User Type", "Email", "Active", "Actions"]
        self.usersTable.setHorizontalHeaderLabels(headers)
        self.verticalLayout_2.addWidget(self.usersTable)
        self.tabWidget.addTab(self.usersTab, "")
        self.coursesTab = QtWidgets.QWidget()
        self.coursesTab.setObjectName("coursesTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.coursesTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.coursesToolbarLayout = QtWidgets.QHBoxLayout()
        self.coursesToolbarLayout.setObjectName("coursesToolbarLayout")
        self.courseSearchInput = QtWidgets.QLineEdit(self.coursesTab)
        self.courseSearchInput.setObjectName("courseSearchInput")
        self.coursesToolbarLayout.addWidget(self.courseSearchInput)
        self.languageFilter = QtWidgets.QComboBox(self.coursesTab)
        self.languageFilter.setObjectName("languageFilter")
        self.languageFilter.addItem("")
        self.coursesToolbarLayout.addWidget(self.languageFilter)
        self.levelFilter = QtWidgets.QComboBox(self.coursesTab)
        self.levelFilter.setObjectName("levelFilter")
        self.levelFilter.addItem("")
        self.coursesToolbarLayout.addWidget(self.levelFilter)
        self.addCourseButton = QtWidgets.QPushButton(self.coursesTab)
        self.addCourseButton.setObjectName("addCourseButton")
        self.coursesToolbarLayout.addWidget(self.addCourseButton)
        self.verticalLayout_3.addLayout(self.coursesToolbarLayout)
        self.coursesTable = QtWidgets.QTableWidget(self.coursesTab)
        self.coursesTable.setObjectName("coursesTable")
        self.coursesTable.setColumnCount(7)
        self.coursesTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.coursesTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.coursesTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.coursesTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.coursesTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.coursesTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.coursesTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.coursesTable.setHorizontalHeaderItem(6, item)
        self.verticalLayout_3.addWidget(self.coursesTable)
        self.tabWidget.addTab(self.coursesTab, "")
        self.schedulesTab = QtWidgets.QWidget()
        self.schedulesTab.setObjectName("schedulesTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.schedulesTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.schedulesToolbarLayout = QtWidgets.QHBoxLayout()
        self.schedulesToolbarLayout.setObjectName("schedulesToolbarLayout")
        self.courseFilter = QtWidgets.QComboBox(self.schedulesTab)
        self.courseFilter.setObjectName("courseFilter")
        self.courseFilter.addItem("")
        self.schedulesToolbarLayout.addWidget(self.courseFilter)
        self.dayFilter = QtWidgets.QComboBox(self.schedulesTab)
        self.dayFilter.setObjectName("dayFilter")
        self.dayFilter.addItem("")
        self.dayFilter.addItem("")
        self.dayFilter.addItem("")
        self.dayFilter.addItem("")
        self.dayFilter.addItem("")
        self.dayFilter.addItem("")
        self.dayFilter.addItem("")
        self.dayFilter.addItem("")
        self.schedulesToolbarLayout.addWidget(self.dayFilter)
        self.addScheduleButton = QtWidgets.QPushButton(self.schedulesTab)
        self.addScheduleButton.setObjectName("addScheduleButton")
        self.schedulesToolbarLayout.addWidget(self.addScheduleButton)
        self.verticalLayout_4.addLayout(self.schedulesToolbarLayout)
        self.schedulesTable = QtWidgets.QTableWidget(self.schedulesTab)
        self.schedulesTable.setObjectName("schedulesTable")
        self.schedulesTable.setColumnCount(7)
        self.schedulesTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.schedulesTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.schedulesTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.schedulesTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.schedulesTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.schedulesTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.schedulesTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.schedulesTable.setHorizontalHeaderItem(6, item)
        self.verticalLayout_4.addWidget(self.schedulesTable)
        self.tabWidget.addTab(self.schedulesTab, "")
        self.paymentsTab = QtWidgets.QWidget()
        self.paymentsTab.setObjectName("paymentsTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.paymentsTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.paymentsToolbarLayout = QtWidgets.QHBoxLayout()
        self.paymentsToolbarLayout.setObjectName("paymentsToolbarLayout")
        self.paymentSearchInput = QtWidgets.QLineEdit(self.paymentsTab)
        self.paymentSearchInput.setObjectName("paymentSearchInput")
        self.paymentsToolbarLayout.addWidget(self.paymentSearchInput)
        self.paymentStatusFilter = QtWidgets.QComboBox(self.paymentsTab)
        self.paymentStatusFilter.setObjectName("paymentStatusFilter")
        self.paymentStatusFilter.addItem("")
        self.paymentStatusFilter.addItem("")
        self.paymentStatusFilter.addItem("")
        self.paymentStatusFilter.addItem("")
        self.paymentStatusFilter.addItem("")
        self.paymentsToolbarLayout.addWidget(self.paymentStatusFilter)
        self.addPaymentButton = QtWidgets.QPushButton(self.paymentsTab)
        self.addPaymentButton.setObjectName("addPaymentButton")
        self.paymentsToolbarLayout.addWidget(self.addPaymentButton)
        self.verticalLayout_5.addLayout(self.paymentsToolbarLayout)
        self.paymentsTable = QtWidgets.QTableWidget(self.paymentsTab)
        self.paymentsTable.setObjectName("paymentsTable")
        self.paymentsTable.setColumnCount(8)
        self.paymentsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.paymentsTable.setHorizontalHeaderItem(7, item)
        self.verticalLayout_5.addWidget(self.paymentsTable)
        self.tabWidget.addTab(self.paymentsTab, "")
        self.reportsTab = QtWidgets.QWidget()
        self.reportsTab.setObjectName("reportsTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.reportsTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.reportsToolbarLayout = QtWidgets.QHBoxLayout()
        self.reportsToolbarLayout.setObjectName("reportsToolbarLayout")
        self.reportTypeComboBox = QtWidgets.QComboBox(self.reportsTab)
        self.reportTypeComboBox.setObjectName("reportTypeComboBox")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportTypeComboBox.addItem("")
        self.reportsToolbarLayout.addWidget(self.reportTypeComboBox)
        self.startDateEdit = QtWidgets.QDateEdit(self.reportsTab)
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setObjectName("startDateEdit")
        self.reportsToolbarLayout.addWidget(self.startDateEdit)
        self.toLabel = QtWidgets.QLabel(self.reportsTab)
        self.toLabel.setObjectName("toLabel")
        self.reportsToolbarLayout.addWidget(self.toLabel)
        self.endDateEdit = QtWidgets.QDateEdit(self.reportsTab)
        self.endDateEdit.setCalendarPopup(True)
        self.endDateEdit.setObjectName("endDateEdit")
        self.reportsToolbarLayout.addWidget(self.endDateEdit)
        self.generateReportButton = QtWidgets.QPushButton(self.reportsTab)
        self.generateReportButton.setObjectName("generateReportButton")
        self.reportsToolbarLayout.addWidget(self.generateReportButton)
        self.exportReportButton = QtWidgets.QPushButton(self.reportsTab)
        self.exportReportButton.setObjectName("exportReportButton")
        self.reportsToolbarLayout.addWidget(self.exportReportButton)
        self.verticalLayout_6.addLayout(self.reportsToolbarLayout)
        self.reportsTable = QtWidgets.QTableWidget(self.reportsTab)
        self.reportsTable.setObjectName("reportsTable")
        self.reportsTable.setColumnCount(0)
        self.reportsTable.setRowCount(0)
        self.verticalLayout_6.addWidget(self.reportsTable)
        self.tabWidget.addTab(self.reportsTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.statusLayout = QtWidgets.QHBoxLayout()
        self.statusLayout.setObjectName("statusLayout")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLayout.addWidget(self.statusLabel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.statusLayout.addItem(spacerItem1)
        self.versionLabel = QtWidgets.QLabel(self.centralwidget)
        self.versionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.statusLayout.addWidget(self.versionLabel)
        self.verticalLayout.addLayout(self.statusLayout)
        AdminDashboard.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AdminDashboard)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuUsers = QtWidgets.QMenu(self.menubar)
        self.menuUsers.setObjectName("menuUsers")
        self.menuCourses = QtWidgets.QMenu(self.menubar)
        self.menuCourses.setObjectName("menuCourses")
        self.menuReports = QtWidgets.QMenu(self.menubar)
        self.menuReports.setObjectName("menuReports")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        AdminDashboard.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AdminDashboard)
        self.statusbar.setObjectName("statusbar")
        AdminDashboard.setStatusBar(self.statusbar)
        self.actionRefresh = QtWidgets.QAction(AdminDashboard)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionLogout = QtWidgets.QAction(AdminDashboard)
        self.actionLogout.setObjectName("actionLogout")
        self.actionExit = QtWidgets.QAction(AdminDashboard)
        self.actionExit.setObjectName("actionExit")
        self.actionAddUser = QtWidgets.QAction(AdminDashboard)
        self.actionAddUser.setObjectName("actionAddUser")
        self.actionImportUsers = QtWidgets.QAction(AdminDashboard)
        self.actionImportUsers.setObjectName("actionImportUsers")
        self.actionExportUsers = QtWidgets.QAction(AdminDashboard)
        self.actionExportUsers.setObjectName("actionExportUsers")
        self.actionAddCourse = QtWidgets.QAction(AdminDashboard)
        self.actionAddCourse.setObjectName("actionAddCourse")
        self.actionImportCourses = QtWidgets.QAction(AdminDashboard)
        self.actionImportCourses.setObjectName("actionImportCourses")
        self.actionExportCourses = QtWidgets.QAction(AdminDashboard)
        self.actionExportCourses.setObjectName("actionExportCourses")
        self.actionGenerateReport = QtWidgets.QAction(AdminDashboard)
        self.actionGenerateReport.setObjectName("actionGenerateReport")
        self.actionExportReport = QtWidgets.QAction(AdminDashboard)
        self.actionExportReport.setObjectName("actionExportReport")
        self.actionAbout = QtWidgets.QAction(AdminDashboard)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(AdminDashboard)
        self.actionHelp.setObjectName("actionHelp")
        self.actionProfile = QtWidgets.QAction(AdminDashboard)
        self.actionProfile.setObjectName("actionProfile")
        # Create actions before they are used
        self.actionEditUser = QtWidgets.QAction(AdminDashboard)
        self.actionEditUser.setObjectName("actionEditUser")
        self.actionDeleteUser = QtWidgets.QAction(AdminDashboard)
        self.actionDeleteUser.setObjectName("actionDeleteUser")
        self.actionExport = QtWidgets.QAction(AdminDashboard)
        self.actionExport.setObjectName("actionExport")
        self.actionPrint = QtWidgets.QAction(AdminDashboard)
        self.actionPrint.setObjectName("actionPrint")
        self.actionPreferences = QtWidgets.QAction(AdminDashboard)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionDocumentation = QtWidgets.QAction(AdminDashboard)
        self.actionDocumentation.setObjectName("actionDocumentation")
        
        # Update menu structure to match UI file
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLogout)
        self.menuFile.addAction(self.actionExit)
        
        self.menuEdit.addAction(self.actionPreferences)
        
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)
        
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(AdminDashboard)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AdminDashboard)

    def retranslateUi(self, AdminDashboard):
        _translate = QtCore.QCoreApplication.translate
        AdminDashboard.setWindowTitle(_translate("AdminDashboard", "Language School - Admin Dashboard"))
        self.welcomeLabel.setText(_translate("AdminDashboard", "Welcome, Admin"))
        self.logoutButton.setText(_translate("AdminDashboard", "Logout"))
        self.userSearchInput.setPlaceholderText(_translate("AdminDashboard", "Search users..."))
        self.userTypeFilter.setItemText(0, _translate("AdminDashboard", "All Types"))
        self.userTypeFilter.setItemText(1, _translate("AdminDashboard", "Admin"))
        self.userTypeFilter.setItemText(2, _translate("AdminDashboard", "Teacher"))
        self.userTypeFilter.setItemText(3, _translate("AdminDashboard", "Student"))
        self.addUserButton.setText(_translate("AdminDashboard", "Add User"))
        item = self.usersTable.horizontalHeaderItem(0)
        item.setText(_translate("AdminDashboard", "ID"))
        item = self.usersTable.horizontalHeaderItem(1)
        item.setText(_translate("AdminDashboard", "Username"))
        item = self.usersTable.horizontalHeaderItem(2)
        item.setText(_translate("AdminDashboard", "Full Name"))
        item = self.usersTable.horizontalHeaderItem(3)
        item.setText(_translate("AdminDashboard", "Type"))
        item = self.usersTable.horizontalHeaderItem(4)
        item.setText(_translate("AdminDashboard", "Email"))
        item = self.usersTable.horizontalHeaderItem(5)
        item.setText(_translate("AdminDashboard", "Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.usersTab), _translate("AdminDashboard", "Users"))
        self.courseSearchInput.setPlaceholderText(_translate("AdminDashboard", "Search courses..."))
        self.languageFilter.setItemText(0, _translate("AdminDashboard", "All Languages"))
        self.levelFilter.setItemText(0, _translate("AdminDashboard", "All Levels"))
        self.addCourseButton.setText(_translate("AdminDashboard", "Add Course"))
        item = self.coursesTable.horizontalHeaderItem(0)
        item.setText(_translate("AdminDashboard", "ID"))
        item = self.coursesTable.horizontalHeaderItem(1)
        item.setText(_translate("AdminDashboard", "Name"))
        item = self.coursesTable.horizontalHeaderItem(2)
        item.setText(_translate("AdminDashboard", "Language"))
        item = self.coursesTable.horizontalHeaderItem(3)
        item.setText(_translate("AdminDashboard", "Level"))
        item = self.coursesTable.horizontalHeaderItem(4)
        item.setText(_translate("AdminDashboard", "Price"))
        item = self.coursesTable.horizontalHeaderItem(5)
        item.setText(_translate("AdminDashboard", "Teacher"))
        item = self.coursesTable.horizontalHeaderItem(6)
        item.setText(_translate("AdminDashboard", "Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.coursesTab), _translate("AdminDashboard", "Courses"))
        self.courseFilter.setItemText(0, _translate("AdminDashboard", "All Courses"))
        self.dayFilter.setItemText(0, _translate("AdminDashboard", "All Days"))
        self.dayFilter.setItemText(1, _translate("AdminDashboard", "Monday"))
        self.dayFilter.setItemText(2, _translate("AdminDashboard", "Tuesday"))
        self.dayFilter.setItemText(3, _translate("AdminDashboard", "Wednesday"))
        self.dayFilter.setItemText(4, _translate("AdminDashboard", "Thursday"))
        self.dayFilter.setItemText(5, _translate("AdminDashboard", "Friday"))
        self.dayFilter.setItemText(6, _translate("AdminDashboard", "Saturday"))
        self.dayFilter.setItemText(7, _translate("AdminDashboard", "Sunday"))
        self.addScheduleButton.setText(_translate("AdminDashboard", "Add Schedule"))
        item = self.schedulesTable.horizontalHeaderItem(0)
        item.setText(_translate("AdminDashboard", "ID"))
        item = self.schedulesTable.horizontalHeaderItem(1)
        item.setText(_translate("AdminDashboard", "Course"))
        item = self.schedulesTable.horizontalHeaderItem(2)
        item.setText(_translate("AdminDashboard", "Day"))
        item = self.schedulesTable.horizontalHeaderItem(3)
        item.setText(_translate("AdminDashboard", "Start Time"))
        item = self.schedulesTable.horizontalHeaderItem(4)
        item.setText(_translate("AdminDashboard", "End Time"))
        item = self.schedulesTable.horizontalHeaderItem(5)
        item.setText(_translate("AdminDashboard", "Room"))
        item = self.schedulesTable.horizontalHeaderItem(6)
        item.setText(_translate("AdminDashboard", "Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.schedulesTab), _translate("AdminDashboard", "Schedules"))
        self.paymentSearchInput.setPlaceholderText(_translate("AdminDashboard", "Search payments..."))
        self.paymentStatusFilter.setItemText(0, _translate("AdminDashboard", "All Statuses"))
        self.paymentStatusFilter.setItemText(1, _translate("AdminDashboard", "Pending"))
        self.paymentStatusFilter.setItemText(2, _translate("AdminDashboard", "Completed"))
        self.paymentStatusFilter.setItemText(3, _translate("AdminDashboard", "Failed"))
        self.paymentStatusFilter.setItemText(4, _translate("AdminDashboard", "Refunded"))
        self.addPaymentButton.setText(_translate("AdminDashboard", "Add Payment"))
        item = self.paymentsTable.horizontalHeaderItem(0)
        item.setText(_translate("AdminDashboard", "ID"))
        item = self.paymentsTable.horizontalHeaderItem(1)
        item.setText(_translate("AdminDashboard", "Student"))
        item = self.paymentsTable.horizontalHeaderItem(2)
        item.setText(_translate("AdminDashboard", "Course"))
        item = self.paymentsTable.horizontalHeaderItem(3)
        item.setText(_translate("AdminDashboard", "Amount"))
        item = self.paymentsTable.horizontalHeaderItem(4)
        item.setText(_translate("AdminDashboard", "Date"))
        item = self.paymentsTable.horizontalHeaderItem(5)
        item.setText(_translate("AdminDashboard", "Method"))
        item = self.paymentsTable.horizontalHeaderItem(6)
        item.setText(_translate("AdminDashboard", "Status"))
        item = self.paymentsTable.horizontalHeaderItem(7)
        item.setText(_translate("AdminDashboard", "Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.paymentsTab), _translate("AdminDashboard", "Payments"))
        self.reportTypeComboBox.setItemText(0, _translate("AdminDashboard", "Student Enrollment"))
        self.reportTypeComboBox.setItemText(1, _translate("AdminDashboard", "Course Revenue"))
        self.reportTypeComboBox.setItemText(2, _translate("AdminDashboard", "Teacher Performance"))
        self.reportTypeComboBox.setItemText(3, _translate("AdminDashboard", "Attendance Report"))
        self.startDateEdit.setDisplayFormat(_translate("AdminDashboard", "yyyy-MM-dd"))
        self.toLabel.setText(_translate("AdminDashboard", "to"))
        self.endDateEdit.setDisplayFormat(_translate("AdminDashboard", "yyyy-MM-dd"))
        self.generateReportButton.setText(_translate("AdminDashboard", "Generate Report"))
        self.exportReportButton.setText(_translate("AdminDashboard", "Export"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.reportsTab), _translate("AdminDashboard", "Reports"))
        self.statusLabel.setText(_translate("AdminDashboard", "Ready"))
        self.versionLabel.setText(_translate("AdminDashboard", "Version 1.0.0"))
        self.menuFile.setTitle(_translate("AdminDashboard", "File"))
        self.menuUsers.setTitle(_translate("AdminDashboard", "Users"))
        self.menuCourses.setTitle(_translate("AdminDashboard", "Courses"))
        self.menuReports.setTitle(_translate("AdminDashboard", "Reports"))
        self.menuHelp.setTitle(_translate("AdminDashboard", "Help"))
        self.menuEdit.setTitle(_translate("AdminDashboard", "Edit"))
        self.actionRefresh.setText(_translate("AdminDashboard", "Refresh"))
        self.actionLogout.setText(_translate("AdminDashboard", "Logout"))
        self.actionExit.setText(_translate("AdminDashboard", "Exit"))
        self.actionAddUser.setText(_translate("AdminDashboard", "Add User"))
        self.actionImportUsers.setText(_translate("AdminDashboard", "Import Users"))
        self.actionExportUsers.setText(_translate("AdminDashboard", "Export Users"))
        self.actionAddCourse.setText(_translate("AdminDashboard", "Add Course"))
        self.actionImportCourses.setText(_translate("AdminDashboard", "Import Courses"))
        self.actionExportCourses.setText(_translate("AdminDashboard", "Export Courses"))
        self.actionGenerateReport.setText(_translate("AdminDashboard", "Generate Report"))
        self.actionExportReport.setText(_translate("AdminDashboard", "Export Report"))
        self.actionAbout.setText(_translate("AdminDashboard", "About"))
        self.actionHelp.setText(_translate("AdminDashboard", "Help"))
        self.actionProfile.setText(_translate("AdminDashboard", "Edit Profile"))
        # Add new action translations
        self.actionExport.setText(_translate("AdminDashboard", "Export..."))
        self.actionPrint.setText(_translate("AdminDashboard", "Print..."))
        self.actionPreferences.setText(_translate("AdminDashboard", "Preferences"))
        self.actionDocumentation.setText(_translate("AdminDashboard", "Documentation"))
        
        # Set tooltips from UI file
        self.actionEditUser.setToolTip(_translate("AdminDashboard", "Edit selected user"))
        self.actionDeleteUser.setToolTip(_translate("AdminDashboard", "Delete selected user"))

        # Set up users table
        self.usersTable.setColumnCount(8)
        headers = ["ID", "Username", "First Name", "Last Name", "Email", "User Type", "Active", "Actions"]
        self.usersTable.setHorizontalHeaderLabels(headers)

        # Make table read-only except Actions column
        self.usersTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.usersTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.usersTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Add context menu for users table
        self.usersTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.usersTable.customContextMenuRequested.connect(self.show_user_context_menu)

        # Set column widths
        self.usersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def show_user_context_menu(self, pos):
        """Show context menu for users table."""
        menu = QtWidgets.QMenu()
        edit_action = menu.addAction("Edit User")
        delete_action = menu.addAction("Delete User")

        # Get selected row
        row = self.usersTable.rowAt(pos.y())
        if row >= 0:
            action = menu.exec_(self.usersTable.viewport().mapToGlobal(pos))
            if action == edit_action:
                user_id = self.usersTable.item(row, 0).text()
                self.edit_user.emit(int(user_id))
            elif action == delete_action:
                user_id = self.usersTable.item(row, 0).text()
                self.delete_user.emit(int(user_id))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AdminDashboard = QtWidgets.QMainWindow()
    ui = Ui_AdminDashboard()
    ui.setupUi(AdminDashboard)
    AdminDashboard.show()
    sys.exit(app.exec_())