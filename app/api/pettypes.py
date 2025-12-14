"""
Pet Types REST API endpoints.
Based on Spring Petclinic REST API.
"""

from flask import request, jsonify, url_for
from app import db
from app.models import PetType
from app.api import api_bp
from app.api.schemas import serialize_pet_type


@api_bp.route('/pettypes', methods=['GET'])
def list_pet_types():
    """Retrieve all pet types."""
    pet_types = PetType.query.all()
    
    if not pet_types:
        return jsonify([]), 200
    
    return jsonify([serialize_pet_type(pt) for pt in pet_types]), 200


@api_bp.route('/pettypes/<int:pet_type_id>', methods=['GET'])
def get_pet_type(pet_type_id):
    """Get a pet type by ID."""
    pet_type = PetType.query.get(pet_type_id)
    if pet_type is None:
        return jsonify({'error': 'Pet type not found'}), 404
    
    return jsonify(serialize_pet_type(pet_type)), 200


@api_bp.route('/pettypes', methods=['POST'])
def add_pet_type():
    """Add a new pet type."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Validate required fields
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'name is required'}), 400
    
    pet_type = PetType(name=data['name'])
    
    db.session.add(pet_type)
    db.session.commit()
    
    response = jsonify(serialize_pet_type(pet_type))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_pet_type', pet_type_id=pet_type.id)
    return response


@api_bp.route('/pettypes/<int:pet_type_id>', methods=['PUT'])
def update_pet_type(pet_type_id):
    """Update pet type details."""
    pet_type = PetType.query.get(pet_type_id)
    if pet_type is None:
        return jsonify({'error': 'Pet type not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Update fields if provided
    if 'name' in data:
        pet_type.name = data['name']
    
    db.session.commit()
    
    return jsonify(serialize_pet_type(pet_type)), 200


@api_bp.route('/pettypes/<int:pet_type_id>', methods=['DELETE'])
def delete_pet_type(pet_type_id):
    """Delete a pet type."""
    pet_type = PetType.query.get(pet_type_id)
    if pet_type is None:
        return jsonify({'error': 'Pet type not found'}), 404
    
    db.session.delete(pet_type)
    db.session.commit()
    
    return '', 204
