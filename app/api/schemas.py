"""
JSON serialization schemas for the REST API.
Provides functions to convert SQLAlchemy models to dictionaries for JSON responses.
"""

from datetime import date


def serialize_pet_type(pet_type):
    """Serialize a PetType model to dictionary."""
    if pet_type is None:
        return None
    return {
        'id': pet_type.id,
        'name': pet_type.name
    }


def serialize_specialty(specialty):
    """Serialize a Specialty model to dictionary."""
    if specialty is None:
        return None
    return {
        'id': specialty.id,
        'name': specialty.name
    }


def serialize_visit(visit, include_pet=False):
    """Serialize a Visit model to dictionary."""
    if visit is None:
        return None
    data = {
        'id': visit.id,
        'date': visit.date.isoformat() if visit.date else None,
        'description': visit.description,
        'petId': visit.pet_id
    }
    if include_pet and visit.pet:
        data['pet'] = serialize_pet(visit.pet, include_visits=False)
    return data


def serialize_pet(pet, include_visits=True, include_owner=False):
    """Serialize a Pet model to dictionary."""
    if pet is None:
        return None
    data = {
        'id': pet.id,
        'name': pet.name,
        'birthDate': pet.birth_date.isoformat() if pet.birth_date else None,
        'type': serialize_pet_type(pet.type),
        'ownerId': pet.owner_id
    }
    if include_visits:
        data['visits'] = [serialize_visit(v, include_pet=False) for v in pet.visits]
    if include_owner and pet.owner:
        data['owner'] = serialize_owner(pet.owner, include_pets=False)
    return data


def serialize_owner(owner, include_pets=True):
    """Serialize an Owner model to dictionary."""
    if owner is None:
        return None
    data = {
        'id': owner.id,
        'firstName': owner.first_name,
        'lastName': owner.last_name,
        'address': owner.address,
        'city': owner.city,
        'telephone': owner.telephone
    }
    if include_pets:
        data['pets'] = [serialize_pet(p, include_visits=True, include_owner=False) for p in owner.pets]
    return data


def serialize_vet(vet):
    """Serialize a Vet model to dictionary."""
    if vet is None:
        return None
    return {
        'id': vet.id,
        'firstName': vet.first_name,
        'lastName': vet.last_name,
        'specialties': [serialize_specialty(s) for s in vet.specialties]
    }


def parse_date(date_str):
    """Parse a date string in ISO format to a date object."""
    if not date_str:
        return None
    if isinstance(date_str, date):
        return date_str
    return date.fromisoformat(date_str)
