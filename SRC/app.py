from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from hospital_db import HospitalManagementSystem
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hospital_management_secret_key'
CORS(app)

# Initialize database connection
db = HospitalManagementSystem()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# ==================== PATIENT ROUTES ====================

@app.route('/patients')
def patients():
    """View all patients"""
    patients_list = db.get_all_patients()
    return render_template('patients.html', patients=patients_list)

@app.route('/add_patient', methods=['POST'])
def add_patient():
    """Add a new patient"""
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['date_of_birth']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        blood_group = request.form['blood_group']
        
        patient_id = db.add_patient(first_name, last_name, dob, gender, 
                                    phone, email, address, blood_group)
        
        if patient_id:
            flash('Patient added successfully!', 'success')
        else:
            flash('Error adding patient!', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('patients'))

@app.route('/search_patient')
def search_patient():
    """Search patients"""
    search_term = request.args.get('term', '')
    if search_term:
        patients = db.search_patient(search_term)
        return render_template('patients.html', patients=patients, search_term=search_term)
    return redirect(url_for('patients'))

# ==================== DOCTOR ROUTES ====================

@app.route('/doctors')
def doctors():
    """View all doctors"""
    doctors_list = db.get_all_doctors()
    return render_template('doctors.html', doctors=doctors_list)

@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    """Add a new doctor"""
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        specialization = request.form['specialization']
        dept_id = request.form['dept_id']
        phone = request.form['phone']
        email = request.form['email']
        salary = request.form['salary']
        hire_date = request.form['hire_date']
        
        doctor_id = db.add_doctor(first_name, last_name, specialization, dept_id,
                                  phone, email, salary, hire_date)
        
        if doctor_id:
            flash('Doctor added successfully!', 'success')
        else:
            flash('Error adding doctor!', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('doctors'))

# ==================== APPOINTMENT ROUTES ====================

@app.route('/appointments')
def appointments():
    """View appointments"""
    date = request.args.get('date', str(datetime.now().date()))
    appointments_list = db.get_appointments_by_date(date)
    return render_template('appointments.html', appointments=appointments_list, selected_date=date)

@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    """Schedule a new appointment"""
    try:
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        symptoms = request.form['symptoms']
        
        appointment_id = db.schedule_appointment(patient_id, doctor_id, 
                                                 appointment_date, appointment_time, symptoms)
        
        if appointment_id:
            flash('Appointment scheduled successfully!', 'success')
        else:
            flash('Error scheduling appointment!', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('appointments'))

@app.route('/update_appointment_status/<int:appointment_id>', methods=['POST'])
def update_appointment_status(appointment_id):
    """Update appointment status"""
    try:
        status = request.form['status']
        diagnosis = request.form.get('diagnosis', '')
        
        result = db.update_appointment_status(appointment_id, status, diagnosis)
        
        if result:
            flash('Appointment updated successfully!', 'success')
        else:
            flash('Error updating appointment!', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('appointments'))

# ==================== ROOM ROUTES ====================

@app.route('/rooms')
def rooms():
    """View rooms"""
    available_rooms = db.get_available_rooms()
    return render_template('rooms.html', rooms=available_rooms)

@app.route('/admit_patient', methods=['POST'])
def admit_patient():
    """Admit a patient to a room"""
    try:
        patient_id = request.form['patient_id']
        room_id = request.form['room_id']
        diagnosis = request.form['diagnosis']
        
        admission_id = db.admit_patient(patient_id, room_id, diagnosis)
        
        if admission_id:
            flash('Patient admitted successfully!', 'success')
        else:
            flash('Error admitting patient! Room might not be available.', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('rooms'))

# ==================== BILLING ROUTES ====================

@app.route('/billing')
def billing():
    """View billing page"""
    return render_template('billing.html')

@app.route('/create_bill', methods=['POST'])
def create_bill():
    """Create a new bill"""
    try:
        patient_id = request.form['patient_id']
        appointment_id = request.form['appointment_id']
        total_amount = request.form['total_amount']
        
        bill_id = db.create_bill(patient_id, appointment_id, total_amount)
        
        if bill_id:
            flash('Bill created successfully!', 'success')
        else:
            flash('Error creating bill!', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('billing'))

@app.route('/make_payment', methods=['POST'])
def make_payment():
    """Process payment"""
    try:
        bill_id = request.form['bill_id']
        amount = request.form['amount']
        
        result = db.make_payment(bill_id, float(amount))
        
        if result:
            flash('Payment processed successfully!', 'success')
        else:
            flash('Error processing payment!', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('billing'))

# ==================== REPORT ROUTES ====================

@app.route('/patient_history/<int:patient_id>')
def patient_history(patient_id):
    """View patient medical history"""
    history = db.get_patient_medical_history(patient_id)
    return render_template('patient_history.html', history=history, patient_id=patient_id)

# ==================== API ROUTES (for AJAX) ====================

@app.route('/api/patients')
def api_patients():
    """API endpoint for patients"""
    patients = db.get_all_patients()
    return jsonify(patients)

@app.route('/api/doctors')
def api_doctors():
    """API endpoint for doctors"""
    doctors = db.get_all_doctors()
    return jsonify(doctors)

@app.route('/api/appointments/<date>')
def api_appointments(date):
    """API endpoint for appointments by date"""
    appointments = db.get_appointments_by_date(date)
    return jsonify(appointments)

if __name__ == '__main__':
    app.run(debug=True, port=5000)