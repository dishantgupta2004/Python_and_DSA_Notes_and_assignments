# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, RadioField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_wtf.csrf import CSRFProtect
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # For production, use a fixed secret key
csrf = CSRFProtect(app)

# Form class for our GenAI course registration
class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=3, max=100, message="Name must be between 3 and 100 characters")
    ])
    
    email = EmailField('Email Address', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\+?[0-9]{10,15}$', message="Please enter a valid phone number")
    ])
    
    education = SelectField('Highest Education Level', choices=[
        ('', 'Select your education level'),
        ('high_school', 'High School'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', 'PhD'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    
    background = SelectField('Technical Background', choices=[
        ('', 'Select your background'),
        ('none', 'No Programming Experience'),
        ('beginner', 'Beginner (Basic programming concepts)'),
        ('intermediate', 'Intermediate (Worked on small projects)'),
        ('advanced', 'Advanced (Professional experience)')
    ], validators=[DataRequired()])
    
    interest = TextAreaField('Why are you interested in this GenAI course?', validators=[
        DataRequired(),
        Length(min=50, max=500, message="Please write between 50 and 500 characters")
    ])
    
    course_track = RadioField('Choose Your Learning Track', choices=[
        ('fundamentals', 'AI Fundamentals - For absolute beginners'),
        ('developer', 'AI Developer - For those with programming experience'),
        ('business', 'AI for Business - Applications and strategy')
    ], validators=[DataRequired()])
    
    referral = SelectField('How did you hear about us?', choices=[
        ('', 'Please select an option'),
        ('search', 'Search Engine'),
        ('social', 'Social Media'),
        ('friend', 'Friend or Colleague'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    
    newsletter = BooleanField('Subscribe to our newsletter for AI updates')
    
    terms = BooleanField('I agree to the terms and conditions', validators=[
        DataRequired(message="You must agree to the terms and conditions")
    ])
    
    submit = SubmitField('Register Now')

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # In a production app, you would save this to a database
        # For this demo, we'll just store in the session
        session['registration'] = {
            'full_name': form.full_name.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'education': dict(form.education.choices).get(form.education.data),
            'background': dict(form.background.choices).get(form.background.data),
            'interest': form.interest.data,
            'course_track': dict(form.course_track.choices).get(form.course_track.data),
            'referral': dict(form.referral.choices).get(form.referral.data),
            'newsletter': form.newsletter.data,
            'registered_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        flash('Registration successful! Welcome to our GenAI course!', 'success')
        return redirect(url_for('confirmation'))
    
    return render_template('index.html', form=form)

@app.route('/confirmation')
def confirmation():
    if 'registration' not in session:
        flash('Please complete the registration form first.', 'error')
        return redirect(url_for('index'))
    
    registration = session['registration']
    return render_template('confirmation.html', registration=registration)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    # Sample course data
    courses = [
        {
            'id': 'fundamentals',
            'title': 'AI Fundamentals',
            'subtitle': 'For absolute beginners',
            'description': 'Start your AI journey with no prerequisites. Learn the basics of AI, machine learning, and how neural networks work.',
            'duration': '8 weeks',
            'level': 'Beginner',
            'projects': ['Chatbot development', 'Image classification', 'AI ethics case study']
        },
        {
            'id': 'developer',
            'title': 'AI Developer',
            'subtitle': 'For those with programming experience',
            'description': 'Dive deep into AI development with hands-on projects. Build and deploy sophisticated AI models using Python and popular frameworks.',
            'duration': '12 weeks',
            'level': 'Intermediate to Advanced',
            'projects': ['Large language model fine-tuning', 'Vision-language model implementation', 'Generative AI application']
        },
        {
            'id': 'business',
            'title': 'AI for Business',
            'subtitle': 'Applications and strategy',
            'description': 'Learn how to leverage AI for business growth, strategy, and innovation. Understand AI capabilities and limitations in a business context.',
            'duration': '6 weeks',
            'level': 'All Levels',
            'projects': ['AI implementation strategy', 'ROI analysis for AI projects', 'AI-driven business model design']
        }
    ]
    
    return render_template('courses.html', courses=courses)

if __name__ == '__main__':
    app.run(debug=True)