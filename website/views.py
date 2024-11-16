from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import PostForm, CommentForm, SearchForm
from .models import Post, Comment, User
from flask import Blueprint
from . import db

views = Blueprint('views', __name__)

@views.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@views.route("/")
def home():
    posts = Post.query.order_by(Post.created)
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/read-post/<int:id>", methods=['GET', 'POST'])
def read_post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(message=form.message.data, user_id=current_user.id, post_id=id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('views.read_post', id=id))
    return render_template("read-post.html", user=current_user, post=post, form=form)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id, description=form.description.data)
        db.session.add(post)
        db.session.commit()
        flash('Post adicionado com sucesso!', category='success')
        return redirect(url_for('auth.profile', id=current_user.id))
    return render_template("create-post.html", user=current_user, form=form)


@views.route("/update-post/<int:id>", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.description = form.description.data
        db.session.add(post)
        db.session.commit()
        flash('Edições salvas com sucesso!')
        return redirect(url_for('views.read_post', id=id))
    form.title.data = post.title
    form.content.data = post.content
    form.description.data = post.description
    return render_template("update-post.html", user=current_user, post=post, form=form)


@views.route("/delete-post/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    user = current_user
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deletado com sucesso', category='success')
        return redirect(url_for('auth.profile', id=user.id))
    except:
        flash('Opa! Algo deu errado...Tente novamente', category='error')
        return redirect(url_for('auth.profile', id=user.id))
    return render_template("delete-message.html", user=user)


@views.route("delete-comment/<int:id>")
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    user = current_user
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Comentário deletado com sucesso', category='success')
        return redirect(url_for('auth.profile', id=user.id))
    except:
        flash('Opa! Algo deu errado...Tente novamente', category='error')
        return redirect(url_for('auth.profile', id=user.id))
    return render_template("delete-message.html", user=user)


@views.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        searched = form.searched.data
        posts = posts.filter(Post.content.like('%' + searched + '%'))
        posts = posts.order_by(Post.title).all()
    return render_template("search-results.html", user=current_user, form=form, searched=searched, posts=posts)

