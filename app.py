from flask import Flask, render_template, request, redirect, url_for, session as flask_session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from database import db
from models import db, User, ChatHistory, Session
import requests
from flask import session


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            flask_session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('chat'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        flash('Please log in first')
        return redirect(url_for('login'))

    # Retrieve all sessions for the dropdown in the template
    sessions = Session.query.filter_by(user_id=session['user_id']).all()

    # Set a default session id if none is specified in the request
    current_session_id = request.args.get('session_id', type=int)
    if not current_session_id and sessions:
        current_session_id = sessions[0].id  # Default to the first session if none specified

    if request.method == 'POST':
        user_input = request.form['user_input']
        # Fetch current session ID from form data
        current_session_id = request.form.get('session_id', type=int)
        
        # Get ChatGPT response
        bot_response = get_chatgpt_response(user_input)
        
        # Save chat history in the database linked to the current session
        chat = ChatHistory(user_id=session['user_id'], session_id=current_session_id, message=user_input, response=bot_response)
        db.session.add(chat)
        db.session.commit()
    
    # Retrieve chat history for the current session
    history = ChatHistory.query.filter_by(user_id=session['user_id'], session_id=current_session_id).all()
    return render_template('chat.html', history=history, sessions=sessions, current_session_id=current_session_id)

@app.route('/create_session', methods=['POST'])
def create_session():
    if 'user_id' not in session:
        flash('Please log in first')
        return redirect(url_for('login'))

    session_name = request.form.get('session_name')
    if session_name:
        new_session = Session(name=session_name, user_id=session['user_id'])
        db.session.add(new_session)
        db.session.commit()
        flash('New session created!')
    else:
        flash('Session name is required.')

    return redirect(url_for('chat'))

@app.route('/logout')
def logout():
    flask_session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

def get_chatgpt_response(message):
    headers = {
        'Authorization': f'Bearer {Config.OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'ft:gpt-4o-2024-08-06:personal:bipolar-finetuned14:BQNdmKFB', #ft:gpt-4o-2024-08-06:personal:bipolar-finetuned8:AoTvbLlx  #'gpt-4o'
        'messages': [{"role": "user", "content": message}]
    }
    try:
        response = requests.post('https://api.openai.com/v1/chat/completions', json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenAI API: {e}")
        return "Sorry, I'm having trouble responding right now."


if __name__ == '__main__':
    app.run(debug=True)
