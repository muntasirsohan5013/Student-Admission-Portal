from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message
import random
from flask_wtf import CSRFProtect
from flask import jsonify
import logging
from flask import session
from sqlalchemy import select
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import os
import io
from flask import Flask, request, redirect, url_for, flash, session
from google_auth_oauthlib.flow import Flow  
from googleapiclient.discovery import build  
from googleapiclient.http import MediaFileUpload  
import os
from flask import send_from_directory
from datetime import datetime



load_dotenv()
# Initialize Flask app
app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'my_secret_key'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:new002@localhost:3306/studentCONT'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '6f14520eb561ee'
app.config['MAIL_PASSWORD'] = 'ca36f8b302bd89'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = '202224405010@njtech.edu.cn'
mail = Mail(app)

otp_storage = {}
messages = []
logging.basicConfig(level=logging.DEBUG)

Base = declarative_base()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
db_session = Session()  
login_manager = LoginManager(app)
login_manager.login_view = 'login'




db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_admin = db.Column(db.Integer, default=0)  


class Admission(db.Model):
    __tablename__ = 'admission'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    user = db.relationship('User', backref=db.backref('admission', uselist=False))

    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    country_code = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    passport_path = db.Column(db.String(200), nullable=False)
    highschool_certificate_path = db.Column(db.String(200), nullable=False)
    mid_school_certificate_path = db.Column(db.String(200), nullable=False)
    physical_exam_certificate_path = db.Column(db.String(200))
    bank_statement_path = db.Column(db.String(200), nullable=False)
    bank_solvency_path = db.Column(db.String(200), nullable=False)
    study_plan_path = db.Column(db.String(200))
    english_proficiency_path = db.Column(db.String(200))
    hsk_certificate_path = db.Column(db.String(200))
    
class University(db.Model):
    __tablename__ = 'university'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    scholarship = db.Column(db.Text, nullable=False)
    dormitory = db.Column(db.Text, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access only!', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))  


@app.route('/')
def index():
    
    return render_template('index.html')



@app.route('/admission', methods=['GET', 'POST'])
@login_required
def admission():
    """Handle the admission form."""
    if request.method == 'POST':
        try:
            existing_admission = Admission.query.filter_by(user_id=current_user.id).first()
            if existing_admission:
                flash('You have already submitted your admission.', 'warning')
                return redirect(url_for('admission'))

            name = request.form['name']
            email = request.form['email']
            country_code = request.form['country-code']
            phone_number = request.form['phone-number']

            def save_file(field_name):
                """Helper function to save an uploaded file and return its path."""
                file = request.files[field_name]
                if file and file.filename:
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(filepath)
                    return filepath
                return None

            passport_path = save_file('passport')
            highschool_certificate_path = save_file('highschool_certificate')
            mid_school_certificate_path = save_file('mid_school_certificate')
            physical_exam_certificate_path = save_file('physical_exam_certificate')
            bank_statement_path = save_file('bank-statement')
            bank_solvency_path = save_file('bank-solvency')
            study_plan_path = save_file('study_plan')
            english_proficiency_path = save_file('english_proficiency')
            hsk_certificate_path = save_file('hsk_certificate')

            new_admission = Admission(
                user_id=current_user.id, 
                name=name,
                email=email,
                country_code=country_code,
                phone_number=phone_number,
                passport_path=passport_path,
                highschool_certificate_path=highschool_certificate_path,
                mid_school_certificate_path=mid_school_certificate_path,
                physical_exam_certificate_path=physical_exam_certificate_path,
                bank_statement_path=bank_statement_path,
                bank_solvency_path=bank_solvency_path,
                study_plan_path=study_plan_path,
                english_proficiency_path=english_proficiency_path,
                hsk_certificate_path=hsk_certificate_path
            )
            db.session.add(new_admission)
            db.session.commit()

            flash('Form submitted successfully!', 'success')
            return redirect(url_for('index'))

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('admission'))

    return render_template('admission.html')

