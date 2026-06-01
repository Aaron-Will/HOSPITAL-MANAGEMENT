-- Insert Departments
INSERT INTO departments (dept_name, location, phone, head_of_dept) VALUES
('Cardiology', '3rd Floor, Block A', '123-456-7890', 'Dr. John Smith'),
('Neurology', '4th Floor, Block B', '123-456-7891', 'Dr. Sarah Johnson'),
('Pediatrics', '2nd Floor, Block C', '123-456-7892', 'Dr. Emily Brown'),
('Orthopedics', '1st Floor, Block D', '123-456-7893', 'Dr. Michael Lee'),
('Emergency', 'Ground Floor', '123-456-7894', 'Dr. Robert Wilson');

-- Insert Doctors
INSERT INTO doctors (first_name, last_name, specialization, dept_id, phone, email, salary, hire_date) VALUES
('John', 'Smith', 'Cardiologist', 1, '123-456-7801', 'john.smith@hospital.com', 150000, '2015-06-01'),
('Sarah', 'Johnson', 'Neurologist', 2, '123-456-7802', 'sarah.johnson@hospital.com', 160000, '2016-03-15'),
('Emily', 'Brown', 'Pediatrician', 3, '123-456-7803', 'emily.brown@hospital.com', 120000, '2017-08-20'),
('Michael', 'Lee', 'Orthopedic', 4, '123-456-7804', 'michael.lee@hospital.com', 140000, '2014-11-10'),
('Robert', 'Wilson', 'Emergency Physician', 5, '123-456-7805', 'robert.wilson@hospital.com', 130000, '2018-01-05');

-- Insert Patients
INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, blood_group) VALUES
('Alice', 'Johnson', '1990-05-15', 'F', '987-654-3210', 'alice@gmail.com', '123 Main St, City', 'O+'),
('Bob', 'Williams', '1985-08-22', 'M', '987-654-3211', 'bob@gmail.com', '456 Oak Ave, Town', 'A+'),
('Charlie', 'Davis', '1978-03-10', 'M', '987-654-3212', 'charlie@gmail.com', '789 Pine St, Village', 'B+'),
('Diana', 'Miller', '1995-12-01', 'F', '987-654-3213', 'diana@gmail.com', '321 Elm St, City', 'AB+');

-- Insert Rooms
INSERT INTO rooms (room_number, room_type, price_per_day, status) VALUES
('101', 'General', 100, 'Available'),
('102', 'General', 100, 'Occupied'),
('201', 'Private', 250, 'Available'),
('202', 'Private', 250, 'Available'),
('ICU1', 'ICU', 500, 'Available'),
('ER1', 'Emergency', 150, 'Available');