# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # For production, use a fixed secret key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Set session expiry to 7 days

# Sample user data (in a real app, this would be in a database)
users = {
    'user1@example.com': {
        'password': 'password123',  # In a real app, this should be hashed
        'name': 'John Doe',
        'role': 'student',
        'joined': '2024-12-15',
        'preferences': {
            'theme': 'light',
            'notifications': True,
            'language': 'english'
        }
    },
    'user2@example.com': {
        'password': 'password456',
        'name': 'Jane Smith',
        'role': 'instructor',
        'joined': '2024-11-10',
        'preferences': {
            'theme': 'dark',
            'notifications': False,
            'language': 'english'
        }
    }
}

# Sample courses data
courses = [
    {
        'id': 1,
        'title': 'Introduction to Python',
        'description': 'Learn the basics of Python programming language.',
        'instructor': 'Jane Smith',
        'duration': '8 weeks',
        'enrolled': ['user1@example.com']
    },
    {
        'id': 2,
        'title': 'Web Development with Flask',
        'description': 'Build web applications using the Flask framework.',
        'instructor': 'Jane Smith',
        'duration': '10 weeks',
        'enrolled': []
    },
    {
        'id': 3,
        'title': 'Data Science Fundamentals',
        'description': 'Introduction to data science concepts and tools.',
        'instructor': 'Robert Johnson',
        'duration': '12 weeks',
        'enrolled': ['user1@example.com']
    }
]

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        if email in users and users[email]['password'] == password:
            # Set up user session
            session.permanent = remember
            session['user'] = {
                'email': email,
                'name': users[email]['name'],
                'role': users[email]['role']
            }
            
            # Record login time
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Load user preferences
            session['preferences'] = users[email]['preferences']
            
            flash(f'Welcome back, {users[email]["name"]}!', 'success')
            
            # Redirect to next parameter if available, otherwise to dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_email = session['user']['email']
    
    # Get courses the user is enrolled in
    enrolled_courses = []
    for course in courses:
        if user_email in course['enrolled']:
            enrolled_courses.append(course)
    
    # Get user session stats
    login_time = session.get('login_time', 'Unknown')
    session_duration = None
    if login_time != 'Unknown':
        login_datetime = datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')
        duration = datetime.now() - login_datetime
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        session_duration = f"{hours}h {minutes}m {seconds}s"
    
    # Get recent activity (in a real app, this would come from a database)
    recent_activity = [
        {
            'type': 'login',
            'description': 'Logged in to the platform',
            'timestamp': login_time
        },
        {
            'type': 'course_view',
            'description': 'Viewed course: Introduction to Python',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    
    return render_template('dashboard.html', 
                           user=session['user'], 
                           preferences=session['preferences'],
                           enrolled_courses=enrolled_courses,
                           login_time=login_time,
                           session_duration=session_duration,
                           recent_activity=recent_activity)

@app.route('/courses')
@login_required
def course_list():
    return render_template('courses.html', courses=courses)

@app.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = next((c for c in courses if c['id'] == course_id), None)
    if course:
        # Track this page view in session
        if 'page_views' not in session:
            session['page_views'] = []
        
        session['page_views'].append({
            'page': f'course/{course_id}',
            'title': course['title'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Keep only the 10 most recent page views
        if len(session['page_views']) > 10:
            session['page_views'] = session['page_views'][-10:]
        
        return render_template('course_detail.html', course=course)
    else:
        flash('Course not found', 'error')
        return redirect(url_for('course_list'))

@app.route('/enroll/<int:course_id>')
@login_required
def enroll(course_id):
    user_email = session['user']['email']
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if course:
        if user_email not in course['enrolled']:
            course['enrolled'].append(user_email)
            flash(f'You have successfully enrolled in {course["title"]}', 'success')
            
            # Store enrollment in session
            if 'enrollments' not in session:
                session['enrollments'] = []
            
            session['enrollments'].append({
                'course_id': course_id,
                'course_title': course['title'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            flash('You are already enrolled in this course', 'info')
    else:
        flash('Course not found', 'error')
    
    return redirect(url_for('course_detail', course_id=course_id))

@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'POST':
        # Update user preferences in session
        session['preferences'] = {
            'theme': request.form.get('theme', 'light'),
            'notifications': 'notifications' in request.form,
            'language': request.form.get('language', 'english')
        }
        
        # In a real app, you would save these to the database
        user_email = session['user']['email']
        users[user_email]['preferences'] = session['preferences']
        
        flash('Your preferences have been updated', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('preferences.html', preferences=session['preferences'])

@app.route('/history')
@login_required
def history():
    page_views = session.get('page_views', [])
    enrollments = session.get('enrollments', [])
    
    return render_template('history.html', 
                           page_views=page_views, 
                           enrollments=enrollments)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if email in users:
            flash('Email already exists', 'error')
        else:
            # In a real app, password should be hashed before saving
            users[email] = {
                'password': password,
                'name': name,
                'role': 'student',
                'joined': datetime.now().strftime('%Y-%m-%d'),
                'preferences': {
                    'theme': 'light',
                    'notifications': True,
                    'language': 'english'
                }
            }
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.context_processor
def inject_user_data():
    """Make user data available to all templates"""
    if 'user' in session:
        return {
            'user': session['user'],
            'preferences': session.get('preferences', {})
        }
    return {'user': None, 'preferences': {}}

if __name__ == '__main__':
    app.run(debug=True)