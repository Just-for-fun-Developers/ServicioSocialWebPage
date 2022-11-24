# services/views.py

from flask import render_template,url_for,flash, redirect,request,Blueprint

services = Blueprint('services',__name__)

@services.route("/news")
def news():
    return render_template('news.html')