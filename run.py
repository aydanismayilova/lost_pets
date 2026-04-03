from app import create_app, db
from app.models import User, PetPost, PetImage, ContactMessage

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'PetPost': PetPost, 'PetImage': PetImage, 'ContactMessage': ContactMessage}

if __name__ == '__main__':
    app.run(debug=True)
