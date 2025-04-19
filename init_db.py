from app import create_app, db
from app.services.db_init import init_db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        init_db()
        print('Database initialized successfully!')