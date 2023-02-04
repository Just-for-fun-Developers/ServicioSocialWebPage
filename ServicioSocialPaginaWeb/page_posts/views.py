#page_posts/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from ServicioSocialPaginaWeb import db
from ServicioSocialPaginaWeb.models import NewsPost, NewsEvent
from ServicioSocialPaginaWeb.page_posts.forms import NewsPostForm, NewsEventForm

news_posts = Blueprint('news_posts', __name__)

#CREATE
@news_posts.route('/create_post', methods=['GET', 'POST'])
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

#CREATE EVENT
@news_posts.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = NewsEventForm()

    if form.validate_on_submit():
        news_event = NewsEvent(title=form.title.data,
                            time = form.time.data,
                            place = form.place.data,
                            user_id=current_user.id)
        db.session.add(news_event)
        db.session.commit()
        
        return redirect(url_for('core.index'))
    return render_template('create_event.html', form=form)

#NEWS EVENT (VIEW)
@news_posts.route('/post/<int:news_post_id>')
def news_post(news_post_id):
    news_post = NewsPost.query.get_or_404(news_post_id)
    return render_template('news_post.html', title=news_post.title, date=news_post.date, post=news_post)

#BLOG POST (VIEW)
@news_posts.route('/event/<int:news_event_id>')
def news_event(news_event_id):
    news_event = NewsEvent.query.get_or_404(news_event_id)
    return render_template('news_event.html', title=news_event.title, date=news_event.date, event=news_event)


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

#UPDATE EVENT
@news_posts.route('/event/<int:news_event_id>/update', methods=['GET', 'POST'])
@login_required
def update_event(news_event_id):
    news_event = NewsEvent.query.get_or_404(news_event_id)
    
    if news_event.author != current_user:
        # abort(403)
        return redirect("/403")
    
    form = NewsEventForm()

    if form.validate_on_submit():
        news_event.title = form.title.data
        news_event.time = form.time.data
        news_event.place = form.place.data
                        
        db.session.commit()
        flash('News Event Updated!')
        return redirect(url_for('news_posts.news_event', news_event_id=news_event.id))
    elif request.method == 'GET':
        form.title.data = news_event.title
        form.time.data = news_event.time
        form.place.data = news_event.place
        print("herhehrehr")
    return render_template('create_event.html', title='Updating', form=form)

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

#DELETE EVENT
@news_posts.route('/event/<int:news_event_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_event(news_event_id):
    news_event = NewsEvent.query.get_or_404(news_event_id)
    
    if news_event.author != current_user:
        abort(403)

    db.session.delete(news_event)
    db.session.commit()
    flash('News Post Deleted!')
    return redirect(url_for('core.index'))