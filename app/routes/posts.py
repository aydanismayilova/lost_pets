import os
from flask import render_template, redirect, url_for, flash, request, abort, current_app, Blueprint
from flask_login import current_user, login_required
from app import db, mail
from app.models import PetPost, PetImage, ContactMessage, User
from app.forms import PetPostForm, ContactForm
from app.utils import save_picture
from flask_mail import Message

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PetPostForm()
    if form.validate_on_submit():
        post = PetPost(
            user_id=current_user.id,
            announcement_type=form.announcement_type.data,
            animal_type=form.animal_type.data,
            breed=form.breed.data,
            color=form.color.data,
            district=form.district.data,
            date_lost_found=form.date_lost_found.data,
            description=form.description.data,
            status='Active'
        )
        db.session.add(post)
        db.session.commit()

        # Multiple images upload (up to 5)
        files = request.files.getlist('images')
        for i, f in enumerate(files):
            if i >= 5:
                break
            if f and f.filename:
                image_fn = save_picture(f)
                image = PetImage(post_id=post.id, image_filename=image_fn)
                db.session.add(image)
        db.session.commit()
        flash('Post created successfully!')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form)

@posts_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = PetPost.query.get_or_404(post_id)
    form = ContactForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please log in to contact the poster')
            return redirect(url_for('auth.login', next=url_for('posts.post_detail', post_id=post_id)))

        message = ContactMessage(
            from_user_id=current_user.id,
            to_user_id=post.user_id,
            pet_post_id=post.id,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()

        # Send Email notification
        try:
            msg = Message(f"Contact for {post.animal_type} - {post.announcement_type}",
                          recipients=[post.author.email])
            msg.body = f"User {current_user.username} sent you a message regarding your post: \n\n {form.message.data}"
            mail.send(msg)
            flash('Message sent successfully!')
        except Exception as e:
            flash('Message saved in system, but email notification failed.', 'warning')
            print(f"Error sending email: {e}")

        return redirect(url_for('posts.post_detail', post_id=post_id))

    return render_template('post_detail.html', title=f'{post.animal_type} {post.announcement_type}', post=post, form=form)

@posts_bp.route('/post/<int:post_id>/reunited', methods=['POST'])
@login_required
def mark_reunited(post_id):
    post = PetPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    post.status = 'Reunited'
    db.session.commit()
    flash('Post marked as Reunited!')
    return redirect(url_for('posts.post_detail', post_id=post_id))
