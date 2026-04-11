# Flask helpers and Match model used for the matches API routes
from flask import Blueprint, jsonify, request
from app.models.match import Match


# Blueprint for all match-related endpoints
matches_bp = Blueprint('matches', __name__)

# Return all matches, with optional city and date filters
@matches_bp.route('', methods=['GET'])
def get_matches():
# Read optional query parameters from the URL
    city = request.args.get('city')
    date = request.args.get('date')

# Start with all matches, then narrow the query if filters are provided
    query = Match.query

# Filter by city ID when a city parameter is supplied
    if city:
        query = query.filter_by(city_id=city)

# Filter matches to the requested date using the kickoff timestamp
    if date:
        query = query.filter(Match.kickoff.startswith(date))

    # Sort matches by kickoff time before returning the response
    matches = query.order_by(Match.kickoff).all()
    # Convert SQLAlchemy objects into JSON-safe dictionaries
    return jsonify([match.to_dict() for match in matches]), 200

# Return one match by ID, or a 404 error if it does not exist
@matches_bp.route('/<id>', methods=['GET'])
def get_match_by_id(id):
    match = Match.query.get(id)
    # Return a 404 response when no match is found
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    return jsonify(match.to_dict()), 200
