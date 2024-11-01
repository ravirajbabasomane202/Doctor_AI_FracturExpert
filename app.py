from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital_finder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database models

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    hospital = db.Column(db.String(250), nullable=False)
    appointment_date = db.Column(db.String(50), nullable=False)
    appointment_time = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)


with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    #return render_template('loginHospital.html')
    return render_template('index.html')


@app.route('/map')
def map_view():
    return render_template('map.html')


# Login route
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pswd')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session
            session['email'] = user.email
            flash("Logged in successfully!", "success")
            return redirect(url_for('home')) 
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')  # Use .get() to avoid KeyError
        email = request.form.get('email')
        password = request.form.get('pswd')
        
        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please choose a different one.", "danger")
        else:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for('login'))

    return render_template('login.html')

# Book appointment route
@app.route('/book', methods=['GET', 'POST'])
def book():
    hospital_name = request.args.get('hospital') 
    if request.method == 'POST':
        appointment = Appointment(
            full_name=request.form['fullName'],
            email=request.form['email'],
            phone=request.form['phone'],
            hospital=request.form['hospital'],
            appointment_date=request.form['appointmentDate'],
            appointment_time=request.form['appointmentTime'],
            notes=request.form['notes']
        )
        db.session.add(appointment)
        db.session.commit()
        flash("Appointment request submitted successfully!", "success")
        return redirect(url_for('home'))
    return render_template('Contact.html', hospital=hospital_name)


# Appointments route
@app.route('/appointments')
def appointments():
    if 'user_id' not in session:
        flash("Please log in to view your appointments.", "warning")
        return redirect(url_for('login'))
    
    # Fetch all appointments for the logged-in user
    user_appointments = Appointment.query.filter_by(email=session.get('email')).all()
    print("User is logged in with email:", session.get('email'))
    print("Fetched appointments:", user_appointments)
    return render_template('appointments.html', appointments=user_appointments)

# Cancel appointment route
@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        flash("Appointment canceled successfully.", "success")
    else:
        flash("Appointment not found.", "danger")
    return redirect(url_for('appointments'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from the Flask session
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
