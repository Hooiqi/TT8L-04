from flask import Blueprint, render_template, url_for, request, redirect, flash
from forms import ResetPasswordForm
from flask_login import login_required, current_user
from flask_bcrypt import Bcrypt
from models import *
import stripe

user_view = Blueprint('user_view', __name__)
bcrypt = Bcrypt()

@user_view.route('/home')
@login_required
def home():
    # Get current datetime
    current_datetime = datetime.now()

    categories_nav = EventCategory.query.all()
    upcoming_event = Event.query.filter(Event.event_start >= current_datetime).filter_by(publish_status="Published").all()
    new_event = Event.query.filter(Event.event_start >= current_datetime).filter_by(publish_status="Published").order_by(Event.last_updated.desc()).all()
    event_images = Event.query.filter(Event.event_img != None, Event.event_start >= current_datetime).filter_by(publish_status="Published").all()

    return render_template('home.html', categories_nav=categories_nav, upcoming=upcoming_event, new=new_event,
                            event_images=event_images, user=current_user)

@user_view.route('/events', defaults={'category': None})
@user_view.route('/events/<category>')
@login_required
def event_category(category):
    # Retrieve value from URL query parameters
    search_query = request.args.get('search', '').strip()
    venue_filter = request.args.get('venue_type', '').strip()
    sort = request.args.get('sort', '').strip()
    include_expired = request.args.get('expired', 'off') == 'on'
    page = request.args.get('page', 1, type=int)  # Get the current page number

    # Get current datetime
    current_datetime = datetime.now()

    # Navigation bar
    categories_nav = EventCategory.query.all()

    # Initialize the event query
    if category:
        category_obj = EventCategory.query.filter_by(category=category).first_or_404()
        event_query = Event.query.filter_by(category_id=category_obj.category_id, publish_status="Published")
    else:
        category_obj = None
        event_query = Event.query.filter_by(publish_status="Published")

    # Apply search filter if search query is provided
    if search_query:
        event_query = event_query.filter(Event.event_name.ilike(f'%{search_query}%'))

    # Apply venue filter if venue type is provided
    if venue_filter:
        event_query = event_query.filter(Event.event_venue.has(location=venue_filter))

    # Apply filter to exclude expired events if include_expired is not selected
    if not include_expired:
        event_query = event_query.filter(Event.event_end >= current_datetime)

    # Apply sorting
    if sort == 'date':
        event_query = event_query.order_by(Event.event_start.asc())
    elif sort == 'a-z':
        event_query = event_query.order_by(Event.event_name.asc())
    elif sort == 'z-a':
        event_query = event_query.order_by(Event.event_name.desc())

    # Paginate the results
    events_pagination = event_query.paginate(page=page, per_page=9)
    events = events_pagination.items

    return render_template('event_category.html', category=category_obj, event=events, categories_nav=categories_nav,
                            current_datetime=current_datetime, search_query=search_query, venue_filter=venue_filter, 
                            sort=sort, pagination=events_pagination, include_expired=include_expired, user=current_user)

@user_view.route('/events/details/<event_id>', methods=['GET'])
@login_required
def event_details(event_id):
    categories_nav = EventCategory.query.all()
    event = Event.query.get_or_404(event_id)
    user_id = current_user.user_id

    # Check if the user has already purchased a ticket for this event
    user_has_ticket = UserOrder.query.join(Ticket).filter(
        UserOrder.user_id == user_id,
        Ticket.event_id == event_id).first() is not None

    # Check if the user is a member with an approved status
    user_membership = Membership.query.filter_by(user_id=user_id, admin_id=event.admin_id, mstatus_id=2).first()  # 2 represents 'Accept' in member_status

    # Format event_start and event_time for display
    event.event_start_formatted = event.event_start.strftime('%A, %B %d, %Y')
    event.event_end_formatted = event.event_end.strftime('%A, %B %d, %Y')
    event.event_time_formatted = event.event_time.strftime('%I:%M %p')

    # Get remaining tickets for each ticket type
    tickets_info = []
    for ticket in event.tickets:
        sold_tickets = UserOrder.query.filter_by(ticket_id=ticket.ticket_id).count()
        remaining_tickets = ticket.max_quantity - sold_tickets
        if user_membership:
            ticket_price = ticket.member_discount
        else:
            ticket_price = ticket.price
        tickets_info.append((ticket, remaining_tickets, ticket_price))

    # Get current datetime
    current_datetime = datetime.now()

    return render_template('event_details.html', event=event, user_has_ticket=user_has_ticket,
                           tickets_info=tickets_info, current_datetime=current_datetime, categories_nav=categories_nav, user=current_user)

