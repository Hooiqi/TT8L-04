from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, DateTimeField, SelectField, FileField, FieldList, FormField, DecimalField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

class TicketForm(FlaskForm):
    ticket_type = StringField('Ticket Type', validators=[DataRequired()], render_kw={"placeholder": "Ticket type (required)"})
    price = DecimalField('Price', validators=[DataRequired()])
    member_discount = DecimalField('Member Price', validators=[Optional()])
    max_quantity = IntegerField('Quantity', validators=[DataRequired()])
    start_sale = DateField('Start Sale', validators=[DataRequired()])
    end_sale = DateField('End Sale', validators=[DataRequired()])

    def validate_end_sale(self, filed):
        if filed.data <= self.start_sale.data:
            raise ValidationError('End sale date should be more than start sale date.')

class EventForm(FlaskForm):
    event_name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Event name (required)"})
    event_cat = SelectField('Category', choices=[('C01', 'Academic'), ('C02', 'Entertainments'), ('C03', 'Sports'), ('C04', 'Others')], validators=[DataRequired()])
    event_start = DateField('Start Date', validators=[DataRequired()])
    event_end = DateField('End Date', validators=[DataRequired()])
    event_time = TimeField('Start Time', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()], render_kw={"placeholder": "hour / minute (required)"})
    event_img = FileField('Poster (max. file size 16MB)', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png'])])
    event_descr = TextAreaField('Description', validators=[DataRequired()], render_kw={"placeholder": "Event details (required)"})
    event_venue = SelectField('Location type', choices=[('V01', 'On campus'), ('V02', 'Off campus'), ('V03', 'Online')], validators=[DataRequired()])
    location_detail = StringField('Location details',  validators=[DataRequired()], render_kw={"placeholder": "Location details (required)"})
    tickets = FieldList(FormField(TicketForm), min_entries=1)

    def validate_event_end(self, filed):
        if filed.data < self.event_start.data:
            raise ValidationError('Event end date should be more than or equal to start date.')