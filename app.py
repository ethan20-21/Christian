from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample in-memory data
students = [
    {"id": 1, "name": "Juan Dela Cruz", "grade": 85, "section": "Stallman"},
    {"id": 2, "name": "Maria Clara", "grade": 90, "section": "Stallman"},
    {"id": 3, "name": "Pedro Penduko", "grade": 75, "section": "Zion"}
]

# CSS para sa Glassmorphism UI
common_css = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: white;
        padding: 20px;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .table { color: white; }
    .btn-glass {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.4);
        color: white;
        transition: 0.3s;
    }
    .btn-glass:hover {
        background: white;
        color: #764ba2;
    }
    input.form-control {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
    }
    input.form-control:focus {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        box-shadow: none;
        border-color: white;
    }
</style>
"""

# --- READ (Main Page) ---
@app.route('/')
@app.route('/students')
def list_students():
    html = common_css + """
    <div class="container mt-5">
        <div class="glass-card">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2>🎓 Student Management</h2>
                <a href="/add_student_form" class="btn btn-glass">+ Add Student</a>
            </div>
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Grade</th>
                        <th>Section</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for s in students %}
                    <tr>
                        <td>{{s.id}}</td>
                        <td><b>{{s.name}}</b></td>
                        <td><span class="badge bg-info">{{s.grade}}</span></td>
                        <td>{{s.section}}</td>
                        <td>
                            <a href="/edit_student/{{s.id}}" class="btn btn-sm btn-warning">Edit</a>
                            <a href="/delete_student/{{s.id}}" class="btn btn-sm btn-danger" onclick="return confirm('Sigurado ka ba?')">Delete</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    """
    return render_template_string(html, students=students)

# --- CREATE (Add Form) ---
@app.route('/add_student_form')
def add_student_form():
    html = common_css + """
    <div class="container mt-5">
        <div class="glass-card mx-auto" style="max-width: 500px;">
            <h3>Add New Student</h3>
            <form action="/add_student" method="POST">
                <div class="mb-3">
                    <label>Full Name</label>
                    <input type="text" name="name" class="form-control" placeholder="Juan Dela Cruz" required>
                </div>
                <div class="mb-3">
                    <label>Grade</label>
                    <input type="number" name="grade" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label>Section</label>
                    <input type="text" name="section" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success w-100">Save Record</button>
                <a href="/students" class="btn btn-link w-100 mt-2 text-white text-decoration-none">Back to List</a>
            </form>
        </div>
    </div>
    """
    return render_template_string(html)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")
    new_id = max([s['id'] for s in students]) + 1 if students else 1
    students.append({"id": new_id, "name": name, "grade": grade, "section": section})
    return redirect(url_for('list_students'))

# --- UPDATE (Edit Form) ---
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student: return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    html = common_css + """
    <div class="container mt-5">
        <div class="glass-card mx-auto" style="max-width: 500px;">
            <h3>Edit Student Record</h3>
            <form method="POST">
                <div class="mb-3">
                    <label>Name</label>
                    <input type="text" name="name" class="form-control" value="{{student.name}}">
                </div>
                <div class="mb-3">
                    <label>Grade</label>
                    <input type="number" name="grade" class="form-control" value="{{student.grade}}">
                </div>
                <div class="mb-3">
                    <label>Section</label>
                    <input type="text" name="section" class="form-control" value="{{student.section}}">
                </div>
                <button type="submit" class="btn btn-warning w-100">Update Record</button>
                <a href="/students" class="btn btn-link w-100 mt-2 text-white text-decoration-none">Cancel</a>
            </form>
        </div>
    </div>
    """
    return render_template_string(html, student=student)

# --- DELETE ---
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(debug=True)