#after choose the ticket type, user will be bring to order summary with order details
@user_view.route('/order_summary', methods=['GET'])
@login_required
def order_summary():
    # Navigation bar
    categories_nav = EventCategory.query.all()

    # Retrieve value from URL query parameters
    event_name = request.args.get('event_name')
    ticket_id = request.args.get('ticket_id')
    ticket_type = request.args.get('ticket_type')
    ticket_price = request.args.get('ticket_price')

    return render_template('order_summary.html', categories_nav=categories_nav, event_name=event_name, ticket_id=ticket_id, 
                           ticket_type=ticket_type, ticket_price=ticket_price, user=current_user)

# for free tickets
@user_view.route('/confirm_order', methods=['POST'])
@login_required
def confirm_order():
    try:
        ticket_id = request.form.get('ticket_id')

        # Create a new order entry
        new_order = UserOrder(
            user_id=current_user.user_id,
            ticket_id=ticket_id,
            order_date=datetime.now(),
            order_quantity=1,
            total_amount=0,  # As the price is 0.00
            invoice="Free"
        )

        db.session.add(new_order)
        db.session.commit()

        return render_template('payment_success.html')  # Adjust the redirect URL as needed

    except Exception as e:
        flash(f'Error confirming order: {str(e)}', 'error')
        return redirect(url_for('user_view.payment_cancel'))


#details will be listed again on checkout page for double confirmation
@user_view.route('/checkout', methods=['POST'])
@login_required
def checkout():
    ticket_id = request.form.get('ticket_id')
    event_name = request.form.get('event_name')
    ticket_type = request.form.get('ticket_type')
    ticket_price = request.form.get('ticket_price')

    event = Event.query.filter_by(event_name=event_name).first()
    admin = event.admin

    stripe.api_key = admin.stripe_secret_key

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'myr',
                'product_data': {
                    'name': f"{event_name} - {ticket_type}",
                },
                'unit_amount': int(float(ticket_price) * 100), # Stripe stores amounts in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        client_reference_id=int(ticket_id), 
        success_url=url_for('user_view.payment_success', _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=url_for('user_view.payment_cancel', _external=True),
    )

    return redirect(session.url, code=303)

def save_order_to_db(session):
    try:
        ticket_id = session['client_reference_id']
        user_id = current_user.user_id
        order_quantity = 1  
        total_amount = session['amount_total'] / 100  

        new_order = UserOrder(
            user_id=user_id,
            ticket_id=ticket_id,
            order_date=datetime.now(),
            order_quantity=order_quantity,
            total_amount=total_amount,
            invoice=session['id']
        )

        db.session.add(new_order)
        db.session.commit()

    except Exception as e:
        flash(f'Error saving order to database: {str(e)}', 'error')
        return redirect(url_for('user_view.home'))  # Adjust the redirect URL as needed

# If payment is successful, show success and redirect to homepage
@user_view.route('/payment_success')
@login_required
def payment_success():
    session_id = request.args.get('session_id')

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            save_order_to_db(session)
            return render_template('payment_success.html')
        else:
            flash('Payment was not successful. Please try again.', 'error')

    except stripe.error.InvalidRequestError as e:
        flash(f'Error retrieving payment details from Stripe: {str(e)}', 'error')

    return redirect(url_for('home'))

#If payment is cancelled, show cancel and redirect to homepage
@user_view.route('/payment_cancel')
@login_required
def payment_cancel():
    return render_template('payment_cancel.html')

