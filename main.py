import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Import the generated UI class
try:
    from ui_main_window import Ui_MainWindow

    UI_FILE_AVAILABLE = True
except ImportError:
    UI_FILE_AVAILABLE = False
    print("UI file not found, using programmatic UI")

from database.models import PatientModel, DoctorModel, AppointmentModel
from dialogs import PatientDialog, DoctorDialog, AppointmentDialog


class HospitalManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.patient_model = PatientModel()
        self.doctor_model = DoctorModel()
        self.appointment_model = AppointmentModel()

        self.current_view = "patients"

        # Load UI from file or create programmatically
        if UI_FILE_AVAILABLE:
            self.load_ui_from_file()
        else:
            self.setup_ui_programmatically()

        self.load_styles()
        self.connect_signals()
        self.show_patients()

    def load_ui_from_file(self):
        """Load UI from generated UI file"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Map UI elements to class attributes for easier access
        self.btn_patients = self.ui.btn_patients
        self.btn_doctors = self.ui.btn_doctors
        self.btn_appointments = self.ui.btn_appointments
        self.search_input = self.ui.search_input
        self.btn_search = self.ui.btn_search
        self.table = self.ui.table
        self.btn_add = self.ui.btn_add
        self.btn_edit = self.ui.btn_edit
        self.btn_delete = self.ui.btn_delete

        print("UI loaded from file successfully")

    # def setup_ui_programmatically(self):
    #     """Fallback: Create UI programmatically"""
    #     self.setWindowTitle("سیستم مدیریت بیمارستان")
    #     self.setLayoutDirection(Qt.RightToLeft)
    #     self.setMinimumSize(1200, 800)
    #
    #     central_widget = QWidget()
    #     self.setCentralWidget(central_widget)
    #     layout = QVBoxLayout(central_widget)
    #
    #     # Title
    #     title = QLabel("سیستم مدیریت بیمارستان")
    #     title.setAlignment(Qt.AlignCenter)
    #     title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 20px;")
    #     layout.addWidget(title)
    #
    #     # Main navigation buttons
    #     nav_layout = QHBoxLayout()
    #     self.btn_patients = QPushButton("مدیریت بیماران")
    #     self.btn_doctors = QPushButton("مدیریت پزشکان")
    #     self.btn_appointments = QPushButton("مدیریت نوبت‌ها")
    #
    #     self.btn_patients.setStyleSheet(
    #         "QPushButton { background-color: #3498db; color: white; padding: 15px; font-size: 14px; border-radius: 5px; }")
    #     self.btn_doctors.setStyleSheet(
    #         "QPushButton { background-color: #2ecc71; color: white; padding: 15px; font-size: 14px; border-radius: 5px; }")
    #     self.btn_appointments.setStyleSheet(
    #         "QPushButton { background-color: #e74c3c; color: white; padding: 15px; font-size: 14px; border-radius: 5px; }")
    #
    #     nav_layout.addWidget(self.btn_patients)
    #     nav_layout.addWidget(self.btn_doctors)
    #     nav_layout.addWidget(self.btn_appointments)
    #     layout.addLayout(nav_layout)
    #
    #     # Search section
    #     search_layout = QHBoxLayout()
    #     self.search_input = QLineEdit()
    #     self.search_input.setPlaceholderText("جستجو...")
    #     self.btn_search = QPushButton("جستجو")
    #     self.btn_search.setStyleSheet("QPushButton { background-color: #95a5a6; color: white; padding: 8px; }")
    #
    #     search_layout.addWidget(self.search_input)
    #     search_layout.addWidget(self.btn_search)
    #     layout.addLayout(search_layout)
    #
    #     # Table
    #     self.table = QTableWidget()
    #     self.table.setAlternatingRowColors(True)
    #     self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
    #     self.table.horizontalHeader().setStretchLastSection(True)
    #     layout.addWidget(self.table)
    #
    #     # Operation buttons
    #     op_layout = QHBoxLayout()
    #     self.btn_add = QPushButton("افزودن")
    #     self.btn_edit = QPushButton("ویرایش")
    #     self.btn_delete = QPushButton("حذف")
    #
    #     self.btn_add.setStyleSheet(
    #         "QPushButton { background-color: #27ae60; color: white; padding: 10px; font-size: 12px; border-radius: 3px; }")
    #     self.btn_edit.setStyleSheet(
    #         "QPushButton { background-color: #f39c12; color: white; padding: 10px; font-size: 12px; border-radius: 3px; }")
    #     self.btn_delete.setStyleSheet(
    #         "QPushButton { background-color: #e74c3c; color: white; padding: 10px; font-size: 12px; border-radius: 3px; }")
    #
    #     op_layout.addWidget(self.btn_add)
    #     op_layout.addWidget(self.btn_edit)
    #     op_layout.addWidget(self.btn_delete)
    #     layout.addLayout(op_layout)
    #
    #     print("UI created programmatically")

    def connect_signals(self):
        """Connect UI signals to slots"""
        self.btn_patients.clicked.connect(self.show_patients)
        self.btn_doctors.clicked.connect(self.show_doctors)
        self.btn_appointments.clicked.connect(self.show_appointments)

        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)

        self.btn_search.clicked.connect(self.search_records)
        self.search_input.returnPressed.connect(self.search_records)

        self.table.doubleClicked.connect(self.edit_record)

    def load_styles(self):
        """Load stylesheet"""
        try:
            style_path = os.path.join("resources", "styles", "style.qss")
            if os.path.exists(style_path):
                with open(style_path, 'r', encoding='utf-8') as file:
                    additional_styles = file.read()
                    current_style = self.styleSheet()
                    self.setStyleSheet(current_style + "\n" + additional_styles)
        except Exception as e:
            print(f"Could not load stylesheet: {e}")

    def show_patients(self):
        self.current_view = "patients"
        self.btn_add.setText("افزودن بیمار")
        self.btn_edit.setText("ویرایش بیمار")
        self.btn_delete.setText("حذف بیمار")
        self.search_input.setPlaceholderText("جستجو در بیماران...")
        self.load_patients_data()

    def show_doctors(self):
        self.current_view = "doctors"
        self.btn_add.setText("افزودن پزشک")
        self.btn_edit.setText("ویرایش پزشک")
        self.btn_delete.setText("حذف پزشک")
        self.search_input.setPlaceholderText("جستجو در پزشکان...")
        self.load_doctors_data()

    def show_appointments(self):
        self.current_view = "appointments"
        self.btn_add.setText("افزودن نوبت")
        self.btn_edit.setText("ویرایش نوبت")
        self.btn_delete.setText("حذف نوبت")
        self.search_input.setPlaceholderText("جستجو در نوبت‌ها...")
        self.load_appointments_data()

    def load_patients_data(self):
        try:
            data = self.patient_model.get_all_patients()
            headers = ["شناسه", "نام", "نام خانوادگی", "کد ملی", "تاریخ تولد", "تلفن", "آدرس", "تماس اضطراری",
                       "گروه خون", "آلرژی‌ها"]
            self.setup_table(data, headers)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری بیماران: {str(e)}")

    def load_doctors_data(self):
        try:
            data = self.doctor_model.get_all_doctors()
            headers = ["شناسه", "نام", "نام خانوادگی", "تخصص", "تلفن", "ایمیل", "شماره نظام پزشکی", "شماره اتاق",
                       "هزینه ویزیت"]
            self.setup_table(data, headers)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری پزشکان: {str(e)}")

    def load_appointments_data(self):
        try:
            data = self.appointment_model.get_all_appointments()
            headers = ["شناسه", "نام بیمار", "نام پزشک", "تاریخ", "ساعت", "وضعیت", "یادداشت"]
            self.setup_table(data, headers)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری نوبت‌ها: {str(e)}")

    def setup_table(self, data, headers):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for row, record in enumerate(data):
            for col, value in enumerate(record):
                item = QTableWidgetItem(str(value) if value is not None else "")
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()

    def add_record(self):
        try:
            if self.current_view == "patients":
                dialog = PatientDialog(self)
                if dialog.exec_() == QDialog.Accepted:
                    self.load_patients_data()
            elif self.current_view == "doctors":
                dialog = DoctorDialog(self)
                if dialog.exec_() == QDialog.Accepted:
                    self.load_doctors_data()
            elif self.current_view == "appointments":
                dialog = AppointmentDialog(self)
                if dialog.exec_() == QDialog.Accepted:
                    self.load_appointments_data()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن فرم: {str(e)}")

    def edit_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "هشدار", "لطفاً یک رکورد را انتخاب کنید.")
            return

        try:
            record_id = self.table.item(current_row, 0).text()

            if self.current_view == "patients":
                dialog = PatientDialog(self, record_id)
                if dialog.exec_() == QDialog.Accepted:
                    self.load_patients_data()
            elif self.current_view == "doctors":
                dialog = DoctorDialog(self, record_id)
                if dialog.exec_() == QDialog.Accepted:
                    self.load_doctors_data()
            elif self.current_view == "appointments":
                dialog = AppointmentDialog(self, record_id)
                if dialog.exec_() == QDialog.Accepted:
                    self.load_appointments_data()
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ویرایش: {str(e)}")

    def delete_record(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "هشدار", "لطفاً یک رکورد را انتخاب کنید.")
            return

        reply = QMessageBox.question(self, "تأیید حذف", "آیا مطمئن هستید که می‌خواهید این رکورد را حذف کنید؟",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                record_id = self.table.item(current_row, 0).text()

                if self.current_view == "patients":
                    self.patient_model.delete_patient(record_id)
                    self.load_patients_data()
                    QMessageBox.information(self, "موفقیت", "بیمار با موفقیت حذف شد.")
                elif self.current_view == "doctors":
                    self.doctor_model.delete_doctor(record_id)
                    self.load_doctors_data()
                    QMessageBox.information(self, "موفقیت", "پزشک با موفقیت حذف شد.")
                elif self.current_view == "appointments":
                    self.appointment_model.delete_appointment(record_id)
                    self.load_appointments_data()
                    QMessageBox.information(self, "موفقیت", "نوبت با موفقیت حذف شد.")
            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف: {str(e)}")

    def search_records(self):
        search_term = self.search_input.text().strip()

        if not search_term:
            if self.current_view == "patients":
                self.load_patients_data()
            elif self.current_view == "doctors":
                self.load_doctors_data()
            elif self.current_view == "appointments":
                self.load_appointments_data()
            return

        try:
            if self.current_view == "patients":
                data = self.patient_model.search_patients(search_term)
                headers = ["شناسه", "نام", "نام خانوادگی", "کد ملی", "تاریخ تولد", "تلفن", "آدرس", "تماس اضطراری",
                           "گروه خون", "آلرژی‌ها"]
                self.setup_table(data, headers)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در جستجو: {str(e)}")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "خروج از برنامه", "آیا مطمئن هستید که می‌خواهید از برنامه خارج شوید؟",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("سیستم مدیریت بیمارستان")
    app.setApplicationVersion("1.0")

    # Set Persian font
    font = QFont("Tahoma", 10)
    app.setFont(font)

    # Set RTL layout direction
    app.setLayoutDirection(Qt.RightToLeft)

    # Create and show main window
    window = HospitalManagementSystem()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()