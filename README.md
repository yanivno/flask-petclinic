# Flask PetClinic

A Python Flask implementation of the Spring PetClinic application.
Vibe coded with Claude & Github Copilot.

## Features

- **Owner Management**: Create, view, edit, and search for pet owners
- **Pet Management**: Add and edit pets for each owner
- **Visit Tracking**: Record visits for pets
- **Veterinarian Directory**: View list of veterinarians and their specialties

## Project Structure

```
flask-petclinic/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py             # SQLAlchemy models
│   ├── forms.py              # WTForms form classes
│   ├── routes/               # Blueprint routes
│   │   ├── main.py           # Home and error routes
│   │   ├── owners.py         # Owner, pet, visit routes
│   │   └── vets.py           # Veterinarian routes
│   ├── templates/            # Jinja2 templates
│   │   ├── base.html         # Base layout
│   │   ├── welcome.html      # Home page
│   │   ├── error.html        # Error page
│   │   ├── owners/           # Owner templates
│   │   ├── pets/             # Pet templates
│   │   └── vets/             # Vet templates
│   └── static/               # Static files (CSS, images)
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── init_db.py                # Database initialization script
└── requirements.txt          # Python dependencies
```

## Quick Start

### 1. Create a virtual environment

```bash
cd flask-petclinic
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the database with sample data

```bash
python init_db.py
```

### 4. Run the application

```bash
python run.py
```

The application will be available at http://localhost:8080

## API Endpoints

### Web Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Home page |
| GET | `/owners/find` | Find owners form |
| GET | `/owners` | List owners (with optional lastName filter) |
| GET | `/owners/new` | New owner form |
| POST | `/owners/new` | Create owner |
| GET | `/owners/<id>` | Owner details |
| GET | `/owners/<id>/edit` | Edit owner form |
| POST | `/owners/<id>/edit` | Update owner |
| GET | `/owners/<id>/pets/new` | New pet form |
| POST | `/owners/<id>/pets/new` | Create pet |
| GET | `/owners/<id>/pets/<pid>/edit` | Edit pet form |
| POST | `/owners/<id>/pets/<pid>/edit` | Update pet |
| GET | `/owners/<id>/pets/<pid>/visits/new` | New visit form |
| POST | `/owners/<id>/pets/<pid>/visits/new` | Create visit |
| GET | `/vets.html` | Veterinarians list (HTML) |
| GET | `/vets` | Veterinarians list (JSON API) |
| GET | `/oups` | Trigger error (demo) |

## Database

By default, the application uses SQLite. The database file (`petclinic.db`) is created in the project root.

To use a different database, set the `DATABASE_URL` environment variable:

```bash
# PostgreSQL
export DATABASE_URL=postgresql://user:password@localhost/petclinic

# MySQL
export DATABASE_URL=mysql://user:password@localhost/petclinic
```

## Configuration

Configuration is managed through `config.py`. Key settings:

- `SECRET_KEY`: Session encryption key (set via environment variable in production)
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled for performance

## Technology Stack

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-WTF**: Form handling and validation
- **SQLite**: Default database (configurable)
- **Jinja2**: Template engine
- **Bootstrap 5**: Frontend styling