@user_view.route('/organisers', methods=['GET', 'POST'])
@login_required
def organisers():
    categories_nav = EventCategory.query.all()
    search_query = request.args.get('search', '').strip()
    sort = request.args.get('sort', '').strip()
    user_id = current_user.user_id

    admin_query = Admin.query

    # Apply search filter if search query is provided
    if search_query:
        admin_query = admin_query.filter(Admin.admin_name.ilike(f'%{search_query}%'))

    # Apply sorting
    if sort == 'a-z':
        admin_query = admin_query.order_by(Admin.admin_name.asc())
    elif sort == 'z-a':
        admin_query = admin_query.order_by(Admin.admin_name.desc())

    admins = admin_query.all()

    # Check membership requests and status
    memberships = Membership.query.filter_by(user_id=user_id).all()
    membership_status = {membership.admin_id: membership.mstatus_id for membership in memberships}

    for admin in admins:
        admin.requested = membership_status.get(admin.admin_id) == 1  # Check 'Pending'
        admin.approved_membership = membership_status.get(admin.admin_id) == 2  # Check 'Accept'

    return render_template('organiser.html', categories_nav=categories_nav, organisers=admins, search_query=search_query, sort=sort, user=current_user)

@user_view.route('/organisers/<admin_id>/<action>', methods=['POST'])
@login_required
def manage_membership(admin_id, action):
    user_id = current_user.user_id

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'request':
            existing_membership = Membership.query.filter_by(user_id=user_id, admin_id=admin_id).first()

            if not existing_membership:
                # If no membership exists, create a new one with status 'Pending'
                new_membership = Membership(
                    user_id=user_id,
                    admin_id=admin_id,
                    mstatus_id=1  # 1 represents 'Pending'
                )
                db.session.add(new_membership)
                db.session.commit()
                flash('Membership request submitted!', 'success')
            else:
                # If membership exists, update its status to 'Pending' if it's not already 'Pending'
                if existing_membership.mstatus_id != 1:  # Check if status is not 'Pending'
                    existing_membership.mstatus_id = 1
                    db.session.commit()
                    flash('Membership request submitted!', 'success')

        elif action == 'unjoin':
            membership = Membership.query.filter_by(user_id=user_id, admin_id=admin_id, mstatus_id=2).first()
            if membership:
                db.session.delete(membership)
                db.session.commit()
                flash('Successfully unjoined membership.', 'success')
        
        elif action == 'cancel':
            membership = Membership.query.filter_by(user_id=user_id, admin_id=admin_id, mstatus_id=1).first()
            if membership:
                db.session.delete(membership)
                db.session.commit()
                flash('Membership request cancelled.', 'success')

    return redirect(url_for('user_view.organisers', admin_id=admin_id))

@user_view.route('/organisers/details/<admin_id>', methods=['GET'])
@login_required
def organiser_details(admin_id):
    categories_nav = EventCategory.query.all()
    admin = Admin.query.get_or_404(admin_id)
    user_id = current_user.user_id

    # Check membership requests and status
    memberships = Membership.query.filter_by(user_id=user_id).all()
    membership_status = {membership.admin_id: membership.mstatus_id for membership in memberships}

    admin.requested = membership_status.get(admin.admin_id) == 1  # Check 'Pending'
    admin.approved_membership = membership_status.get(admin.admin_id) == 2  # Check 'Accept'

    # Get current datetime
    current_datetime = datetime.now()

    # Fetch events with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Define the number of items per page
    events_pagination = Event.query.filter_by(admin_id=admin_id, publish_status="Published").order_by(Event.event_start.desc()).paginate(page=page, per_page=per_page)
    events = events_pagination.items

    return render_template('organiser_details.html', organiser=admin, categories_nav=categories_nav, events=events, current_datetime=current_datetime, 
                           pagination=events_pagination, user=current_user)

