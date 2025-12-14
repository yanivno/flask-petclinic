from datetime import date
from app import db

# Association table for vet specialties (many-to-many)
vet_specialties = db.Table('vet_specialties',
    db.Column('vet_id', db.Integer, db.ForeignKey('vets.id'), primary_key=True),
    db.Column('specialty_id', db.Integer, db.ForeignKey('specialties.id'), primary_key=True)
)


class PetType(db.Model):
    __tablename__ = 'types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return self.name


class Specialty(db.Model):
    __tablename__ = 'specialties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return self.name


class Owner(db.Model):
    __tablename__ = 'owners'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    
    pets = db.relationship('Pet', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_pet(self, pet_id):
        return Pet.query.filter_by(id=pet_id, owner_id=self.id).first()
    
    def __repr__(self):
        return f'<Owner {self.first_name} {self.last_name}>'


class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.Date)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    
    type = db.relationship('PetType')
    visits = db.relationship('Visit', backref='pet', lazy='dynamic', cascade='all, delete-orphan',
                            order_by='Visit.date')
    
    def __repr__(self):
        return f'<Pet {self.name}>'


class Visit(db.Model):
    __tablename__ = 'visits'
    
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    date = db.Column(db.Date, default=date.today)
    description = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f'<Visit {self.date}>'


class Vet(db.Model):
    __tablename__ = 'vets'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    specialties = db.relationship('Specialty', secondary=vet_specialties,
                                  backref=db.backref('vets', lazy='dynamic'))
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Vet {self.first_name} {self.last_name}>'
