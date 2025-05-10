from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Calculate completion statistics
    ot_percentage = current_user.get_completion_percentage(testament='OT')
    nt_percentage = current_user.get_completion_percentage(testament='NT')
    total_percentage = current_user.get_completion_percentage()
    target_percentage = current_user.get_target_percentage()
    completion_count = current_user.get_completion_count()
    chapters_per_day = current_user.chapters_per_day()

    context = {
        'user': current_user,
        'ot_percentage': round(ot_percentage, 1),
        'nt_percentage': round(nt_percentage, 1),
        'total_percentage': round(total_percentage, 1),
        'target_percentage': round(target_percentage, 1),
        'completion_count': completion_count,
        'chapters_per_day': round(chapters_per_day, 1)
    }

    return render_template('main/dashboard.html', **context)

@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    from flask import request, flash
    from datetime import datetime

    if request.method == 'POST':
        start_date_str = request.form.get('start_date')
        target_days = request.form.get('target_days')
        reset = request.form.get('reset')
        generate_token = request.form.get('generate_token')
        delete_token = request.form.get('delete_token')
        pin_code = request.form.get('pin_code')

        # Handle form submission
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                current_user.start_date = start_date
            except ValueError:
                flash('日期格式錯誤', 'danger')

        if target_days:
            try:
                current_user.target_days = int(target_days)
            except ValueError:
                flash('目標天數必須是整數', 'danger')

        # Handle reset
        if reset == 'true':
            from app.models.bible import ReadingProgress

            # Delete all reading progress for this user
            ReadingProgress.query.filter_by(user_id=current_user.id).delete()
            flash('閱讀進度已重置', 'success')

        # Handle token generation
        if generate_token == 'true':
            if not pin_code or not pin_code.isdigit() or len(pin_code) < 4 or len(pin_code) > 6:
                flash('請設定4-6位數字PIN碼', 'danger')
            else:
                current_user.generate_auto_login_token(pin=pin_code)
                flash('自動登入連結已生成', 'success')

        # Handle token deletion
        if delete_token == 'true':
            current_user.clear_auto_login_token()
            flash('自動登入連結已刪除', 'success')

        from app import db
        db.session.commit()
        flash('設定已更新', 'success')
        return redirect(url_for('main.settings'))

    # Calculate suggested reading
    from app.models.bible import BibleBook
    total_chapters = sum(book.chapters for book in BibleBook.query.all())
    target_days = current_user.target_days or 365
    chapters_per_day = total_chapters / target_days

    # Get auto-login URL if token exists
    auto_login_url = None
    if current_user.auto_login_token:
        auto_login_url = current_user.get_auto_login_url(request.base_url)

    context = {
        'user': current_user,
        'total_chapters': total_chapters,
        'chapters_per_day': round(chapters_per_day, 1),
        'auto_login_url': auto_login_url
    }

    return render_template('main/settings.html', **context)