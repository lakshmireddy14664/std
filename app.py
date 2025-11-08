from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ******* Database Configuration ******
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ******* Model Definition ******
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

with app.app_context():
        db.create_all()
# ******* Routes ******

@app.route('/')
def home():
    students = Students.query.all()
    return render_template('index.html', students=students)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        class_name = request.form['class']
        email = request.form['email']

        new_student = Students(name=name, roll=roll, student_class=class_name, email=email)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

# ✅ Supports inline editing (AJAX/JSON) and traditional form update
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Students.query.get_or_404(id)

    # Handle inline edit (JSON request)
    if request.is_json:
        data = request.get_json()
        student.name = data.get('name', student.name)
        student.roll = data.get('roll', student.roll)
        student.student_class = data.get('class', student.student_class)
        student.email = data.get('email', student.email)
        db.session.commit()
        return jsonify({'success': True})

    # Handle normal form update
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll = request.form['roll']
        student.student_class = request.form['class']
        student.email = request.form['email']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Students.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    
    app.run(debug=True)
