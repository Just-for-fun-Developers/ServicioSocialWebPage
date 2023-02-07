# users/views.py
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from ServicioSocialPaginaWeb import db
from ServicioSocialPaginaWeb.models import User, NewsPost
from ServicioSocialPaginaWeb.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from ServicioSocialPaginaWeb.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)
# register


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)
# login


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        print(form.password.data)
        print(user.check_password(form.password.data))
        if user.check_password(form.password.data) and user is not None:
            print('ok1')
            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('core.index')
                print("ok2")
            return redirect(next)
    return render_template('login.html', form=form)


# logout


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))

# account (update UserForm)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        print(form.picture.data)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for(
        'static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

# user's list of News Post


@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    news_posts = NewsPost.query.filter_by(author=user).order_by(
        NewsPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('user_news_posts.html', news_posts=news_posts, user=user)
