"""
Generated Python code for teacher dashboard UI
-------------------------------------------
This file was generated from teacher_dashboard.ui using pyuic5.
Do not edit this file directly.
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TeacherDashboard(object):
    def setupUi(self, TeacherDashboard):
        TeacherDashboard.setObjectName("TeacherDashboard")
        TeacherDashboard.resize(1000, 700)
        TeacherDashboard.setMinimumSize(QtCore.QSize(1000, 700))
        TeacherDashboard.setStyleSheet("QMainWindow {\n"
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
        self.centralwidget = QtWidgets.QWidget(TeacherDashboard)
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
        self.coursesTab = QtWidgets.QWidget()
        self.coursesTab.setObjectName("coursesTab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.coursesTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.coursesTable = QtWidgets.QTableWidget(self.coursesTab)
        self.coursesTable.setObjectName("coursesTable")
        self.coursesTable.setColumnCount(6)
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
        self.verticalLayout_2.addWidget(self.coursesTable)
        self.tabWidget.addTab(self.coursesTab, "")
        self.lessonsTab = QtWidgets.QWidget()
        self.lessonsTab.setObjectName("lessonsTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.lessonsTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lessonsToolbarLayout = QtWidgets.QHBoxLayout()
        self.lessonsToolbarLayout.setObjectName("lessonsToolbarLayout")
        self.courseFilterComboBox = QtWidgets.QComboBox(self.lessonsTab)
        self.courseFilterComboBox.setObjectName("courseFilterComboBox")
        self.courseFilterComboBox.addItem("")
        self.lessonsToolbarLayout.addWidget(self.courseFilterComboBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lessonsToolbarLayout.addItem(spacerItem1)
        self.addLessonButton = QtWidgets.QPushButton(self.lessonsTab)
        self.addLessonButton.setObjectName("addLessonButton")
        self.lessonsToolbarLayout.addWidget(self.addLessonButton)
        self.verticalLayout_3.addLayout(self.lessonsToolbarLayout)
        self.lessonsTable = QtWidgets.QTableWidget(self.lessonsTab)
        self.lessonsTable.setObjectName("lessonsTable")
        self.lessonsTable.setColumnCount(6)
        self.lessonsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.lessonsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.lessonsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.lessonsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.lessonsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.lessonsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.lessonsTable.setHorizontalHeaderItem(5, item)
        self.verticalLayout_3.addWidget(self.lessonsTable)
        self.tabWidget.addTab(self.lessonsTab, "")
        self.studentsTab = QtWidgets.QWidget()
        self.studentsTab.setObjectName("studentsTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.studentsTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.studentsToolbarLayout = QtWidgets.QHBoxLayout()
        self.studentsToolbarLayout.setObjectName("studentsToolbarLayout")
        self.studentCourseFilterComboBox = QtWidgets.QComboBox(self.studentsTab)
        self.studentCourseFilterComboBox.setObjectName("studentCourseFilterComboBox")
        self.studentCourseFilterComboBox.addItem("")
        self.studentsToolbarLayout.addWidget(self.studentCourseFilterComboBox)
        self.studentSearchInput = QtWidgets.QLineEdit(self.studentsTab)
        self.studentSearchInput.setObjectName("studentSearchInput")
        self.studentsToolbarLayout.addWidget(self.studentSearchInput)
        self.verticalLayout_4.addLayout(self.studentsToolbarLayout)
        self.studentsTable = QtWidgets.QTableWidget(self.studentsTab)
        self.studentsTable.setObjectName("studentsTable")
        self.studentsTable.setColumnCount(7)
        self.studentsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.studentsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.studentsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.studentsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.studentsTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.studentsTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.studentsTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.studentsTable.setHorizontalHeaderItem(6, item)
        self.verticalLayout_4.addWidget(self.studentsTable)
        self.tabWidget.addTab(self.studentsTab, "")
        self.attendanceTab = QtWidgets.QWidget()
        self.attendanceTab.setObjectName("attendanceTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.attendanceTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.attendanceToolbarLayout = QtWidgets.QHBoxLayout()
        self.attendanceToolbarLayout.setObjectName("attendanceToolbarLayout")
        self.attendanceCourseFilterComboBox = QtWidgets.QComboBox(self.attendanceTab)
        self.attendanceCourseFilterComboBox.setObjectName("attendanceCourseFilterComboBox")
        self.attendanceCourseFilterComboBox.addItem("")
        self.attendanceToolbarLayout.addWidget(self.attendanceCourseFilterComboBox)
        self.attendanceDateEdit = QtWidgets.QDateEdit(self.attendanceTab)
        self.attendanceDateEdit.setCalendarPopup(True)
        self.attendanceDateEdit.setObjectName("attendanceDateEdit")
        self.attendanceToolbarLayout.addWidget(self.attendanceDateEdit)
        self.saveAttendanceButton = QtWidgets.QPushButton(self.attendanceTab)
        self.saveAttendanceButton.setObjectName("saveAttendanceButton")
        self.attendanceToolbarLayout.addWidget(self.saveAttendanceButton)
        self.verticalLayout_5.addLayout(self.attendanceToolbarLayout)
        self.attendanceTable = QtWidgets.QTableWidget(self.attendanceTab)
        self.attendanceTable.setObjectName("attendanceTable")
        self.attendanceTable.setColumnCount(5)
        self.attendanceTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.attendanceTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.attendanceTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.attendanceTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.attendanceTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.attendanceTable.setHorizontalHeaderItem(4, item)
        self.verticalLayout_5.addWidget(self.attendanceTable)
        self.tabWidget.addTab(self.attendanceTab, "")
        self.gradesTab = QtWidgets.QWidget()
        self.gradesTab.setObjectName("gradesTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.gradesTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gradesToolbarLayout = QtWidgets.QHBoxLayout()
        self.gradesToolbarLayout.setObjectName("gradesToolbarLayout")
        self.gradesCourseFilterComboBox = QtWidgets.QComboBox(self.gradesTab)
        self.gradesCourseFilterComboBox.setObjectName("gradesCourseFilterComboBox")
        self.gradesCourseFilterComboBox.addItem("")
        self.gradesToolbarLayout.addWidget(self.gradesCourseFilterComboBox)
        self.gradesTypeFilterComboBox = QtWidgets.QComboBox(self.gradesTab)
        self.gradesTypeFilterComboBox.setObjectName("gradesTypeFilterComboBox")
        self.gradesTypeFilterComboBox.addItem("")
        self.gradesTypeFilterComboBox.addItem("")
        self.gradesTypeFilterComboBox.addItem("")
        self.gradesToolbarLayout.addWidget(self.gradesTypeFilterComboBox)
        self.saveGradesButton = QtWidgets.QPushButton(self.gradesTab)
        self.saveGradesButton.setObjectName("saveGradesButton")
        self.gradesToolbarLayout.addWidget(self.saveGradesButton)
        self.verticalLayout_6.addLayout(self.gradesToolbarLayout)
        self.gradesTable = QtWidgets.QTableWidget(self.gradesTab)
        self.gradesTable.setObjectName("gradesTable")
        self.gradesTable.setColumnCount(7)
        self.gradesTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.gradesTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.gradesTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.gradesTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.gradesTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.gradesTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.gradesTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.gradesTable.setHorizontalHeaderItem(6, item)
        self.verticalLayout_6.addWidget(self.gradesTable)
        self.tabWidget.addTab(self.gradesTab, "")
        self.messagesTab = QtWidgets.QWidget()
        self.messagesTab.setObjectName("messagesTab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.messagesTab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.messagesSplitter = QtWidgets.QSplitter(self.messagesTab)
        self.messagesSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.messagesSplitter.setObjectName("messagesSplitter")
        self.layoutWidget = QtWidgets.QWidget(self.messagesSplitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.chatsLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.chatsLayout.setContentsMargins(0, 0, 0, 0)
        self.chatsLayout.setObjectName("chatsLayout")
        self.chatsLabel = QtWidgets.QLabel(self.layoutWidget)
        self.chatsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.chatsLabel.setObjectName("chatsLabel")
        self.chatsLayout.addWidget(self.chatsLabel)
        self.chatsList = QtWidgets.QListWidget(self.layoutWidget)
        self.chatsList.setObjectName("chatsList")
        self.chatsLayout.addWidget(self.chatsList)
        self.newChatButton = QtWidgets.QPushButton(self.layoutWidget)
        self.newChatButton.setObjectName("newChatButton")
        self.chatsLayout.addWidget(self.newChatButton)
        self.layoutWidget1 = QtWidgets.QWidget(self.messagesSplitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.messagesLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.messagesLayout.setContentsMargins(0, 0, 0, 0)
        self.messagesLayout.setObjectName("messagesLayout")
        self.messagesLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.messagesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.messagesLabel.setObjectName("messagesLabel")
        self.messagesLayout.addWidget(self.messagesLabel)
        self.messagesList = QtWidgets.QListWidget(self.layoutWidget1)
        self.messagesList.setObjectName("messagesList")
        self.messagesLayout.addWidget(self.messagesList)
        self.messageInputLayout = QtWidgets.QHBoxLayout()
        self.messageInputLayout.setObjectName("messageInputLayout")
        self.messageInput = QtWidgets.QLineEdit(self.layoutWidget1)
        self.messageInput.setObjectName("messageInput")
        self.messageInputLayout.addWidget(self.messageInput)
        self.sendMessageButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.sendMessageButton.setObjectName("sendMessageButton")
        self.messageInputLayout.addWidget(self.sendMessageButton)
        self.messagesLayout.addLayout(self.messageInputLayout)
        self.verticalLayout_7.addWidget(self.messagesSplitter)
        self.tabWidget.addTab(self.messagesTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.statusLayout = QtWidgets.QHBoxLayout()
        self.statusLayout.setObjectName("statusLayout")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLayout.addWidget(self.statusLabel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.statusLayout.addItem(spacerItem2)
        self.versionLabel = QtWidgets.QLabel(self.centralwidget)
        self.versionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.statusLayout.addWidget(self.versionLabel)
        self.verticalLayout.addLayout(self.statusLayout)
        TeacherDashboard.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TeacherDashboard)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCourses = QtWidgets.QMenu(self.menubar)
        self.menuCourses.setObjectName("menuCourses")
        self.menuStudents = QtWidgets.QMenu(self.menubar)
        self.menuStudents.setObjectName("menuStudents")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        TeacherDashboard.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TeacherDashboard)
        self.statusbar.setObjectName("statusbar")
        TeacherDashboard.setStatusBar(self.statusbar)
        self.actionRefresh = QtWidgets.QAction(TeacherDashboard)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionLogout = QtWidgets.QAction(TeacherDashboard)
        self.actionLogout.setObjectName("actionLogout")
        self.actionExit = QtWidgets.QAction(TeacherDashboard)
        self.actionExit.setObjectName("actionExit")
        self.actionViewCourses = QtWidgets.QAction(TeacherDashboard)
        self.actionViewCourses.setObjectName("actionViewCourses")
        self.actionAddLesson = QtWidgets.QAction(TeacherDashboard)
        self.actionAddLesson.setObjectName("actionAddLesson")
        self.actionViewStudents = QtWidgets.QAction(TeacherDashboard)
        self.actionViewStudents.setObjectName("actionViewStudents")
        self.actionTakeAttendance = QtWidgets.QAction(TeacherDashboard)
        self.actionTakeAttendance.setObjectName("actionTakeAttendance")
        self.actionGradeStudents = QtWidgets.QAction(TeacherDashboard)
        self.actionGradeStudents.setObjectName("actionGradeStudents")
        self.actionAbout = QtWidgets.QAction(TeacherDashboard)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(TeacherDashboard)
        self.actionHelp.setObjectName("actionHelp")
        self.actionProfile = QtWidgets.QAction(TeacherDashboard)
        self.actionProfile.setObjectName("actionProfile")
        self.menuFile.addAction(self.actionRefresh)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionLogout)
        self.menuFile.addAction(self.actionExit)
        self.menuCourses.addAction(self.actionViewCourses)
        self.menuCourses.addAction(self.actionAddLesson)
        self.menuStudents.addAction(self.actionViewStudents)
        self.menuStudents.addAction(self.actionTakeAttendance)
        self.menuStudents.addAction(self.actionGradeStudents)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionHelp)
        self.menuEdit.addAction(self.actionProfile)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCourses.menuAction())
        self.menubar.addAction(self.menuStudents.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(TeacherDashboard)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TeacherDashboard)

    def retranslateUi(self, TeacherDashboard):
        _translate = QtCore.QCoreApplication.translate
        TeacherDashboard.setWindowTitle(_translate("TeacherDashboard", "Language School - Teacher Dashboard"))
        self.welcomeLabel.setText(_translate("TeacherDashboard", "Welcome, Teacher"))
        self.logoutButton.setText(_translate("TeacherDashboard", "Logout"))
        item = self.coursesTable.horizontalHeaderItem(0)
        item.setText(_translate("TeacherDashboard", "ID"))
        item = self.coursesTable.horizontalHeaderItem(1)
        item.setText(_translate("TeacherDashboard", "Name"))
        item = self.coursesTable.horizontalHeaderItem(2)
        item.setText(_translate("TeacherDashboard", "Language"))
        item = self.coursesTable.horizontalHeaderItem(3)
        item.setText(_translate("TeacherDashboard", "Level"))
        item = self.coursesTable.horizontalHeaderItem(4)
        item.setText(_translate("TeacherDashboard", "Students"))
        item = self.coursesTable.horizontalHeaderItem(5)
        item.setText(_translate("TeacherDashboard", "Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.coursesTab), _translate("TeacherDashboard", "My Courses"))
        self.courseFilterComboBox.setItemText(0, _translate("TeacherDashboard", "All Courses"))
        self.addLessonButton.setText(_translate("TeacherDashboard", "Add Lesson"))
        item = self.lessonsTable.horizontalHeaderItem(0)
        item.setText(_translate("TeacherDashboard", "ID"))
        item = self.lessonsTable.horizontalHeaderItem(1)
        item.setText(_translate("TeacherDashboard", "Course"))
        item = self.lessonsTable.horizontalHeaderItem(2)
        item.setText(_translate("TeacherDashboard", "Name"))
        item = self.lessonsTable.horizontalHeaderItem(3)
        item.setText(_translate("TeacherDashboard", "Order"))
        item = self.lessonsTable.horizontalHeaderItem(4)
        item.setText(_translate("TeacherDashboard", "Duration"))
        item = self.lessonsTable.horizontalHeaderItem(5)
        item.setText(_translate("TeacherDashboard", "Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lessonsTab), _translate("TeacherDashboard", "Lessons"))
        self.studentCourseFilterComboBox.setItemText(0, _translate("TeacherDashboard", "All Courses"))
        self.studentSearchInput.setPlaceholderText(_translate("TeacherDashboard", "Search students..."))
        item = self.studentsTable.horizontalHeaderItem(0)
        item.setText(_translate("TeacherDashboard", "ID"))
        item = self.studentsTable.horizontalHeaderItem(1)
        item.setText(_translate("TeacherDashboard", "Name"))
        item = self.studentsTable.horizontalHeaderItem(2)
        item.setText(_translate("TeacherDashboard", "Email"))
        item = self.studentsTable.horizontalHeaderItem(3)
        item.setText(_translate("TeacherDashboard", "Course"))
        item = self.studentsTable.horizontalHeaderItem(4)
        item.setText(_translate("TeacherDashboard", "Level"))
        item = self.studentsTable.horizontalHeaderItem(5)
        item.setText(_translate("TeacherDashboard", "Progress"))
        item = self.studentsTable.horizontalHeaderItem(6)
        item.setText(_translate("TeacherDashboard", "Actions"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.studentsTab), _translate("TeacherDashboard", "Students"))
        self.attendanceCourseFilterComboBox.setItemText(0, _translate("TeacherDashboard", "All Courses"))
        self.attendanceDateEdit.setDisplayFormat(_translate("TeacherDashboard", "yyyy-MM-dd"))
        self.saveAttendanceButton.setText(_translate("TeacherDashboard", "Save Attendance"))
        item = self.attendanceTable.horizontalHeaderItem(0)
        item.setText(_translate("TeacherDashboard", "ID"))
        item = self.attendanceTable.horizontalHeaderItem(1)
        item.setText(_translate("TeacherDashboard", "Student"))
        item = self.attendanceTable.horizontalHeaderItem(2)
        item.setText(_translate("TeacherDashboard", "Course"))
        item = self.attendanceTable.horizontalHeaderItem(3)
        item.setText(_translate("TeacherDashboard", "Status"))
        item = self.attendanceTable.horizontalHeaderItem(4)
        item.setText(_translate("TeacherDashboard", "Notes"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.attendanceTab), _translate("TeacherDashboard", "Attendance"))
        self.gradesCourseFilterComboBox.setItemText(0, _translate("TeacherDashboard", "All Courses"))
        self.gradesTypeFilterComboBox.setItemText(0, _translate("TeacherDashboard", "All Types"))
        self.gradesTypeFilterComboBox.setItemText(1, _translate("TeacherDashboard", "Exercises"))
        self.gradesTypeFilterComboBox.setItemText(2, _translate("TeacherDashboard", "Tests"))
        self.saveGradesButton.setText(_translate("TeacherDashboard", "Save Grades"))
        item = self.gradesTable.horizontalHeaderItem(0)
        item.setText(_translate("TeacherDashboard", "ID"))
        item = self.gradesTable.horizontalHeaderItem(1)
        item.setText(_translate("TeacherDashboard", "Student"))
        item = self.gradesTable.horizontalHeaderItem(2)
        item.setText(_translate("TeacherDashboard", "Course"))
        item = self.gradesTable.horizontalHeaderItem(3)
        item.setText(_translate("TeacherDashboard", "Type"))
        item = self.gradesTable.horizontalHeaderItem(4)
        item.setText(_translate("TeacherDashboard", "Name"))
        item = self.gradesTable.horizontalHeaderItem(5)
        item.setText(_translate("TeacherDashboard", "Grade"))
        item = self.gradesTable.horizontalHeaderItem(6)
        item.setText(_translate("TeacherDashboard", "Feedback"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gradesTab), _translate("TeacherDashboard", "Grades"))
        self.chatsLabel.setText(_translate("TeacherDashboard", "Chats"))
        self.newChatButton.setText(_translate("TeacherDashboard", "New Chat"))
        self.messagesLabel.setText(_translate("TeacherDashboard", "Messages"))
        self.messageInput.setPlaceholderText(_translate("TeacherDashboard", "Type a message..."))
        self.sendMessageButton.setText(_translate("TeacherDashboard", "Send"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.messagesTab), _translate("TeacherDashboard", "Messages"))
        self.statusLabel.setText(_translate("TeacherDashboard", "Ready"))
        self.versionLabel.setText(_translate("TeacherDashboard", "Version 1.0.0"))
        self.menuFile.setTitle(_translate("TeacherDashboard", "File"))
        self.menuCourses.setTitle(_translate("TeacherDashboard", "Courses"))
        self.menuStudents.setTitle(_translate("TeacherDashboard", "Students"))
        self.menuHelp.setTitle(_translate("TeacherDashboard", "Help"))
        self.menuEdit.setTitle(_translate("TeacherDashboard", "Edit"))
        self.actionRefresh.setText(_translate("TeacherDashboard", "Refresh"))
        self.actionLogout.setText(_translate("TeacherDashboard", "Logout"))
        self.actionExit.setText(_translate("TeacherDashboard", "Exit"))
        self.actionViewCourses.setText(_translate("TeacherDashboard", "View Courses"))
        self.actionAddLesson.setText(_translate("TeacherDashboard", "Add Lesson"))
        self.actionViewStudents.setText(_translate("TeacherDashboard", "View Students"))
        self.actionTakeAttendance.setText(_translate("TeacherDashboard", "Take Attendance"))
        self.actionGradeStudents.setText(_translate("TeacherDashboard", "Grade Students"))
        self.actionAbout.setText(_translate("TeacherDashboard", "About"))
        self.actionHelp.setText(_translate("TeacherDashboard", "Help"))
        self.actionProfile.setText(_translate("TeacherDashboard", "Profile"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TeacherDashboard = QtWidgets.QMainWindow()
    ui = Ui_TeacherDashboard()
    ui.setupUi(TeacherDashboard)
    TeacherDashboard.show()
    sys.exit(app.exec_())