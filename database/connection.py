import sqlite3
import os


class DatabaseConnection:
    def __init__(self, db_path="hospital.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # Create patients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    national_id TEXT UNIQUE NOT NULL,
                    birth_date DATE,
                    phone TEXT,
                    address TEXT,
                    emergency_contact TEXT,
                    blood_type TEXT,
                    allergies TEXT
                )
            ''')

            # Create doctors table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    specialty TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    license_number TEXT UNIQUE,
                    office_number TEXT,
                    consultation_fee REAL DEFAULT 0
                )
            ''')

            # Create appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    doctor_id INTEGER NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status TEXT DEFAULT 'فعال',
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors (id)
                )
            ''')

            conn.commit()
            print("Database initialized successfully")

        except Exception as e:
            print(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()


# Global database instance
db = DatabaseConnection()