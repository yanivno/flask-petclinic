"""
Database initialization script with sample data.
Run this script to populate the database with sample data.
"""
from datetime import date
from app import create_app, db
from app.models import Owner, Pet, PetType, Visit, Vet, Specialty


def init_db():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create pet types
        pet_types = [
            PetType(name='cat'),
            PetType(name='dog'),
            PetType(name='lizard'),
            PetType(name='snake'),
            PetType(name='bird'),
            PetType(name='hamster'),
        ]
        for pt in pet_types:
            db.session.add(pt)
        db.session.commit()
        
        # Create specialties
        specialties = [
            Specialty(name='radiology'),
            Specialty(name='surgery'),
            Specialty(name='dentistry'),
        ]
        for s in specialties:
            db.session.add(s)
        db.session.commit()
        
        # Create vets
        vets_data = [
            {'first_name': 'James', 'last_name': 'Carter', 'specialties': []},
            {'first_name': 'Helen', 'last_name': 'Leary', 'specialties': ['radiology']},
            {'first_name': 'Linda', 'last_name': 'Douglas', 'specialties': ['surgery', 'dentistry']},
            {'first_name': 'Rafael', 'last_name': 'Ortega', 'specialties': ['surgery']},
            {'first_name': 'Henry', 'last_name': 'Stevens', 'specialties': ['radiology']},
            {'first_name': 'Sharon', 'last_name': 'Jenkins', 'specialties': []},
        ]
        
        specialty_map = {s.name: s for s in Specialty.query.all()}
        
        for v_data in vets_data:
            vet = Vet(first_name=v_data['first_name'], last_name=v_data['last_name'])
            for spec_name in v_data['specialties']:
                vet.specialties.append(specialty_map[spec_name])
            db.session.add(vet)
        db.session.commit()
        
        # Create owners
        owners_data = [
            {'first_name': 'George', 'last_name': 'Franklin', 'address': '110 W. Liberty St.', 'city': 'Madison', 'telephone': '6085551023'},
            {'first_name': 'Betty', 'last_name': 'Davis', 'address': '638 Cardinal Ave.', 'city': 'Sun Prairie', 'telephone': '6085551749'},
            {'first_name': 'Eduardo', 'last_name': 'Rodriquez', 'address': '2693 Commerce St.', 'city': 'McFarland', 'telephone': '6085558763'},
            {'first_name': 'Harold', 'last_name': 'Davis', 'address': '563 Friendly St.', 'city': 'Windsor', 'telephone': '6085553198'},
            {'first_name': 'Peter', 'last_name': 'McTavish', 'address': '2387 S. Fair Way', 'city': 'Madison', 'telephone': '6085552765'},
            {'first_name': 'Jean', 'last_name': 'Coleman', 'address': '105 N. Lake St.', 'city': 'Monona', 'telephone': '6085552654'},
            {'first_name': 'Jeff', 'last_name': 'Black', 'address': '1450 Oak Blvd.', 'city': 'Monona', 'telephone': '6085555387'},
            {'first_name': 'Maria', 'last_name': 'Escobito', 'address': '345 Maple St.', 'city': 'Madison', 'telephone': '6085557683'},
            {'first_name': 'David', 'last_name': 'Schroeder', 'address': '2749 Blackhawk Trail', 'city': 'Madison', 'telephone': '6085559435'},
            {'first_name': 'Carlos', 'last_name': 'Estaban', 'address': '2335 Independence La.', 'city': 'Waunakee', 'telephone': '6085555487'},
        ]
        
        for o_data in owners_data:
            owner = Owner(**o_data)
            db.session.add(owner)
        db.session.commit()
        
        # Get pet types by name
        type_map = {pt.name: pt for pt in PetType.query.all()}
        
        # Create pets
        pets_data = [
            {'name': 'Leo', 'birth_date': date(2010, 9, 7), 'type': 'cat', 'owner_id': 1},
            {'name': 'Basil', 'birth_date': date(2012, 8, 6), 'type': 'hamster', 'owner_id': 2},
            {'name': 'Rosy', 'birth_date': date(2011, 4, 17), 'type': 'dog', 'owner_id': 3},
            {'name': 'Jewel', 'birth_date': date(2010, 3, 7), 'type': 'dog', 'owner_id': 3},
            {'name': 'Iggy', 'birth_date': date(2010, 11, 30), 'type': 'lizard', 'owner_id': 4},
            {'name': 'George', 'birth_date': date(2010, 1, 20), 'type': 'snake', 'owner_id': 5},
            {'name': 'Samantha', 'birth_date': date(2012, 9, 4), 'type': 'cat', 'owner_id': 6},
            {'name': 'Max', 'birth_date': date(2012, 9, 4), 'type': 'cat', 'owner_id': 6},
            {'name': 'Lucky', 'birth_date': date(2011, 8, 6), 'type': 'bird', 'owner_id': 7},
            {'name': 'Mulligan', 'birth_date': date(2007, 2, 24), 'type': 'dog', 'owner_id': 8},
            {'name': 'Freddy', 'birth_date': date(2010, 3, 9), 'type': 'bird', 'owner_id': 9},
            {'name': 'Lucky', 'birth_date': date(2010, 6, 24), 'type': 'dog', 'owner_id': 10},
            {'name': 'Sly', 'birth_date': date(2012, 6, 8), 'type': 'cat', 'owner_id': 10},
        ]
        
        for p_data in pets_data:
            pet = Pet(
                name=p_data['name'],
                birth_date=p_data['birth_date'],
                type_id=type_map[p_data['type']].id,
                owner_id=p_data['owner_id']
            )
            db.session.add(pet)
        db.session.commit()
        
        # Create visits
        visits_data = [
            {'pet_id': 7, 'date': date(2013, 1, 1), 'description': 'rabies shot'},
            {'pet_id': 8, 'date': date(2013, 1, 2), 'description': 'rabies shot'},
            {'pet_id': 8, 'date': date(2013, 1, 3), 'description': 'neutered'},
            {'pet_id': 7, 'date': date(2013, 1, 4), 'description': 'spayed'},
        ]
        
        for v_data in visits_data:
            visit = Visit(**v_data)
            db.session.add(visit)
        db.session.commit()
        
        print("Database initialized with sample data!")


if __name__ == '__main__':
    init_db()
