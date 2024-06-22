from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from forms import EventForm
from models import *
from werkzeug.utils import secure_filename
import os
from sqlalchemy import func

admin_view = Blueprint('admin_view', __name__)

@admin_view.route('/dashboard', methods=['GET', 'POST'])
@login_required
def admin_home():
    if request.method == 'POST':
        admin = current_user
        admin.admin_name = request.form['name']
        admin.admin_email = request.form['email']
        admin.admin_phone = request.form['phonenumber']
        admin.admin_descr = request.form['description']
        
        try:
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('admin_view.admin_home'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile.', 'danger')

    admin_id = current_user.admin_id

    # Total members for current admin
    total_members = db.session.query(func.count(Membership.membership_id)).filter(    ).filter(
        Membership.mstatus_id == 2,
        Membership.admin_id == admin_id).scalar()

    # Total events for current admin
    total_events = db.session.query(func.count(Event.event_id)).filter(Event.admin_id == admin_id).scalar()

    # Total tickets sold for current admin's events
    total_tickets_sold = db.session.query(func.sum(UserOrder.order_quantity)).join(Ticket, UserOrder.ticket_id == Ticket.ticket_id).join(Event, Ticket.event_id == Event.event_id).filter(Event.admin_id == admin_id).scalar()

    # Total sales for current admin's events
    total_sales = db.session.query(func.sum(UserOrder.total_amount)).join(
        Ticket, UserOrder.ticket_id == Ticket.ticket_id).join(
        Event, Ticket.event_id == Event.event_id).filter(
        Event.admin_id == admin_id
    ).scalar()

    return render_template(
        "admin_dashboard.html", 
        admin=current_user, 
        total_members=total_members, 
        total_events=total_events, 
        total_tickets_sold=total_tickets_sold, 
        total_sales=total_sales
    )

@admin_view.route('/manage-event', methods=['GET', 'POST'])
@login_required
def manage_event():
    if request.method == 'POST':
        event_id = request.form.get('event_id')
        action = request.form.get('action')

        if action == 'delete':
            if event_id:
                event = Event.query.get(event_id)
                if event:
                    try:
                        # Find and delete event likes related to the event
                        # Find tickets related to the event
                        tickets = Ticket.query.filter_by(event_id=event_id).all()
                        for ticket in tickets:
                            # Find user orders related to the ticket
                            user_orders = UserOrder.query.filter_by(ticket_id=ticket.ticket_id).all()
                            for user_order in user_orders:
                                # Delete each user order
                                db.session.delete(user_order)
                            # Delete the ticket after all related user orders have been deleted
                            db.session.delete(ticket)
                        
                        # Delete the event
                        db.session.delete(event)
                        db.session.commit()

                        flash('Event, associated tickets, user orders, and likes deleted successfully!', category='success')
                    except Exception as e:
                        db.session.rollback()
                        flash('An error occurred while deleting the event.', category='error')
                        print(f"Error: {e}")
                else:
                    flash('Event not found.', category='error')
            else:
                flash('Invalid event ID.', category='error')
        
        return redirect(url_for('admin_view.manage_event'))

    # events = Event.query.all()
    admin_id = current_user.admin_id
    events = Event.query.filter_by(admin_id=admin_id, publish_status="Draft").all()
    return render_template("manage_event.html", user=current_user, events=events)

@admin_view.route('/manage-member', methods=['GET', 'POST'])
@login_required
def manage_member():
    admin_id = current_user.admin_id
    accepted_members = db.session.query(
        Membership.membership_id,
        User.user_id,
        User.user_name,
        User.user_phone,
        Admin.admin_id,
        MemberStatus.mstatus_id
    ).join(
        User, Membership.user_id == User.user_id
    ).join(
        Admin, Membership.admin_id == Admin.admin_id
    ).join(
        MemberStatus, Membership.mstatus_id == MemberStatus.mstatus_id
    ).filter(
        Membership.mstatus_id == 2,
        Membership.admin_id == admin_id
    ).all()

    return render_template("member_list.html", user=current_user, members=accepted_members)

@admin_view.route('/member-request', methods=['GET', 'POST'])
@login_required
def member_request():
    if request.method == 'POST':
        membership_id = request.form.get('membership_id')
        new_status_id = request.form.get('mstatus_id')

        membership = Membership.query.get(membership_id)
        if membership:
            membership.mstatus_id = new_status_id
            membership.last_updated = datetime.now()
            db.session.commit()
            flash('Status updated successfully!', category='success')
        else:
            flash('Membership not found!', category='error')

    admin_id = current_user.admin_id
    member_requests = db.session.query(
        Membership.membership_id,
        User.user_id,
        User.user_name,
        MemberStatus.mstatus_id,
        Membership.last_updated,
        MemberStatus.mstatus_name
    ).join(
        User, Membership.user_id == User.user_id
    ).join(
        MemberStatus, Membership.mstatus_id == MemberStatus.mstatus_id
    ).filter(
        Membership.admin_id == admin_id
    ).all()

    statuses = MemberStatus.query.all()
    
    return render_template("member_request.html", user=current_user, member_requests=member_requests, statuses=statuses)

@admin_view.route('/update_member_status', methods=['POST'])
@login_required
def update_member_status():
    if request.method == 'POST':
        for membership_id, status in request.form.items():
            if membership_id.startswith('status_'):
                membership_id = membership_id.split('_')[1]
                membership = Membership.query.get(membership_id)
                if membership:
                    membership.mstatus_name = status

                    db.session.commit()
                else:
                    flash(f'Membership with ID {membership_id} not found.', category='error')
        
        flash('Member statuses updated successfully!', category='success')
        return redirect(url_for('admin_view.member_request'))  # Redirect to the member request page

    flash('Failed to update member statuses.', category='error')
    return redirect(url_for('admin_view.member_request'))

@admin_view.route('/view-tickets', methods=['GET', 'POST'])
@login_required
def view_tickets():
    admin_id = current_user.admin_id
    events = Event.query.filter_by(admin_id=admin_id,publish_status="Published").all()
    for event in events:
        # Calculate total tickets sold for each event
        event.total_tickets_sold = db.session.query(func.sum(UserOrder.order_quantity)).join(Ticket, UserOrder.ticket_id == Ticket.ticket_id).filter(Ticket.event_id == event.event_id).scalar() or 0
        # Total sales for each event
        event.total_sales = db.session.query(func.sum(UserOrder.total_amount)).join(
        Ticket, UserOrder.ticket_id == Ticket.ticket_id).join(
        Event, Ticket.event_id == Event.event_id
        ).filter(Ticket.event_id == event.event_id).scalar() or "0.00"
    return render_template("view_ticket.html", user=current_user, events=events)

@admin_view.route('/view-ticket/details/<int:event_id>', methods=['GET'])
@login_required
def view_ticket_details(event_id):
    # Fetch all tickets related to the event_id
    tickets = Ticket.query.filter_by(event_id=event_id).all()

    # Initialize an empty list to store user orders related to these tickets
    user_orders = []

    # Dictionary to store total tickets sold for each ticket type
    total_tickets_sold = {}

    # Loop through each ticket to fetch its associated user orders
    for ticket in tickets:
        orders = UserOrder.query.filter_by(ticket_id=ticket.ticket_id).all()
        user_orders.extend(orders)  # Append orders to the list
        
    # Pass the total tickets sold information to the template
    return render_template("view_ticket_details.html", tickets=tickets, user_orders=user_orders, total_tickets_sold=total_tickets_sold)

@admin_view.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    form.event_cat.choices = [("", "--Select an event category*--")] + [(cat.category_id, cat.category) for cat in EventCategory.query.all()]
    form.event_venue.choices = [("", "--Select a location category*--")] + [(ven.eventvenue_id, ven.location) for ven in EventVenue.query.all()]

    if request.method == 'POST':
        action = request.form.get('action')
        
        if form.validate_on_submit():
            if form.event_img.data:
                filename = secure_filename(form.event_img.data.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
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
                admin_id=current_user.admin_id,
                publish_status='Draft' if action == 'save' else 'Published',
                last_updated=datetime.now()
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
            return redirect(url_for('admin_view.create_event'))
        
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

            flash('Failed to save event!' if action == 'save' else 'Failed to publish event!', 'danger')

    return render_template('create_event.html', form=form)

@admin_view.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('admin_view.create_event'))
        
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
                        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        form.event_img.data.save(file_path)
                        event.event_img = filename
                else:
                    event.event_img = event.event_img  # Keep existing image

                event.category_id = form.event_cat.data
                event.eventvenue_id = form.event_venue.data
                event.location_details = form.location_detail.data
                event.publish_status = 'Draft' if action == 'update' else 'Published'
                event.last_updated = datetime.now()

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
                return redirect(url_for('admin_view.edit_event', event_id=event_id))
            
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

