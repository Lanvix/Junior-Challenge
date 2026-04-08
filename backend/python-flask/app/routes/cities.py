from flask import Blueprint, jsonify
from app.models.city import City

cities_bp = Blueprint('cities', __name__)
# Fetch all cities and convert each SQLAlchemy object
# into a dictionary so Flask can return a JSON array.
@cities_bp.route('/')
def get_all():
    cities = City.query.all()
    return jsonify([city.to_dict() for city in cities]) 