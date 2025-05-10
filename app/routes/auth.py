from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            next_page = request.args.get('next')

            # If user does not have a name, redirect to profile setup
            if not user.name:
                flash('請輸入您的名稱以完成註冊', 'info')
                return redirect(url_for('auth.profile_setup'))

            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('登入失敗，請檢查您的帳號和密碼', 'danger')

    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('密碼不一致', 'danger')
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('帳號已經存在', 'danger')
            return render_template('auth/register.html')

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('註冊成功，請登入', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth.route('/profile-setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    if current_user.name:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')

        if not name:
            flash('請輸入您的名稱', 'danger')
            return render_template('auth/profile_setup.html')

        current_user.name = name
        db.session.commit()

        flash('個人資料設定成功', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('auth/profile_setup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/auto-login/<token>')
def auto_login(token):
    """Handle automatic login with token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    user = User.query.filter_by(auto_login_token=token).first()

    if not user:
        flash('無效的登入連結', 'danger')
        return redirect(url_for('auth.login'))

    # Check if pin is in the URL parameters
    pin = request.args.get('pin')

    # Initialize session for tracking PIN attempts if not present
    session_key = f'pin_attempts_{token}'
    if session_key not in session:
        session[session_key] = 0

    # If there's no PIN in the URL and user has a PIN set, show PIN form
    if not pin and user.auto_login_pin:
        return render_template('auth/enter_pin.html', token=token)

    # Check if too many failed attempts (limit to 5)
    if session[session_key] >= 5:
        flash('嘗試次數過多，請稍後再試', 'danger')
        return redirect(url_for('auth.login'))

    # If PIN is provided, verify it
    if user.auto_login_pin and pin != user.auto_login_pin:
        session[session_key] += 1
        flash(f'PIN碼錯誤，剩餘嘗試次數：{5 - session[session_key]}', 'danger')
        return render_template('auth/enter_pin.html', token=token)

    # Reset attempts counter on successful login
    if session_key in session:
        session.pop(session_key)

    login_user(user)
    flash(f'歡迎回來，{user.name}！', 'success')
    return redirect(url_for('main.dashboard'))