from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL
        )
    ''')
    # Initialize default budget if none exists
    c.execute("SELECT COUNT(*) FROM budget")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO budget (id, amount) VALUES (1, 1000)")
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if request.method == 'POST':
        max_budget = float(request.form.get('max_budget', 0))
        c.execute("UPDATE budget SET amount = ? WHERE id = 1", (max_budget,))
        conn.commit()
        flash('Budget updated!', 'info')
        return redirect(url_for('index'))

    # Filtering expenses by date
    filter_type = request.args.get('filter', 'all')
    from_date = request.args.get('from')
    to_date = request.args.get('to')

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if filter_type == 'today':
        today = datetime.now().strftime('%Y-%m-%d')
        query += " AND date = ?"
        params.append(today)
    elif filter_type == 'week':
        start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        query += " AND date >= ?"
        params.append(start)
    elif filter_type == 'month':
        start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        query += " AND date >= ?"
        params.append(start)
    elif filter_type == 'custom' and from_date and to_date:
        query += " AND date BETWEEN ? AND ?"
        params += [from_date, to_date]

    c.execute(query, params)
    expenses = c.fetchall()

    # Get budget
    c.execute("SELECT amount FROM budget WHERE id = 1")
    budget_row = c.fetchone()
    budget = budget_row[0] if budget_row else 0

    total = sum([e[2] for e in expenses])  # sum amounts from filtered expenses
    percent_used = (total / budget * 100) if budget else 0

    # Data for charts
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_data = c.fetchall()
    categories = [row[0] for row in category_data]
    category_totals = [row[1] for row in category_data]

    c.execute("SELECT date, SUM(amount) FROM expenses GROUP BY date ORDER BY date")
    daily_data = c.fetchall()
    daily_dates = [row[0] for row in daily_data]
    daily_sums = [row[1] for row in daily_data]

    conn.close()

    return render_template('index.html',
                           expenses=expenses,
                           total=total,
                           budget=budget,
                           percent_used=percent_used,
                           categories=categories,
                           category_totals=category_totals,
                           daily_dates=daily_dates,
                           daily_sums=daily_sums)


@app.route('/add', methods=['POST'])
def add_expense():
    title = request.form['title']
    amount = float(request.form['amount'])
    category = request.form['category']
    date = request.form['date']

    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
              (title, amount, category, date))
    conn.commit()
    conn.close()
    return redirect(url_for('index', added=1))


@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index', deleted=1))


if __name__ == '__main__':
    app.run(debug=True)
