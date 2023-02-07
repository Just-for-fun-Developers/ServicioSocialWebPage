# services/views.py
from flask import render_template,url_for,flash, redirect,request,Blueprint
from ServicioSocialPaginaWeb.models import NewsPost, NewsEvent

services = Blueprint('services',__name__)

@services.route("/news")
def news():
    page = request.args.get('page', 1, type=int)
    news_posts = NewsPost.query.order_by(NewsPost.date.desc()).paginate(page=page, per_page=5)
    news_events = NewsEvent.query.order_by(NewsEvent.date.desc())
    return render_template('news.html', news_posts=news_posts, news_events=news_events )