import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from config import DatabaseConfig

class HospitalManagementSystem:
    def __init__(self):
        self.db_config = DatabaseConfig()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        connection = self.db_config.get_connection()
        cursor = None
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    # Patient Management
    def add_patient(self, first_name, last_name, date_of_birth, gender, phone, email, address, blood_group):
        """Add a new patient"""
        query = """
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, blood_group)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, date_of_birth, gender, phone, email, address, blood_group)
        return self.execute_query(query, params)
    
    def get_all_patients(self):
        """Get all patients"""
        query = "SELECT * FROM patients ORDER BY patient_id DESC"
        return self.execute_query(query)
    
    def search_patient(self, search_term):
        """Search patients by name or phone"""
        query = """
            SELECT * FROM patients 
            WHERE first_name LIKE %s OR last_name LIKE %s OR phone LIKE %s
        """
        search_pattern = f"%{search_term}%"
        params = (search_pattern, search_pattern, search_pattern)
        return self.execute_query(query, params)
    
    # Doctor Management
    def add_doctor(self, first_name, last_name, specialization, dept_id, phone, email, salary, hire_date):
        """Add a new doctor"""
        query = """
            INSERT INTO doctors (first_name, last_name, specialization, dept_id, phone, email, salary, hire_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (first_name, last_name, specialization, dept_id, phone, email, salary, hire_date)
        return self.execute_query(query, params)
    
    def get_all_doctors(self):
        """Get all doctors with department info"""
        query = """
            SELECT d.*, dept.dept_name 
            FROM doctors d
            JOIN departments dept ON d.dept_id = dept.dept_id
        """
        return self.execute_query(query)
    
    def get_doctors_by_department(self, dept_id):
        """Get doctors by department"""
        query = "SELECT * FROM doctors WHERE dept_id = %s"
        return self.execute_query(query, (dept_id,))
    
    # Appointment Management
    def schedule_appointment(self, patient_id, doctor_id, appointment_date, appointment_time, symptoms):
        """Schedule a new appointment"""
        query = """
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, symptoms, status)
            VALUES (%s, %s, %s, %s, %s, 'Scheduled')
        """
        params = (patient_id, doctor_id, appointment_date, appointment_time, symptoms)
        return self.execute_query(query, params)
    
    def get_appointments_by_date(self, appointment_date):
        """Get appointments for a specific date"""
        query = """
            SELECT a.*, p.first_name as patient_fname, p.last_name as patient_lname,
                   d.first_name as doctor_fname, d.last_name as doctor_lname
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_date = %s
            ORDER BY a.appointment_time
        """
        return self.execute_query(query, (appointment_date,))
    
    def update_appointment_status(self, appointment_id, status, diagnosis=None):
        """Update appointment status and diagnosis"""
        if diagnosis:
            query = "UPDATE appointments SET status = %s, diagnosis = %s WHERE appointment_id = %s"
            params = (status, diagnosis, appointment_id)
        else:
            query = "UPDATE appointments SET status = %s WHERE appointment_id = %s"
            params = (status, appointment_id)
        return self.execute_query(query, params)
    
    # Billing Management
    def create_bill(self, patient_id, appointment_id, total_amount):
        """Create a new bill"""
        query = """
            INSERT INTO billing (patient_id, appointment_id, total_amount, payment_status)
            VALUES (%s, %s, %s, 'Pending')
        """
        params = (patient_id, appointment_id, total_amount)
        return self.execute_query(query, params)
    
    def make_payment(self, bill_id, amount):
        """Process payment"""
        # Get current bill
        query = "SELECT * FROM billing WHERE bill_id = %s"
        bill = self.execute_query(query, (bill_id,))
        
        if bill:
            bill = bill[0]
            new_paid = bill['paid_amount'] + amount
            
            if new_paid >= bill['total_amount']:
                status = 'Paid'
            else:
                status = 'Partial'
            
            update_query = """
                UPDATE billing 
                SET paid_amount = %s, payment_status = %s, payment_date = %s
                WHERE bill_id = %s
            """
            params = (new_paid, status, date.today(), bill_id)
            return self.execute_query(update_query, params)
        return None
    
    # Room Management
    def get_available_rooms(self):
        """Get all available rooms"""
        query = "SELECT * FROM rooms WHERE status = 'Available'"
        return self.execute_query(query)
    
    def admit_patient(self, patient_id, room_id, diagnosis):
        """Admit a patient to a room"""
        # Check if room is available
        room_query = "SELECT status FROM rooms WHERE room_id = %s"
        room = self.execute_query(room_query, (room_id,))
        
        if room and room[0]['status'] == 'Available':
            # Create admission record
            admit_query = """
                INSERT INTO admissions (patient_id, room_id, diagnosis, status)
                VALUES (%s, %s, %s, 'Active')
            """
            result = self.execute_query(admit_query, (patient_id, room_id, diagnosis))
            
            if result:
                # Update room status
                update_room = "UPDATE rooms SET status = 'Occupied' WHERE room_id = %s"
                self.execute_query(update_room, (room_id,))
                return result
        return None
    
    # Reports
    def get_patient_medical_history(self, patient_id):
        """Get complete medical history for a patient"""
        query = """
            SELECT a.appointment_date, a.diagnosis, a.symptoms,
                   CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
                   p.medicine_name, p.dosage, p.duration
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            LEFT JOIN prescriptions p ON a.appointment_id = p.appointment_id
            WHERE a.patient_id = %s
            ORDER BY a.appointment_date DESC
        """
        return self.execute_query(query, (patient_id,))
    
    def get_daily_report(self, report_date):
        """Get daily hospital report"""
        report = {}
        
        # Appointments for the day
        report['appointments'] = self.get_appointments_by_date(report_date)
        
        # Admissions for the day
        query = """
            SELECT a.*, p.first_name, p.last_name, r.room_number
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN rooms r ON a.room_id = r.room_id
            WHERE DATE(a.admission_date) = %s
        """
        report['admissions'] = self.execute_query(query, (report_date,))
        
        # Bills generated
        query = """
            SELECT * FROM billing 
            WHERE payment_date = %s OR payment_date IS NULL
        """
        report['bills'] = self.execute_query(query, (report_date,))
        
        return report