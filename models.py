from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.String(10), primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(39), unique=True, nullable=False)
    user_phone = db.Column(db.String(11), nullable=False)
    user_pwd = db.Column(db.String(60), nullable=False)
    
    orders = db.relationship('UserOrder', backref='user', lazy=True)
    memberships = db.relationship('Membership', backref='user', lazy=True)

    def get_id(self):
        return self.user_id

class UserOrder(db.Model):
    __tablename__ = 'user_order'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    order_quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    invoice = db.Column(db.String(255), nullable=True)

    ticket = db.relationship('Ticket', backref='user_orders')
    
class MemberStatus(db.Model):
    __tablename__ = 'member_status'
    mstatus_id = db.Column(db.Integer, primary_key=True)
    mstatus_name = db.Column(db.String(10))

    memberships = db.relationship('Membership', backref='member_status', lazy=True)

class Membership(db.Model):
    __tablename__ = 'membership'
    membership_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    admin_id = db.Column(db.String(4), db.ForeignKey('admin.admin_id'), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.now)
    mstatus_id = db.Column(db.Integer, db.ForeignKey('member_status.mstatus_id'), nullable=False)

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(4), primary_key=True)
    admin_name = db.Column(db.String(100), nullable=False)
    admin_email = db.Column(db.String(100), nullable=False, unique=True)
    admin_phone = db.Column(db.String(11), nullable=False)
    admin_pwd = db.Column(db.String(50), nullable=False)
    admin_descr = db.Column(db.Text)
    stripe_public_key = db.Column(db.String(255), nullable=False)
    stripe_secret_key = db.Column(db.String(255), nullable=False)
    admin_img = db.Column(db.String(255), nullable=False)

    events = db.relationship('Event', backref='admin', lazy=True)
    memberships = db.relationship('Membership', backref='admin', lazy=True)

    def get_id(self):
        return self.admin_id
    
class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_descr = db.Column(db.Text, nullable=False)
    event_start = db.Column(db.DateTime, nullable=False)
    event_end = db.Column(db.DateTime, nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    event_duration = db.Column(db.String(50), nullable=False)
    event_img = db.Column(db.String(255))
    category_id = db.Column(db.String(3), db.ForeignKey('event_category.category_id'), nullable=False)
    eventvenue_id = db.Column(db.String(3), db.ForeignKey('event_venue.eventvenue_id'), nullable=False)
    location_details = db.Column(db.String(255), nullable=False)
    admin_id = db.Column(db.String(4), db.ForeignKey('admin.admin_id'), nullable=False)
    publish_status = db.Column(db.String(45), nullable=False)

    tickets = db.relationship('Ticket', backref='event', lazy=True)
    category = db.relationship('EventCategory', backref='events', lazy=True)
    venue = db.relationship('EventVenue', backref='events', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    ticket_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    member_discount = db.Column(db.Numeric(10, 2), nullable=False)
    max_quantity = db.Column(db.Integer, nullable=False)
    start_sale = db.Column(db.Date, nullable=False)
    end_sale = db.Column(db.Date, nullable=False)

class EventVenue(db.Model):
    __tablename__ = 'event_venue'
    eventvenue_id = db.Column(db.String(3), primary_key=True)
    location = db.Column(db.String(10), nullable=False)

    venue = db.relationship('Event', backref='event_venue', lazy=True)

class EventCategory(db.Model):
    __tablename__ = 'event_category'
    category_id = db.Column(db.String(3), primary_key=True)
    category = db.Column(db.String(30), nullable=False)
