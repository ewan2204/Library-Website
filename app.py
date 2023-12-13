from database import get_books, get_book, loan_book, create_user, get_user
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

#
import datetime
import sqlite3


app = Flask(__name__)
app.secret_key = "Generate Secret Key Here"

# Load sqlite database
db = sqlite3.connect('database.db')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		password = generate_password_hash(request.form.get('password'))
		create_user(first_name, last_name, email, password)
		return redirect(url_for('login'))
	return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user(request.form.get('email'))
        if user and check_password_hash(user['password'], request.form.get('password')):
            print("User logged in")
            session['user'] = user
            return redirect(url_for('index'))
        print("Incorrect email or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



@app.route('/reserve/<int:book_id>', methods=['POST', 'GET'])
def borrow(book_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    book = get_book(book_id)
    if book and book['on_loan_until'] == "Not On Loan":
        loan_book(book_id, session['user']['id'])
    return redirect(url_for('index'))


@app.route('/', methods=['POST', 'GET'])
def index():
	print(f'filter: {request.form.get("filter", "all")}')
	filter = request.form.get('filter', 'all')
	books = get_books(filter)
	return render_template('booktable.html', books=books)


@app.route('/book/<int:book_id>', methods=['POST', 'GET'])
def book(book_id):
	# Calculate the date a week from now
	date_in_two_weeks = datetime.datetime.now() + datetime.timedelta(days=7)
	date_string = date_in_two_weeks.strftime('%Y-%m-%d')
	book = get_book(book_id)
	return render_template('book.html', book=book, date_in_a_week=date_string)


if __name__ == '__main__':
    app.run(debug=True)
