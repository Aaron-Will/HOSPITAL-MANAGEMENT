from hospital_db import HospitalManagementSystem
from datetime import date, datetime
import sys

class HospitalApp:
    def __init__(self):
        self.hms = HospitalManagementSystem()
    
    def display_menu(self):
        print("\n" + "="*50)
        print("HOSPITAL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Billing Management")
        print("5. Room Management")
        print("6. Reports")
        print("7. Exit")
        print("="*50)
    
    def patient_menu(self):
        while True:
            print("\n--- Patient Management ---")
            print("1. Add New Patient")
            print("2. View All Patients")
            print("3. Search Patient")
            print("4. Back to Main Menu")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.add_patient()
            elif choice == '2':
                self.view_all_patients()
            elif choice == '3':
                self.search_patient()
            elif choice == '4':
                break
    
    def add_patient(self):
        print("\n--- Add New Patient ---")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")
        gender = input("Gender (M/F/Other): ")
        phone = input("Phone: ")
        email = input("Email: ")
        address = input("Address: ")
        blood_group = input("Blood Group: ")
        
        patient_id = self.hms.add_patient(first_name, last_name, dob, gender, phone, email, address, blood_group)
        if patient_id:
            print(f"Patient added successfully! Patient ID: {patient_id}")
        else:
            print("Failed to add patient!")
    
    def view_all_patients(self):
        patients = self.hms.get_all_patients()
        if patients:
            print("\n--- All Patients ---")
            for patient in patients:
                print(f"ID: {patient['patient_id']}, Name: {patient['first_name']} {patient['last_name']}, "
                      f"Phone: {patient['phone']}, Blood: {patient['blood_group']}")
        else:
            print("No patients found!")
    
    def search_patient(self):
        search_term = input("Enter search term (name/phone): ")
        patients = self.hms.search_patient(search_term)
        if patients:
            print("\n--- Search Results ---")
            for patient in patients:
                print(f"ID: {patient['patient_id']}, Name: {patient['first_name']} {patient['last_name']}, "
                      f"Phone: {patient['phone']}")
        else:
            print("No patients found!")
    
    def doctor_menu(self):
        while True:
            print("\n--- Doctor Management ---")
            print("1. Add New Doctor")
            print("2. View All Doctors")
            print("3. Back to Main Menu")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.add_doctor()
            elif choice == '2':
                self.view_all_doctors()
            elif choice == '3':
                break
    
    def add_doctor(self):
        print("\n--- Add New Doctor ---")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        specialization = input("Specialization: ")
        dept_id = input("Department ID: ")
        phone = input("Phone: ")
        email = input("Email: ")
        salary = input("Salary: ")
        hire_date = input("Hire Date (YYYY-MM-DD): ")
        
        doctor_id = self.hms.add_doctor(first_name, last_name, specialization, dept_id, phone, email, salary, hire_date)
        if doctor_id:
            print(f"Doctor added successfully! Doctor ID: {doctor_id}")
        else:
            print("Failed to add doctor!")
    
    def view_all_doctors(self):
        doctors = self.hms.get_all_doctors()
        if doctors:
            print("\n--- All Doctors ---")
            for doctor in doctors:
                print(f"ID: {doctor['doctor_id']}, Name: {doctor['first_name']} {doctor['last_name']}, "
                      f"Specialization: {doctor['specialization']}, Dept: {doctor['dept_name']}")
        else:
            print("No doctors found!")
    
    def appointment_menu(self):
        while True:
            print("\n--- Appointment Management ---")
            print("1. Schedule Appointment")
            print("2. View Appointments by Date")
            print("3. Update Appointment Status")
            print("4. Back to Main Menu")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.schedule_appointment()
            elif choice == '2':
                self.view_appointments_by_date()
            elif choice == '3':
                self.update_appointment()
            elif choice == '4':
                break
    
    def schedule_appointment(self):
        print("\n--- Schedule Appointment ---")
        patient_id = input("Patient ID: ")
        doctor_id = input("Doctor ID: ")
        appointment_date = input("Date (YYYY-MM-DD): ")
        appointment_time = input("Time (HH:MM:SS): ")
        symptoms = input("Symptoms: ")
        
        appointment_id = self.hms.schedule_appointment(patient_id, doctor_id, appointment_date, appointment_time, symptoms)
        if appointment_id:
            print(f"Appointment scheduled! Appointment ID: {appointment_id}")
        else:
            print("Failed to schedule appointment!")
    
    def view_appointments_by_date(self):
        date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
        if not date_input:
            date_input = str(date.today())
        
        appointments = self.hms.get_appointments_by_date(date_input)
        if appointments:
            print(f"\n--- Appointments for {date_input} ---")
            for apt in appointments:
                print(f"ID: {apt['appointment_id']}, Time: {apt['appointment_time']}, "
                      f"Patient: {apt['patient_fname']} {apt['patient_lname']}, "
                      f"Doctor: {apt['doctor_fname']} {apt['doctor_lname']}, "
                      f"Status: {apt['status']}")
        else:
            print("No appointments found for this date!")
    
    def update_appointment(self):
        apt_id = input("Appointment ID: ")
        status = input("Status (Scheduled/Completed/Cancelled): ")
        diagnosis = input("Diagnosis (optional): ")
        
        result = self.hms.update_appointment_status(apt_id, status, diagnosis if diagnosis else None)
        if result:
            print("Appointment updated successfully!")
        else:
            print("Failed to update appointment!")
    
    def billing_menu(self):
        while True:
            print("\n--- Billing Management ---")
            print("1. Create Bill")
            print("2. Make Payment")
            print("3. Back to Main Menu")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.create_bill()
            elif choice == '2':
                self.make_payment()
            elif choice == '3':
                break
    
    def create_bill(self):
        patient_id = input("Patient ID: ")
        appointment_id = input("Appointment ID: ")
        total_amount = input("Total Amount: ")
        
        bill_id = self.hms.create_bill(patient_id, appointment_id, total_amount)
        if bill_id:
            print(f"Bill created! Bill ID: {bill_id}")
        else:
            print("Failed to create bill!")
    
    def make_payment(self):
        bill_id = input("Bill ID: ")
        amount = input("Payment Amount: ")
        
        result = self.hms.make_payment(bill_id, float(amount))
        if result:
            print("Payment processed successfully!")
        else:
            print("Failed to process payment!")
    
    def room_menu(self):
        while True:
            print("\n--- Room Management ---")
            print("1. View Available Rooms")
            print("2. Admit Patient")
            print("3. Back to Main Menu")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.view_available_rooms()
            elif choice == '2':
                self.admit_patient()
            elif choice == '3':
                break
    
    def view_available_rooms(self):
        rooms = self.hms.get_available_rooms()
        if rooms:
            print("\n--- Available Rooms ---")
            for room in rooms:
                print(f"Room: {room['room_number']}, Type: {room['room_type']}, Price: ${room['price_per_day']}")
        else:
            print("No available rooms!")
    
    def admit_patient(self):
        patient_id = input("Patient ID: ")
        room_id = input("Room ID: ")
        diagnosis = input("Diagnosis: ")
        
        admission_id = self.hms.admit_patient(patient_id, room_id, diagnosis)
        if admission_id:
            print(f"Patient admitted! Admission ID: {admission_id}")
        else:
            print("Failed to admit patient!")
    
    def reports_menu(self):
        while True:
            print("\n--- Reports ---")
            print("1. Patient Medical History")
            print("2. Daily Report")
            print("3. Back to Main Menu")
            
            choice = input("Enter choice: ")
            
            if choice == '1':
                self.view_patient_history()
            elif choice == '2':
                self.view_daily_report()
            elif choice == '3':
                break
    
    def view_patient_history(self):
        patient_id = input("Patient ID: ")
        history = self.hms.get_patient_medical_history(patient_id)
        
        if history:
            print(f"\n--- Medical History for Patient ID: {patient_id} ---")
            for record in history:
                print(f"Date: {record['appointment_date']}")
                print(f"Doctor: {record['doctor_name']}")
                print(f"Symptoms: {record['symptoms']}")
                print(f"Diagnosis: {record['diagnosis']}")
                if record['medicine_name']:
                    print(f"Medicine: {record['medicine_name']} - {record['dosage']} for {record['duration']}")
                print("-" * 30)
        else:
            print("No medical history found!")
    
    def view_daily_report(self):
        date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
        if not date_input:
            date_input = str(date.today())
        
        report = self.hms.get_daily_report(date_input)
        
        print(f"\n--- Daily Report for {date_input} ---")
        print(f"\nAppointments: {len(report['appointments'])}")
        print(f"Admissions: {len(report['admissions'])}")
        print(f"Bills: {len(report['bills'])}")
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.patient_menu()
            elif choice == '2':
                self.doctor_menu()
            elif choice == '3':
                self.appointment_menu()
            elif choice == '4':
                self.billing_menu()
            elif choice == '5':
                self.room_menu()
            elif choice == '6':
                self.reports_menu()
            elif choice == '7':
                print("Thank you for using Hospital Management System!")
                sys.exit(0)
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    app = HospitalApp()
    app.run()