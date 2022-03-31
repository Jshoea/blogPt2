"""Blogly application."""

from curses import flash
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
from  flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Homepage + show first 5 recent posts"""
    
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)



@app.route('/users')
def users_index():
    """Show page with user info"""
    users =  User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Page to create a user"""
    return render_template('users/new.html')

@app.route("/user/new", methods= ["POST"])
def users_new():
    """Handle form submissions"""

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url' or None]
    )

    db.sesssion.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added!")
    return redirect("/users")


@app.route('users/<int:user_id>')
def users_show(user_id):
    """Page of info on user"""

    user = User.query.get_or_404(user_id),
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit existing user info"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Will handle the form submission and update the existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")
    #go back to users after this

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handles the form submission to delete a user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect ("/users")


@app.errorhandler(404)
def page_not_found(e):
    """the 404 page"""

    return render_template('404.html'), 404


#Post Route
@app.route('/users/<int:user_id>/posts/new')
def posts_new_form(user_id):
    """Shows form to create new post for a user"""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating new post for a user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title= request.form['title'],
                    content= request.form['content'],
                    user = user)

    db.sesion.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added!")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with info of a specific post"""

    post=Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a page with info of a specific post to update"""

    post=Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/post/<int:post_id>/edit', methods=["POST"])
def post_update(post_id):
    """Handle form for updating post"""

    post=Post.query.get_or_404(post_id)
    post.title= request.form('title')
    post.content= request.content('cotent')

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' has been editted")


    return redirect(f"/users/{post.user_id}")

@app.route('/post/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handles Form for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit
    flash(f"Post '{post.title}' was deleted")

    return redirect(f"/users/{post.user_id}")