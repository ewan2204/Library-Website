import datetime
import sqlite3


def get_books(filter: str) -> [dict]:
    if filter == 'available':
        return get_available_books()
    elif filter == 'loaned':
        return get_loaned_books()
    elif filter == 'returningToday':
        return get_returning_books()
    else:
        return get_all_books()

def get_book(book_id: int) -> dict:
	connect = sqlite3.connect('database.db')

	connect.row_factory = sqlite3.Row
	cursor = connect.cursor()

	cursor.execute("""
		SELECT 
			b.title,
			b.description,
			CASE
				WHEN bl.end IS NOT NULL AND DATE('now') BETWEEN bl.start AND bl.end THEN date(bl.end)
				ELSE "Not On Loan"
			END AS on_loan_until,
			b.image_location,
			b.id AS bookid
		FROM
		books AS b
		LEFT JOIN
		(
			SELECT DISTINCT *
			FROM book_loans
			WHERE DATE('now') BETWEEN start AND end
		) AS bl ON b.id = bl.book_id
		WHERE id = ?;
		""", (book_id,))
	row = cursor.fetchone()
	connect.close()
	if row:
		row = dict(row)
		loan_details = get_loan_details(book_id)
		if loan_details:
			row.update(loan_details)
			loaner_details = get_user_by_id(loan_details['user_id'])
			if(loaner_details):
				row.update(loaner_details)
		return row
	else:
		return None

# Makes assumption that book exists and user can loan it.
def loan_book(book_id: int, user_id: int) -> None:
	connect = sqlite3.connect('database.db')
	cursor = connect.cursor()
	cursor.execute('INSERT INTO book_loans (book_id, user_id, start, end) VALUES (?, ?, DATE("now"), DATE("now", "+7 days"))', (book_id, user_id))
	connect.commit()
	connect.close()

def create_user(first_name: str, last_name: str, email: str, password: str) -> None:
	connect = sqlite3.connect('database.db')
	cursor = connect.cursor()
	cursor.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)', (first_name, last_name, email, password))
	connect.commit()
	connect.close()
 
# Makes assumption that email is unique.
def get_user(email: str) -> dict:
	connect = sqlite3.connect('database.db')
	connect.row_factory = sqlite3.Row
	cursor = connect.cursor()
	cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
	row = cursor.fetchone()
	connect.close()
	if row:
		return dict(row)
	else:
		return None

def get_user_by_id(user_id: int) -> dict:
	connect = sqlite3.connect('database.db')
	connect.row_factory = sqlite3.Row
	cursor = connect.cursor()
	cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
	row = cursor.fetchone()
	connect.close()
	if row:
		return dict(row)
	else:
		return None



def get_loan_details(book_id: int) -> dict:
	connect = sqlite3.connect('database.db')
	connect.row_factory = sqlite3.Row
	cursor = connect.cursor()
	cursor.execute('SELECT * FROM book_loans WHERE book_id = ? ORDER BY end', (book_id,))
	row = cursor.fetchone()
	connect.close()
	if row:
		return dict(row)
	else:
		return None




def get_all_books() -> [dict]:
    connect = sqlite3.connect('database.db')
    # This enables column access by name: row['column_name']
    connect.row_factory = sqlite3.Row
    cursor = connect.cursor()

    cursor.execute("""
    SELECT 
		b.title,
		b.description,
		CASE
			WHEN bl.end IS NOT NULL AND DATE('now') BETWEEN bl.start AND bl.end THEN date(bl.end)
			ELSE "Not On Loan"
		END AS on_loan_until,
		b.image_location,
		b.id AS bookid
    FROM
    books AS b
	LEFT JOIN
    (
        SELECT DISTINCT *
        FROM book_loans
        WHERE DATE('now') BETWEEN start AND end
    ) AS bl ON b.id = bl.book_id;""")
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    books = [dict(row) for row in rows]
    connect.close()
    return books


def get_loaned_books() -> [dict]:
	all_books = get_all_books()
	loaned_books = [row for row in all_books if row['on_loan_until'] != 'Not On Loan']
	return loaned_books

def get_available_books() -> [dict]:
	all_books = get_all_books()
	avaliable_books = [row for row in all_books if row['on_loan_until'] == 'Not On Loan']
	return avaliable_books

def get_returning_books() -> [dict]:
	all_books = get_all_books()
	returning_books = [book for book in all_books if book['on_loan_until'] != "Not On Loan" and datetime.datetime.strptime(
                book['on_loan_until'], "%Y-%m-%d") <= datetime.datetime.now() + datetime.timedelta(days=1)]
	return returning_books
