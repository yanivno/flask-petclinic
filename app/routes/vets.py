from flask import Blueprint, render_template, request, jsonify
from app.models import Vet

bp = Blueprint('vets', __name__)

PAGE_SIZE = 5


@bp.route('/vets.html')
def show_vets():
    page = request.args.get('page', 1, type=int)
    pagination = Vet.query.paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    vets = pagination.items
    
    return render_template('vets/vetList.html',
                          vets=vets,
                          pagination=pagination,
                          current_page=page)


@bp.route('/vets')
def vets_json():
    """Return vets as JSON for API access"""
    vets = Vet.query.all()
    return jsonify({
        'vets': [
            {
                'id': vet.id,
                'firstName': vet.first_name,
                'lastName': vet.last_name,
                'specialties': [{'id': s.id, 'name': s.name} for s in vet.specialties]
            }
            for vet in vets
        ]
    })
