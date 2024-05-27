from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, DateTimeField, SelectField, FileField, FieldList, FormField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length

class TicketForm(FlaskForm):
    ticket_type = StringField('Ticket Type', validators=[DataRequired()], render_kw={"placeholder": "Ticket type"})
    price = DecimalField('Price', validators=[DataRequired()])
    member_discount = DecimalField('Member Price')
    max_quantity = IntegerField('Quantity', validators=[DataRequired()])
    start_sale = DateField('Start Sale', validators=[DataRequired()])
    end_sale = DateField('End Sale', validators=[DataRequired()])

class EventForm(FlaskForm):
    event_name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Event name"})
    event_cat = SelectField('Category', choices=[('C01', 'Academic'), ('C02', 'Entertainments'), ('C03', 'Sports'), ('C04', 'Social'), ('C05', 'Others')], validators=[DataRequired()])
    event_start = DateField('Start Date', validators=[DataRequired()])
    event_end = DateField('End Date')
    event_time = TimeField('Start Time', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()], render_kw={"placeholder": "hour / minute"})
    event_img = FileField('Poster')
    event_descr = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Event details"})
    event_venue = SelectField('Location type', choices=[('V01', 'On campus'), ('V02', 'Off campus'), ('V03', 'Online')], validators=[DataRequired()])
    location_detail = StringField('Location details', render_kw={"placeholder": "Location details"})
    tickets = FieldList(FormField(TicketForm), min_entries=1)