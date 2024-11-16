from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegisterForm, LoginForm, SearchForm
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = User.query.filter_by(username=form.username.data).first()
    password = form.password.data
    password_2 = form.password_confirm.data
    if form.validate_on_submit():
        if user:
            flash('Usuário não disponível.Tente novamente', category='error')
        elif password != password_2:
            flash('Senhas incompatíveis. Tente novamente', category='error')
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Conta adicionada com Sucesso!', category='success')
            login_user(new_user)
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user, form=form)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Você está logado!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta! Tente novamente', category='error')
        else:
            flash('Email não cadastrado!', category='error')
    return render_template("login.html", user=current_user, form=form)


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route("/profile/<int:id>/")
def profile(id):
    profile_owner = User.query.get_or_404(id)
    profile_owner_posts = profile_owner.posts
    user = current_user
    return render_template("profile.html", user=user, profile_owner=profile_owner,
                           profile_owner_posts=profile_owner_posts)

