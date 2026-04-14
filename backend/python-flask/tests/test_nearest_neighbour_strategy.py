import pytest
from app.strategies.nearest_neighbour_strategy import NearestNeighbourStrategy


class TestNearestNeighbourStrategy:
    """
    NearestNeighbourStrategyTest — YOUR TASK #4

    ============================================================
    WHAT YOU NEED TO IMPLEMENT:
    ============================================================

    Write unit tests for the NearestNeighbourStrategy.
    Each test has a TODO comment explaining what to test.

    """

def setup_method(self):
    self.strategy = NearestNeighbourStrategy()

def test_happy_path_returns_valid_route(self):
    """Should return a valid route for multiple matches (happy path)"""
    matches = [
        {
            "id": "match-1",
            "kickoff": "2024-11-01T20:00:00Z",
            "city": { "id": "city-1", "name": "City 1", "latitude": 40.7128, "longitude": -74.0060 }
        },
        {
            "id": "match-2",
            "kickoff": "2024-11-02T20:00:00Z",
            "city": { "id": "city-2", "name": "City 2", "latitude": 34.0522, "longitude": -118.2437 }
        },
        {
            "id": "match-3",
            "kickoff": "2024-11-02T21:00:00Z",
            "city": { "id": "city-3", "name": "City 3", "latitude": 41.8781, "longitude": -87.6298 }
        }
    ]
    result = self.strategy.optimise(matches)
    assert 'stops' in result
    assert 'totalDistance' in result
    assert len(result['stops']) == 3
    assert result['totalDistance'] > 0

    def test_empty_matches_returns_empty_route(self):
        """Should return an empty route for empty matches"""
        result = self.strategy.optimise([])
        assert result['stops'] == []
        assert result['totalDistance'] == 0
  
    def test_single_match_returns_zero_distance(self):
        """Should return zero distance for a single match"""
        match = {
            "id": "match-1",
            "kickoff": "2024-11-01T20:00:00Z",
            "city": { "id": "city-1", "name": "City 1", "latitude": 40.7128, "longitude": -74.0060 }
        }
        result = self.strategy.optimise([match])
        assert len(result['stops']) == 1
        assert result['totalDistance'] == 0