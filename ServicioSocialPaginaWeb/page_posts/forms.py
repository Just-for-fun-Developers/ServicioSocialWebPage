#page_posts/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class NewsPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    image1 = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField("Post")


class NewsEventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    time = TextAreaField('Time', validators=[DataRequired()])
    place = TextAreaField('Place', validators=[DataRequired()])
    submit = SubmitField("Event")