from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user, login_required
from app import db, admin_panel
from app.models import User, PetPost, PetImage, ContactMessage
from flask_admin.contrib.sqla import ModelView

admin_bp = Blueprint('admin_custom', __name__)

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('You must be an admin to access this page.')
        return redirect(url_for('auth.login', next=request.url))

# Add views to Flask-Admin
admin_panel.add_view(AdminModelView(User, db.session))
admin_panel.add_view(AdminModelView(PetPost, db.session))
admin_panel.add_view(AdminModelView(PetImage, db.session))
admin_panel.add_view(AdminModelView(ContactMessage, db.session))

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        abort(403)

    stats = {
        'total_users': User.query.count(),
        'total_posts': PetPost.query.count(),
        'reunited_posts': PetPost.query.filter_by(status='Reunited').count(),
        'active_posts': PetPost.query.filter_by(status='Active').count(),
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/admin/user/<int:user_id>/make_admin', methods=['POST'])
@login_required
def make_admin(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f'{user.username} is now an admin.')
    return redirect(url_for('admin_custom.dashboard'))
