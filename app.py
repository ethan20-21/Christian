from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Sample in-memory data (Dito muna ise-save habang wala pang database)
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Stallman"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Stallman"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# --- READ (List All) ---
@app.route('/')
@app.route('/students')
def list_students():
    html = """
    <h2>Student Management System (CRUD)</h2>
    <a href="/add_student_form"><b>+ Add New Student</b></a>
    <hr>
    <ul>
        {% for s in students %}
        <li>
            ID: {{s.id}} | <b>{{s.name}}</b> (Grade: {{s.grade}}, Section: {{s.section}})
            | <a href="/edit_student/{{s.id}}">Edit</a> 
            | <a href="/delete_student/{{s.id}}" onclick="return confirm('Sigurado ka ba?')">Delete</a>
        </li>
        {% endfor %}
    </ul>
    """
    return render_template_string(html, students=students)

# --- CREATE (Form & Action) ---
@app.route('/add_student_form')
def add_student_form():
    html = """
    <h2>Add New Student</h2>
    <form action="/add_student" method="POST">
        Name: <input type="text" name="name" required><br><br>
        Grade: <input type="number" name="grade" required><br><br>
        Section: <input type="text" name="section" required><br><br>
        <button type="submit">Save Student</button>
    </form>
    <br><a href="/students">Back to List</a>
    """
    return render_template_string(html)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")
    
    # Auto-increment ID logic
    new_id = max([s['id'] for s in students]) + 1 if students else 1
    
    new_student = {"id": new_id, "name": name, "grade": grade, "section": section}
    students.append(new_student)
    return redirect(url_for('list_students'))

# --- UPDATE (Edit Form & Action) ---
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]
        return redirect(url_for('list_students'))

    html = """
    <h2>Edit Student</h2>
    <form method="POST">
        Name: <input type="text" name="name" value="{{student.name}}"><br><br>
        Grade: <input type="number" name="grade" value="{{student.grade}}"><br><br>
        Section: <input type="text" name="section" value="{{student.section}}"><br><br>
        <button type="submit">Update</button>
    </form>
    <br><a href="/students">Back to List</a>
    """
    return render_template_string(html, student=student)

# --- DELETE ---
@app.route('/delete_student/<int:id>')
def delete_student(id):
    global students
    # Tatanggalin ang student na may kaparehong ID
    students = [s for s in students if s["id"] != id]
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(debug=True)