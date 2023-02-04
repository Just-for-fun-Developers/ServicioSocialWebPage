#page_posts/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NewsPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField("Post")


class NewsEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    time = TextAreaField('Time', validators=[DataRequired()])
    place = TextAreaField('Place', validators=[DataRequired()])
    submit = SubmitField("Event")