from flask import Flask, render_template, redirect, url_for, session, flash
from forms import ContactForm, LoginForm

app = Flask(__name__)
app.secret_key = "very_secret_key"


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        flash("Форма успішно відправлена!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", form=form)


# ---------------- LOGIN -----------------

USER = {"username": "user1", "password": "12345"}

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if username == USER["username"] and password == USER["password"]:
            session["user"] = username

            msg = " (remember=yes)" if form.remember.data else ""
            flash("Login successful!" + msg, "success")

            return redirect(url_for("profile"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/profile")
def profile():
    if "user" not in session:
        flash("You must log in first", "error")
        return redirect(url_for("login"))

    return render_template("profile.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You are logged out", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
