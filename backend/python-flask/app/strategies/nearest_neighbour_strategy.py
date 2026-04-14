from app.strategies.route_strategy import RouteStrategy, build_route
from app.utils.haversine import calculate_distance


class NearestNeighbourStrategy(RouteStrategy):

    def optimise(self, matches: list) -> dict:
          # Sort matches by kickoff time so the route is planned in chronological order

        sorted_matches = sorted(matches, key=lambda m: m['kickoff'])

        # Group matches by date so we only compare locations within the same day
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

            # If there is only one match for the day, it becomes the chosen match automatically
            if len(daily_matches) == 1:
                chosen_match = daily_matches[0]
            else:

                 # If no current city exists yet, start with the first match in the list
                if current_city is None:
                    chosen_match = daily_matches[0]  # Start with the first match if we have no current city
                else:
                    
                    # Otherwise pick the match closest to the current city
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

                    # Add the selected match and update the current location for the next step
            
            ordered_matches.append(chosen_match)
            current_city = chosen_match['city']


        return build_route(ordered_matches, 'nearest-neighbour')
