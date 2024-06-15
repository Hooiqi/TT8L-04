from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import *
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from models import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:tt8l_04@localhost/event_management_system'
app.config['SECRET_KEY'] = 'ihopethiscanrun'
db.init_app(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

#Image path
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

        flash('User created successfully!', 'success')
        return redirect(url_for('signup'))

    return render_template('Signuppage.html', form=form)

@app.route('/account/profile/<user_id>', methods=['GET'])
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    form = ResetPasswordForm()
    return render_template('user_profile.html', user=user, form=form)

@app.route('/account/profile/reset_password', methods=['POST'])
def reset_password():
    form = ResetPasswordForm()
    user_id = request.args.get('user_id')  # Extract user_id from request arguments
    print(f"Received request to reset password for user_id: {user_id}")
    
    if form.validate_on_submit():
        print("Form validated successfully.")
        user = User.query.get_or_404(user_id)
        
        if bcrypt.check_password_hash(user.user_pwd, form.old_pwd.data):
            print("Old password matched.")
            new_hashed_password = bcrypt.generate_password_hash(form.new_pwd.data).decode('utf-8')
            user.user_pwd = new_hashed_password
            db.session.commit()
            flash('Your password has been reset!', 'success')
        else:
            print("Old password did not match.")
            flash('Old password is incorrect', 'danger')
    else:
        print("Form validation failed.")
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('user_profile', user_id=user_id))

@app.route('/account/tickethistory/<user_id>', methods=['GET'])
def ticket_history(user_id):
    # Retrieve search query and status filter from URL query parameters
    search_query = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()
    
    user = User.query.get_or_404(user_id)
    user_orders = db.session.query(UserOrder, Ticket, Event)\
        .join(Ticket, UserOrder.ticket_id == Ticket.ticket_id)\
        .join(Event, Ticket.event_id == Event.event_id)\
        .filter(UserOrder.user_id == user_id)
    
    #Search ticket history by event name
    if search_query:
        user_orders = user_orders.filter(Event.event_name.ilike(f'%{search_query}%'))
    
    #Filter ticket history by order status
    if status_filter:
        user_orders = user_orders.filter(UserOrder.order_status.has(ostatus_name=status_filter))
    
    user_orders = user_orders.all()
    
    return render_template('ticket_history.html', user=user, user_orders=user_orders, search_query=search_query, status_filter=status_filter)

