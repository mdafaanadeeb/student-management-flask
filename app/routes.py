from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Student, User
from app import db
from app.ai_engine import analyze_performance

main = Blueprint("main", __name__)


@main.route("/")
@login_required
def dashboard():
    search = request.args.get("search")
    sort = request.args.get("sort")

    students = Student.query.all()

    if search:
        students = [s for s in students if search.lower() in s.name.lower()]

    if sort == "gpa":
        students = sorted(students, key=lambda x: x.gpa, reverse=True)

    total = len(students)
    avg_gpa = round(sum(s.gpa for s in students) / total, 2) if total > 0 else 0

    return render_template(
        "dashboard.html",
        students=students,
        total=total,
        avg_gpa=avg_gpa,
        analyze=analyze_performance
    )


@main.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        student = Student(
            name=request.form["name"],
            email=request.form["email"],
            branch=request.form["branch"],
            roll_no=request.form["roll_no"],
            section=request.form["section"],
            gpa=float(request.form["gpa"]),
        )

        db.session.add(student)
        db.session.commit()

        flash("Student Added Successfully")
        return redirect(url_for("main.dashboard"))

    return render_template("add_student.html")


@main.route("/delete/<int:id>")
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student Deleted")
    return redirect(url_for("main.dashboard"))


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form["username"])
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        flash("User Registered")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid Credentials")

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))