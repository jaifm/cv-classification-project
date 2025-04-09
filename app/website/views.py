from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import PyPDF2
from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
from sqlalchemy.sql import func
from .models import CV, CVData, CATEGORY_MAPPING
from . import db
import hashlib
import spacy

views = Blueprint('views', __name__)

# Load the saved BERT model and tokenizer
model_path = "../models/saved_bert_model"
bert_model = TFBertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define upload folder
UPLOAD_FOLDER = r"C:\Users\ItsLo\Desktop\Dissertation\Project\cv-classification-project\app\website\static\uploads"
ALLOWED_EXTENSIONS = {'pdf'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

def preprocess_and_predict(text):
    # Preprocess the text
    encodings = tokenizer(text, truncation=True, padding='max_length', max_length=128, return_tensors='tf')
    # Predict the category
    predictions = bert_model(encodings)
    predicted_class = tf.argmax(predictions.logits, axis=1).numpy()[0]
    return predicted_class

# Define a dictionary mapping categories to required skills
category_skills = {
    "INFORMATION-TECHNOLOGY": [
        "Programming",
        "Cybersecurity",
        "Cloud Computing",
        "Data Analysis",
        "Networking",
        "Database Management",
        "Artificial Intelligence & Machine Learning",
        "Project Management",
        "Technical Support",
        "DevOps"
    ],
    "BUSINESS-DEVELOPMENT": [
        "Sales",
        "Communication",
        "Marketing",
        "Business Intelligence",
        "ROI and Data Analysis",
        "Project Management",
        "Negotiation",
        "Strategic Planning",
        "Networking",
        "Customer Relationship Management"
    ],
    "FINANCE": [
        "Financial Analysis",
        "Accounting",
        "Budgeting",
        "Risk Management",
        "Investment Analysis",
        "Financial Modeling",
        "Attention to Detail",
        "Regulatory Compliance",
        "Data Analysis",
        "Economics"
    ],
    "ADVOCATE": [
        "Legal Research",
        "Oral Advocacy",
        "Written Communication",
        "Negotiation",
        "Analytical Thinking",
        "Client Counseling",
        "Ethical Judgment",
        "Time Management",
        "Interpersonal Skills",
        "Attention to Detail"
    ],
    "ACCOUNTANT": [
        "Financial Reporting",
        "Tax Preparation",
        "Auditing",
        "Budgeting",
        "Regulatory Compliance",
        "Attention to Detail",
        "Analytical Skills",
        "Spreadsheet Proficiency",
        "Cost Accounting",
        "Problem-Solving"
    ],
    "ENGINEERING": [
        "Problem-Solving",
        "Technical Proficiency",
        "Project Management",
        "Teamwork",
        "Communication Skills",
        "Attention to Detail",
        "Creativity",
        "Analytical Thinking",
        "Mathematics",
        "Computer-Aided Design (CAD)"
    ],
    "CHEF": [
        "Culinary Skills",
        "Menu Planning",
        "Kitchen Management",
        "Food Safety Knowledge",
        "Creativity",
        "Time Management",
        "Attention to Detail",
        "Leadership",
        "Budgeting",
        "Inventory Management"
    ],
    "AVIATION": [
        "Aeronautical Knowledge",
        "Navigation Skills",
        "Communication Skills",
        "Problem-Solving",
        "Attention to Detail",
        "Teamwork",
        "Technical Proficiency",
        "Situational Awareness",
        "Decision Making",
        "Adaptability"
    ],
    "FITNESS": [
        "Anatomy Knowledge",
        "Exercise Physiology",
        "Nutrition Knowledge",
        "Personal Training",
        "Motivational Skills",
        "Communication Skills",
        "Adaptability",
        "Customer Service",
        "Injury Prevention",
        "First Aid and CPR"
    ],
    "SALES": [
        "Communication Skills",
        "Negotiation",
        "Customer Relationship Management",
        "Product Knowledge",
        "Active Listening",
        "Persuasion",
        "Time Management",
        "Problem-Solving",
        "Adaptability",
        "Networking"
    ],
    "BANKING": [
        "Financial Analysis",
        "Customer Service",
        "Risk Management",
        "Attention to Detail",
        "Regulatory Compliance",
        "Communication Skills",
        "Problem-Solving",
        "Numeracy Skills",
        "Sales Skills",
        "Time Management"
    ],
    "HEALTHCARE": [
        "Patient Care",
        "Medical Knowledge",
        "Communication Skills",
        "Empathy",
        "Attention to Detail",
        "Problem-Solving",
        "Teamwork",
        "Time Management",
        "Adaptability",
        "Ethical Judgment"
    ],
    "CONSULTANT": [
        "Analytical Thinking",
        "Problem-Solving",
        "Communication Skills",
        "Project Management",
        "Industry Knowledge",
        "Data Analysis",
        "Presentation Skills",
        "Adaptability",
        "Teamwork",
        "Time Management"
    ],
    "CONSTRUCTION": [
        "Project Management",
        "Blueprint Reading",
        "Building Codes and Regulations",
        "Safety Compliance",
        "Carpentry",
        "Masonry",
        "Plumbing",
        "Electrical Systems",
        "Welding",
        "Heavy Equipment Operation"
    ],
    "PUBLIC-RELATIONS": [
        "Communication Skills",
        "Writing and Editing",
        "Media Relations",
        "Crisis Management",
        "Social Media Management",
        "Event Planning",
        "Public Speaking",
        "Strategic Planning",
        "Research Skills",
        "Attention to Detail"
    ],
    "HR": [
        "Employee Relations",
        "Recruitment and Staffing",
        "Performance Management",
        "Training and Development",
        "HRIS",
        "Compensation and Benefits",
        "Labor Law Knowledge",
        "Conflict Resolution",
        "Organizational Skills",
        "Communication Skills"
    ],
    "DESIGNER": [
        "Creativity",
        "Adobe Creative Suite Proficiency",
        "Typography",
        "Color Theory",
        "Layout and Composition",
        "User Experience (UX) Design",
        "User Interface (UI) Design",
        "Web Design",
        "Print Design",
        "Branding"
    ],
    "ARTS": [
        "Creativity",
        "Drawing and Illustration",
        "Painting Techniques",
        "Sculpting",
        "Art History Knowledge",
        "Photography",
        "Digital Art",
        "Printmaking",
        "Composition",
        "Color Theory"
    ],
    "TEACHER": [
        "Lesson Planning",
        "Classroom Management",
        "Curriculum Development",
        "Assessment and Evaluation",
        "Subject Matter Expertise",
        "Communication Skills",
        "Patience",
        "Adaptability",
        "Organization",
        "Technology Integration"
    ],
    "APPAREL": [
        "Fashion Design",
        "Textile Knowledge",
        "Pattern Making",
        "Sewing and Garment Construction",
        "Trend Analysis",
        "Visual Merchandising",
        "Branding",
        "Retail Management",
        "Inventory Control",
        "Sales Skills"
    ],
    "DIGITAL-MEDIA": [
        "Content Creation",
        "Social Media Management",
        "SEO Optimization",
        "Video Production",
        "Graphic Design",
        "Web Analytics",
        "Email Marketing",
        "Copywriting",
        "Photography",
        "Marketing Strategy"
    ],
    "AGRICULTURE": [
        "Crop Production",
        "Soil Science",
        "Pest Management",
        "Agricultural Machinery Operation",
        "Irrigation Management",
        "Animal Husbandry",
        "Farm Management",
        "Sustainable Practices",
        "Data Analysis",
        "Weather Analysis"
    ],
    "AUTOMOBILE": [
        "Mechanical Aptitude",
        "Diagnostics",
        "Electrical Systems",
        "Engine Repair",
        "Brake Systems",
        "Transmission Repair",
        "Suspension and Steering",
        "Air Conditioning Systems",
        "Welding",
        "Computer Skills"
    ],
    "BPO": [
    "Effective Communication",
    "Active Listening",
    "Problem-Solving",
    "Adaptability",
    "Technical Proficiency",
    "Time Management",
    "Customer Service Orientation",
    "Multitasking",
    "Empathy",
    "Teamwork"
]}

@views.route('/') #home route
@login_required
def home():
    return render_template("index.html", user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file', category='error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Extract text from the uploaded PDF
            text = extract_text_from_pdf(file_path)

            # Hash the content
            content_hash = hashlib.sha256(text.encode()).hexdigest()

            # Predict the category using the BERT model
            predicted_class = preprocess_and_predict(text)
            category_name = CATEGORY_MAPPING.get(predicted_class, "Unknown")

            # Save the CV and its data to the database
            new_cv = CV(user_id=current_user.id, cv=content_hash, date=func.now())
            db.session.add(new_cv)
            db.session.commit()

            new_cv_data = CVData(cv_id=new_cv.id, data=category_name)
            db.session.add(new_cv_data)
            db.session.commit()

            # Delete the uploaded file after processing
            os.remove(file_path)

            return render_template('upload.html', user=current_user, predicted_category=category_name, category_skills=category_skills)

    return render_template('upload.html', user=current_user, category_skills=category_skills)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        new_email = request.form.get('email')
        password = request.form.get('password')

        if not new_email or not password:
            flash('Please provide both email and password.', category='error')
        elif not current_user.check_password(password):
            flash('Incorrect password. Please try again.', category='error')
        else:
            current_user.email = new_email
            db.session.commit()
            flash('Email updated successfully!', category='success')

    user_cvs = CV.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', user=current_user, cvs=user_cvs)
