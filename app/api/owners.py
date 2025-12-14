"""
Owners REST API endpoints.
Based on Spring Petclinic REST API.
"""

from flask import request, jsonify, url_for
from app import db
from app.models import Owner, Pet, PetType, Visit
from app.api import api_bp
from app.api.schemas import (
    serialize_owner, serialize_pet, serialize_visit, parse_date
)


@api_bp.route('/owners', methods=['GET'])
def list_owners():
    """
    Retrieve all pet owners.
    Optional query param: lastName - filter owners by last name.
    """
    last_name = request.args.get('lastName')
    
    if last_name:
        owners = Owner.query.filter(Owner.last_name.ilike(f'{last_name}%')).all()
    else:
        owners = Owner.query.all()
    
    if not owners:
        return jsonify([]), 200
    
    return jsonify([serialize_owner(owner) for owner in owners]), 200


@api_bp.route('/owners/<int:owner_id>', methods=['GET'])
def get_owner(owner_id):
    """Get a pet owner by ID."""
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    
    return jsonify(serialize_owner(owner)), 200


@api_bp.route('/owners', methods=['POST'])
def add_owner():
    """Add a new pet owner."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Validate required fields
    required_fields = ['firstName', 'lastName', 'address', 'city', 'telephone']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    owner = Owner(
        first_name=data['firstName'],
        last_name=data['lastName'],
        address=data['address'],
        city=data['city'],
        telephone=data['telephone']
    )
    
    db.session.add(owner)
    db.session.commit()
    
    response = jsonify(serialize_owner(owner))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_owner', owner_id=owner.id)
    return response


@api_bp.route('/owners/<int:owner_id>', methods=['PUT'])
def update_owner(owner_id):
    """Update an owner's details."""
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Update fields if provided
    if 'firstName' in data:
        owner.first_name = data['firstName']
    if 'lastName' in data:
        owner.last_name = data['lastName']
    if 'address' in data:
        owner.address = data['address']
    if 'city' in data:
        owner.city = data['city']
    if 'telephone' in data:
        owner.telephone = data['telephone']
    
    db.session.commit()
    
    return jsonify(serialize_owner(owner)), 200


@api_bp.route('/owners/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    """Delete an owner."""
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    
    db.session.delete(owner)
    db.session.commit()
    
    return '', 204


# Owner's pets endpoints

@api_bp.route('/owners/<int:owner_id>/pets/<int:pet_id>', methods=['GET'])
def get_owners_pet(owner_id, pet_id):
    """Get a pet by ID (owner's pet)."""
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    
    pet = owner.get_pet(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    return jsonify(serialize_pet(pet)), 200


@api_bp.route('/owners/<int:owner_id>/pets', methods=['POST'])
def add_pet_to_owner(owner_id):
    """Add a new pet to an owner."""
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Validate required fields
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'name is required'}), 400
    
    # Get pet type
    pet_type = None
    if 'type' in data and data['type']:
        if isinstance(data['type'], dict) and 'id' in data['type']:
            pet_type = PetType.query.get(data['type']['id'])
        elif isinstance(data['type'], int):
            pet_type = PetType.query.get(data['type'])
    
    pet = Pet(
        name=data['name'],
        birth_date=parse_date(data.get('birthDate')),
        type=pet_type,
        owner_id=owner.id
    )
    
    db.session.add(pet)
    db.session.commit()
    
    response = jsonify(serialize_pet(pet))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_pet', pet_id=pet.id)
    return response


@api_bp.route('/owners/<int:owner_id>/pets/<int:pet_id>', methods=['PUT'])
def update_owners_pet(owner_id, pet_id):
    """Update pet details (owner's pet)."""
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    
    pet = owner.get_pet(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Update fields if provided
    if 'name' in data:
        pet.name = data['name']
    if 'birthDate' in data:
        pet.birth_date = parse_date(data['birthDate'])
    if 'type' in data and data['type']:
        if isinstance(data['type'], dict) and 'id' in data['type']:
            pet.type_id = data['type']['id']
        elif isinstance(data['type'], int):
            pet.type_id = data['type']
    
    db.session.commit()
    
    return '', 204


# Owner's pet's visits endpoints

@api_bp.route('/owners/<int:owner_id>/pets/<int:pet_id>/visits', methods=['POST'])
def add_visit_to_pet(owner_id, pet_id):
    """Add a vet visit for a pet."""
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    
    pet = owner.get_pet(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Validate required fields
    if 'description' not in data or not data['description']:
        return jsonify({'error': 'description is required'}), 400
    
    visit = Visit(
        pet_id=pet.id,
        date=parse_date(data.get('date')),
        description=data['description']
    )
    
    db.session.add(visit)
    db.session.commit()
    
    response = jsonify(serialize_visit(visit))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_visit', visit_id=visit.id)
    return response
