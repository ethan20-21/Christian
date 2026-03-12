from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample in-memory data
students = [
    {"id": 1, "name": "Juan Dela Cruz", "grade": 85, "section": "Stallman"},
    {"id": 2, "name": "Maria Clara", "grade": 90, "section": "Stallman"},
    {"id": 3, "name": "Pedro Penduko", "grade": 75, "section": "Zion"},
    {"id": 4, "name": "Sandro Magsaysay", "grade": 88, "section": "Zion"},
    {"id": 5, "name": "Teresa Magbanua", "grade": 98, "section": "Rizal"}
]

# --- THE PROFESSIONAL UI TEMPLATE ---
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
        .search-wrapper { position: relative; flex: 1; max-width: 400px; }
        .search-wrapper i { position: absolute; left: 15px; top: 50%; transform: translateY(-50%); color: var(--text-muted); }
        .search-input {
            width: 100%; padding: 12px 15px 12px 45px; background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--glass-border); border-radius: 10px; color: white; outline: none;
        }
        .btn {
            padding: 10px 20px; border-radius: 10px; border: none; cursor: pointer; color: white;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: inline-flex; align-items: center; gap: 8px; text-decoration: none; font-weight: 500;
        }
        .btn:hover { opacity: 0.9; }
        .btn-sm { padding: 6px 12px; font-size: 0.85rem; }
        .btn-icon { width: 35px; height: 35px; padding: 0; justify-content: center; border-radius: 8px; }
        .btn-edit { background: rgba(234, 179, 8, 0.2); color: #facc15; }
        .btn-delete { background: rgba(239, 68, 68, 0.2); color: #f87171; }
        
        table { width: 100%; border-collapse: collapse; }
        thead th { text-align: left; padding: 15px; color: var(--text-muted); font-weight: 500; border-bottom: 1px solid var(--glass-border); }
        tbody tr { border-bottom: 1px solid rgba(255, 255, 255, 0.05); transition: 0.2s; }
        tbody tr:hover { background: rgba(255, 255, 255, 0.03); }
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
                <div class="search-wrapper">
                    <i class="fa-solid fa-search"></i>
                    <input type="text" class="search-input" placeholder="Search students..." onkeyup="filterTable(this.value)">
                </div>
            </div>
            
            <div style="overflow-x:auto;">
                <table id="studentTable">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Section</th>
                            <th>Grade</th>
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

    <script>
        function filterTable(value) {
            const rows = document.getElementById('studentTable').getElementsByTagName('tr');
            for (let i = 1; i < rows.length; i++) {
                const name = rows[i].getElementsByTagName('td')[0].textContent.toLowerCase();
                const section = rows[i].getElementsByTagName('td')[1].textContent.toLowerCase();
                if (name.indexOf(value.toLowerCase()) > -1 || section.indexOf(value.toLowerCase()) > -1) {
                    rows[i].style.display = "";
                } else {
                    rows[i].style.display = "none";
                }
            }
        }
    </script>
</body>
</html>
"""

# UPDATED FORM HTML with dynamic action
form_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Manage Student</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background: #0f172a; color: white; font-family: 'Outfit', sans-serif;
            display: flex; align-items: center; justify-content: center; min-height: 100vh;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 40px;
            width: 100%; max-width: 450px; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }
        .form-control {
            background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1);
            color: white; margin-bottom: 20px; border-radius: 10px; padding: 12px;
        }
        .form-control:focus { background: rgba(0,0,0,0.5); color: white; box-shadow: none; border-color: #6366f1; }
        .btn-primary { background: linear-gradient(135deg, #6366f1, #a855f7); border: none; padding: 12px; width: 100%; border-radius: 10px; font-weight: 600; }
        .btn-link { color: #94a3b8; text-decoration: none; margin-top: 15px; display: inline-block; }
        .btn-link:hover { color: white; }
    </style>
</head>
<body>
    <div class="glass-card">
        <h2 class="mb-4 text-center">{{ title }}</h2>
        
        <!-- FIX IS HERE: Added 'action' attribute dynamically -->
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
        <a href="/" class="btn-link w-100 text-center"><i class="fa-solid fa-arrow-left"></i> Back to Dashboard</a>
    </div>
</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
@app.route('/students')
def list_students():
    return render_template_string(base_html, students=students)

@app.route('/add_student_form')
def add_student_form():
    return render_template_string(form_html, title="Add New Student", student=None)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")
    new_id = max([s['id'] for s in students]) + 1 if students else 1
    students.append({"id": new_id, "name": name, "grade": grade, "section": section})
    return redirect(url_for('list_students'))

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student: return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    return render_template_string(form_html, title="Edit Student", student=student)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(debug=True)