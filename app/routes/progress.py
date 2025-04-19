from flask import Blueprint, render_template, redirect, url_for, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.bible import BibleBook, ReadingProgress

progress = Blueprint('progress', __name__)

@progress.route('/progress')
@login_required
def index():
    testament = request.args.get('testament', 'OT')
    if testament not in ['OT', 'NT']:
        testament = 'OT'

    books = BibleBook.query.filter_by(testament=testament).order_by(BibleBook.position).all()

    # Get user's progress for each book
    user_progress = {}
    for book in books:
        progress_record = ReadingProgress.query.filter_by(
            user_id=current_user.id,
            book_id=book.id
        ).first()

        if progress_record:
            user_progress[book.id] = progress_record.chapters_read
        else:
            user_progress[book.id] = []

    context = {
        'testament': testament,
        'books': books,
        'user_progress': user_progress
    }

    return render_template('progress/index.html', **context)

@progress.route('/progress/book/<int:book_id>')
@login_required
def book_detail(book_id):
    book = BibleBook.query.get_or_404(book_id)

    # Get user's progress for this book
    progress_record = ReadingProgress.query.filter_by(
        user_id=current_user.id,
        book_id=book.id
    ).first()

    chapters_read = []
    if progress_record:
        chapters_read = progress_record.chapters_read

    context = {
        'book': book,
        'chapters_read': chapters_read,
        'total_chapters': book.chapters,
        'chapter_range': range(1, book.chapters + 1)
    }

    return render_template('progress/book_detail.html', **context)

@progress.route('/api/progress/toggle-chapter', methods=['POST'])
@login_required
def toggle_chapter():
    book_id = request.json.get('book_id')
    chapter = request.json.get('chapter')

    if not book_id or not chapter:
        return jsonify({'success': False, 'message': '缺少必要參數'}), 400

    try:
        book_id = int(book_id)
        chapter = int(chapter)
    except ValueError:
        return jsonify({'success': False, 'message': '參數格式錯誤'}), 400

    # Get the book to make sure it exists
    book = BibleBook.query.get_or_404(book_id)

    # Validate chapter number
    if chapter < 1 or chapter > book.chapters:
        return jsonify({'success': False, 'message': '章節號碼無效'}), 400

    # Get or create user's progress record for this book
    progress_record = ReadingProgress.query.filter_by(
        user_id=current_user.id,
        book_id=book.id
    ).first()

    if not progress_record:
        progress_record = ReadingProgress(
            user_id=current_user.id,
            book_id=book.id,
            chapters_read=[]
        )
        db.session.add(progress_record)

    # Toggle chapter in chapters_read
    chapters_read = progress_record.chapters_read or []

    if chapter in chapters_read:
        chapters_read.remove(chapter)
    else:
        chapters_read.append(chapter)
        chapters_read.sort()

    progress_record.chapters_read = chapters_read
    db.session.commit()

    return jsonify({
        'success': True,
        'book_id': book_id,
        'chapter': chapter,
        'is_read': chapter in chapters_read,
        'chapters_read': chapters_read
    })