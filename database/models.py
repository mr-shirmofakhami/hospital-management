import sqlite3
from .connection import db


class PatientModel:
    def __init__(self):
        pass

    def get_all_patients(self):
        """Get all patients"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM patients ORDER BY id DESC")
            return cursor.fetchall()
        finally:
            conn.close()

    def get_patient_by_id(self, patient_id):
        """Get patient by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def create_patient(self, patient_data):
        """Create new patient"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO patients (first_name, last_name, national_id, birth_date, 
                                    phone, address, emergency_contact, blood_type, allergies)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', patient_data)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_patient(self, patient_id, patient_data):
        """Update patient - FIXED: Removed updated_at reference"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE patients SET 
                    first_name=?, last_name=?, national_id=?, birth_date=?,
                    phone=?, address=?, emergency_contact=?, blood_type=?, allergies=?
                WHERE id=?
            ''', patient_data + (patient_id,))
            conn.commit()
            print(f"Patient {patient_id} updated successfully")
        except Exception as e:
            print(f"Error updating patient: {e}")
            raise
        finally:
            conn.close()

    def delete_patient(self, patient_id):
        """Delete patient"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
            conn.commit()
        finally:
            conn.close()

    def search_patients(self, search_term):
        """Search patients"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT * FROM patients 
                WHERE first_name LIKE ? OR last_name LIKE ? OR national_id LIKE ?
                ORDER BY id DESC
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            return cursor.fetchall()
        finally:
            conn.close()


class DoctorModel:
    def __init__(self):
        pass

    def get_all_doctors(self):
        """Get all doctors"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM doctors ORDER BY id DESC")
            return cursor.fetchall()
        finally:
            conn.close()

    def get_doctor_by_id(self, doctor_id):
        """Get doctor by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def create_doctor(self, doctor_data):
        """Create new doctor"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO doctors (first_name, last_name, specialty, phone, 
                                   email, license_number, office_number, consultation_fee)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', doctor_data)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_doctor(self, doctor_id, doctor_data):
        """Update doctor - FIXED: Removed updated_at reference"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE doctors SET 
                    first_name=?, last_name=?, specialty=?, phone=?,
                    email=?, license_number=?, office_number=?, consultation_fee=?
                WHERE id=?
            ''', doctor_data + (doctor_id,))
            conn.commit()
            print(f"Doctor {doctor_id} updated successfully")
        except Exception as e:
            print(f"Error updating doctor: {e}")
            raise
        finally:
            conn.close()

    def delete_doctor(self, doctor_id):
        """Delete doctor"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            conn.commit()
        finally:
            conn.close()


class AppointmentModel:
    def __init__(self):
        pass

    def get_all_appointments(self):
        """Get all appointments with patient and doctor names"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT a.id, 
                       p.first_name || ' ' || p.last_name as patient_name,
                       d.first_name || ' ' || d.last_name as doctor_name,
                       a.appointment_date, a.appointment_time, a.status, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            ''')
            return cursor.fetchall()
        finally:
            conn.close()

    def get_appointment_by_id(self, appointment_id):
        """Get appointment by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def create_appointment(self, appointment_data):
        """Create new appointment"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, 
                                        appointment_time, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', appointment_data)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def update_appointment(self, appointment_id, appointment_data):
        """Update appointment - FIXED: Removed updated_at reference"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE appointments SET 
                    patient_id=?, doctor_id=?, appointment_date=?, 
                    appointment_time=?, status=?, notes=?
                WHERE id=?
            ''', appointment_data + (appointment_id,))
            conn.commit()
            print(f"Appointment {appointment_id} updated successfully")
        except Exception as e:
            print(f"Error updating appointment: {e}")
            raise
        finally:
            conn.close()

    def delete_appointment(self, appointment_id):
        """Delete appointment"""
        conn = db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            conn.commit()
        finally:
            conn.close()