# otp
@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return {'success': False, 'message': 'Email is required'}, 400

    generated_otp = str(random.randint(100000, 999999))
    otp_storage[email] = generated_otp

    msg = Message('Your OTP for registration', recipients=[email])
    msg.body = f'Your OTP is {generated_otp}. Please enter this OTP to complete your registration.'

    try:
        mail.send(msg)
        return {'success': True, 'message': 'OTP sent successfully'}, 200
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return {'success': False, 'message': 'Failed to send OTP'}, 500
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        otp = request.form.get('otp')

        if otp:
            # Check if the OTP is valid
            if otp_storage.get(email) == otp:
                hashed_password = generate_password_hash(password)  # Hash the password

                try:
                    new_user = User(username=username, email=email, password=hashed_password)
                    db_session.add(new_user)
                    db_session.commit()
                    flash('Registration successful!', 'success')
                    otp_storage.pop(email, None)  # Remove OTP once registration is complete
                    return redirect(url_for('login'))
                except Exception as e:
                    db_session.rollback()
                    flash('Error: Username or email already exists.', 'danger')
                    print(f"Registration error: {e}")
                    return redirect(url_for('register'))
            else:
                flash('Invalid OTP!', 'danger')
                return redirect(url_for('register'))

        # If no OTP, generate and send it
        generated_otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP
        otp_storage[email] = generated_otp  # Store the OTP for the email

        # Send the OTP via email
        msg = Message('Your OTP for registration', recipients=[email])
        msg.body = f'Your OTP is {generated_otp}. Please enter this OTP to complete your registration.'
        mail.send(msg)

        flash('OTP sent to your email. Please verify to complete registration.', 'info')
        return render_template('register.html', email=email)

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()  # Ensure to remove whitespaces
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        
        # Try to find the user by username or email
        user = db_session.query(User).filter((User.username == username) | (User.email == email)).first()
        
        if user:
            # Check if the password matches
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!' , 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('Login failed. User not found.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        otp = request.form.get('otp')

        # Check if OTP is provided
        if otp:
            # Validate OTP
            if otp_storage.get(email) == otp:
                # Hash the new password
                hashed_password = generate_password_hash(password)

                try:
                    # Query the user from the database
                    user = db_session.query(User).filter_by(email=email).first()

                    if user:
                        # Update the password for the user
                        user.password = hashed_password
                        db_session.commit()  # Commit the changes to the database

                        flash('Password reset successful! Please login with your new password.', 'success')

                        # Remove OTP after successful reset
                        otp_storage.pop(email, None)

                        return redirect(url_for('login'))  # Redirect to login page after success
                    else:
                        flash('User not found.', 'danger')
                        return redirect(url_for('reset_password'))  # Go back to reset password page

                except Exception as e:
                    db_session.rollback()  # Rollback any changes in case of error
                    flash(f'Error updating password: {str(e)}', 'danger')  # Show the actual error message
                    print(f"Error updating password: {str(e)}")  # Log the error in the server console
                    return redirect(url_for('reset_password'))  # Go back to reset password page

        # If no OTP, generate and send it
        generated_otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP
        otp_storage[email] = generated_otp  # Store the OTP for the email

        # Send the OTP via email
        msg = Message('Your OTP for password reset', recipients=[email])
        msg.body = f'Your OTP is {generated_otp}. Please enter this OTP to reset your password.'
        mail.send(msg)

        flash('OTP sent to your email. Please verify to complete the password reset.', 'info')
        return render_template('reset_password.html', email=email)

    return render_template('reset_password.html')  


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/update_uni', methods=['GET', 'POST'])
def update_uni():
    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        scholarship = request.form['scholarship']
        dormitory = request.form['dormitory']
        rank = request.form['rank']
        files = request.files.getlist('universityPictures')

        filenames = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
            else:
                flash('Invalid file format. Please upload image files only.')
                return redirect(request.url)

        new_university = University(
            title=title,
            details=details,
            scholarship=scholarship,
            dormitory=dormitory,
            rank=rank,
            pictures=','.join(filenames)
        )
        db.session.add(new_university)
        db.session.commit()

        flash('University information updated successfully!')
        return redirect(url_for('update_uni'))

    all_universities = University.query.order_by(University.created_at.desc()).all()

    return render_template('update_uni.html', universities=all_universities)
    
@app.route('/post/<int:university_id>', methods=['GET'])
def readmore(university_id):
    post = db_session.query(University).filter_by(id=university_id).first()
    
    if post:
        return render_template('readmore.html',  university=post)
    else:
        print("Post not found")  # Debugging line
        return "Post not found", 404

    

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        details = request.form['details']
        scholarship = request.form['scholarship']
        dormitory = request.form['dormitory']
        rank = request.form['rank']
        

        # Handle file uploads
        picture_files = request.files.getlist('universityPicture')
        picture_filenames = []
        
        for file in picture_files:
            if file:
                filename = file.filename
                file.save(os.path.join('uploads', filename))  # Save the file to the uploads directory
                picture_filenames.append(filename)

        # Create a new university record
        new_university = University(
            title=title,
            details=details,
            scholarship=scholarship,
            dormitory=dormitory,
            rank=rank,
            picture=', '.join(picture_filenames)  # Store filenames as a comma-separated string
        )
        
        db.session.add(new_university)
        db.session.commit()
        
        return redirect(url_for('success')) 
    
@app.route('/success')
def success():
    return "University information uploaded successfully!"



if __name__ == '__main__':
    app.run(debug=True)