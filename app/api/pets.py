"""
Pets REST API endpoints.
Based on Spring Petclinic REST API.
"""

from flask import request, jsonify, url_for
from app import db
from app.models import Pet, PetType
from app.api import api_bp
from app.api.schemas import serialize_pet, parse_date


@api_bp.route('/pets', methods=['GET'])
def list_pets():
    """Retrieve all pets."""
    pets = Pet.query.all()
    
    if not pets:
        return jsonify([]), 200
    
    return jsonify([serialize_pet(pet) for pet in pets]), 200


@api_bp.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Get a pet by ID."""
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    return jsonify(serialize_pet(pet)), 200


@api_bp.route('/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    """Update pet details."""
    pet = Pet.query.get(pet_id)
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
    if 'ownerId' in data:
        pet.owner_id = data['ownerId']
    
    db.session.commit()
    
    return jsonify(serialize_pet(pet)), 200


@api_bp.route('/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    """Delete a pet."""
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    db.session.delete(pet)
    db.session.commit()
    
    return '', 204
