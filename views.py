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
    print("Check current_user >> " + str(current_user))
    # Total members
    total_members = db.session.query(func.count(Membership.membership_id)).scalar()

    # Total events
    total_events = db.session.query(func.count(Event.event_id)).scalar()

    # Total tickets sold
    total_tickets_sold = db.session.query(func.sum(UserOrder.order_quantity)).scalar()

    # Total sales
    total_sales = db.session.query(func.sum(Ticket.price * UserOrder.order_quantity)).join(UserOrder, UserOrder.ticket_id == Ticket.ticket_id).scalar()
    return render_template("adminhomepage.html", user=current_user, admin=current_user, total_members=total_members, total_events=total_events, total_tickets_sold=total_tickets_sold, total_sales=total_sales)

@views.route('/admin-profile', methods=['GET', 'POST'])
def admin_profile():
    print("Check current_user >> " + str(current_user))
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

    events = Event.query.all()
    return render_template("manage.html", user=current_user, events=events)

@views.route('/manage-member', methods=['GET', 'POST'])
def manage_member():
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
        Membership.mstatus_id == 2
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

    member_requests = db.session.query(
        Membership.membership_id,
        User.user_id,
        MemberStatus.mstatus_id,
        MemberStatus.mstatus_name
    ).join(
        User, Membership.user_id == User.user_id
    ).join(
        MemberStatus, Membership.mstatus_id == MemberStatus.mstatus_id
    ).all()

    statuses = MemberStatus.query.all()
    
    return render_template("request.html", user=current_user, member_requests=member_requests, statuses=statuses)
