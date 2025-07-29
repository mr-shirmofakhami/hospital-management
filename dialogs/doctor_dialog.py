from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from database.models import DoctorModel
import sqlite3


class DoctorDialog(QDialog):
    def __init__(self, parent=None, doctor_id=None):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.doctor_model = DoctorModel()
        self.setup_ui()

        if doctor_id:
            self.load_doctor_data()

    def setup_ui(self):
        self.setWindowTitle("افزودن پزشک جدید" if not self.doctor_id else "ویرایش اطلاعات پزشک")
        self.setLayoutDirection(Qt.RightToLeft)
        self.resize(500, 500)
        self.setModal(True)

        layout = QFormLayout(self)

        # Create form fields
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("نام پزشک را وارد کنید")

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("نام خانوادگی پزشک را وارد کنید")

        self.specialty = QLineEdit()
        self.specialty.setPlaceholderText("تخصص پزشک (مثل: قلب، مغز و اعصاب)")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("شماره تلفن")

        self.email = QLineEdit()
        self.email.setPlaceholderText("آدرس ایمیل")

        self.license_number = QLineEdit()
        self.license_number.setPlaceholderText("شماره نظام پزشکی")

        self.office_number = QLineEdit()
        self.office_number.setPlaceholderText("شماره اتاق یا مطب")

        self.consultation_fee = QDoubleSpinBox()
        self.consultation_fee.setRange(0, 10000000)
        self.consultation_fee.setSuffix(" تومان")
        self.consultation_fee.setValue(0)

        # Add to layout with styling
        layout.addRow(self.create_label("نام:"), self.first_name)
        layout.addRow(self.create_label("نام خانوادگی:"), self.last_name)
        layout.addRow(self.create_label("تخصص:"), self.specialty)
        layout.addRow(self.create_label("تلفن:"), self.phone)
        layout.addRow(self.create_label("ایمیل:"), self.email)
        layout.addRow(self.create_label("شماره نظام پزشکی:"), self.license_number)
        layout.addRow(self.create_label("شماره اتاق:"), self.office_number)
        layout.addRow(self.create_label("هزینه ویزیت:"), self.consultation_fee)

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

        buttons.accepted.connect(self.save_doctor)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        # Apply general styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit, QDoubleSpinBox {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus, QDoubleSpinBox:focus {
                border-color: #2ecc71;
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

    def load_doctor_data(self):
        try:
            doctor = self.doctor_model.get_doctor_by_id(self.doctor_id)
            if doctor:
                self.first_name.setText(doctor[1] or "")
                self.last_name.setText(doctor[2] or "")
                self.specialty.setText(doctor[3] or "")
                self.phone.setText(doctor[4] or "")
                self.email.setText(doctor[5] or "")
                self.license_number.setText(doctor[6] or "")
                self.office_number.setText(doctor[7] or "")
                self.consultation_fee.setValue(doctor[8] or 0)
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری: {str(e)}")

    def save_doctor(self):
        if not self.validate_input():
            return

        try:
            doctor_data = (
                self.first_name.text().strip(),
                self.last_name.text().strip(),
                self.specialty.text().strip(),
                self.phone.text().strip(),
                self.email.text().strip(),
                self.license_number.text().strip(),
                self.office_number.text().strip(),
                self.consultation_fee.value()
            )

            if self.doctor_id:
                self.doctor_model.update_doctor(self.doctor_id, doctor_data)
                QMessageBox.information(self, "موفقیت", "اطلاعات پزشک با موفقیت به‌روزرسانی شد.")
            else:
                self.doctor_model.create_doctor(doctor_data)
                QMessageBox.information(self, "موفقیت", "پزشک جدید با موفقیت ثبت شد.")

            self.accept()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "خطا", "شماره نظام پزشکی تکراری است.")
        except Exception as e:
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

        if not self.specialty.text().strip():
            QMessageBox.warning(self, "خطا", "تخصص الزامی است.")
            self.specialty.setFocus()
            return False

        return True