from flask import Flask, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
from flask_ckeditor import CKEditor


'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)



# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    posts = BlogPost.query.all()
    posts_list = [post for post in posts]
    return render_template("index.html", all_posts=posts_list)

# TODO: Add a route so that you can click on individual posts.
@app.route('/')
def show_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id
    requested_post = BlogPost.query.get(post_id)
    
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    body = CKEditorField('Body', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Create Post')

@app.route('/newpost', methods=['GET', 'POST'])
def add_new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        body = form.body.data
        author = form.author.data
        img_url = form.img_url.data
        
        # Create a new BlogPost object
        new_post = BlogPost(
            title=title,
            subtitle=subtitle,
            date=date.today().strftime("%B %d, %Y"),
            body=body,
            author=author,
            img_url=img_url
        )
        
        # Add the new post to the database
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('get_all_posts'))
    
    return render_template("make-post.html", form=form)



@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.author = form.author.data
        post.img_url = form.img_url.data

        db.session.commit()
        return redirect(url_for('get_all_posts'))

    # Pre-fill the form with the existing post data
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.body.data = post.body
        form.author.data = post.author
        form.img_url.data = post.img_url


    return render_template("make-post.html", form=form, post_id=post_id)
   

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True, port=5003)
