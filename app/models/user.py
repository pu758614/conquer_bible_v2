from datetime import datetime, timedelta
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date, default=datetime.utcnow().date)
    target_days = db.Column(db.Integer, default=365)  # Default to 1 year
    auto_login_token = db.Column(db.String(255), unique=True, index=True)  # Added for auto-login feature
    auto_login_pin = db.Column(db.String(6))  # PIN code for auto-login

    # Reading progress
    progresses = db.relationship('ReadingProgress', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == 'admin@example.com':
            self.is_admin = True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_completion_percentage(self, testament=None):
        from app.models.bible import BibleBook
        total_chapters = 0
        read_chapters = 0

        query = BibleBook.query
        if testament:
            query = query.filter_by(testament=testament)

        for book in query.all():
            total_chapters += book.chapters
            for progress in self.progresses.filter_by(book_id=book.id).all():
                read_chapters += len(progress.chapters_read)

        if total_chapters == 0:
            return 0

        return (read_chapters / total_chapters) * 100

    def get_target_percentage(self):
        # Calculate what percentage should be completed by now based on start date and target days
        if not self.start_date or not self.target_days:
            return 0

        days_elapsed = (datetime.utcnow().date() - self.start_date).days
        if days_elapsed < 0:
            return 0

        if days_elapsed > self.target_days:
            return 100

        return (days_elapsed / self.target_days) * 100

    def get_completion_count(self):
        # Calculate how many times user has read the entire Bible
        from app.models.bible import BibleBook
        total_chapters = sum(book.chapters for book in BibleBook.query.all())
        read_chapters = sum(len(progress.chapters_read) for progress in self.progresses.all())

        if total_chapters == 0:
            return 0

        return read_chapters // total_chapters

    def chapters_per_day(self):
        from app.models.bible import BibleBook
        total_chapters = sum(book.chapters for book in BibleBook.query.all())

        if not self.target_days or self.target_days == 0:
            return 0

        return total_chapters / self.target_days

    def generate_auto_login_token(self, pin=None):
        """Generate a secure token for automatic login"""
        if not pin or not pin.isdigit() or len(pin) < 4 or len(pin) > 6:
            return None

        self.auto_login_token = secrets.token_urlsafe(32)
        self.auto_login_pin = pin
        db.session.commit()
        return self.auto_login_token

    def clear_auto_login_token(self):
        """Remove the auto-login token"""
        self.auto_login_token = None
        self.auto_login_pin = None
        db.session.commit()

    def get_auto_login_url(self, request_base_url):
        """Get the full auto-login URL including domain"""
        from flask import url_for
        if not self.auto_login_token:
            return None

        # Extract the base URL (domain) from the request
        base_url = request_base_url.split('/')[0] + '//' + request_base_url.split('/')[2]
        token_url = url_for('auth.auto_login', token=self.auto_login_token, _external=False)
        return f"{base_url}{token_url}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))