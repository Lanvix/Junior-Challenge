from datetime import datetime
from typing import Optional
from app.strategies.route_strategy import BudgetResult, CostBreakdown


class CostCalculator:
    """
    CostCalculator — YOUR TASK #5

    ============================================================
    WHAT YOU NEED TO IMPLEMENT:
    ============================================================

    The calculate method should:
    1. Calculate ticket costs (sum of ticketPrice for all matches)
    2. Calculate flight costs (between consecutive cities + from origin)
    3. Calculate accommodation costs (nights × city's accommodationPerNight rate)
    4. Check feasibility (total ≤ budget AND visits USA, Mexico, Canada)
    5. Return suggestions if not feasible

    ============================================================
    HELPER METHODS PROVIDED:
    ============================================================

    The helper methods below are already implemented for you:
    - get_flight_price(): Look up flight price between two cities
    - calculate_nights_between(): Calculate nights between two dates
    - get_countries_visited(): Get list of unique countries from matches
    - get_missing_countries(): Check which required countries are missing
    - generate_suggestions(): Create cost-saving suggestions

    """

    REQUIRED_COUNTRIES = ['USA', 'Mexico', 'Canada']

def calculate(
    self,
    matches: list,
    budget: float,
    origin_city_id: str,
    flight_prices: list
) -> BudgetResult:
    ticket_cost = sum(match['ticketPrice'] for match in matches)
    flight_cost = 0
    accommodation_cost = 0

    current_city_id = origin_city_id
    current_date = None

    for match in matches:
        city = match['city']

        flight_cost += self.get_flight_price(current_city_id, city['id'], flight_prices)

        if current_date:
            nights = self.calculate_nights_between(current_date, match['kickoff'])
            accommodation_cost += nights * city['accommodationPerNight']

        current_city_id = city['id']
        current_date = match['kickoff']

    total_cost = ticket_cost + flight_cost + accommodation_cost

    countries_visited = self.get_countries_visited(matches)
    missing_countries = self.get_missing_countries(countries_visited)

    feasible = total_cost <= budget and not missing_countries
    minimum_budget_required = total_cost if not feasible else None
    suggestions = self.generate_suggestions(matches, total_cost, budget) if not feasible else []

    return BudgetResult(
        feasible=feasible,
        route={
            'stops': matches,
            'totalDistance': 0,
            'strategy': 'cost-calculator'
        },
        costBreakdown=CostBreakdown(
            flights=flight_cost,
            accommodation=accommodation_cost,
            tickets=ticket_cost,
            total=total_cost
        ),
        countriesVisited=countries_visited,
        missingCountries=missing_countries,
        minimumBudgetRequired=minimum_budget_required,
        suggestions=suggestions
    )


    # HELPER METHODS (Already implemented for you)
    # ============================================================

    def get_flight_price(
        self,
        from_city_id: str,
        to_city_id: str,
        flight_prices: list
    ) -> float:
        """
        Look up the flight price between two cities.
        Returns an estimated price if no direct flight exists.
        """
        if from_city_id == to_city_id:
            return 0

        for fp in flight_prices:
            if fp['from_city_id'] == from_city_id and fp['to_city_id'] == to_city_id:
                return fp['price']

        # If no direct flight, estimate based on average
        if flight_prices:
            avg_price = sum(fp['price'] for fp in flight_prices) / len(flight_prices)
            return avg_price * 1.2  # 20% markup for indirect routes
        return 300 * 1.2

    def calculate_nights_between(self, date1: str, date2: str) -> int:
        """Calculate the number of nights between two dates."""
        d1 = datetime.fromisoformat(date1.split('T')[0])
        d2 = datetime.fromisoformat(date2.split('T')[0])
        return max(0, (d2 - d1).days)

    def get_countries_visited(self, matches: list) -> list:
        """Get list of unique countries visited from matches."""
        countries = set()
        for match in matches:
            countries.add(match['city']['country'])
        return list(countries)

    def get_missing_countries(self, countries_visited: list) -> list:
        """Check which required countries (USA, Mexico, Canada) are missing."""
        return [c for c in self.REQUIRED_COUNTRIES if c not in countries_visited]

    def generate_suggestions(
        self,
        matches: list,
        total: float,
        budget: float
    ) -> list:
        """Generate cost-saving suggestions when budget is exceeded."""
        suggestions = []
        overage = total - budget

        if len(matches) > 5:
            most_expensive = max(matches, key=lambda m: m['ticketPrice'])
            suggestions.append(
                f"Consider removing the {most_expensive['homeTeam']['name']} vs "
                f"{most_expensive['awayTeam']['name']} match to save ${most_expensive['ticketPrice']}"
            )

        suggestions.append(
            f"You are ${overage:.0f} over budget. Consider reducing the number of matches."
        )

        return suggestions
