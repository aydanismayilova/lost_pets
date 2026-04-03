from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli-acar-123'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.instance_path}/database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Verilənlər Bazası Modeli (İstifadəçi) [cite: 28]
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    pets = db.relationship('Pet', backref='owner', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='lost')  # lost or found
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Qeydiyyat (Registration) 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Bu istifadəçi adı artıq mövcuddur. Başqa ad seçin.')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            password=generate_password_hash(password, method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Qeydiyyat uğurla tamamlandı. Zəhmət olmasa giriş edin.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Giriş (Login) 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and (check_password_hash(user.password, password) or user.password == password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('İstifadəçi adı və ya şifrə səhvdir!')
    return render_template('login.html')

@app.route('/')
@login_required
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/post_ad', methods=['GET', 'POST'])
@login_required
def post_ad():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        location = request.form.get('location')
        contact = request.form.get('contact')
        status = request.form.get('status')

        new_pet = Pet(
            name=name,
            description=description,
            location=location,
            contact=contact,
            status=status,
            user_id=current_user.id
        )
        db.session.add(new_pet)
        db.session.commit()
        flash('Elan uğurla yerləşdirildi!')
        return redirect(url_for('index'))
    return render_template('post_ad.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Verilənlər bazasını yaradır
    app.run(debug=True)