# from PyQt5.QtWidgets import QMainWindow, QDialog
#
# class MainWindowUI(QMainWindow):
#     """Base class for main window UI"""
#     def __init__(self):
#         super().__init__()
#
# class PatientDialogUI(QDialog):
#     """Base class for patient dialog UI"""
#     def __init__(self):
#         super().__init__()
#
# class DoctorDialogUI(QDialog):
#     """Base class for doctor dialog UI"""
#     def __init__(self):
#         super().__init__()
#
# class AppointmentDialogUI(QDialog):
#     """Base class for appointment dialog UI"""
#     def __init__(self):
#         super().__init__()

import os
import sys

# Try to import generated UI files
try:
    from .ui_main_window import Ui_MainWindow
    from .ui_patient_form import Ui_PatientDialog
    from .ui_doctor_form import Ui_DoctorDialog
    from .ui_appointment_form import Ui_AppointmentDialog
    UI_FILES_AVAILABLE = True
except ImportError:
    UI_FILES_AVAILABLE = False
    print("UI files not found, using fallback classes")

from PyQt5.QtWidgets import QMainWindow, QDialog

class MainWindowUI(QMainWindow):
    """Main window UI class"""
    def __init__(self):
        super().__init__()
        if UI_FILES_AVAILABLE:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            # Map UI elements to class attributes
            self.btn_patients = self.ui.btn_patients
            self.btn_doctors = self.ui.btn_doctors
            self.btn_appointments = self.ui.btn_appointments
            self.search_input = self.ui.search_input
            self.btn_search = self.ui.btn_search
            self.table = self.ui.table
            self.btn_add = self.ui.btn_add
            self.btn_edit = self.ui.btn_edit
            self.btn_delete = self.ui.btn_delete

class PatientDialogUI(QDialog):
    """Patient dialog UI class"""
    def __init__(self):
        super().__init__()
        if UI_FILES_AVAILABLE:
            self.ui = Ui_PatientDialog()
            self.ui.setupUi(self)
            # Map UI elements to class attributes
            self.lineEdit_firstName = self.ui.lineEdit_firstName
            self.lineEdit_lastName = self.ui.lineEdit_lastName
            self.lineEdit_nationalId = self.ui.lineEdit_nationalId
            self.dateEdit_birthDate = self.ui.dateEdit_birthDate
            self.lineEdit_phone = self.ui.lineEdit_phone
            self.textEdit_address = self.ui.textEdit_address
            self.lineEdit_emergencyContact = self.ui.lineEdit_emergencyContact
            self.comboBox_bloodType = self.ui.comboBox_bloodType
            self.textEdit_allergies = self.ui.textEdit_allergies
            self.buttonBox = self.ui.buttonBox

class DoctorDialogUI(QDialog):
    """Doctor dialog UI class"""
    def __init__(self):
        super().__init__()
        if UI_FILES_AVAILABLE:
            self.ui = Ui_DoctorDialog()
            self.ui.setupUi(self)
            # Map UI elements to class attributes
            self.lineEdit_firstName = self.ui.lineEdit_firstName
            self.lineEdit_lastName = self.ui.lineEdit_lastName
            self.lineEdit_specialty = self.ui.lineEdit_specialty
            self.lineEdit_phone = self.ui.lineEdit_phone
            self.lineEdit_email = self.ui.lineEdit_email
            self.lineEdit_licenseNumber = self.ui.lineEdit_licenseNumber
            self.lineEdit_officeNumber = self.ui.lineEdit_officeNumber
            self.doubleSpinBox_consultationFee = self.ui.doubleSpinBox_consultationFee
            self.buttonBox = self.ui.buttonBox

class AppointmentDialogUI(QDialog):
    """Appointment dialog UI class"""
    def __init__(self):
        super().__init__()
        if UI_FILES_AVAILABLE:
            self.ui = Ui_AppointmentDialog()
            self.ui.setupUi(self)
            # Map UI elements to class attributes
            self.comboBox_patient = self.ui.comboBox_patient
            self.comboBox_doctor = self.ui.comboBox_doctor
            self.dateEdit_appointmentDate = self.ui.dateEdit_appointmentDate
            self.timeEdit_appointmentTime = self.ui.timeEdit_appointmentTime
            self.comboBox_status = self.ui.comboBox_status
            self.textEdit_notes = self.ui.textEdit_notes
            self.buttonBox = self.ui.buttonBox