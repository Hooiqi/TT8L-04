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
    form = EventForm(obj=event)
    form.event_cat.choices = [("", "--Select an event category--")]+[(cat.category_id, cat.category) for cat in EventCategory.query.all()]
    form.event_venue.choices = [("", "--Select a location category--")]+[(ven.eventvenue_id, ven.location) for ven in EventVenue.query.all()]

    # Set the existing value for the SelectField
    form.event_cat.data = event.category_id
    form.event_venue.data = event.eventvenue_id

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update' and form.validate_on_submit():
            event.event_name = form.event_name.data
            event.event_descr = form.event_descr.data
            event.event_start = form.event_start.data
            event.event_end = form.event_end.data
            event.event_time = form.event_time.data
            event.event_duration = form.duration.data
            event.event_img = form.event_img.data.read() if form.event_img.data else event.event_img
            event.category_id = form.event_cat.data
            event.eventvenue_id = form.event_venue.data
            event.location_details = form.location_detail.data

            db.session.commit()

            Ticket.query.filter_by(event_id=event_id).delete()
            for ticket_form in form.tickets:
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

            flash('Event updated successfully!', 'success')
            return redirect(url_for('edit_event', event_id=event_id))
        
        elif action == 'delete':
            Ticket.query.filter_by(event_id=event_id).delete()
            db.session.delete(event)
            db.session.commit()
            flash('Event deleted successfully!', 'success')
            return redirect(url_for('create_event'))

    return render_template('edit_event.html', form=form, event=event)


if __name__ == "__main__":
    app.run(debug=True)