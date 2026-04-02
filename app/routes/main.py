from flask import render_template, request, url_for, Blueprint
from app.models import PetPost
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    announcement_type = request.args.get('announcement_type')
    animal_type = request.args.get('animal_type')
    district = request.args.get('district')
    search_query = request.args.get('search_query')
    sort_order = request.args.get('sort_order', 'newest')

    query = PetPost.query.filter_by(status='Active')

    if announcement_type:
        query = query.filter_by(announcement_type=announcement_type)
    if animal_type:
        query = query.filter_by(animal_type=animal_type)
    if district:
        query = query.filter_by(district=district)
    if search_query:
        search = f"%{search_query}%"
        query = query.filter(PetPost.description.like(search) | PetPost.breed.like(search))

    if sort_order == 'oldest':
        query = query.order_by(PetPost.created_at.asc())
    else:
        query = query.order_by(PetPost.created_at.desc())

    posts = query.paginate(page=page, per_page=10, error_out=False)

    return render_template('index.html', title='Home', posts=posts,
                           announcement_type=announcement_type,
                           animal_type=animal_type,
                           district=district,
                           search_query=search_query,
                           sort_order=sort_order)
