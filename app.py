from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sql12671039:JqL9KQLQvb@sql12.freesqldatabase.com:3306/sql12671039'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Ishu1234@$%'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



with app.app_context():
    db.create_all()




@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()

        # Check if the user exists
        if user:
            # Fetch only expenses associated with the current user
            expenses = Expense.query.filter_by(user_id=user.id).all()
            return render_template('dashboard.html', username=username, expenses=expenses)

    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Use SQLAlchemy for database queries instead of the incorrect MySQL cursor
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='No Account found with these credentials!!')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('login.html', error='Username already exists. Please choose another username.')

        # Create a new user
        new_user = User(username=username, password=password)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page (you can change this to any other route)
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        username = session.get('username')

        # Fetch the user from the database
        user = User.query.filter_by(username=username).first()

        # Create a new expense associated with the user
        new_expense = Expense(name=name, amount=amount, user_id=user.id)

        # Add the expense to the database
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_expense.html')   

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


