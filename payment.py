import json
from datetime import datetime

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDesktopWidget
from escpos import printer

from paymentObject import Payment


class ComboBox(QtWidgets.QComboBox):
    def paintEvent(self, event):

        painter = QtWidgets.QStylePainter(self)
        painter.setPen(self.palette().color(QtGui.QPalette.Text))

        # draw the combobox frame, focusrect and selected etc.
        opt = QtWidgets.QStyleOptionComboBox()
        self.initStyleOption(opt)
        painter.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt)

        if self.currentIndex() < 0:
            opt.palette.setBrush(
                QtGui.QPalette.ButtonText,
                opt.palette.brush(QtGui.QPalette.ButtonText).color().lighter(),
            )
            if self.placeholderText():
                opt.currentText = self.placeholderText()

        # draw the icon and text
        painter.drawControl(QtWidgets.QStyle.CE_ComboBoxLabel, opt)


class Ui_Payment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.message_box = QtWidgets.QMessageBox()
        self.type = ''

    def setupUi(self, connection):
        self.setObjectName("Payment")
        self.setFixedSize(1200, 580)
        self.center()
        self.api = connection
        self.layoutWidget = QtWidgets.QWidget(self)
        self.layoutWidget.setGeometry(QtCore.QRect(14, 11, 1170, 542))
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget1 = QtWidgets.QWidget(self)
        self.layoutWidget1.setEnabled(True)
        self.layoutWidget1.setGeometry(QtCore.QRect(950, 550, 231, 27))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.type_label = QtWidgets.QLabel(self.layoutWidget)
        self.type_label.setObjectName("type_label")
        self.gridLayout.addWidget(self.type_label, 1, 0, 1, 1)
        self.month = QtWidgets.QComboBox(self.layoutWidget)
        self.month.setObjectName("month")
        self.gridLayout.addWidget(self.month, 4, 4, 1, 1)
        self.group = ComboBox(self.layoutWidget)
        self.group.setObjectName("group")
        self.group.setPlaceholderText("Guruhni tanlang.")
        self.group.setCurrentIndex(-1)
        self.gridLayout.addWidget(self.group, 5, 4, 1, 1)
        self.comment_label = QtWidgets.QLabel(self.layoutWidget)
        self.comment_label.setObjectName("comment_label")
        self.gridLayout.addWidget(self.comment_label, 8, 0, 1, 1)
        self.direction_label = QtWidgets.QLabel(self.layoutWidget)
        self.direction_label.setObjectName("direction_label")
        self.gridLayout.addWidget(self.direction_label, 5, 0, 1, 1)
        self.month_label = QtWidgets.QLabel(self.layoutWidget)
        self.month_label.setObjectName("month_label")
        self.gridLayout.addWidget(self.month_label, 4, 3, 1, 1)
        self.teacher_label = QtWidgets.QLabel(self.layoutWidget)
        self.teacher_label.setObjectName("teacher_label")
        self.gridLayout.addWidget(self.teacher_label, 7, 0, 1, 1)
        self.naqd = QtWidgets.QRadioButton(self.layoutWidget)
        self.naqd.setObjectName("naqd")
        self.gridLayout.addWidget(self.naqd, 1, 1, 1, 1)
        self.price_label = QtWidgets.QLabel(self.layoutWidget)
        self.price_label.setObjectName("price_label")
        self.gridLayout.addWidget(self.price_label, 4, 0, 1, 1)
        self.balance = QtWidgets.QLabel(self.layoutWidget)
        self.balance.setObjectName("balance")
        self.gridLayout.addWidget(self.balance, 9, 1, 1, 1)
        self.comment = QtWidgets.QPlainTextEdit(self.layoutWidget)
        self.comment.setObjectName("comment")
        self.gridLayout.addWidget(self.comment, 8, 1, 1, 4)
        self.group_label = QtWidgets.QLabel(self.layoutWidget)
        self.group_label.setObjectName("group_label")
        self.gridLayout.addWidget(self.group_label, 5, 3, 1, 1)
        self.date = QtWidgets.QLineEdit(self.layoutWidget)
        self.date.setReadOnly(True)
        self.date.setObjectName("date")
        self.gridLayout.addWidget(self.date, 0, 1, 1, 1)
        self.direction = ComboBox(self.layoutWidget)
        self.direction.setObjectName("direction")
        self.direction.setPlaceholderText("Yo'nalishni tanlang.")
        self.direction.setCurrentIndex(-1)
        self.gridLayout.addWidget(self.direction, 5, 1, 1, 1)
        self.student_label = QtWidgets.QLabel(self.layoutWidget)
        self.student_label.setObjectName("student_label")
        self.gridLayout.addWidget(self.student_label, 6, 0, 1, 1)
        self.balance_label = QtWidgets.QLabel(self.layoutWidget)
        self.balance_label.setObjectName("balance_label")
        self.gridLayout.addWidget(self.balance_label, 9, 0, 1, 1)
        self.date_label = QtWidgets.QLabel(self.layoutWidget)
        self.date_label.setObjectName("date_label")
        self.gridLayout.addWidget(self.date_label, 0, 0, 1, 1)
        self.price = QtWidgets.QLineEdit(self.layoutWidget)
        self.price.setObjectName("price")
        self.price.textChanged.connect(self.on_change_price)
        self.gridLayout.addWidget(self.price, 4, 1, 1, 1)
        self.id_label = QtWidgets.QLabel(self.layoutWidget)
        self.id_label.setObjectName("id_label")
        self.id_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.id_label, 0, 3, 1, 1)
        self.plastik = QtWidgets.QRadioButton(self.layoutWidget)
        self.plastik.setObjectName("plastik")
        self.gridLayout.addWidget(self.plastik, 2, 1, 1, 1)
        self.hisob_raqam = QtWidgets.QRadioButton(self.layoutWidget)
        self.hisob_raqam.setObjectName("hisob_raqam")
        self.gridLayout.addWidget(self.hisob_raqam, 3, 1, 1, 1)
        self.id = QtWidgets.QLineEdit(self.layoutWidget)
        self.id.setObjectName("id")
        self.gridLayout.addWidget(self.id, 0, 4, 1, 1)
        self.student = ComboBox(self.layoutWidget)
        self.student.setObjectName("student")
        self.student.setPlaceholderText("O'quvchini tanlang.")
        self.student.setCurrentIndex(-1)
        self.gridLayout.addWidget(self.student, 6, 1, 1, 4)
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 0, 2, 1, 1)
        self.teacher = QtWidgets.QLineEdit(self.layoutWidget)
        self.teacher.setObjectName("teacher")
        self.gridLayout.addWidget(self.teacher, 7, 1, 1, 4)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.payment_table = QtWidgets.QTableWidget(self.layoutWidget)
        self.payment_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.payment_table.setObjectName("payment_table")
        self.payment_table.setColumnCount(4)
        self.payment_table.setRowCount(1)
        header = self.payment_table.horizontalHeader()
        header.setMinimumSectionSize(140)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        item = QtWidgets.QTableWidgetItem()
        self.payment_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.payment_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.payment_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.payment_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.payment_table.setHorizontalHeaderItem(3, item)
        self.gridLayout_2.addWidget(self.payment_table, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setHorizontalSpacing(20)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.total_price_label = QtWidgets.QLabel(self.layoutWidget)
        self.total_price_label.setObjectName("total_price_label")
        self.gridLayout_3.addWidget(self.total_price_label, 0, 0, 1, 1)
        self.total_price = QtWidgets.QLabel(self.layoutWidget)
        self.total_price.setText("0")
        self.total_price.setObjectName("total_price")
        self.gridLayout_3.addWidget(self.total_price, 0, 1, 1, 1)
        self.gridLayout_3.setColumnMinimumWidth(1, 1)
        self.gridLayout_3.setColumnStretch(1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_2.setRowStretch(0, 5)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.gridLayout_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.print_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.print_btn.setEnabled(True)
        self.print_btn.setAutoFillBackground(False)
        self.print_btn.setStyleSheet("background-color: rgb(64, 77, 191);\n"
                                     "color: rgb(255, 255, 255);")
        self.print_btn.setObjectName("print_btn")
        self.horizontalLayout_2.addWidget(self.print_btn)
        self.save_bnt = QtWidgets.QPushButton(self.layoutWidget1)
        self.save_bnt.setEnabled(True)
        self.save_bnt.setStyleSheet("background-color: rgb(115, 210, 22);")
        self.save_bnt.setIconSize(QtCore.QSize(16, 16))
        self.save_bnt.setObjectName("save_bnt")
        self.horizontalLayout_2.addWidget(self.save_bnt)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Payment", "Payment"))
        self.type_label.setText(_translate("Payment", "To\'lov turi:"))
        self.comment_label.setText(_translate("Payment", "Izohlar:"))
        self.direction_label.setText(_translate("Payment", "Kurs:"))
        self.month_label.setText(_translate("Payment", "Oy:"))
        self.teacher_label.setText(_translate("Payment", "O\'qituvchi:"))
        self.naqd.setText(_translate("Payment", "Naqd"))
        self.plastik.setText(_translate("Payment", "Plastik"))
        self.hisob_raqam.setText(_translate("Payment", "Hisob raqam"))
        self.price_label.setText(_translate("Payment", "Summa:"))
        self.balance.setText(_translate("Payment", "0"))
        self.group_label.setText(_translate("Payment", "Guruh:"))
        self.student_label.setText(_translate("Payment", "O\'quvchi:"))
        self.balance_label.setText(_translate("Payment", "Balans:"))
        self.date_label.setText(_translate("Payment", "Sana:"))
        self.id_label.setText(_translate("Payment", "№"))
        self.checkBox.setText(_translate("Payment", "10 %"))
        item = self.payment_table.verticalHeaderItem(0)
        item.setText(_translate("Payment", "1"))
        item = self.payment_table.horizontalHeaderItem(0)
        item.setText(_translate("Payment", "Kurs"))
        item = self.payment_table.horizontalHeaderItem(1)
        item.setText(_translate("Payment", "Guruh"))
        item = self.payment_table.horizontalHeaderItem(2)
        item.setText(_translate("Payment", "Oy"))
        item = self.payment_table.horizontalHeaderItem(3)
        item.setText(_translate("Payment", "Qarz"))
        self.total_price_label.setText(_translate("Payment", "Umumiy balans:"))
        self.print_btn.setText(_translate("Payment", "Chop qilish"))
        self.save_bnt.setText(_translate("Payment", "Saqlash"))
        self.print_btn.clicked.connect(self.generate_and_print)
        self.save_bnt.clicked.connect(self.add_payment)
        self.naqd.toggled.connect(self.onChecked)
        self.plastik.toggled.connect(self.onChecked)
        self.hisob_raqam.toggled.connect(self.onChecked)
        self.checkBox.toggled.connect(self.onCheckCheckbox)
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.id.setText(self.api.getLastPaymentId())
        self.month.addItems([str(x) for x in range(1, 10)])
        self.set_directions()
        self.direction_id = self.direction.currentData()
        self.direction.currentIndexChanged.connect(self.on_change_direction)
        self.groups_list = self.api.getGroups()
        self.set_groups()
        self.teachers_list = self.api.getTeachers()
        self.group_id = self.group.currentData()
        self.group.currentIndexChanged.connect(self.on_change_group)
        self.set_teacher()
        self.set_students(self.group_id)
        self.student_id = self.student.currentData()
        self.payment_list = self.api.getPaymentsByStudentId(self.student_id)
        self.generate_table()
        self.student.currentIndexChanged.connect(self.on_change_student)

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def on_change_direction(self, index):
        self.direction_id = self.direction.itemData(index)
        self.set_groups()

    def on_change_group(self, index):
        self.group_id = self.group.itemData(index)
        self.set_students(self.group_id)

    def on_change_student(self, index):
        self.student_id = self.student.itemData(index)
        self.payment_list = self.api.getPaymentsByStudentId(self.student_id)
        self.generate_table()

    def on_change_price(self, str):
        self.balance.setText(str)

    def set_teacher(self):
        for g in self.groups_list:
            if g.id == self.group_id:
                for t in self.teachers_list:
                    if t.id == g.teacher_id:
                        self.teacher.setText(t.name)

    def generate_table(self):
        self.payment_table.setRowCount(len(self.payment_list))
        for i, data in enumerate(sorted(self.payment_list, key=lambda x: x.key)):
            self.payment_table.setItem(i, 0, QTableWidgetItem(data.reports[0].direction_name))
            self.payment_table.setItem(i, 1, QTableWidgetItem(data.reports[0].group_name))
            self.payment_table.setItem(i, 2, QTableWidgetItem(str(data.reports[0].payment_month)))
            self.payment_table.setItem(i, 3, QTableWidgetItem(str(self.get_total_debt(data.reports))))

    def set_directions(self):
        for direction in self.api.getDirections():
            self.direction.addItem(direction.name, direction.id)

    def set_groups(self):
        self.group.clear()
        direction_groups = filter(lambda g: g.direction_id == self.direction_id, self.groups_list)
        for group in direction_groups:
            self.group.addItem(group.name, group.id)

    def set_students(self, group_id):
        students = self.api.getStudentByGroupId(group_id)
        self.student.clear()
        for student in students:
            self.student.addItem(student.firstname + " " + student.lastname, student.id)

    def show_time(self):
        time = QDateTime.currentDateTime()
        time_display = time.toString('yyyy.MM.dd hh:mm:ss')
        self.date.setText(time_display)

    def onChecked(self):
        radio_btn = self.sender()
        if radio_btn.isChecked():
            self.type = radio_btn.text()

    def onCheckCheckbox(self):
        check_box = self.sender()
        self.direction.setEnabled(not check_box.isChecked())
        if check_box.isChecked():
            self.group.clear()
            not_active_group = filter(lambda g: g.isActive == False, self.groups_list)
            for group in not_active_group:
                self.group.addItem(group.name, group.id)
        else:
            self.set_groups()

    def check_validation(self):
        if not self.id.text():
            self.message_box.setText("Iltimos chek raqamini kiriting!")
            self.message_box.exec_()
            return False
        elif self.type == '':
            self.message_box.setText("Iltimos to'lov turini kiriting!")
            self.message_box.exec_()
            return False
        elif not self.price.text():
            self.message_box.setText("Iltimos summani kiriting!")
            self.message_box.exec_()
            return False
        elif not self.student_id:
            self.message_box.setText("Iltimos talabani tanlang!")
            self.message_box.exec_()
            return False
        elif not self.month.currentText():
            self.message_box.setText("Iltimos qaysi oy uchun to'lamoqchiligingizni kiriting!")
            self.message_box.exec_()
            return False
        elif not self.group_id:
            self.message_box.setText("Iltimos qaysi oy uchun to'lamoqchiligingizni kiriting!")
            self.message_box.exec_()
            return False
        else:
            return True

    def get_total_debt(self, reports):
        sum = 0
        for report in reports:
            sum += report.debt
        self.total_price.setText(str(int(self.total_price.text()) + sum))
        return sum - reports[0].price_group

    def get_debt(self):
        sum = 0
        for key, reports in self.payment_list:
            if key == self.month.currentText():
                for report in reports:
                    sum += report.debt
                return sum + int(self.price.text()) - reports[0].price_group

        for _ in self.payment_list:
            if sum == 0:
                for group in self.groups_list:
                    if group.id == self.group_id:
                        return int(self.price.text()) - group.price_group

    def send_payment(self, payment):
        data = json.dumps(payment.__dict__)
        result = self.api.addPayment(data)
        self.student.setCurrentIndex(-1)
        self.direction.setCurrentIndex(-1)
        self.group.setCurrentIndex(-1)
        self.month.setCurrentIndex(0)
        self.price.setText('')
        if result.status_code == 200:
            self.id.setText(self.api.getLastPaymentId())
            self.payment_list = self.api.getPaymentsByStudentId(self.student_id)
            self.generate_table()
        self.message_box.setText(result.text)
        self.message_box.exec_()

    def generate_and_print(self):
        if self.check_validation():
            payment = Payment(int(self.id.text()), self.type, self.price.text(), self.get_debt(),
                              int(self.month.currentText()), self.group_id, self.comment.toPlainText(), self.student_id,
                              self.group.currentText(), self.student.currentText())
            self.print_action()
            self.send_payment(payment)

    def add_payment(self):
        if self.check_validation():
            payment = Payment(int(self.id.text()), self.type, self.price.text(), self.get_debt(),
                              int(self.month.currentText()), self.group_id, self.comment.toPlainText(), self.student_id,
                              self.group.currentText(), self.student.currentText())
            self.send_payment(payment)

    def print_action(self):
        try:
            Xprinter = printer.Usb(0x1fc9, 0x2016)
            # Xprinter = printer.Network("192.162.1.101", 9100)
            for copies in range(0, 2):
                Xprinter.set(bold=True, align='center')
                Xprinter.image("img/data_logo_250.png")
                Xprinter.text("\"DATA UNION\" MCHJ")
                Xprinter.set(align='center')
                Xprinter.text(" ga qarashli\n")
                Xprinter.set(bold=True, align='center')
                Xprinter.text("\"DATA\"")
                Xprinter.set(align='center')
                Xprinter.textln(f" o'quv markazi\n Kirim order No: {self.id.text()}")
                Xprinter.ln()
                Xprinter.set(align='left', font='a')
                Xprinter.control("HT", tab_size=22)
                Xprinter.text("   To'lovchi:\t")
                Xprinter.textln(self.student.currentText())

                Xprinter.text("   To'lov summasi:\t")
                Xprinter.textln(self.price.text())

                Xprinter.text("   To'lov turi:\t")
                Xprinter.textln(self.type)

                Xprinter.text("   Sana:\t")
                date_time = datetime.now()
                Xprinter.textln(date_time.strftime("%d.%m.%Y %H:%M:%S"))

                Xprinter.text("   Guruh:\t")
                Xprinter.textln(self.group.currentText())

                Xprinter.text("   Kurs oyi uchun:\t")
                Xprinter.textln(self.month.currentText())

                Xprinter.text("   Qarz qoldig'i:\t")
                Xprinter.textln(self.get_debt())
                Xprinter.ln()

                Xprinter.set(align='center', font='b')
                if copies == 1:
                    Xprinter.textln('@data_learning_centre\n')
                    Xprinter.set(align='left', bold=True)
                    Xprinter.text('   Imzo:     _______________________________')
                else:
                    Xprinter.text('@data_learning_centre\n'
                                  '+99899 757 88 86 \n'
                                  '+99899 758 88 86 \n'
                                  '+99899 759 88 86')
                Xprinter.cut()
        except Exception as ex:
            self.message_box.setText(f"Xatolik yuz berdi: {ex}")
            self.message_box.exec_()
