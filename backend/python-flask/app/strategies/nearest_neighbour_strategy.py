from app.strategies.route_strategy import RouteStrategy, build_route
from app.utils.haversine import calculate_distance


class NearestNeighbourStrategy(RouteStrategy):
    """
    NearestNeighbourStrategy — YOUR TASK #3

    Implement a smarter route optimisation using the nearest-neighbour heuristic.
    The idea: when you have multiple matches on the same day (or close dates),
    choose the one that's geographically closest to where you currently are.

    This should produce shorter total distances than DateOnlyStrategy.
    """

    def optimise(self, matches: list) -> dict:
        sorted_matches = sorted(matches, key=lambda m: m['kickoff'])
        matches_by_date = {}
        for match in sorted_matches:
            date = match['kickoff'].split('T')[0]
            if date not in matches_by_date:
                matches_by_date[date] = []
            matches_by_date[date].append(match)
        
        ordered_matches = []
        current_city = None
        for date in sorted(matches_by_date.keys()):
            daily_matches = matches_by_date[date]
            if len(daily_matches) == 1:
                chosen_match = daily_matches[0]
            else:
                if current_city is None:
                    chosen_match = daily_matches[0]  # Start with the first match if we have no current city
                else:
                    closest_match = daily_matches[0]
                    closest_distance = float('inf')
                    for candidate in daily_matches:
                        dist = calculate_distance(
                            current_city['latitude'], current_city['longitude'],
                            candidate['city']['latitude'], candidate['city']['longitude']
                        )
                        if dist < closest_distance:
                            closest_distance = dist
                            closest_match = candidate
                    chosen_match = closest_match
            
            ordered_matches.append(chosen_match)
            current_city = chosen_match['city']


        return build_route(ordered_matches, 'nearest-neighbour')
