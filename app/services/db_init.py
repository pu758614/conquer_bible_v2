from app import db
from app.models.bible import BibleBook
from app.models.bible_data import BIBLE_BOOKS
from app.models.user import User
from werkzeug.security import generate_password_hash

def init_bible_books():
    """Initialize the Bible books in the database."""
    if BibleBook.query.count() == 0:
        for book_data in BIBLE_BOOKS:
            book = BibleBook(**book_data)
            db.session.add(book)
        db.session.commit()
        print('Bible books initialized successfully.')
    else:
        print('Bible books already initialized.')

def create_admin_user():
    """Create the default admin user if it doesn't exist."""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password='1234567891',
            name='Administrator',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully.')
    else:
        print('Admin user already exists.')

def init_db():
    """Initialize the database with required data."""
    init_bible_books()
    create_admin_user()
    print('Database initialized successfully.')