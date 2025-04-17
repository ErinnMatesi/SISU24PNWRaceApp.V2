from flask import Blueprint, request, jsonify
from models import db, Racer, Trail, RaceEntry, Team, BonusObjective
from datetime import datetime

routes = Blueprint("routes", __name__)

# ------------------------------------
# RACERS ROUTES
# ------------------------------------

@routes.route("/racers", methods=["GET"])
def get_all_racers():
    racers = Racer.query.all()
    return jsonify([{
        "id": r.id,
        "bib_number": r.bib_number,
        "first_name": r.first_name,
        "last_name": r.last_name,
        "total_miles": r.total_miles,
        "total_elevation_gain": r.total_elevation_gain,
        "total_points": r.total_points
    } for r in racers])

@routes.route("/racers/<int:id>", methods=["GET"])
def get_racer(id):
    racer = Racer.query.get_or_404(id)
    return jsonify({
        "id": racer.id,
        "bib_number": racer.bib_number,
        "first_name": racer.first_name,
        "last_name": racer.last_name,
        "total_miles": racer.total_miles,
        "total_elevation_gain": racer.total_elevation_gain,
        "total_points": racer.total_points
    })

@routes.route("/racers", methods=["POST"])
def add_racer():
    data = request.json

    # Duplicate BibNumber check
    existing = Racer.query.filter_by(bib_number=data["bib_number"]).first()
    if existing:
        return jsonify({"error": "Bib number already exists"}), 400

    new_racer = Racer(**data)
    db.session.add(new_racer)
    db.session.commit()
    return jsonify({"message": "Racer added successfully!"}), 201


@routes.route("/racers/<int:id>", methods=["PUT"])
def update_racer(id):
    racer = Racer.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(racer, key, value)
    db.session.commit()
    return jsonify({"message": "Racer updated successfully!"})

@routes.route("/racers/<int:id>", methods=["DELETE"])
def delete_racer(id):
    racer = Racer.query.get_or_404(id)
    db.session.delete(racer)
    db.session.commit()
    return jsonify({"message": "Racer deleted successfully!"})

# ------------------------------------
# TRAILS ROUTES
# ------------------------------------

@routes.route("/trails", methods=["GET"])
def get_all_trails():
    trails = Trail.query.all()
    return jsonify([{
        "id": t.id,
        "name": t.name,
        "distance": t.distance,
        "elevation_gain": t.elevation_gain,
        "base_points": t.base_points,
        "time_limit_minutes": t.time_limit_minutes
    } for t in trails])

@routes.route("/trails/<int:id>", methods=["GET"])
def get_trail(id):
    trail = Trail.query.get_or_404(id)
    return jsonify({
        "id": trail.id,
        "name": trail.name,
        "distance": trail.distance,
        "elevation_gain": trail.elevation_gain,
        "base_points": trail.base_points,
        "time_limit_minutes": trail.time_limit_minutes
    })

@routes.route("/trails", methods=["POST"])
def add_trail():
    data = request.json
    new_trail = Trail(**data)
    db.session.add(new_trail)
    db.session.commit()
    return jsonify({"message": "Trail added successfully!"}), 201

@routes.route("/trails/<int:id>", methods=["PUT"])
def update_trail(id):
    trail = Trail.query.get_or_404(id)
    data = request.json
    for key, value in data.items():
        setattr(trail, key, value)
    db.session.commit()
    return jsonify({"message": "Trail updated successfully!"})

@routes.route("/trails/<int:id>", methods=["DELETE"])
def delete_trail(id):
    trail = Trail.query.get_or_404(id)
    db.session.delete(trail)
    db.session.commit()
    return jsonify({"message": "Trail deleted successfully!"})

# ------------------------------------
# RACE ENTRIES ROUTES
# ------------------------------------

@routes.route("/race-entries", methods=["GET"])
def get_all_race_entries():
    race_entries = RaceEntry.query.all()
    return jsonify([{
        "id": re.id,
        "racer_id": re.racer_id,
        "trail_id": re.trail_id,
        "start_time": re.start_time,
        "end_time": re.end_time,
        "points_earned": re.points_earned,
        "bonus_points_earned": re.bonus_points_earned,
        "bonus_objective_id": re.bonus_objective_id
    } for re in race_entries])

@routes.route("/race-entries/<int:id>", methods=["GET"])
def get_race_entry(id):
    entry = RaceEntry.query.get_or_404(id)
    return jsonify({
        "id": entry.id,
        "racer_id": entry.racer_id,
        "trail_id": entry.trail_id,
        "start_time": entry.start_time,
        "end_time": entry.end_time,
        "points_earned": entry.points_earned,
        "bonus_points_earned": entry.bonus_points_earned,
        "bonus_objective_id": entry.bonus_objective_id
    })

# ------------------------------------
# TEAMS ROUTES
# ------------------------------------

@routes.route("/teams", methods=["GET"])
def get_all_teams():
    teams = Team.query.all()
    return jsonify([{
        "id": t.id,
        "team_name": t.team_name,
        "total_points": t.total_points
    } for t in teams])

@routes.route("/teams/<int:id>", methods=["GET"])
def get_team(id):
    team = Team.query.get_or_404(id)
    return jsonify({
        "id": team.id,
        "team_name": team.team_name,
        "total_points": team.total_points
    })

@routes.route("/teams", methods=["POST"])
def add_team():
    data = request.json

    # Check for existing team name
    existing = Team.query.filter_by(team_name=data["team_name"]).first()
    if existing:
        return jsonify({"error": "Team name already exists"}), 400
    
    new_team = Team(**data)
    db.session.add(new_team)
    db.session.commit()
    return jsonify({"message": "Team added successfully!"}), 201

# ------------------------------------
# BONUS OBJECTIVES ROUTES
# ------------------------------------

@routes.route("/bonus-objectives", methods=["GET"])
def get_all_bonus_objectives():
    bonus_objectives = BonusObjective.query.all()
    return jsonify([{
        "id": bo.id,
        "description": bo.description,
        "associated_trail_id": bo.associated_trail_id,
        "bonus_points": bo.bonus_points
    } for bo in bonus_objectives])

@routes.route("/bonus-objectives/<int:id>", methods=["GET"])
def get_bonus_objective(id):
    bonus_objective = BonusObjective.query.get_or_404(id)
    return jsonify({
        "id": bonus_objective.id,
        "description": bonus_objective.description,
        "associated_trail_id": bonus_objective.associated_trail_id,
        "bonus_points": bonus_objective.bonus_points
    })

@routes.route("/bonus-objectives", methods=["POST"])
def add_bonus_objective():
    data = request.json
    new_bonus_objective = BonusObjective(**data)
    db.session.add(new_bonus_objective)
    db.session.commit()
    return jsonify({"message": "Bonus Objective added successfully!"}), 201
