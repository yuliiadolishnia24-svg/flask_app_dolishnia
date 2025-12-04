from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional

# --- Форма з першого завдання (не видаляємо)
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone")
    subject = StringField("Subject")
    message = StringField("Message")
    submit = SubmitField("Send")

# --- НОВА форма для login
class LoginForm(FlaskForm):
    username = StringField(
        "Username / Email",
        validators=[DataRequired(message="Це поле обов'язкове")]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Field must be between 4 and 10 characters long."),
            Length(min=4, max=10, message="Field must be between 4 and 10 characters long.")
        ]
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")