-- Create and use database
CREATE DATABASE IF NOT EXISTS hospital_management;
USE hospital_management;

-- Departments table
CREATE TABLE departments (
    dept_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL,
    location VARCHAR(200),
    phone VARCHAR(20),
    head_of_dept VARCHAR(100)
);

-- Doctors table
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100),
    dept_id INT,
    phone VARCHAR(20),
    email VARCHAR(100),
    salary DECIMAL(10, 2),
    hire_date DATE,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

-- Patients table
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    blood_group VARCHAR(5),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Rooms table
CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_number VARCHAR(10) NOT NULL,
    room_type VARCHAR(20) NOT NULL,
    price_per_day DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'Available'
);

-- Appointments table
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    appointment_time TIME,
    status VARCHAR(20) DEFAULT 'Scheduled',
    symptoms TEXT,
    diagnosis TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Prescriptions table
CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    appointment_id INT,
    medicine_name VARCHAR(100),
    dosage VARCHAR(100),
    duration VARCHAR(100),
    instructions TEXT,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

-- Billing table
CREATE TABLE billing (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    appointment_id INT,
    total_amount DECIMAL(10, 2),
    paid_amount DECIMAL(10, 2) DEFAULT 0,
    payment_status VARCHAR(20) DEFAULT 'Pending',
    payment_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

-- Admissions table
CREATE TABLE admissions (
    admission_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    room_id INT,
    admission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    discharge_date DATETIME,
    diagnosis TEXT,
    status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- Create indexes
CREATE INDEX idx_patient_name ON patients(last_name, first_name);
CREATE INDEX idx_doctor_name ON doctors(last_name, first_name);
CREATE INDEX idx_appointment_date ON appointments(appointment_date);
CREATE INDEX idx_patient_appointments ON appointments(patient_id, appointment_date);

-- Verify everything
SHOW TABLES;