from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from database.models import PatientModel
import sqlite3


class PatientDialog(QDialog):
    def __init__(self, parent=None, patient_id=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.patient_model = PatientModel()
        self.setup_ui()

        if patient_id:
            self.load_patient_data()

    def setup_ui(self):
        self.setWindowTitle("افزودن بیمار جدید" if not self.patient_id else "ویرایش اطلاعات بیمار")
        self.setLayoutDirection(Qt.RightToLeft)
        self.resize(500, 600)
        self.setModal(True)

        layout = QFormLayout(self)

        # Create form fields
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("نام بیمار را وارد کنید")

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("نام خانوادگی بیمار را وارد کنید")

        self.national_id = QLineEdit()
        self.national_id.setPlaceholderText("کد ملی 10 رقمی")
        self.national_id.setMaxLength(10)

        self.birth_date = QDateEdit()
        self.birth_date.setDate(QDate.currentDate().addYears(-30))
        self.birth_date.setCalendarPopup(True)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("شماره تلفن")

        self.address = QTextEdit()
        self.address.setMaximumHeight(80)
        self.address.setPlaceholderText("آدرس کامل")

        self.emergency_contact = QLineEdit()
        self.emergency_contact.setPlaceholderText("شماره تماس اضطراری")

        self.blood_type = QComboBox()
        self.blood_type.addItems(["انتخاب کنید", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

        self.allergies = QTextEdit()
        self.allergies.setMaximumHeight(80)
        self.allergies.setPlaceholderText("آلرژی‌های بیمار (در صورت وجود)")

        # Add to layout with styling
        layout.addRow(self.create_label("نام:"), self.first_name)
        layout.addRow(self.create_label("نام خانوادگی:"), self.last_name)
        layout.addRow(self.create_label("کد ملی:"), self.national_id)
        layout.addRow(self.create_label("تاریخ تولد:"), self.birth_date)
        layout.addRow(self.create_label("تلفن:"), self.phone)
        layout.addRow(self.create_label("آدرس:"), self.address)
        layout.addRow(self.create_label("تماس اضطراری:"), self.emergency_contact)
        layout.addRow(self.create_label("گروه خون:"), self.blood_type)
        layout.addRow(self.create_label("آلرژی‌ها:"), self.allergies)

        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("ذخیره")
        buttons.button(QDialogButtonBox.Cancel).setText("انصراف")

        # Style buttons
        buttons.button(QDialogButtonBox.Ok).setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)

        buttons.button(QDialogButtonBox.Cancel).setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        buttons.accepted.connect(self.save_patient)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        # Apply general styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #3498db;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
            }
        """)

    def create_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        return label

    def load_patient_data(self):
        try:
            patient = self.patient_model.get_patient_by_id(self.patient_id)
            if patient:
                self.first_name.setText(patient[1] or "")
                self.last_name.setText(patient[2] or "")
                self.national_id.setText(patient[3] or "")
                if patient[4]:
                    date = QDate.fromString(patient[4], "yyyy-MM-dd")
                    self.birth_date.setDate(date)
                self.phone.setText(patient[5] or "")
                self.address.setPlainText(patient[6] or "")
                self.emergency_contact.setText(patient[7] or "")
                if patient[8]:
                    index = self.blood_type.findText(patient[8])
                    if index >= 0:
                        self.blood_type.setCurrentIndex(index)
                self.allergies.setPlainText(patient[9] or "")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری: {str(e)}")

    def save_patient(self):
        if not self.validate_input():
            return

        try:
            patient_data = (
                self.first_name.text().strip(),
                self.last_name.text().strip(),
                self.national_id.text().strip(),
                self.birth_date.date().toString("yyyy-MM-dd"),
                self.phone.text().strip(),
                self.address.toPlainText().strip(),
                self.emergency_contact.text().strip(),
                self.blood_type.currentText() if self.blood_type.currentText() != "انتخاب کنید" else "",
                self.allergies.toPlainText().strip()
            )

            print(f"Patient data: {patient_data}")  # DEBUG
            print(f"Patient ID: {self.patient_id}")  # DEBUG

            if self.patient_id:
                print("Attempting to update patient...")  # DEBUG
                self.patient_model.update_patient(self.patient_id, patient_data)
                QMessageBox.information(self, "موفقیت", "اطلاعات بیمار با موفقیت به‌روزرسانی شد.")
            else:
                print("Attempting to create patient...")  # DEBUG
                self.patient_model.create_patient(patient_data)
                QMessageBox.information(self, "موفقیت", "بیمار جدید با موفقیت ثبت شد.")

            self.accept()

        except sqlite3.IntegrityError as e:
            print(f"Integrity Error: {e}")  # DEBUG
            QMessageBox.warning(self, "خطا", "کد ملی تکراری است. لطفاً کد ملی دیگری وارد کنید.")
        except Exception as e:
            print(f"General Error: {e}")  # DEBUG
            import traceback
            traceback.print_exc()  # DEBUG
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره اطلاعات: {str(e)}")

    def validate_input(self):
        if not self.first_name.text().strip():
            QMessageBox.warning(self, "خطا", "نام الزامی است.")
            self.first_name.setFocus()
            return False

        if not self.last_name.text().strip():
            QMessageBox.warning(self, "خطا", "نام خانوادگی الزامی است.")
            self.last_name.setFocus()
            return False

        if not self.national_id.text().strip():
            QMessageBox.warning(self, "خطا", "کد ملی الزامی است.")
            self.national_id.setFocus()
            return False

        national_id = self.national_id.text().strip()
        if len(national_id) != 10 or not national_id.isdigit():
            QMessageBox.warning(self, "خطا", "کد ملی باید 10 رقم باشد.")
            self.national_id.setFocus()
            return False

        return True