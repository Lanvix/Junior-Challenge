from flask import Blueprint, jsonify, request
from app.models.match import Match
from app.models.flight_price import FlightPrice
from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy
# Tip: You can also import DateOnlyStrategy to compare results
# from app.strategies.date_only_strategy import DateOnlyStrategy

optimise_bp = Blueprint('optimise', __name__)

@optimise_bp.route('/optimise', methods=['POST'])
def optimise():
    match_ids = request.get_json().get('matchIds', [])
    if not match_ids:
        return jsonify({"error": "No matchIds provided"}), 400
    matches = Match.query.filter(Match.id.in_(match_ids)).all()
    if not matches:
        return jsonify({"error": "No matches found for provided IDs"}), 404
    match_dicts = [match.to_dict() for match in matches]
    strategy = NearestNeighbourStrategy()
    optimised_route = strategy.optimise(match_dicts)
    return jsonify(optimised_route), 200



@optimise_bp.route('/budget', methods=['POST'])
def budget_optimise():
    data = request.get_json()
    budget = data.get('budget')
    match_ids = data.get('matchIds', [])
    origin_city_id = data.get('originCityId')
    if budget is None or not match_ids or not origin_city_id:
        return jsonify({"error": "Missing required fields: budget, matchIds, originCityId"}), 400
    matches = Match.query.filter(Match.id.in_(match_ids)).all()
    if not matches:
        return jsonify({"error": "No matches found for provided IDs"}), 404
    match_dicts = [match.to_dict() for match in matches]
    flight_prices = FlightPrice.query.all()

    CostCalculator = __import__('app.utils.cost_calculator', fromlist=['CostCalculator']).CostCalculator
    calculator = CostCalculator()

    budget_result = calculator.calculate(match_dicts, budget, origin_city_id, flight_prices)
    return jsonify(budget_result), 200


# ============================================================
#  POST /api/route/best-value — Find best match combination within budget
# ============================================================
#
# TODO: Implement this endpoint (BONUS CHALLENGE #1)
#
# Request body:
# {
#   "budget": 5000.00,
#   "originCityId": "city-atlanta"
# }
#
# Steps:
#   1. Extract budget and originCityId from request JSON
#   2. Fetch all available matches from the database
#   3. Convert matches to dicts (using match.to_dict())
#   4. Fetch all flight prices from the database
#   5. Create a BestValueFinder instance
#   6. Call finder.find_best_value(match_dicts, budget, origin_city_id, flight_prices)
#   7. Return the BestValueResult as JSON
#
# Requirements:
#   - Find the maximum number of matches that fit within budget
#   - Must include at least 1 match in each country (USA, Mexico, Canada)
#   - Minimum 5 matches required
#   - Return optimised route with cost breakdown
#
# ============================================================
@optimise_bp.route('/best-value', methods=['POST'])
def best_value():
    # TODO: Replace with your implementation (BONUS CHALLENGE #1)
    return jsonify({}), 200