@user_view.route('/organisers/details/<admin_id>/<action>', methods=['POST'])
@login_required
def details_manage_membership(admin_id, action):
    user_id = current_user.user_id

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'request':
            existing_membership = Membership.query.filter_by(user_id=user_id, admin_id=admin_id).first()

            if not existing_membership:
                # If no membership exists, create a new one with status 'Pending'
                new_membership = Membership(
                    user_id=user_id,
                    admin_id=admin_id,
                    mstatus_id=1  # 1 represents 'Pending'
                )
                db.session.add(new_membership)
                db.session.commit()
                flash('Membership request submitted!', 'success')
            else:
                # If membership exists, update its status to 'Pending' if it's not already 'Pending'
                if existing_membership.mstatus_id != 1:  # Check if status is not 'Pending'
                    existing_membership.mstatus_id = 1
                    db.session.commit()
                    flash('Membership status updated to Pending.', 'success')
                else:
                    flash('Membership request already exists.', 'info')

        elif action == 'unjoin':
            membership = Membership.query.filter_by(user_id=user_id, admin_id=admin_id, mstatus_id=2).first()
            if membership:
                db.session.delete(membership)
                db.session.commit()
                flash('Successfully unjoined membership.', 'success')
        
        elif action == 'cancel':
            membership = Membership.query.filter_by(user_id=user_id, admin_id=admin_id, mstatus_id=1).first()
            if membership:
                db.session.delete(membership)
                db.session.commit()
                flash('Membership request cancelled.', 'success')

    return redirect(url_for('user_view.organiser_details', admin_id=admin_id))


@user_view.route('/account/profile/<user_id>', methods=['GET'])
@login_required
def user_profile(user_id):
    user_id = current_user.user_id
    
    user = User.query.get_or_404(user_id)
    form = ResetPasswordForm() # Get form
    categories_nav = EventCategory.query.all() # Event category in navigation bar
    return render_template('user_profile.html', user=user, form=form, categories_nav=categories_nav)

@user_view.route('/account/profile/reset_password', methods=['POST'])
@login_required
def reset_password():
    user_id = current_user.user_id
    
    form = ResetPasswordForm()
    user_id = request.args.get('user_id')  # Extract user_id from request arguments
    
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)

        # Check hashed old password
        if bcrypt.check_password_hash(user.user_pwd, form.old_pwd.data):
            new_hashed_password = bcrypt.generate_password_hash(form.new_pwd.data).decode('utf-8')
            user.user_pwd = new_hashed_password
            db.session.commit()
            flash('Password reset successfully!', 'success')
        else:
            flash('Old password is incorrect', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Wrong value in '{getattr(form, field).label.text}': {error}", 'danger')

    return redirect(url_for('user_view.user_profile', user_id=user_id))

@user_view.route('/account/tickethistory/<user_id>', methods=['GET'])
@login_required
def ticket_history(user_id):
    user_id = current_user.user_id

    # Retrieve search query and status filter from URL query parameters
    search_query = request.args.get('search', '').strip()
    
    categories_nav = EventCategory.query.all() # Event category in navigation bar

    user = User.query.get_or_404(user_id)
    user_orders = db.session.query(UserOrder, Ticket, Event)\
        .join(Ticket, UserOrder.ticket_id == Ticket.ticket_id)\
        .join(Event, Ticket.event_id == Event.event_id)\
        .filter(UserOrder.user_id == user_id)
    
    #Search ticket history by event name
    if search_query:
        user_orders = user_orders.filter(Event.event_name.ilike(f'%{search_query}%'))
    
    user_orders = user_orders.all()
    
    return render_template('ticket_history.html', user=user, user_orders=user_orders, search_query=search_query,
                           categories_nav=categories_nav)

@user_view.route('/account/membership/<user_id>', methods=['GET'])
@login_required
def user_membership(user_id):
    user_id = current_user.user_id

    # Retrieve search query and status filter from URL query parameters
    search_query = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()
    
    categories_nav = EventCategory.query.all() # Event category in navigation bar

    user = User.query.get_or_404(user_id)
    memberships = db.session.query(Admin, Membership)\
        .join(Membership, Admin.admin_id == Membership.admin_id)\
        .filter(Membership.user_id == user_id)
    
    # Search membership history by admin event name
    if search_query:
        memberships = memberships.filter(Admin.admin_name.ilike(f'%{search_query}%'))
    
    # Filter membership history by member status
    if status_filter:
        memberships = memberships.filter(Membership.member_status.has(mstatus_name=status_filter))
    
    memberships = memberships.all()
    
    return render_template('user_membership.html', user=user, memberships=memberships, search_query=search_query, status_filter=status_filter,
                           categories_nav=categories_nav)
