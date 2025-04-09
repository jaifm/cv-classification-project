from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pandas as pd

# Load the dataset to extract unique category names
data_path = r"C:\Users\ItsLo\Desktop\Dissertation\Project\cv-classification-project\data\resume_data.csv"
df = pd.read_csv(data_path)
CATEGORY_MAPPING = {i: category for i, category in enumerate(df['Category'].unique())}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    cvs = db.relationship('CV')

class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cv = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    cv_data = db.relationship('CVData', uselist=False, back_populates='cv', cascade='all, delete-orphan')

class CVData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cv_id = db.Column(db.Integer, db.ForeignKey('cv.id'), unique=True)
    data = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    cv = db.relationship('CV', back_populates='cv_data')