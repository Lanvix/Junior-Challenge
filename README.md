World Cup 2026 Travel Route Planner — Python/Flask Solution
My solution to the Unosquare Graduate / Junior Software Engineer coding challenge. The brief was to build a system that helps FIFA World Cup 2026 fans plan optimal travel routes between host cities based on the match schedule (48 teams, 16 cities, 3 countries).

The challenge offered four backend options — Node/Express, Java/Spring, Python/Flask and .NET. I built mine in Python with Flask.
The original challenge brief lives in CHALLENGE.md. This README covers what I implemented and how to run it.
Tech stack
Language: Python 3.10+
Framework: Flask
Persistence: SQLAlchemy + SQLite (seeded from the provided dataset)
Testing: pytest

What I implemented
The working code is in backend/python-flask.
Cities API — GET /api/cities returns all 16 host cities
Matches API — GET /api/matches with optional ?city= and ?date= filters
Single match — GET /api/matches/<id> returns one match by id
Route optimisation — POST /api/route/optimise runs the nearest-neighbour strategy
Trip cost — POST /api/route/budget calculates flights, accommodation and ticket costs

Design notes
Route optimisation — Strategy Pattern. The route optimiser is built behind a common strategy interface, so the optimisation algorithm can be swapped without changing the calling code. My NearestNeighbourStrategy groups the requested matches by date and then, from the current city, repeatedly moves to the nearest unvisited host city using the provided haversine distance helper.
Why nearest-neighbour. It's a greedy heuristic: fast, simple to reason about, and a good fit for the size of this problem. The trade-off is that it doesn't guarantee a globally optimal route — it can be led astray by a cheap early hop that forces an expensive later one. For 16 cities that's an acceptable trade-off, and keeping it behind the Strategy interface means a more sophisticated algorithm could be dropped in later without touching the API layer.
Testing. The unit tests in tests/ exercise the optimiser directly, checking it returns a sensible ordering for known inputs rather than just confirming it runs.

Running it locally
cd backend/python-flask
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.seed
flask run --port 3008

The server starts on http://localhost:3008. On Windows, activate the venv with venv\Scripts\activate.

Running the tests
cd backend/python-flask
source venv/bin/activate
pytest

A note on AI assistance
The challenge encouraged using AI tools as a productivity aid. I used them to speed up learning and check my understanding while building this, rather than to generate code I couldn't account for — I'm happy to walk through any part of the implementation and the trade-offs behind it.