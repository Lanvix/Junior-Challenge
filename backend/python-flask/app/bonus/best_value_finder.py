from datetime import datetime
from typing import TypedDict, Optional


class BestValueResult(TypedDict):
    """Response for best value finder."""
    withinBudget: bool
    matches: list
    route: Optional[dict]
    costBreakdown: dict
    countriesVisited: list
    matchCount: int
    message: str


class BestValueFinder:
    """
    BestValueFinder — BONUS CHALLENGE #1

    ============================================================
    WHAT YOU NEED TO IMPLEMENT:
    ============================================================

    Find the best combination of matches within a given budget.

    Requirements:
    - Maximize the number of matches that fit within budget
    - Must include at least 1 match in each country (USA, Mexico, Canada)
    - Minimum 5 matches required
    - Return optimised route with cost breakdown

    This is a combinatorial optimisation problem. You can use:
    - Greedy approach: Start with cheapest matches, ensure country coverage
    - Dynamic programming: Find optimal subset within budget
    - Heuristic approach: Start with required countries, add cheapest remaining

    ============================================================
    HELPER METHODS PROVIDED:
    ============================================================

    Use the helper methods below in your implementation:
    - get_matches_by_country(): Group matches by country
    - get_flight_price(): Look up flight price between cities
    - calculate_trip_cost(): Calculate total cost for a set of matches

    """

    REQUIRED_COUNTRIES = ['USA', 'Mexico', 'Canada']

def find_best_value(self, all_matches, budget, origin_city_id, flight_prices):
    matches_by_country = self.get_matches_by_country(all_matches)

    for country in self.REQUIRED_COUNTRIES:
        if country not in matches_by_country or not matches_by_country[country]:
            return BestValueResult(
                withinBudget=False,
                matches=[],
                route=None,
                costBreakdown={},
                countriesVisited=[],
                matchCount=0,
                message=f"Cannot meet requirement: No matches in {country}"
            )

    selected_matches = []
    for country in self.REQUIRED_COUNTRIES:
        cheapest_match = min(matches_by_country[country], key=lambda m: m['ticketPrice'])
        selected_matches.append(cheapest_match)

    remaining_matches = [m for m in all_matches if m not in selected_matches]
    remaining_matches.sort(key=lambda m: m['ticketPrice'])

    for match in remaining_matches:
        if len(selected_matches) >= 5:
            break

        candidate_matches = selected_matches + [match]
        candidate_cost = self.calculate_trip_cost(candidate_matches, origin_city_id, flight_prices)

        if candidate_cost <= budget:
            selected_matches.append(match)

    total_cost = self.calculate_trip_cost(selected_matches, origin_city_id, flight_prices)
    within_budget = total_cost <= budget and len(selected_matches) >= 5
    countries_visited = list({m['country'] for m in selected_matches})

    return BestValueResult(
        withinBudget=within_budget,
        matches=selected_matches,
        route=None,
        costBreakdown={
            'totalCost': total_cost,
            'ticketCost': sum(m['ticketPrice'] for m in selected_matches),
            'flightCost': total_cost - sum(m['ticketPrice'] for m in selected_matches),
            'accommodationCost': 0
        },
        countriesVisited=countries_visited,
        matchCount=len(selected_matches),
        message="Best value matches found within budget." if within_budget else "Cannot find enough matches within budget."
    )



    def get_matches_by_country(self, matches: list) -> dict:
        """Group matches by their country."""
        by_country = {}
        for match in matches:
            country = match['city']['country']
            if country not in by_country:
                by_country[country] = []
            by_country[country].append(match)
        return by_country

    def get_flight_price(
        self,
        from_city_id: str,
        to_city_id: str,
        flight_prices: list
    ) -> float:
        """Look up the flight price between two cities."""
        if from_city_id == to_city_id:
            return 0

        for fp in flight_prices:
            if fp['from_city_id'] == from_city_id and fp['to_city_id'] == to_city_id:
                return fp['price']

        if flight_prices:
            avg_price = sum(fp['price'] for fp in flight_prices) / len(flight_prices)
            return avg_price * 1.2
        return 300 * 1.2

    def calculate_trip_cost(
        self,
        matches: list,
        origin_city_id: str,
        flight_prices: list
    ) -> float:
        """Calculate the total cost for a set of matches."""
        if not matches:
            return 0

        sorted_matches = sorted(matches, key=lambda m: m['kickoff'])

        # Ticket costs
        ticket_cost = sum(m['ticketPrice'] for m in matches)

        # Flight costs
        flight_cost = self.get_flight_price(
            origin_city_id,
            sorted_matches[0]['city']['id'],
            flight_prices
        )
        for i in range(1, len(sorted_matches)):
            flight_cost += self.get_flight_price(
                sorted_matches[i - 1]['city']['id'],
                sorted_matches[i]['city']['id'],
                flight_prices
            )

        # Accommodation costs (simplified)
        accommodation_cost = 0.0
        for i, match in enumerate(sorted_matches):
            nights = 1  # At least one night per match
            if i < len(sorted_matches) - 1:
                d1 = datetime.fromisoformat(match['kickoff'].split('T')[0])
                d2 = datetime.fromisoformat(sorted_matches[i + 1]['kickoff'].split('T')[0])
                nights = max(1, (d2 - d1).days)
            accommodation_cost += nights * match['city']['accommodationPerNight']

        return ticket_cost + flight_cost + accommodation_cost
