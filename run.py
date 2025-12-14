from app import create_app, db
from app.models import Owner, Pet, PetType, Visit, Vet, Specialty

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Owner': Owner,
        'Pet': Pet,
        'PetType': PetType,
        'Visit': Visit,
        'Vet': Vet,
        'Specialty': Specialty
    }


if __name__ == '__main__':
    app.run(debug=True, port=8080)
