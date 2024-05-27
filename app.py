from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import TicketForm, EventForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:tt8l_04@localhost/event_management_system'
app.config['SECRET_KEY'] = 'ihopethiscanrun'
db = SQLAlchemy(app)

# Models
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(4), primary_key=True)
    admin_name = db.Column(db.String(100), nullable=False)
    admin_email = db.Column(db.String(100), nullable=False, unique=True)
    admin_phone = db.Column(db.String(11), nullable=False)
    admin_pwd = db.Column(db.String(50), nullable=False)
    admin_descr = db.Column(db.Text)
    stripeacc_id = db.Column(db.String(255), nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_descr = db.Column(db.Text, nullable=False)
    event_start = db.Column(db.Date, nullable=False)
    event_end = db.Column(db.Date)
    event_time = db.Column(db.Time, nullable=False)
    event_duration = db.Column(db.String(50), nullable=False)
    event_img = db.Column(db.LargeBinary)
    category_id = db.Column(db.String(3), db.ForeignKey('event_category.category_id'), nullable=False)
    eventvenue_id = db.Column(db.String(3), db.ForeignKey('event_venue.eventvenue_id'), nullable=False)
    location_details = db.Column(db.String(255))
    admin_id = db.Column(db.String(4), db.ForeignKey('admin.admin_id'), nullable=False)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    ticket_type = db.Column(db.String(50))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    member_discount = db.Column(db.Numeric(10, 2))
    max_quantity = db.Column(db.Integer)
    start_sale = db.Column(db.Date, nullable=False)
    end_sale = db.Column(db.Date)

class EventVenue(db.Model):
    __tablename__ = 'event_venue'
    eventvenue_id = db.Column(db.String(3), primary_key=True)
    location = db.Column(db.String(10), nullable=False)

class EventCategory(db.Model):
    __tablename__ = 'event_category'
    category_id = db.Column(db.String(3), primary_key=True)
    category = db.Column(db.String(30), nullable=False)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    form.event_cat.choices = [(cat.category_id, cat.category) for cat in EventCategory.query.all()]
    form.event_venue.choices = [(ven.eventvenue_id, ven.location) for ven in EventVenue.query.all()]

    if form.validate_on_submit():
        new_event = Event(
            event_name=form.event_name.data,
            event_descr=form.event_descr.data,
            event_start=form.event_start.data,
            event_end=form.event_end.data,
            event_time=form.event_time.data,
            event_duration=form.duration.data,
            event_img=form.event_img.data.read() if form.event_img.data else None,
            category_id=form.event_cat.data,
            eventvenue_id=form.event_venue.data,
            location_details=form.location_detail.data,
            admin_id='A001'  # Replace with dynamic admin ID
        )
        db.session.add(new_event)
        db.session.commit()

        for ticket_form in form.tickets:
            new_ticket = Ticket(
                event_id=new_event.event_id,
                ticket_type=ticket_form.ticket_type.data,
                price=ticket_form.price.data,
                member_discount=ticket_form.member_discount.data,
                max_quantity=ticket_form.max_quantity.data,
                start_sale=ticket_form.start_sale.data,
                end_sale=ticket_form.end_sale.data
            )
            db.session.add(new_ticket)
        db.session.commit()

        flash('Event and tickets created successfully!', 'success-create')
        return redirect(url_for('create_event'))

    return render_template('create_event.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)