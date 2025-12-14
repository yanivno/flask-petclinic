from flask import Blueprint, render_template

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('welcome.html')


@bp.route('/oups')
def trigger_error():
    raise RuntimeError('Expected: controller used to showcase what happens when an exception is thrown')


@bp.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html', error=str(error)), 500
