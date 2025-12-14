from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models import Owner, Pet, PetType, Visit
from app.forms import OwnerForm, PetForm, VisitForm

bp = Blueprint('owners', __name__, url_prefix='/owners')

PAGE_SIZE = 5


@bp.route('/find')
def find_owners():
    return render_template('owners/findOwners.html')


@bp.route('/')
def list_owners():
    page = request.args.get('page', 1, type=int)
    last_name = request.args.get('lastName', '')
    
    query = Owner.query
    if last_name:
        query = query.filter(Owner.last_name.ilike(f'{last_name}%'))
    
    query = query.order_by(Owner.last_name)
    pagination = query.paginate(page=page, per_page=PAGE_SIZE, error_out=False)
    owners = pagination.items
    
    # If no owners found
    if not owners:
        flash('No owners found', 'warning')
        return render_template('owners/findOwners.html', not_found=True)
    
    # If exactly one owner found, redirect to details
    if pagination.total == 1:
        return redirect(url_for('owners.show_owner', owner_id=owners[0].id))
    
    return render_template('owners/ownersList.html',
                          owners=owners,
                          pagination=pagination,
                          current_page=page)


@bp.route('/new', methods=['GET', 'POST'])
def new_owner():
    form = OwnerForm()
    if form.validate_on_submit():
        owner = Owner(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            address=form.address.data,
            city=form.city.data,
            telephone=form.telephone.data
        )
        db.session.add(owner)
        db.session.commit()
        flash('New Owner Created', 'success')
        return redirect(url_for('owners.show_owner', owner_id=owner.id))
    return render_template('owners/createOrUpdateOwnerForm.html', form=form, is_new=True)


@bp.route('/<int:owner_id>')
def show_owner(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    return render_template('owners/ownerDetails.html', owner=owner)


@bp.route('/<int:owner_id>/edit', methods=['GET', 'POST'])
def edit_owner(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    form = OwnerForm(obj=owner)
    
    if form.validate_on_submit():
        owner.first_name = form.first_name.data
        owner.last_name = form.last_name.data
        owner.address = form.address.data
        owner.city = form.city.data
        owner.telephone = form.telephone.data
        db.session.commit()
        flash('Owner Updated', 'success')
        return redirect(url_for('owners.show_owner', owner_id=owner.id))
    
    return render_template('owners/createOrUpdateOwnerForm.html', form=form, owner=owner, is_new=False)


# Pet routes
@bp.route('/<int:owner_id>/pets/new', methods=['GET', 'POST'])
def new_pet(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    form = PetForm()
    form.type_id.choices = [(t.id, t.name) for t in PetType.query.all()]
    
    if form.validate_on_submit():
        pet = Pet(
            name=form.name.data,
            birth_date=form.birth_date.data,
            type_id=form.type_id.data,
            owner_id=owner.id
        )
        db.session.add(pet)
        db.session.commit()
        flash('New Pet Added', 'success')
        return redirect(url_for('owners.show_owner', owner_id=owner.id))
    
    return render_template('pets/createOrUpdatePetForm.html', form=form, owner=owner, is_new=True)


@bp.route('/<int:owner_id>/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(owner_id, pet_id):
    owner = Owner.query.get_or_404(owner_id)
    pet = owner.get_pet(pet_id)
    if not pet:
        flash('Pet not found', 'error')
        return redirect(url_for('owners.show_owner', owner_id=owner.id))
    
    form = PetForm(obj=pet)
    form.type_id.choices = [(t.id, t.name) for t in PetType.query.all()]
    
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.birth_date = form.birth_date.data
        pet.type_id = form.type_id.data
        db.session.commit()
        flash('Pet Updated', 'success')
        return redirect(url_for('owners.show_owner', owner_id=owner.id))
    
    return render_template('pets/createOrUpdatePetForm.html', form=form, owner=owner, pet=pet, is_new=False)


# Visit routes
@bp.route('/<int:owner_id>/pets/<int:pet_id>/visits/new', methods=['GET', 'POST'])
def new_visit(owner_id, pet_id):
    owner = Owner.query.get_or_404(owner_id)
    pet = owner.get_pet(pet_id)
    if not pet:
        flash('Pet not found', 'error')
        return redirect(url_for('owners.show_owner', owner_id=owner.id))
    
    form = VisitForm()
    
    if form.validate_on_submit():
        visit = Visit(
            pet_id=pet.id,
            date=form.date.data,
            description=form.description.data
        )
        db.session.add(visit)
        db.session.commit()
        flash('Your visit has been booked', 'success')
        return redirect(url_for('owners.show_owner', owner_id=owner.id))
    
    return render_template('pets/createOrUpdateVisitForm.html', form=form, owner=owner, pet=pet)
