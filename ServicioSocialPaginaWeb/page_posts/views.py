#page_posts/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from ServicioSocialPaginaWeb import db
from ServicioSocialPaginaWeb.models import NewsPost
from ServicioSocialPaginaWeb.page_posts.forms import NewsPostForm

news_posts = Blueprint('news_posts', __name__)

#CREATE
@news_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = NewsPostForm()

    if form.validate_on_submit():
        news_post = NewsPost(title=form.title.data,
                            text = form.text.data,
                            user_id=current_user.id)
        db.session.add(news_post)
        db.session.commit()
        flash('News Post Created!')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

#BLOG POST (VIEW)
@news_posts.route('/<int:news_post_id>')
def news_post(news_post_id):
    news_post = NewsPost.query.get_or_404(news_post_id)
    return render_template('news_post.html', title=news_post.title, date=news_post.date, post=news_post)


#UPDATE
@news_posts.route('/<int:news_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(news_post_id):
    news_post = NewsPost.query.get_or_404(news_post_id)
    
    if news_post.author != current_user:
        # abort(403)
        return redirect("/403")
    
    form = NewsPostForm()

    if form.validate_on_submit():
        news_post.title = form.title.data
        news_post.text = form.text.data
                        
        db.session.commit()
        flash('News Post Updated!')
        return redirect(url_for('news_posts.news_post', news_post_id=news_post.id))
    elif request.method == 'GET':
        form.title.data = news_post.title
        form.text.data = news_post.text
        print("herhehrehr")
    return render_template('create_post.html', title='Updating', form=form)

#DELETE

@news_posts.route('/<int:news_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(news_post_id):
    news_post = NewsPost.query.get_or_404(news_post_id)
    
    if news_post.author != current_user:
        abort(403)

    db.session.delete(news_post)
    db.session.commit()
    flash('News Post Deleted!')
    return redirect(url_for('core.index'))