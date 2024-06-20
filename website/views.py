from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Membership, User, Admin, MemberStatus, Event, Ticket, UserOrder, EventLikes
import json
from sqlalchemy import func

views = Blueprint('views', __name__)


@views.route('/student', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("Homepage.html", user=current_user)

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_home():
    admin_id = current_user.admin_id

    # Total members for current admin
    total_members = db.session.query(func.count(Membership.membership_id)).filter(Membership.admin_id == admin_id).scalar()

    # Total events for current admin
    total_events = db.session.query(func.count(Event.event_id)).filter(Event.admin_id == admin_id).scalar()

    # Total tickets sold for current admin's events
    total_tickets_sold = db.session.query(func.sum(UserOrder.order_quantity)).join(Ticket, UserOrder.ticket_id == Ticket.ticket_id).join(Event, Ticket.event_id == Event.event_id).filter(Event.admin_id == admin_id).scalar()

    # Total sales for current admin's events
    total_sales = db.session.query(func.sum(Ticket.price * UserOrder.order_quantity)).join(UserOrder, UserOrder.ticket_id == Ticket.ticket_id).join(Event, Ticket.event_id == Event.event_id).filter(Event.admin_id == admin_id).scalar()

    return render_template(
        "adminhomepage.html", 
        user=current_user, 
        admin=current_user, 
        total_members=total_members, 
        total_events=total_events, 
        total_tickets_sold=total_tickets_sold, 
        total_sales=total_sales
    )

@views.route('/admin-profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    print("Check current_user >> " + str(current_user))
    if request.method == 'POST':
        # Get form data
        new_name = request.form.get('admin-name')
        new_description = request.form.get('admin-description')
        
        # Update admin profile
        if new_name:
            current_user.admin_name = new_name
        if new_description:
            current_user.admin_descr = new_description
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', category='success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the profile.', category='error')
            print(f"Error: {e}")

        return redirect(url_for('views.admin_profile'))

    return render_template("admin.html", user=current_user, admin=current_user)

@views.route('/manage-event', methods=['GET', 'POST'])
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
                        event_likes = EventLikes.query.filter_by(event_id=event_id).all()
                        for event_like in event_likes:
                            db.session.delete(event_like)
                        
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
        
        return redirect(url_for('views.manage_event'))

    # events = Event.query.all()
    admin_id = current_user.admin_id
    events = Event.query.filter_by(admin_id=admin_id).all()
    return render_template("manage.html", user=current_user, events=events)

@views.route('/manage-member', methods=['GET', 'POST'])
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

    return render_template("member.html", user=current_user, members=accepted_members)

@views.route('/member-request', methods=['GET', 'POST'])
def member_request():
    if request.method == 'POST':
        membership_id = request.form.get('membership_id')
        new_status_id = request.form.get('mstatus_id')

        membership = Membership.query.get(membership_id)
        if membership:
            membership.mstatus_id = new_status_id
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
        MemberStatus.mstatus_name
    ).join(
        User, Membership.user_id == User.user_id
    ).join(
        MemberStatus, Membership.mstatus_id == MemberStatus.mstatus_id
    ).filter(
        Membership.admin_id == admin_id
    ).all()

    statuses = MemberStatus.query.all()
    
    return render_template("request.html", user=current_user, member_requests=member_requests, statuses=statuses)

@views.route('/view-tickets', methods=['GET', 'POST'])
def view_tickets():
    admin_id = current_user.admin_id
    events = Event.query.filter_by(admin_id=admin_id).all()
    for event in events:
        # Calculate total tickets sold for each event
        event.total_tickets_sold = db.session.query(func.sum(UserOrder.order_quantity)).join(Ticket, UserOrder.ticket_id == Ticket.ticket_id).filter(Ticket.event_id == event.event_id).scalar() or 0
    return render_template("view-ticket.html", user=current_user, events=events)

@views.route('/view-ticket-details/<int:event_id>', methods=['GET'])
def view_ticket_details(event_id):
    # Fetch all tickets related to the event_id
    tickets = Ticket.query.filter_by(event_id=event_id).all()

    # Initialize an empty list to store user orders related to these tickets
    user_orders = []

    # Loop through each ticket to fetch its associated user orders
    for ticket in tickets:
        orders = UserOrder.query.filter_by(ticket_id=ticket.ticket_id).all()
        user_orders.extend(orders)  # Append orders to the list

    return render_template("view-ticket-details.html", tickets=tickets, user_orders=user_orders)