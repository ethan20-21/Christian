from flask import Flask, request, render_template_string, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# Kukunin ang DATABASE_URL mula sa Render Environment Variables
db_url = os.environ.get('DATABASE_URL')

# Fix para sa "postgres://" vs "postgresql://"
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50), nullable=False)

# Gagawa ng tables sa PostgreSQL kung wala pa
with app.app_context():
    db.create_all()

# --- THE PROFESSIONAL UI TEMPLATES ---
base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1; --secondary: #a855f7; --accent: #ec4899;
            --dark-bg: #0f172a; --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1); --text-main: #f8fafc; --text-muted: #94a3b8;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Outfit', sans-serif; }
        body {
            background-color: var(--dark-bg);
            background-image: radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
            min-height: 100vh; color: var(--text-main); padding-bottom: 50px;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;
            background: var(--glass-bg); backdrop-filter: blur(16px); border: 1px solid var(--glass-border);
            border-radius: 16px; padding: 20px;
        }
        .brand { display: flex; align-items: center; gap: 15px; }
        .brand i { font-size: 1.8rem; background: linear-gradient(45deg, var(--primary), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .main-card {
            background: var(--glass-bg); backdrop-filter: blur(16px); border: 1px solid var(--glass-border);
            border-radius: 20px; padding: 25px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .toolbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; flex-wrap: wrap; gap: 15px; }
        .btn {
            padding: 10px 20px; border-radius: 10px; border: none; cursor: pointer; color: white;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: inline-flex; align-items: center; gap: 8px; text-decoration: none; font-weight: 500;
        }
        .btn-sm { padding: 6px 12px; font-size: 0.85rem; }
        .btn-icon { width: 35px; height: 35px; padding: 0; justify-content: center; border-radius: 8px; }
        .btn-edit { background: rgba(234, 179, 8, 0.2); color: #facc15; }
        .btn-delete { background: rgba(239, 68, 68, 0.2); color: #f87171; }
        table { width: 100%; border-collapse: collapse; }
        thead th { text-align: left; padding: 15px; color: var(--text-muted); font-weight: 500; border-bottom: 1px solid var(--glass-border); }
        tbody tr { border-bottom: 1px solid rgba(255, 255, 255, 0.05); transition: 0.2s; }
        td { padding: 15px; vertical-align: middle; }
        .badge { padding: 5px 10px; border-radius: 20px; font-size: 0.75rem; background: rgba(255,255,255,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="brand">
                <i class="fa-solid fa-graduation-cap"></i>
                <h1>EduManager</h1>
            </div>
            <a href="/add_student_form" class="btn"><i class="fa-solid fa-plus"></i> New Student</a>
        </header>
        <div class="main-card">
            <div class="toolbar">
                <h2>Records</h2>
            </div>
            <div style="overflow-x:auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Section</th>
                            <th>Grade</th>
                            <th>Remarks</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in students %}
                        <tr>
                            <td><b>{{s.name}}</b><br><small style="color:var(--text-muted)">ID: {{s.id}}</small></td>
                            <td><span class="badge">{{s.section}}</span></td>
                            <td>{{s.grade}}</td>
                            <td>
                                {% if s.grade >= 75 %}
                                <span class="badge" style="background: rgba(34, 197, 94, 0.2); color: #4ade80;">Pass</span>
                                {% else %}
                                <span class="badge" style="background: rgba(239, 68, 68, 0.2); color: #f87171;">Fail</span>
                                {% endif %}
                            </td>
                            <td>
                                <a href="/edit_student/{{s.id}}" class="btn btn-sm btn-icon btn-edit"><i class="fa-solid fa-pen"></i></a>
                                <a href="/delete_student/{{s.id}}" class="btn btn-sm btn-icon btn-delete" onclick="return confirm('Delete this record?')"><i class="fa-solid fa-trash"></i></a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
"""

form_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Manage Student</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #0f172a; color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 40px; width: 100%; max-width: 450px; }
        .form-control { background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); color: white; margin-bottom: 20px; }
        .form-control:focus { background: rgba(0,0,0,0.5); color: white; border-color: #6366f1; box-shadow: none; }
        .btn-primary { background: linear-gradient(135deg, #6366f1, #a855f7); border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: 600; }
    </style>
</head>
<body>
    <div class="glass-card">
        <h2 class="mb-4 text-center">{{ title }}</h2>
        <form method="POST" action="{% if student %}/edit_student/{{ student.id }}{% else %}/add_student{% endif %}">
            <label>Full Name</label>
            <input type="text" name="name" class="form-control" value="{{ student.name if student else '' }}" required>
            <label>Section</label>
            <input type="text" name="section" class="form-control" value="{{ student.section if student else '' }}" required>
            <label>Grade</label>
            <input type="number" name="grade" class="form-control" value="{{ student.grade if student else '' }}" required>
            <button type="submit" class="btn btn-primary mt-3">
                <i class="fa-solid fa-save"></i> {{ 'Update' if student else 'Save' }} Record
            </button>
        </form>
        <a href="/" class="btn-link d-block text-center mt-3 text-secondary text-decoration-none">Cancel</a>
    </div>
</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
@app.route('/students')
def list_students():
    # Kukuha ng records mula sa PostgreSQL
    all_students = Student.query.order_by(Student.id.asc()).all()
    return render_template_string(base_html, students=all_students)

@app.route('/add_student_form')
def add_student_form():
    return render_template_string(form_html, title="Add New Student", student=None)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")
    
    # Save sa Database
    new_student = Student(name=name, grade=grade, section=section)
    db.session.add(new_student)
    db.session.commit()
    
    return redirect(url_for('list_students'))

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form["name"]
        student.grade = int(request.form["grade"])
        student.section = request.form["section"]
        db.session.commit()
        return redirect(url_for('list_students'))

    return render_template_string(form_html, title="Edit Student", student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(debug=True)
