"""
Vets REST API endpoints.
Based on Spring Petclinic REST API.
"""

from flask import request, jsonify, url_for
from app import db
from app.models import Vet, Specialty
from app.api import api_bp
from app.api.schemas import serialize_vet


@api_bp.route('/vets', methods=['GET'])
def list_vets():
    """Retrieve all veterinarians."""
    vets = Vet.query.all()
    
    if not vets:
        return jsonify([]), 200
    
    return jsonify([serialize_vet(vet) for vet in vets]), 200


@api_bp.route('/vets/<int:vet_id>', methods=['GET'])
def get_vet(vet_id):
    """Get a vet by ID."""
    vet = Vet.query.get(vet_id)
    if vet is None:
        return jsonify({'error': 'Vet not found'}), 404
    
    return jsonify(serialize_vet(vet)), 200


@api_bp.route('/vets', methods=['POST'])
def add_vet():
    """Add a new vet."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Validate required fields
    if 'firstName' not in data or not data['firstName']:
        return jsonify({'error': 'firstName is required'}), 400
    if 'lastName' not in data or not data['lastName']:
        return jsonify({'error': 'lastName is required'}), 400
    
    vet = Vet(
        first_name=data['firstName'],
        last_name=data['lastName']
    )
    
    # Handle specialties
    if 'specialties' in data and data['specialties']:
        for spec_data in data['specialties']:
            if isinstance(spec_data, dict) and 'id' in spec_data:
                specialty = Specialty.query.get(spec_data['id'])
                if specialty:
                    vet.specialties.append(specialty)
            elif isinstance(spec_data, dict) and 'name' in spec_data:
                specialty = Specialty.query.filter_by(name=spec_data['name']).first()
                if specialty:
                    vet.specialties.append(specialty)
    
    db.session.add(vet)
    db.session.commit()
    
    response = jsonify(serialize_vet(vet))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_vet', vet_id=vet.id)
    return response


@api_bp.route('/vets/<int:vet_id>', methods=['PUT'])
def update_vet(vet_id):
    """Update vet details."""
    vet = Vet.query.get(vet_id)
    if vet is None:
        return jsonify({'error': 'Vet not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Update fields if provided
    if 'firstName' in data:
        vet.first_name = data['firstName']
    if 'lastName' in data:
        vet.last_name = data['lastName']
    
    # Handle specialties
    if 'specialties' in data:
        vet.specialties = []
        if data['specialties']:
            for spec_data in data['specialties']:
                if isinstance(spec_data, dict) and 'id' in spec_data:
                    specialty = Specialty.query.get(spec_data['id'])
                    if specialty:
                        vet.specialties.append(specialty)
                elif isinstance(spec_data, dict) and 'name' in spec_data:
                    specialty = Specialty.query.filter_by(name=spec_data['name']).first()
                    if specialty:
                        vet.specialties.append(specialty)
    
    db.session.commit()
    
    return jsonify(serialize_vet(vet)), 200


@api_bp.route('/vets/<int:vet_id>', methods=['DELETE'])
def delete_vet(vet_id):
    """Delete a vet."""
    vet = Vet.query.get(vet_id)
    if vet is None:
        return jsonify({'error': 'Vet not found'}), 404
    
    db.session.delete(vet)
    db.session.commit()
    
    return '', 204
