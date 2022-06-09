from flask_app import app
from flask import Flask, redirect, render_template, request, session
from flask_app.model.students_model import Students
from flask_app.model.subjects_model import Subjects
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/main')
def main():
    subject = Subjects.get_subject()
    return render_template("main.html", all_subjects = subject)

#register
@app.route('/register_user', methods=['POST'])
def register_user():
    if not Students.validate_registration(request.form):
        return redirect('/home')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "fullname":request.form['fullname'],
        "course":request.form['course'],
        "email":request.form['email'],
        "password":pw_hash
    }
    Students.register_student(data)
    return redirect('/home')

#login
@app.route('/login_user', methods=['POST'])
def login_user():
    if not Students.validate_login(request.form):
        return redirect('/home')
    data = {
        "email":request.form['email'],
        "password":request.form['password']
    }
    student = Students.verify_student(data)
    if not student:
        flash ('Wrong email or password')
        return redirect('/home')
    if not bcrypt.check_password_hash(student.password, request.form['password']):
        flash ('Wrong email or password')
        return redirect('/home')

    session['student_id'] = student.id
    session['fullname'] = student.fullname
    return redirect('/main')

#add route
@app.route('/enroll_subjects' , methods=['POST'])
def enroll_subjects():
    data = {
        "course_code":request.form['course_code'],
        "description":request.form['course_description'],
        "semester_offered":request.form['semester'],
        "student_id":session['student_id']
    }
    Subjects.add_subject(data)
    flash('Subject successfully added!')
    return redirect('/main')

#edit route
@app.route('/edit_subject/<id>')
def edit_subject(id):
    data = {
        "id":id
    }
    subject = Subjects.edit_subject(data)
    return render_template("update.html", all_subjects = subject)

#view route
@app.route('/view_subject/<id>')
def view_subject(id):
    data = {
        "id":id
    }
    subject = Subjects.view_subject(data)
    return render_template("view.html", all_subjects = subject)


#delete route
@app.route('/delete_subject/<id>')
def delete_subject(id):
    data = {
        "id": id
    }
    Subjects.delete_subject(data)
    return redirect('/main')
#update route
@app.route('/update_subject', methods=['POST'])
def update_subject():
    data = {
        "course_code":request.form['course_code'],
        "description":request.form['course_description'],
        "semester_offered":request.form['semester'],
        "id":request.form['id']
    }
    Subjects.update_subject(data)
    flash("Record Updated!")
    return redirect('/main')
