"""
Specialties REST API endpoints.
Based on Spring Petclinic REST API.
"""

from flask import request, jsonify, url_for
from app import db
from app.models import Specialty
from app.api import api_bp
from app.api.schemas import serialize_specialty


@api_bp.route('/specialties', methods=['GET'])
def list_specialties():
    """Retrieve all vet specialties."""
    specialties = Specialty.query.all()
    
    if not specialties:
        return jsonify([]), 200
    
    return jsonify([serialize_specialty(s) for s in specialties]), 200


@api_bp.route('/specialties/<int:specialty_id>', methods=['GET'])
def get_specialty(specialty_id):
    """Get a specialty by ID."""
    specialty = Specialty.query.get(specialty_id)
    if specialty is None:
        return jsonify({'error': 'Specialty not found'}), 404
    
    return jsonify(serialize_specialty(specialty)), 200


@api_bp.route('/specialties', methods=['POST'])
def add_specialty():
    """Add a new specialty."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Validate required fields
    if 'name' not in data or not data['name']:
        return jsonify({'error': 'name is required'}), 400
    
    specialty = Specialty(name=data['name'])
    
    db.session.add(specialty)
    db.session.commit()
    
    response = jsonify(serialize_specialty(specialty))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_specialty', specialty_id=specialty.id)
    return response


@api_bp.route('/specialties/<int:specialty_id>', methods=['PUT'])
def update_specialty(specialty_id):
    """Update specialty details."""
    specialty = Specialty.query.get(specialty_id)
    if specialty is None:
        return jsonify({'error': 'Specialty not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Update fields if provided
    if 'name' in data:
        specialty.name = data['name']
    
    db.session.commit()
    
    return jsonify(serialize_specialty(specialty)), 200


@api_bp.route('/specialties/<int:specialty_id>', methods=['DELETE'])
def delete_specialty(specialty_id):
    """Delete a specialty."""
    specialty = Specialty.query.get(specialty_id)
    if specialty is None:
        return jsonify({'error': 'Specialty not found'}), 404
    
    db.session.delete(specialty)
    db.session.commit()
    
    return '', 204
