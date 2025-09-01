# 💰 Expense Tracker

A simple **Flask-based expense tracker** with budget management, category insights, and daily spending trends. It uses **SQLite** for storage and **Chart.js** for data visualization.

---

## 🚀 Features

- Add, view, and delete expenses
- Set and update a budget
- Track spending progress against the budget
- Filter expenses by:
  - **Today**
  - **Last 7 days**
  - **Last 30 days**
  - **Custom date range**
- Visualize:
  - Spending by category (pie/donut chart)
  - Daily spending trends (line/bar chart)

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (`expenses.db`)
- **Frontend:** HTML, Tailwind CSS, Chart.js (for charts)

---

## 📂 Project Structure

```
.
├── app.py          # Main Flask app
├── expenses.db     # SQLite database
├── templates/
│   └── index.html  # Main UI
├── static/
│   ├── style.css   # Custom styles (if added)
│   └── ...         # JS/CSS assets
```

---
## 📊 Usage

1. Open the app in your browser.
2. Set your budget.
3. Add expenses with title, amount, category, and date.
4. View progress bar and charts for insights.
5. Delete unwanted entries.

---
