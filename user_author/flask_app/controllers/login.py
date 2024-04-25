from flask_app import app
from flask import render_template, session, request, flash, redirect
from flask_app.models.user import User



@app.route('/')
def home():
    return render_template ('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    user = User.get_user_by_email(request.form["email"])
    if user is None or not User.verify_password(user, request.form["password"]):
        flash("Incorrect email or password!", "warning")
        return render_template("login.html")

    session["uid"] = user.id
    return redirect("/dashboard")

@app.route('/user/register', methods={'POST'})
def register():
    is_valid, errors = User.validate(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
        return render_template("login.html")

    if request.form["password"] != request.form.get("password_confirmation"):
        flash("Password and password confirmation must be equal!", "error")
        return render_template("login.html")

    User.save({
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': User.hash_password(request.form['password']),
    })
    user = User.get_user_by_email(request.form["email"])
    flash('Thank you for registering')

    @app.route('/logout')
    def logout():
      session.clear
      return redirect("/")