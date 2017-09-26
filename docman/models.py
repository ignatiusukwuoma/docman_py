from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
from docman import db, login_manager


class User(UserMixin, db.Model):
    """
    User Table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True, nullable=False)
    email = db.Column(db.String(60), index=True, unique=True, nullable=False)
    name = db.Column(db.String(60), index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=2, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    documents = db.relationship("Document", back_populates="user")
    role = db.relationship("Role", back_populates="users")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Document(db.Model):
    """
    Document Table
    """
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.UnicodeText)
    access = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    user = db.relationship("User", back_populates="documents")

    def __repr__(self):
        return '<Document: {}, User {}>'.format(self.title, self.user)


class Role(db.Model):
    """
    Role Table
    """
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    users = db.relationship("User", back_populates="role")

    def __repr__(self):
        return '<Role: {}>'.format(self.title)
