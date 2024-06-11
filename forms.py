from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, DateTimeField, SelectField, PasswordField, FieldList, FormField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Optional, EqualTo, Length, NumberRange, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask import flash
from models import User

class SignupForm(FlaskForm):
    user_id = StringField('Student ID', validators=[DataRequired(), Length(min=10,max=10)], render_kw={"placeholder": "Student ID"})
    user_name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    user_email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    user_phone = StringField('Phone number', validators=[DataRequired(), Length(min=10,max=11)], render_kw={"placeholder": "Phone Number (without -)"})
    user_pwd = PasswordField('Password ', validators=[DataRequired(), EqualTo('confirm_pwd', message='Both password must match. ')], render_kw={"placeholder": "Password"})
    confirm_pwd = PasswordField('Confirm Password: ', validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
    signup_submit = SubmitField('Sign up')

    def validate_user_id(self, user_id):
        # Check if the user ID already exists in the database
        if User.query.filter_by(user_id=user_id.data).first():
            raise ValidationError("This student ID already exists.")

    def validate_user_email(self, user_email):
        # Check if the email matches the required format
        if user_email.data != f"{self.user_id.data}@student.mmu.edu.my":
            raise ValidationError('Email must be in the format: student_id@student.mmu.edu.my')
        
class TicketForm(FlaskForm):
    ticket_type = StringField('Ticket Type', validators=[DataRequired()], render_kw={"placeholder": "Ticket type*"})
    price = DecimalField('Normal Price', validators=[InputRequired(), NumberRange(min=0)], render_kw={"placeholder": "Normal price*"})
    member_discount = DecimalField('Member Price', validators=[InputRequired(), NumberRange(min=0)], render_kw={"placeholder": "Member price"})
    max_quantity = IntegerField('Quantity', validators=[DataRequired()], render_kw={"placeholder": "Quantity*"})
    start_sale = DateField('Start Sale', validators=[DataRequired()])
    end_sale = DateField('End Sale', validators=[DataRequired()])

    def validate_end_sale(self, filed):
        if filed.data <= self.start_sale.data:
            raise ValidationError('Tickets end sale date should be later than start sale date')

class EventForm(FlaskForm):
    event_name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Event name*"})
    event_cat = SelectField('Category', choices=[('C01', 'Academic'), ('C02', 'Entertainments'), ('C03', 'Sports'), ('C04', 'Others')], validators=[DataRequired()])
    event_start = DateField('Start Date', validators=[DataRequired()])
    event_end = DateField('End Date', validators=[DataRequired()])
    event_time = TimeField('Start Time', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()], render_kw={"placeholder": "hour / minute *"})
    event_img = FileField('Poster', validators=[FileAllowed(['jpg','jpeg','png'], 'Image format only accepts jpeg, jpg or png')])
    event_descr = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Event details*"})
    event_venue = SelectField('Location type', choices=[('V01', 'On campus'), ('V02', 'Off campus'), ('V03', 'Online')], validators=[DataRequired()])
    location_detail = StringField('Location/Platform',  validators=[DataRequired()], render_kw={"placeholder": "Details*"})
    tickets = FieldList(FormField(TicketForm), min_entries=1)
    publish_status = StringField('Publish Status')

    def validate_event_end(self, filed):
        if filed.data < self.event_start.data:
            raise ValidationError('Event end date should be later than or the same as start date')
        