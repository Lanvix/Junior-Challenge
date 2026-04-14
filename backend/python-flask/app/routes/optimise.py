from flask import Blueprint, jsonify, request
from app.models.match import Match
from app.models.flight_price import FlightPrice
from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy
from app.bonus.best_value_finder import BestValueFinder

optimise_bp = Blueprint('optimise', __name__)

# Handle requests that optimise a selected list of matches using the nearest-neighbour strategy
@optimise_bp.route('/optimise', methods=['POST'])
def optimise():
     # Read match IDs from the JSON payload
    match_ids = request.get_json().get('matchIds', [])

    # Reject the request early if no match IDs were provided
    if not match_ids:
        return jsonify({"error": "No matchIds provided"}), 400
    
    # Fetch only the matches requested by the client
    matches = Match.query.filter(Match.id.in_(match_ids)).all()
    
     # Return a 404 if none of the requested matches exist
    if not matches:
        return jsonify({"error": "No matches found for provided IDs"}), 404
    
    # Convert database objects into plain dictionaries for the strategy class
    match_dicts = [match.to_dict() for match in matches]

    # Use the nearest-neighbour strategy to produce an ordered route
    strategy = NearestNeighbourStrategy()
    optimised_route = strategy.optimise(match_dicts)
    return jsonify(optimised_route), 200



@optimise_bp.route('/budget', methods=['POST'])
def budget_optimise():
    data = request.get_json()
    budget = data.get('budget')
    match_ids = data.get('matchIds', [])
    origin_city_id = data.get('originCityId')

    # Reject incomplete requests before doing any expensive work
    if budget is None or not match_ids or not origin_city_id:
        return jsonify({"error": "Missing required fields: budget, matchIds, originCityId"}), 400
    
     # Fetch the requested matches so the optimisation only works on the selected set
    matches = Match.query.filter(Match.id.in_(match_ids)).all()
    if not matches:
        return jsonify({"error": "No matches found for provided IDs"}), 404
    
    # Convert ORM objects into dictionaries for the cost calculator
    match_dicts = [match.to_dict() for match in matches]

    # Load all flight prices because the budget calculation depends on travel costs
    flight_prices = FlightPrice.query.all()

    # Create the calculator and compute the final best-value result
    CostCalculator = __import__('app.utils.cost_calculator', fromlist=['CostCalculator']).CostCalculator
    calculator = CostCalculator()
    budget_result = calculator.calculate(match_dicts, budget, origin_city_id, flight_prices)
    
    return jsonify(budget_result), 200



@optimise_bp.route('/best-value', methods=['POST'])
def best_value():
    data = request.get_json() or {}

    budget = data.get('budget')
    origin_city_id = data.get('originCityId')

    if budget is None or not origin_city_id:
        return jsonify({
            "error": "Missing required fields: budget, originCityId"
        }), 400

    matches = Match.query.all()
    match_dicts = [match.to_dict() for match in matches]

    flights = FlightPrice.query.all()

    finder = BestValueFinder()
    result = finder.find_best_value(match_dicts, budget, origin_city_id, flights)

    return jsonify(result), 200
