from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.bible import ReadingProgress

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.before_request
def restrict_to_admins():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)  # Forbidden

@admin.route('/')
@login_required
def index():
    users = User.query.all()

    # Calculate completion percentage for each user
    user_stats = []
    for user in users:
        user_stats.append({
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'is_admin': user.is_admin,
            'completion': round(user.get_completion_percentage(), 1)
        })

    return render_template('admin/index.html', users=user_stats)

@admin.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)

    # Calculate stats
    ot_percentage = user.get_completion_percentage(testament='OT')
    nt_percentage = user.get_completion_percentage(testament='NT')
    total_percentage = user.get_completion_percentage()
    target_percentage = user.get_target_percentage()
    completion_count = user.get_completion_count()

    context = {
        'user': user,
        'ot_percentage': round(ot_percentage, 1),
        'nt_percentage': round(nt_percentage, 1),
        'total_percentage': round(total_percentage, 1),
        'target_percentage': round(target_percentage, 1),
        'completion_count': completion_count
    }

    return render_template('admin/user_detail.html', **context)

@admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')
        is_admin = 'is_admin' in request.form

        # Update user data
        user.username = username
        user.name = name
        if password:
            user.password = password
        user.is_admin = is_admin

        db.session.commit()
        flash(f'使用者 {username} 已更新', 'success')
        return redirect(url_for('admin.user_detail', user_id=user.id))

    return render_template('admin/edit_user.html', user=user)

@admin.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('無法刪除自己的帳號', 'danger')
        return redirect(url_for('admin.index'))

    # Delete user's reading progress
    ReadingProgress.query.filter_by(user_id=user.id).delete()

    username = user.username
    db.session.delete(user)
    db.session.commit()

    flash(f'使用者 {username} 已刪除', 'success')
    return redirect(url_for('admin.index'))