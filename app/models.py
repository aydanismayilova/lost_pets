from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('PetPost', backref='author', lazy='dynamic')
    messages_sent = db.relationship('ContactMessage', foreign_keys='ContactMessage.from_user_id', backref='sender', lazy='dynamic')
    messages_received = db.relationship('ContactMessage', foreign_keys='ContactMessage.to_user_id', backref='recipient', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class PetPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    announcement_type = db.Column(db.String(10), nullable=False) # 'Lost' or 'Found'
    animal_type = db.Column(db.String(20), nullable=False) # 'Cat', 'Dog', 'Bird', 'Other'
    breed = db.Column(db.String(50))
    color = db.Column(db.String(30))
    district = db.Column(db.String(50), nullable=False)
    date_lost_found = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Active') # 'Active', 'Reunited', 'Removed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship('PetImage', backref='post', lazy='dynamic', cascade="all, delete-orphan")
    messages = db.relationship('ContactMessage', backref='post', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<PetPost {self.id} - {self.announcement_type}>'

class PetImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('pet_post.id'), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<PetImage {self.image_filename}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pet_post_id = db.Column(db.Integer, db.ForeignKey('pet_post.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactMessage from {self.from_user_id} to {self.to_user_id}>'
