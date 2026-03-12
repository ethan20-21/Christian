from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    grade = int(request.args.get('grade', 0))

    remarks = "Pass" if grade >= 75 else "Fail"

    return jsonify({
        "name": "Juan",
        "grade": grade,
        "section": "Zechariah",
        "remarks": remarks
    })

if __name__ == '__main__':
    app.run(debug=True)