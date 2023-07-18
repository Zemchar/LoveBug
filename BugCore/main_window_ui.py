# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LoveBug(object):
    def setupUi(self, LoveBug):
        LoveBug.setObjectName("LoveBug")
        LoveBug.resize(409, 409)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoveBug.sizePolicy().hasHeightForWidth())
        LoveBug.setSizePolicy(sizePolicy)
        LoveBug.setMinimumSize(QtCore.QSize(409, 409))
        LoveBug.setMaximumSize(QtCore.QSize(409, 409))
        self.widget = QtWidgets.QWidget(parent=LoveBug)
        self.widget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.widget.setAutoFillBackground(False)
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.widget)
        self.verticalLayoutWidget.setEnabled(True)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-10, 0, 421, 411))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.verticalLayoutWidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setStyleSheet("QTabWidget::tab-bar {\n"
"alignment: centerl\n"
"}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.South)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(30, 30))
        self.tabWidget.setElideMode(QtCore.Qt.TextElideMode.ElideMiddle)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 0, 373, 350))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.PFP = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        self.PFP.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.PFP.setLineWidth(4)
        self.PFP.setMidLineWidth(0)
        self.PFP.setText("")
        self.PFP.setPixmap(QtGui.QPixmap(":/images/images/AfwEDi.jpg"))
        self.PFP.setScaledContents(False)
        self.PFP.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PFP.setWordWrap(False)
        self.PFP.setObjectName("PFP")
        self.verticalLayout_4.addWidget(self.PFP)
        self.Name = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        self.Name.setMaximumSize(QtCore.QSize(16777215, 20))
        self.Name.setStyleSheet("QLabel{font-size:17px}")
        self.Name.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.Name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Name.setObjectName("Name")
        self.verticalLayout_4.addWidget(self.Name)
        self.Mood = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        self.Mood.setMaximumSize(QtCore.QSize(16777215, 20))
        self.Mood.setStyleSheet("QLabel{\n"
"font-size: 13px;\n"
"}")
        self.Mood.setScaledContents(False)
        self.Mood.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Mood.setObjectName("Mood")
        self.verticalLayout_4.addWidget(self.Mood)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.b_kiss = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        self.b_kiss.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/BugCore/images/kiss__49640.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon.addPixmap(QtGui.QPixmap(":/images/BugCore/images/kiss__49640.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.b_kiss.setIcon(icon)
        self.b_kiss.setIconSize(QtCore.QSize(6, 20))
        self.b_kiss.setCheckable(False)
        self.b_kiss.setObjectName("b_kiss")
        self.horizontalLayout_2.addWidget(self.b_kiss)
        self.b_think = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        self.b_think.setObjectName("b_think")
        self.horizontalLayout_2.addWidget(self.b_think)
        self.b_love = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        self.b_love.setObjectName("b_love")
        self.horizontalLayout_2.addWidget(self.b_love)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.verticalLayoutWidget_2)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        icon = QtGui.QIcon.fromTheme("mail-unread")
        self.tabWidget.addTab(self.tab, icon, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.tab_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 400, 341))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.game_img = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.game_img.setStyleSheet("QLabel {text-align: center;}")
        self.game_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.game_img.setObjectName("game_img")
        self.verticalLayout_2.addWidget(self.game_img)
        self.cb_SelectGame = QtWidgets.QComboBox(parent=self.verticalLayoutWidget_3)
        self.cb_SelectGame.setAutoFillBackground(False)
        self.cb_SelectGame.setStyleSheet("QComboBox::drop-down {subcontrol-origin: padding;  subcontrol-position: top right;width: 40px;border: 0px ;}")
        self.cb_SelectGame.setObjectName("cb_SelectGame")
        self.verticalLayout_2.addWidget(self.cb_SelectGame)
        self.b_Randomize = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.b_Randomize.setEnabled(True)
        self.b_Randomize.setObjectName("b_Randomize")
        self.verticalLayout_2.addWidget(self.b_Randomize)
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.label_2.setStyleSheet("QLabel{\n"
"font-size: 20px\n"
"}")
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.t_custom = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget_3)
        self.t_custom.setMaximumSize(QtCore.QSize(16777215, 30))
        self.t_custom.setObjectName("t_custom")
        self.verticalLayout_2.addWidget(self.t_custom)
        self.b_Request = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.b_Request.setObjectName("b_Request")
        self.verticalLayout_2.addWidget(self.b_Request)
        icon = QtGui.QIcon.fromTheme("input-gaming")
        self.tabWidget.addTab(self.tab_2, icon, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget1 = QtWidgets.QTabWidget(parent=self.tab_3)
        self.tabWidget1.setEnabled(True)
        self.tabWidget1.setGeometry(QtCore.QRect(19, 10, 381, 331))
        self.tabWidget1.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget1.setObjectName("tabWidget1")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.tabWidgetPage1)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(30, 70, 320, 141))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_24 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        self.label_24.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_24.setStyleSheet("QLabel {font-size:20px}")
        self.label_24.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_5.addWidget(self.label_24)
        self.t_MoodBox = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget_4)
        self.t_MoodBox.setText("")
        self.t_MoodBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.t_MoodBox.setClearButtonEnabled(True)
        self.t_MoodBox.setObjectName("t_MoodBox")
        self.verticalLayout_5.addWidget(self.t_MoodBox)
        self.b_SubmitButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_4)
        self.b_SubmitButton.setObjectName("b_SubmitButton")
        self.verticalLayout_5.addWidget(self.b_SubmitButton)
        self.tabWidget1.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QtWidgets.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.scrollArea = QtWidgets.QScrollArea(parent=self.tabWidgetPage2)
        self.scrollArea.setGeometry(QtCore.QRect(-10, -10, 391, 310))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 100))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.L_settings = QtWidgets.QWidget()
        self.L_settings.setGeometry(QtCore.QRect(0, -294, 366, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.L_settings.sizePolicy().hasHeightForWidth())
        self.L_settings.setSizePolicy(sizePolicy)
        self.L_settings.setMinimumSize(QtCore.QSize(0, 600))
        self.L_settings.setTabletTracking(True)
        self.L_settings.setObjectName("L_settings")
        self.layoutWidget = QtWidgets.QWidget(parent=self.L_settings)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 10, 341, 503))
        self.layoutWidget.setObjectName("layoutWidget")
        self.settingsForm = QtWidgets.QFormLayout(self.layoutWidget)
        self.settingsForm.setContentsMargins(0, 0, 0, 0)
        self.settingsForm.setObjectName("settingsForm")
        self.label_21 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_21.setEnabled(True)
        self.label_21.setStyleSheet("QLabel{ font-size: 20px}")
        self.label_21.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.settingsForm.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label_21)
        self.label_17 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_17.setEnabled(True)
        self.label_17.setObjectName("label_17")
        self.settingsForm.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_17)
        self.cb_NotifBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.cb_NotifBox.setEnabled(True)
        self.cb_NotifBox.setObjectName("cb_NotifBox")
        self.cb_NotifBox.addItem("")
        self.cb_NotifBox.addItem("")
        self.settingsForm.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_NotifBox)
        self.label_18 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_18.setEnabled(True)
        self.label_18.setObjectName("label_18")
        self.settingsForm.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_18)
        self.t_userName = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.t_userName.setEnabled(True)
        self.t_userName.setClearButtonEnabled(True)
        self.t_userName.setObjectName("t_userName")
        self.settingsForm.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.t_userName)
        self.label_19 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_19.setEnabled(True)
        self.label_19.setObjectName("label_19")
        self.settingsForm.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_19)
        self.t_UserCode = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.t_UserCode.setEnabled(True)
        self.t_UserCode.setReadOnly(True)
        self.t_UserCode.setObjectName("t_UserCode")
        self.settingsForm.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.t_UserCode)
        self.label_20 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_20.setEnabled(True)
        self.label_20.setObjectName("label_20")
        self.settingsForm.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_20)
        self.t_PartnerCode = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.t_PartnerCode.setEnabled(True)
        self.t_PartnerCode.setReadOnly(False)
        self.t_PartnerCode.setClearButtonEnabled(True)
        self.t_PartnerCode.setObjectName("t_PartnerCode")
        self.settingsForm.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.t_PartnerCode)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.settingsForm.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.t_SteamID = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.t_SteamID.setClearButtonEnabled(True)
        self.t_SteamID.setObjectName("t_SteamID")
        self.settingsForm.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.t_SteamID)
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.settingsForm.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.b_pfpSelect = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.b_pfpSelect.setEnabled(True)
        self.b_pfpSelect.setObjectName("b_pfpSelect")
        self.settingsForm.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.b_pfpSelect)
        self.label_22 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_22.setEnabled(True)
        self.label_22.setObjectName("label_22")
        self.settingsForm.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_22)
        self.cb_ThemeBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.cb_ThemeBox.setEnabled(True)
        self.cb_ThemeBox.setObjectName("cb_ThemeBox")
        self.cb_ThemeBox.addItem("")
        self.cb_ThemeBox.addItem("")
        self.settingsForm.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_ThemeBox)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.settingsForm.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.t_AdditionalGames = QtWidgets.QTextEdit(parent=self.layoutWidget)
        self.t_AdditionalGames.setTabletTracking(True)
        self.t_AdditionalGames.setObjectName("t_AdditionalGames")
        self.settingsForm.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.t_AdditionalGames)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.settingsForm.setWidget(9, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.label_23 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_23.setEnabled(True)
        self.label_23.setObjectName("label_23")
        self.settingsForm.setWidget(10, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_23)
        self.cb_funnyModeBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.cb_funnyModeBox.setEnabled(True)
        self.cb_funnyModeBox.setObjectName("cb_funnyModeBox")
        self.cb_funnyModeBox.addItem("")
        self.cb_funnyModeBox.addItem("")
        self.settingsForm.setWidget(10, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cb_funnyModeBox)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.verticalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.t_URL = QtWidgets.QLineEdit(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.t_URL.sizePolicy().hasHeightForWidth())
        self.t_URL.setSizePolicy(sizePolicy)
        self.t_URL.setMinimumSize(QtCore.QSize(200, 0))
        self.t_URL.setMaximumSize(QtCore.QSize(20000, 100))
        self.t_URL.setTabletTracking(True)
        self.t_URL.setClearButtonEnabled(True)
        self.t_URL.setObjectName("t_URL")
        self.verticalLayout_6.addWidget(self.t_URL)
        self.settingsForm.setLayout(9, QtWidgets.QFormLayout.ItemRole.FieldRole, self.verticalLayout_6)
        self.b_saveSettings = QtWidgets.QPushButton(parent=self.L_settings)
        self.b_saveSettings.setGeometry(QtCore.QRect(20, 530, 341, 34))
        self.b_saveSettings.setObjectName("b_saveSettings")
        self.scrollArea.setWidget(self.L_settings)
        self.tabWidget1.addTab(self.tabWidgetPage2, "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/images/467616-200.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.tab_3, icon1, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        LoveBug.setCentralWidget(self.widget)
        self.label_18.setBuddy(self.t_userName)
        self.label_19.setBuddy(self.t_UserCode)
        self.label_20.setBuddy(self.t_PartnerCode)
        self.label_3.setBuddy(self.t_SteamID)
        self.label.setBuddy(self.b_pfpSelect)
        self.label_22.setBuddy(self.cb_ThemeBox)
        self.label_4.setBuddy(self.t_AdditionalGames)
        self.label_5.setBuddy(self.t_URL)
        self.label_23.setBuddy(self.cb_funnyModeBox)

        self.retranslateUi(LoveBug)
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget1.setCurrentIndex(1)
        self.b_SubmitButton.clicked.connect(self.t_MoodBox.clear) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(LoveBug)
        LoveBug.setTabOrder(self.b_kiss, self.b_think)
        LoveBug.setTabOrder(self.b_think, self.b_love)
        LoveBug.setTabOrder(self.b_love, self.textBrowser)
        LoveBug.setTabOrder(self.textBrowser, self.cb_SelectGame)
        LoveBug.setTabOrder(self.cb_SelectGame, self.b_Randomize)
        LoveBug.setTabOrder(self.b_Randomize, self.t_custom)
        LoveBug.setTabOrder(self.t_custom, self.b_Request)
        LoveBug.setTabOrder(self.b_Request, self.t_MoodBox)
        LoveBug.setTabOrder(self.t_MoodBox, self.b_SubmitButton)

    def retranslateUi(self, LoveBug):
        _translate = QtCore.QCoreApplication.translate
        LoveBug.setWindowTitle(_translate("LoveBug", "MainWindow"))
        self.Name.setText(_translate("LoveBug", "Name"))
        self.Mood.setText(_translate("LoveBug", "Mood"))
        self.b_kiss.setText(_translate("LoveBug", "Kiss"))
        self.b_think.setText(_translate("LoveBug", "Think"))
        self.b_love.setText(_translate("LoveBug", "Love"))
        self.textBrowser.setHtml(_translate("LoveBug", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">7</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">8</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">9</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">10</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.game_img.setText(_translate("LoveBug", "No Game Selected"))
        self.cb_SelectGame.setPlaceholderText(_translate("LoveBug", "Select Game"))
        self.b_Randomize.setText(_translate("LoveBug", "Randomize"))
        self.label_2.setText(_translate("LoveBug", "OR"))
        self.t_custom.setPlaceholderText(_translate("LoveBug", "Write in your own game"))
        self.b_Request.setText(_translate("LoveBug", "Play!"))
        self.label_24.setText(_translate("LoveBug", "Mood"))
        self.t_MoodBox.setPlaceholderText(_translate("LoveBug", "How are you feeling right now?"))
        self.b_SubmitButton.setText(_translate("LoveBug", "Submit"))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.tabWidgetPage1), _translate("LoveBug", "Mood"))
        self.label_21.setText(_translate("LoveBug", "General Settings"))
        self.label_17.setText(_translate("LoveBug", "Notifications"))
        self.cb_NotifBox.setItemText(0, _translate("LoveBug", "On"))
        self.cb_NotifBox.setItemText(1, _translate("LoveBug", "Off"))
        self.label_18.setText(_translate("LoveBug", "Your Name"))
        self.label_19.setText(_translate("LoveBug", "Your BugCode"))
        self.label_20.setText(_translate("LoveBug", "Partner\'s BugCode"))
        self.label_3.setText(_translate("LoveBug", "SteamID"))
        self.label.setText(_translate("LoveBug", "Profile Picture"))
        self.b_pfpSelect.setText(_translate("LoveBug", "Select Image"))
        self.label_22.setText(_translate("LoveBug", "Theme"))
        self.cb_ThemeBox.setItemText(0, _translate("LoveBug", "Dinosaur"))
        self.cb_ThemeBox.setItemText(1, _translate("LoveBug", "Cat"))
        self.label_4.setText(_translate("LoveBug", "Additional Games"))
        self.t_AdditionalGames.setPlaceholderText(_translate("LoveBug", "Enter in as many non-steam games as you want. Seperate each game with a comma (,)"))
        self.label_5.setText(_translate("LoveBug", "Remote Server Url"))
        self.label_23.setText(_translate("LoveBug", "skeleton mode"))
        self.cb_funnyModeBox.setItemText(0, _translate("LoveBug", "Off"))
        self.cb_funnyModeBox.setItemText(1, _translate("LoveBug", "On"))
        self.t_URL.setPlaceholderText(_translate("LoveBug", "http://example.com:port/"))
        self.b_saveSettings.setText(_translate("LoveBug", "Save Settings"))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.tabWidgetPage2), _translate("LoveBug", "Settings"))
