#page_posts/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from ServicioSocialPaginaWeb import db
from ServicioSocialPaginaWeb.models import NewsPost, NewsEvent
from ServicioSocialPaginaWeb.page_posts.forms import NewsPostForm, NewsEventForm
from ServicioSocialPaginaWeb.page_posts.image_handler import add_profile_pic
import time
import base64

news_posts = Blueprint('news_posts', __name__)

#CREATE
@news_posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = NewsPostForm()

    if form.validate_on_submit():
        # prefix_img = time.strftime("%Y%m%d-%H%M%S")
        # print(form.image1.data)
        # print(form.title.data)
        # img = add_profile_pic(form.image1.data, prefix_img)
        img = form.image1.data.read()
        news_post = NewsPost(title=form.title.data,
                             description=form.description.data,
                             imagen1=img,
                             text=form.text.data,
                             user_id=current_user.id)
        db.session.add(news_post)
        db.session.commit()
        
        
        return redirect(url_for('services.news'))
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
        
        return redirect(url_for('services.news'))
    return render_template('create_event.html', form=form)

#NEWS POST (VIEW)
@news_posts.route('/post/<int:news_post_id>')
def news_post(news_post_id):
    news_post = NewsPost.query.get_or_404(news_post_id)
    binary_data = news_post.image1
    base64_data = base64.b64encode(binary_data).decode("utf-8")
    data_url = "data:image/jpeg;base64," + base64_data

    return render_template('news_post.html', data_url=data_url, post=news_post)

#NEWS EVENT (VIEW)
@news_posts.route('/event/<int:news_event_id>')
def news_event(news_event_id):
    news_event = NewsEvent.query.get_or_404(news_event_id)
    
    return render_template('news_event.html', title=news_event.title, date=news_event.date, event=news_event)


#UPDATE POST
@news_posts.route('/<int:news_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(news_post_id):
    news_post = NewsPost.query.get_or_404(news_post_id)
    
    if news_post.author != current_user:
        # abort(403)
        return redirect("/403")
    
    form = NewsPostForm()

    if form.validate_on_submit():
        if form.image1.data:
            img = form.image1.data.read()
            news_post.image1 = img
              
        news_post.title = form.title.data
        news_post.description = form.description.data
        news_post.text = form.text.data
                        
        db.session.commit()
        
        return redirect(url_for('news_posts.news_post', news_post_id=news_post.id))
    elif request.method == 'GET':
        form.title.data = news_post.title
        form.description.data = news_post.description
        form.text.data = news_post.text
        
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

#DELETE POST

@news_posts.route('/<int:news_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(news_post_id):
    news_post = NewsPost.query.get_or_404(news_post_id)
    
    if news_post.author != current_user:
        abort(403)

    db.session.delete(news_post)
    db.session.commit()
    flash('News Post Deleted!')
    return redirect(url_for('services.news'))

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
    return redirect(url_for('services.news'))