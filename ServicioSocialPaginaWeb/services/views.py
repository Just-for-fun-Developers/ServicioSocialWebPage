# services/views.py
from flask import render_template,url_for,flash, redirect,request,Blueprint
from ServicioSocialPaginaWeb.models import NewsPost, NewsEvent
import base64

services = Blueprint('services',__name__)

@services.route("/news")
def news():
    page = request.args.get('page', 1, type=int)
    news_posts = NewsPost.query.order_by(NewsPost.date.desc()).paginate(page=page, per_page=5)
    news_events = NewsEvent.query.order_by(NewsEvent.date.desc())
    data_urls = []
    for post in news_posts.items:
        binary_data = post.image1
        base64_data = base64.b64encode(binary_data).decode("utf-8")
        data_url = "data:image/jpeg;base64," + base64_data
        data_urls.append(data_url)
    return render_template("news.html", news_posts=news_posts, news_events=news_events, data_urls=data_urls, zip=zip, list = list)