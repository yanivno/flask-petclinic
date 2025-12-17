import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Use /tmp directory on Azure for writable SQLite database
# Note: /tmp is ephemeral and data will be lost on app restart
if os.environ.get('WEBSITE_INSTANCE_ID'):  # Running on Azure
    db_path = '/tmp/petclinic.db'
else:
    db_path = os.path.join(basedir, 'petclinic.db')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
