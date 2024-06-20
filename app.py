from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from forms import EventForm
from models import *
import os
import mysql.connector
import stripe


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Ghq1003.@localhost/event_management_system'
app.config['SECRET_KEY'] = 'ihopethiscanrun'
db.init_app(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

publishable_key ='pk_test_51PMWarFeLdpgIRLCQdaDneDpcOxMLWM2vMtAI8CAAMvwl1gRrOMTgouy5HWvthCAjjsDayhkgpcj4OG6armC6bKC00oZh8R1VY'
stripe.api_key = 'sk_test_51PMWarFeLdpgIRLCcD1YhpdSwJESnWBcMmxvtFXvlx9aEfh11QwoCY3eaSMi43B7Ho1BBIld9qMDAaCRIsVbUZpw00lInyAKH0'

@app.route('/home')
def home():
    categories_nav = EventCategory.query.all()
    events = Event.query.all()

    return render_template('Homepage.html', categories_nav=categories_nav, events=events)

@app.route('/events', defaults={'category': None})
@app.route('/events/<category>')
def event_category(category):
    # Retrieve search query and venue filter from URL query parameters
    search_query = request.args.get('search', '').strip()
    venue_filter = request.args.get('venue_type', '').strip()
    sort = request.args.get('sort', '').strip()
    page = request.args.get('page', 1, type=int)  # Get the current page number

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

    return render_template('event-category.html', category=category_obj, event=events, categories_nav=categories_nav,
                           search_query=search_query, venue_filter=venue_filter, sort=sort, pagination=events_pagination)

@app.route('/events/details/<event_id>', methods=['GET'])
#@login_required
def event_details(event_id):
    categories_nav = EventCategory.query.all()
    event = Event.query.get_or_404(event_id)
   # user_id = current_user.user_id

    # Check if the user has already purchased a ticket for this event
    user_has_ticket = UserOrder.query.join(Ticket).filter(
    #    UserOrder.user_id == user_id,
        Ticket.event_id == event_id).first() is not None

    # Check if the user is a member with an approved status
   # user_membership = Membership.query.filter_by(user_id=user_id, admin_id=event.admin_id, mstatus_id=2).first()  # 2 represents 'Accept' in member_status

    # Format event_start and event_time for display
    event.event_start_formatted = event.event_start.strftime('%A, %B %d, %Y')
    event.event_end_formatted = event.event_end.strftime('%A, %B %d, %Y')
    event.event_time_formatted = event.event_time.strftime('%I:%M %p')

    # Get remaining tickets for each ticket type
    tickets_info = []
    for ticket in event.tickets:
        sold_tickets = UserOrder.query.filter_by(ticket_id=ticket.ticket_id).count()
        remaining_tickets = ticket.max_quantity - sold_tickets
       # if user_membership:
       #     ticket_price = ticket.member_discount
       # else:
        ticket_price = ticket.price
        tickets_info.append((ticket, remaining_tickets, ticket_price))

    # Get current datetime
    current_datetime = datetime.now()

    return render_template('EventDetails.html', event=event, user_has_ticket=user_has_ticket,
                           tickets_info=tickets_info, current_datetime=current_datetime, categories_nav=categories_nav)

@app.route('/order_summary', methods=['GET'])
#@login_required
def order_summary():
    # Navigation bar
    categories_nav = EventCategory.query.all()

    event_name = request.args.get('event_name')
    ticket_type = request.args.get('ticket_type')
    ticket_price = request.args.get('ticket_price')

    return render_template('order_summary.html', categories_nav=categories_nav, event_name=event_name,
                           ticket_type=ticket_type, ticket_price=ticket_price)

@app.route('/checkout', methods=['POST'])
#@login_required
def checkout():
    event_name = request.form.get('event_name')
    ticket_type = request.form.get('ticket_type')
    ticket_price = request.form.get('ticket_price')

    # Retrieve the event and admin details
    event = Event.query.filter_by(event_name=event_name).first()
    admin = event.admin

    # Set Stripe API key dynamically based on the admin
    stripe.api_key = admin.stripe_secret_key

    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'myr',
                'product_data': {
                    'name': f"{event_name} - {ticket_type}",
                },
                'unit_amount': int(float(ticket_price) * 100),  # Stripe expects the amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('payment_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('payment_cancel', _external=True),
    )

    return redirect(session.url, code=303)

@app.route('/payment_success')
#@login_required
def payment_success():
    session_id = request.args.get('session_id')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        customer_id = session.get('customer')

        # Check if customer_id exists before retrieving customer
        if customer_id:
            customer = stripe.Customer.retrieve(customer_id)
            # Handle successful payment logic here, update database, etc.
            flash('Your payment was successful!', 'success')
            return render_template('payment_success.html') #new new new
        else:
            flash('Customer ID not found in Stripe session.', 'error')

    except stripe.error.InvalidRequestError as e:
        flash('Error retrieving payment details from Stripe.', 'error')

    return redirect(url_for('home'))

@app.route('/payment_cancel')
#@login_required
def payment_cancel():
    flash('Your payment was canceled.', 'danger')
    return render_template('payment_cancel.html') #new new new

# MySQL database connection setup
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='event_management_system',
        user='root',
        password='Ghq1003.'
    )
    if connection.is_connected():
        print("Connected to MySQL database")
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")

# Wrapper function to query the database
def query(sql, params=None):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    return rows

if __name__ == '__main__':
    app.run(debug=True)