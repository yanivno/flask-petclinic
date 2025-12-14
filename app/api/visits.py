"""
Visits REST API endpoints.
Based on Spring Petclinic REST API.
"""

from flask import request, jsonify, url_for
from app import db
from app.models import Visit, Pet
from app.api import api_bp
from app.api.schemas import serialize_visit, parse_date


@api_bp.route('/visits', methods=['GET'])
def list_visits():
    """Retrieve all vet visits."""
    visits = Visit.query.all()
    
    if not visits:
        return jsonify([]), 200
    
    return jsonify([serialize_visit(visit) for visit in visits]), 200


@api_bp.route('/visits/<int:visit_id>', methods=['GET'])
def get_visit(visit_id):
    """Get a visit by ID."""
    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({'error': 'Visit not found'}), 404
    
    return jsonify(serialize_visit(visit)), 200


@api_bp.route('/visits', methods=['POST'])
def add_visit():
    """Add a new visit."""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Validate required fields
    if 'description' not in data or not data['description']:
        return jsonify({'error': 'description is required'}), 400
    if 'petId' not in data or not data['petId']:
        return jsonify({'error': 'petId is required'}), 400
    
    # Validate pet exists
    pet = Pet.query.get(data['petId'])
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    
    visit = Visit(
        pet_id=data['petId'],
        date=parse_date(data.get('date')),
        description=data['description']
    )
    
    db.session.add(visit)
    db.session.commit()
    
    response = jsonify(serialize_visit(visit))
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_visit', visit_id=visit.id)
    return response


@api_bp.route('/visits/<int:visit_id>', methods=['PUT'])
def update_visit(visit_id):
    """Update a visit."""
    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({'error': 'Visit not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Update fields if provided
    if 'date' in data:
        visit.date = parse_date(data['date'])
    if 'description' in data:
        visit.description = data['description']
    if 'petId' in data:
        visit.pet_id = data['petId']
    
    db.session.commit()
    
    return jsonify(serialize_visit(visit)), 200


@api_bp.route('/visits/<int:visit_id>', methods=['DELETE'])
def delete_visit(visit_id):
    """Delete a visit."""
    visit = Visit.query.get(visit_id)
    if visit is None:
        return jsonify({'error': 'Visit not found'}), 404
    
    db.session.delete(visit)
    db.session.commit()
    
    return '', 204