@app.route('/event/details/<event_id>', methods=['GET'])
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    user_id = "1221107001"  # Change to current_user later

    # Check if the user has already purchased a ticket for this event
    user_has_ticket = UserOrder.query.join(Ticket).filter(
        UserOrder.user_id == user_id,
        Ticket.event_id == event_id).first() is not None

    # Check if the user is a member with an approved status
    user_membership = Membership.query.filter_by(user_id=user_id, mstatus_id=2).first()  # 2 corresponds to 'Accept' in member_status

    # Format event_start and event_time for display
    event.event_start_formatted = event.event_start.strftime('%A, %B %d, %Y')
    event.event_end_formatted = event.event_end.strftime('%A, %B %d, %Y')
    event.event_time_formatted = event.event_time.strftime('%I:%M %p')

    return render_template('EventDetails.html', event=event, user_has_ticket=user_has_ticket, user_member_status='Accept' if user_membership else 'None')

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    form.event_cat.choices = [("", "--Select an event category*--")] + [(cat.category_id, cat.category) for cat in EventCategory.query.all()]
    form.event_venue.choices = [("", "--Select a location category*--")] + [(ven.eventvenue_id, ven.location) for ven in EventVenue.query.all()]

    if request.method == 'POST':
        action = request.form.get('action')
        
        if form.validate_on_submit():
            if form.event_img.data:
                filename = secure_filename(form.event_img.data.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                form.event_img.data.save(file_path)
            else:
                filename = None

            new_event = Event(
                event_name=form.event_name.data,
                event_descr=form.event_descr.data,
                event_start=form.event_start.data,
                event_end=form.event_end.data,
                event_time=form.event_time.data,
                event_duration=form.duration.data,
                event_img=filename,
                category_id=form.event_cat.data,
                eventvenue_id=form.event_venue.data,
                location_details=form.location_detail.data,
                admin_id='A001',  # Replace with dynamic admin ID
                publish_status='Draft' if action == 'save' else 'Published'
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

            flash('Event saved successfully!' if action == 'save' else 'Event published successfully!', 'success')
            return redirect(url_for('create_event'))
        
        else:
            # Flash errors for event
            for field, errors in form.errors.items():
                if field != 'tickets':
                    for error in errors:
                        flash(f"Invalid data in '{getattr(form, field).label.text}' field! {error}", 'error')

            # Flash errors for tickets
            for i, ticket_form in enumerate(form.tickets):
                for field, errors in ticket_form.errors.items():
                    for error in errors:
                        flash(f"Invalid data in ticket '{ticket_form.ticket_type.data}': {getattr(ticket_form, field).label.text} - {error}", 'error')

            flash('Failed to save event!' if action == 'save' else 'Failed to publish event!', 'error')

    return render_template('create_event.html', form=form)

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)
    form.event_cat.choices = [("", "--Select an event category*--")] + [(cat.category_id, cat.category) for cat in EventCategory.query.all()]
    form.event_venue.choices = [("", "--Select a location category*--")] + [(ven.eventvenue_id, ven.location) for ven in EventVenue.query.all()]

    #Pre-populate data for category and venue
    form.event_cat.data = event.category_id
    form.event_venue.data = event.eventvenue_id

    # Format event_start and event_time for display
    event.event_start_formatted = event.event_start.strftime('%A, %B %d, %Y')
    event.event_end_formatted = event.event_end.strftime('%A, %B %d, %Y')
    event.event_time_formatted = event.event_time.strftime('%I:%M %p')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'delete':
            Ticket.query.filter_by(event_id=event_id).delete()
            db.session.delete(event)
            db.session.commit()
            flash('Event deleted successfully!', 'success')
            return redirect(url_for('create_event'))
        
        elif action in ['update', 'edit-publish']:
            if form.validate_on_submit():
                event.event_name = form.event_name.data
                event.event_descr = form.event_descr.data
                event.event_start = form.event_start.data
                event.event_end = form.event_end.data
                event.event_time = form.event_time.data
                event.event_duration = form.duration.data

                if form.event_img.data:
                    file = form.event_img.data
                    if file and hasattr(file, 'filename'): 
                        filename = secure_filename(form.event_img.data.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        form.event_img.data.save(file_path)
                        event.event_img = filename
                else:
                    event.event_img = event.event_img  # Keep existing image

                event.category_id = form.event_cat.data
                event.eventvenue_id = form.event_venue.data
                event.location_details = form.location_detail.data
                event.publish_status = 'Draft' if action == 'update' else 'Published'

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

                flash('Changes saved successfully!' if action == 'update' else 'Event published successfully!', 'success')
                return redirect(url_for('edit_event', event_id=event_id))
            
            else:
                # Flash errors for event
                for field, errors in form.errors.items():
                    if field != 'tickets':
                        for error in errors:
                            flash(f"Invalid data in '{getattr(form, field).label.text}' field! {error}", 'danger')

                # Flash errors for tickets
                for i, ticket_form in enumerate(form.tickets):
                    for field, errors in ticket_form.errors.items():
                        for error in errors:
                            flash(f"Invalid data in ticket '{ticket_form.ticket_type.data}': {getattr(ticket_form, field).label.text} - {error}", 'danger')
                            
                flash('Failed to save event!' if action == 'update' else 'Failed to publish event!', 'danger')

    return render_template('edit_event.html', form=form, event=event)


if __name__ == "__main__":
    app.run(debug=True)