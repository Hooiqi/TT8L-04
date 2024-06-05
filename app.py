from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import TicketForm, EventForm, SignupForm
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:tt8l_04@localhost/event_management_system'
app.config['SECRET_KEY'] = 'ihopethiscanrun'
db.init_app(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

#route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.user_pwd.data).decode('utf-8')
        new_user = User(
            user_id=form.user_id.data,
            user_name=form.user_name.data,
            user_email=form.user_email.data,
            user_phone=form.user_phone.data,
            user_pwd=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        flash('User created successfully!', 'success-create')
        return redirect(url_for('signup'))

    return render_template('Signuppage.html', form=form)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    form.event_cat.choices = [("", "--Select an event category--")]+[(cat.category_id, cat.category) for cat in EventCategory.query.all()]
    form.event_venue.choices = [("", "--Select a location category--")]+[(ven.eventvenue_id, ven.location) for ven in EventVenue.query.all()]

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

        flash('Event and tickets created successfully!', 'success')
        return redirect(url_for('create_event'))

    return render_template('create_event.html', form=form)

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)  # Prepopulate the form with event data
    form.event_cat.choices = [("", "--Select an event category--")] + [(cat.category_id, cat.category) for cat in EventCategory.query.all()]
    form.event_venue.choices = [("", "--Select a location category--")] + [(ven.eventvenue_id, ven.location) for ven in EventVenue.query.all()]

    # Set the current value for the SelectField
    form.event_cat.data = event.category_id
    form.event_venue.data = event.eventvenue_id
    
    # Create a dictionary to hold ticket data
    ticket_data = {}
    for ticket in event.tickets:
        ticket_data[ticket.ticket_id] = {
            'ticket_type': ticket.ticket_type,
            'price': ticket.price,
            'member_discount': ticket.member_discount,
            'max_quantity': ticket.max_quantity,
            'start_sale': ticket.start_sale,
            'end_sale': ticket.end_sale,
        }

    if form.validate_on_submit():
        # Update event details
        event.event_name = form.event_name.data
        event.event_descr = form.event_descr.data
        event.event_start = form.event_start.data
        event.event_end = form.event_end.data
        event.event_time = form.event_time.data
        event.event_duration = form.duration.data
        if form.event_img.data:
            event.event_img = form.event_img.data.read()
        event.category_id = form.event_cat.data
        event.eventvenue_id = form.event_venue.data
        event.location_details = form.location_detail.data

        # Update tickets
        for ticket_form in form.tickets:
            ticket = Ticket.query.filter_by(event_id=event_id, ticket_type=ticket_form.ticket_type.data).first()
            if ticket:
                ticket.price = ticket_form.price.data
                ticket.member_discount = ticket_form.member_discount.data
                ticket.max_quantity = ticket_form.max_quantity.data
                ticket.start_sale = ticket_form.start_sale.data
                ticket.end_sale = ticket_form.end_sale.data
            else:
                new_ticket = Ticket(
                    event_id=event.event_id,
                    ticket_type=ticket_form.ticket_type.data,
                    price=ticket_form.price.data,
                    member_discount=ticket_form.member_discount.data,
                    max_quantity=ticket_form.max_quantity.data,
                    start_sale=ticket_form.start_sale.data,
                    end_sale=ticket_form.end_sale.data
                )
                db.session.add(new_ticket)
        db.session.commit()

        flash('Event and tickets updated successfully!', 'success')
        return redirect(url_for('edit_event', event_id=event_id))

    return render_template('edit_event.html', form=form, event=event, ticket_data=ticket_data)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    try:
        # Delete associated tickets first
        Ticket.query.filter_by(event_id=event_id).delete()
        # Delete the event
        db.session.delete(event)
        db.session.commit()
        flash('Event and associated tickets deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'danger')
    
    return redirect(url_for('create_event'))

if __name__ == "__main__":
    app.run(debug=True)