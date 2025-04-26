from app import db

class BibleBook(db.Model):
    __tablename__ = 'bible_books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    testament = db.Column(db.String(3))  # 'OT' or 'NT'
    position = db.Column(db.Integer)  # Order in the Bible
    chapters = db.Column(db.Integer)  # Number of chapters

    progresses = db.relationship('ReadingProgress', backref='book', lazy='dynamic')

    def __repr__(self):
        return f'<BibleBook {self.name}>'

class ReadingProgress(db.Model):
    __tablename__ = 'reading_progresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('bible_books.id'))
    chapters_read = db.Column(db.JSON, default=list)  # List of chapter numbers that have been read
    chapters_timestamps = db.Column(db.JSON, default=dict)  # Dict mapping chapter numbers to timestamps

    def __repr__(self):
        return f'<ReadingProgress User {self.user_id} Book {self.book_id}>'