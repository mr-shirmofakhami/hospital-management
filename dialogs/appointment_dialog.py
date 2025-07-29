from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from database.models import AppointmentModel, PatientModel, DoctorModel


class AppointmentDialog(QDialog):
    def __init__(self, parent=None, appointment_id=None):
        super().__init__(parent)
        self.appointment_id = appointment_id
        self.appointment_model = AppointmentModel()
        self.patient_model = PatientModel()
        self.doctor_model = DoctorModel()
        self.setup_ui()
        self.load_combo_data()

        if appointment_id:
            self.load_appointment_data()

    def setup_ui(self):
        self.setWindowTitle("افزودن نوبت جدید" if not self.appointment_id else "ویرایش نوبت")
        self.setLayoutDirection(Qt.RightToLeft)
        self.resize(500, 450)
        self.setModal(True)

        layout = QFormLayout(self)

        # Create form fields
        self.patient_combo = QComboBox()
        self.patient_combo.setMinimumHeight(35)

        self.doctor_combo = QComboBox()
        self.doctor_combo.setMinimumHeight(35)

        self.appointment_date = QDateEdit()
        self.appointment_date.setDate(QDate.currentDate())
        self.appointment_date.setCalendarPopup(True)
        self.appointment_date.setMinimumHeight(35)

        self.appointment_time = QTimeEdit()
        self.appointment_time.setTime(QTime.currentTime())
        self.appointment_time.setMinimumHeight(35)

        self.status = QComboBox()
        self.status.addItems(["فعال", "انجام شده", "لغو شده", "به تعویق افتاده"])
        self.status.setMinimumHeight(35)

        self.notes = QTextEdit()
        self.notes.setMaximumHeight(80)
        self.notes.setPlaceholderText("یادداشت‌های مربوط به نوبت...")

        # Add to layout with styling
        layout.addRow(self.create_label("بیمار:"), self.patient_combo)
        layout.addRow(self.create_label("پزشک:"), self.doctor_combo)
        layout.addRow(self.create_label("تاریخ نوبت:"), self.appointment_date)
        layout.addRow(self.create_label("ساعت نوبت:"), self.appointment_time)
        layout.addRow(self.create_label("وضعیت:"), self.status)
        layout.addRow(self.create_label("یادداشت:"), self.notes)

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

        buttons.accepted.connect(self.save_appointment)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        # Apply general styling
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QComboBox, QDateEdit, QTimeEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 4px;
                font-size: 12px;
            }
            QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, QTextEdit:focus {
                border-color: #e74c3c;
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

    def load_combo_data(self):
        try:
            # Load patients
            patients = self.patient_model.get_all_patients()
            self.patient_combo.clear()
            self.patient_combo.addItem("انتخاب بیمار", None)
            for patient in patients:
                display_text = f"{patient[1]} {patient[2]} - {patient[3]}"
                self.patient_combo.addItem(display_text, patient[0])

            # Load doctors
            doctors = self.doctor_model.get_all_doctors()
            self.doctor_combo.clear()
            self.doctor_combo.addItem("انتخاب پزشک", None)
            for doctor in doctors:
                display_text = f"دکتر {doctor[1]} {doctor[2]} - {doctor[3]}"
                self.doctor_combo.addItem(display_text, doctor[0])

        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری اطلاعات: {str(e)}")

    def load_appointment_data(self):
        try:
            appointment = self.appointment_model.get_appointment_by_id(self.appointment_id)
            if appointment:
                # Set patient
                patient_index = self.patient_combo.findData(appointment[1])
                if patient_index >= 0:
                    self.patient_combo.setCurrentIndex(patient_index)

                # Set doctor
                doctor_index = self.doctor_combo.findData(appointment[2])
                if doctor_index >= 0:
                    self.doctor_combo.setCurrentIndex(doctor_index)

                # Set date and time
                if appointment[3]:
                    date = QDate.fromString(appointment[3], "yyyy-MM-dd")
                    self.appointment_date.setDate(date)

                if appointment[4]:
                    time = QTime.fromString(appointment[4], "HH:mm")
                    self.appointment_time.setTime(time)

                # Set status
                status_index = self.status.findText(appointment[5])
                if status_index >= 0:
                    self.status.setCurrentIndex(status_index)

                # Set notes
                self.notes.setPlainText(appointment[6] or "")

        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در بارگذاری: {str(e)}")

    def save_appointment(self):
        if not self.validate_input():
            return

        try:
            appointment_data = (
                self.patient_combo.currentData(),
                self.doctor_combo.currentData(),
                self.appointment_date.date().toString("yyyy-MM-dd"),
                self.appointment_time.time().toString("HH:mm"),
                self.status.currentText(),
                self.notes.toPlainText().strip()
            )

            if self.appointment_id:
                self.appointment_model.update_appointment(self.appointment_id, appointment_data)
                QMessageBox.information(self, "موفقیت", "نوبت با موفقیت به‌روزرسانی شد.")
            else:
                self.appointment_model.create_appointment(appointment_data)
                QMessageBox.information(self, "موفقیت", "نوبت جدید با موفقیت ثبت شد.")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در ذخیره اطلاعات: {str(e)}")

    def validate_input(self):
        if self.patient_combo.currentData() is None:
            QMessageBox.warning(self, "خطا", "انتخاب بیمار الزامی است.")
            self.patient_combo.setFocus()
            return False

        if self.doctor_combo.currentData() is None:
            QMessageBox.warning(self, "خطا", "انتخاب پزشک الزامی است.")
            self.doctor_combo.setFocus()
            return False

        if self.appointment_date.date() < QDate.currentDate():
            QMessageBox.warning(self, "خطا", "تاریخ نوبت نمی‌تواند در گذشته باشد.")
            self.appointment_date.setFocus()
            return False

        return True