from flask import render_template, request, redirect, url_for, session, flash, make_response
from . import accounts_bp

# Заглушка для автентифікації
VALID_USER = {
    "username": "user1",
    "password": "12345"
}

# Login
@accounts_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USER['username'] and password == VALID_USER['password']:
            session['user'] = username
            flash('Вхід успішний!', 'success')
            return redirect(url_for('accounts.profile'))
        else:
            flash('Невірний логін або пароль', 'error')
            return redirect(url_for('accounts.login'))

    return render_template('accounts/login.html')


# Profile
@accounts_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        flash('Ви повинні увійти', 'error')
        return redirect(url_for('accounts.login'))

    # Створюємо словник поточних кукі для шаблону
    cookies_dict = dict(request.cookies)

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_cookie':
            key = request.form.get('key')
            value = request.form.get('value')
            max_age = int(request.form.get('max_age', 3600))
            if key and value:
                flash(f'Cookie "{key}" додано', 'success')
                cookies_dict[key] = value  # одразу додаємо в словник
            else:
                flash('Будь ласка, заповніть ключ та значення', 'error')

        elif action == 'delete_cookie':
            key = request.form.get('key')
            if key:
                flash(f'Cookie "{key}" видалено', 'success')
                cookies_dict.pop(key, None)  # видаляємо з словника
            else:
                flash('Всі кукі видалено', 'success')
                cookies_dict.clear()

    # Створюємо відповідь з шаблону
    resp = make_response(render_template(
        'accounts/profile.html',
        user=session['user'],
        cookies=cookies_dict,
        theme=request.cookies.get('theme', 'light')
    ))

    # Встановлюємо/видаляємо кукі у відповіді
    if request.method == 'POST':
        if action == 'add_cookie' and key and value:
            resp.set_cookie(key, value, max_age=max_age)
        elif action == 'delete_cookie':
            if key:
                resp.delete_cookie(key)
            else:
                for k in request.cookies.keys():
                    resp.delete_cookie(k)

    return resp


# Logout
@accounts_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Ви вийшли з системи', 'info')
    return redirect(url_for('accounts.login'))


# Вибір кольорової теми
@accounts_bp.route('/set_theme/<theme>')
def set_theme(theme):
    if theme not in ['light', 'dark']:
        theme = 'light'

    resp = make_response(redirect(url_for('accounts.profile')))
    resp.set_cookie('theme', theme, max_age=60*60*24*30)  # зберігаємо на 30 днів
    flash(f'Тема змінена на {theme}', 'info')
    return resp
