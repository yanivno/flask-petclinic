"""
REST API for Flask PetClinic
Based on Spring Petclinic REST API: https://github.com/spring-petclinic/spring-petclinic-rest

API Endpoints Overview:
| Method | Endpoint                                    | Description              |
|--------|---------------------------------------------|--------------------------|
| Owners                                                                         |
| GET    | /api/owners                                 | Retrieve all pet owners  |
| GET    | /api/owners/{ownerId}                       | Get a pet owner by ID    |
| POST   | /api/owners                                 | Add a new pet owner      |
| PUT    | /api/owners/{ownerId}                       | Update an owner's details|
| DELETE | /api/owners/{ownerId}                       | Delete an owner          |
| GET    | /api/owners/{ownerId}/pets/{petId}          | Get a pet by ID          |
| PUT    | /api/owners/{ownerId}/pets/{petId}          | Update pet details       |
| POST   | /api/owners/{ownerId}/pets                  | Add a new pet to owner   |
| POST   | /api/owners/{ownerId}/pets/{petId}/visits   | Add a vet visit for pet  |
| Pets                                                                           |
| GET    | /api/pets                                   | Retrieve all pets        |
| GET    | /api/pets/{petId}                           | Get a pet by ID          |
| PUT    | /api/pets/{petId}                           | Update pet details       |
| DELETE | /api/pets/{petId}                           | Delete a pet             |
| Vets                                                                           |
| GET    | /api/vets                                   | Retrieve all vets        |
| GET    | /api/vets/{vetId}                           | Get a vet by ID          |
| POST   | /api/vets                                   | Add a new vet            |
| PUT    | /api/vets/{vetId}                           | Update vet details       |
| DELETE | /api/vets/{vetId}                           | Delete a vet             |
| Pet Types                                                                      |
| GET    | /api/pettypes                               | Retrieve all pet types   |
| GET    | /api/pettypes/{petTypeId}                   | Get a pet type by ID     |
| POST   | /api/pettypes                               | Add a new pet type       |
| PUT    | /api/pettypes/{petTypeId}                   | Update pet type details  |
| DELETE | /api/pettypes/{petTypeId}                   | Delete a pet type        |
| Specialties                                                                    |
| GET    | /api/specialties                            | Retrieve all specialties |
| GET    | /api/specialties/{specialtyId}              | Get a specialty by ID    |
| POST   | /api/specialties                            | Add a new specialty      |
| PUT    | /api/specialties/{specialtyId}              | Update specialty details |
| DELETE | /api/specialties/{specialtyId}              | Delete a specialty       |
| Visits                                                                         |
| GET    | /api/visits                                 | Retrieve all vet visits  |
| GET    | /api/visits/{visitId}                       | Get a visit by ID        |
| POST   | /api/visits                                 | Add a new visit          |
| PUT    | /api/visits/{visitId}                       | Update a visit           |
| DELETE | /api/visits/{visitId}                       | Delete a visit           |
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import owners, pets, vets, visits, pettypes, specialties
