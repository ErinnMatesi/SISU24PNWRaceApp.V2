from flask import Blueprint, request, jsonify
from models import db, Racer, Trail, RaceEntry, Team, BonusObjective, RacerTrailMap
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

    # Convert empty team_id to None
    if "team_id" in data and data["team_id"] == "":
        data["team_id"] = None

    required_fields = ["bib_number", "first_name", "last_name", "gender", "division"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"'{field}' is required"}), 400

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

# GET RACER BY BIBNUMBER
@routes.route("/racers/bib/<int:bib_number>", methods=["GET"])
def get_racer_by_bib(bib_number):
    racer = Racer.query.filter_by(bib_number=bib_number).first()
    if racer is None:
        return jsonify({"error": "Racer not found"}), 404

    return jsonify({
        "racer_id": racer.id,
        "first_name": racer.first_name,
        "last_name": racer.last_name,
        "bib_number": racer.bib_number
    }), 200


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

@routes.route("/raceentry/checkout", methods=["POST"])
def check_out():
    try:
        data = request.json
        racer_id = data.get("racer_id")
        trail_id = data.get("trail_id")

        # Validate inputs
        if not racer_id or not trail_id:
            return jsonify({"error": "Racer ID and Trail ID are required."}), 400

        # Ensure the racer is not already on a trail
        active_map = RacerTrailMap.query.filter_by(racer_id=racer_id).first()
        if active_map:
            return jsonify({"error": "Racer is already out on a trail."}), 400

        # Fetch trail details for confirmation message
        trail = Trail.query.get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found."}), 404

        # Create a new race entry
        new_entry = RaceEntry(
            racer_id=racer_id,
            trail_id=trail_id,
            start_time=datetime.utcnow()
        )
        db.session.add(new_entry)

        # Add to racer trail map
        new_map_entry = RacerTrailMap(
            racer_id=racer_id,
            trail_id=trail_id,
            start_time=datetime.utcnow()
        )
        db.session.add(new_map_entry)

        # Commit changes
        db.session.commit()

        # Include trail name in response
        return jsonify({
            "message": f"Racer checked out successfully on {trail.name}.",
            "trail_name": trail.name
        }), 201

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to check out racer."}), 500

    
@routes.route("/raceentry/checkin/<int:racer_id>", methods=["PUT"])
def check_in(racer_id):
    try:
        # Check for active trail map entry
        active_trail_entry = RacerTrailMap.query.filter_by(racer_id=racer_id).first()
        
        if not active_trail_entry:
            return jsonify({"error": "No active trail found for this racer."}), 404
        
        # Get the associated trail directly from the active trail map
        trail = Trail.query.get(active_trail_entry.trail_id)
        if not trail:
            return jsonify({"error": "Associated trail not found."}), 404
        
        # Extract trail attributes
        base_points = trail.base_points
        distance = trail.distance
        elevation_gain = trail.elevation_gain
        first_ten_points = trail.first_ten_points or 0
        second_ten_points = trail.second_ten_points or 0

        
        # Extract bonus type from the request
        bonus_type = request.json.get("bonus_type", None)  # "first_ten" or "second_ten"
        bonus_points = 0

        # Apply the correct bonus based on the selected type
        if bonus_type == "first_ten":
            bonus_points = first_ten_points
            if trail.first_ten_points and trail.first_ten_points > 0:
                trail.first_ten_points -= 1

        elif bonus_type == "second_ten":
            bonus_points = second_ten_points
            if trail.second_ten_points and trail.second_ten_points > 0:
                trail.second_ten_points -= 1


        # Total points earned for this trail
        points_earned = base_points + bonus_points

        # Update the active race entry
        race_entry = RaceEntry.query.filter_by(racer_id=racer_id, trail_id=trail.id, end_time=None).first()
        if not race_entry:
            return jsonify({"error": "No active race entry found for this racer."}), 404
        
        race_entry.end_time = datetime.utcnow()
        race_entry.points_earned = points_earned
        
        # Update the racer's cumulative stats
        racer = Racer.query.get(racer_id)
        if not racer:
            return jsonify({"error": "Racer not found."}), 404
        
        racer.total_points += points_earned
        racer.total_miles += distance
        racer.total_elevation_gain += elevation_gain

        # Clean up active trail entry
        db.session.delete(active_trail_entry)

        # Commit all changes
        db.session.commit()

        return jsonify({
            "message": f"Racer checked in successfully from {trail.name}.",
            "points_earned": points_earned,
            "total_miles": racer.total_miles,
            "total_elevation_gain": racer.total_elevation_gain,
            "total_points": racer.total_points
        }), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to check in racer."}), 500


@routes.route("/raceentry/bonuspoints", methods=["POST"])
def add_bonus_points():
    try:
        data = request.json
        racer_id = data.get("racer_id")
        bonus_objective_id = data.get("bonus_objective_id")

        # Validate inputs
        if not racer_id or not bonus_objective_id:
            return jsonify({"error": "Racer ID and Bonus Objective ID are required."}), 400

        # Check if this bonus objective has already been assigned to this racer
        existing_entry = RaceEntry.query.filter_by(
            racer_id=racer_id, 
            bonus_objective_id=bonus_objective_id
        ).first()
        if existing_entry:
            return jsonify({"error": "This racer has already completed this bonus objective."}), 400

        # Fetch the bonus objective to get points
        bonus_objective = BonusObjective.query.filter_by(id=bonus_objective_id).first()
        if not bonus_objective:
            return jsonify({"error": "Bonus Objective not found."}), 404
        
        # Fetch trail if associated
        trail = None
        if bonus_objective.associated_trail_id:
            trail = Trail.query.get(bonus_objective.associated_trail_id)

        # Create a race entry for the bonus points
        new_entry = RaceEntry(
            racer_id=racer_id,
            trail_id=trail.id if trail else None,
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),  # Bonus points are instant
            points_earned=bonus_objective.bonus_points,
            bonus_objective_id=bonus_objective.id,
            bonus_objective_description=bonus_objective.description
        )
        db.session.add(new_entry)

        # Update racer totals
        racer = Racer.query.filter_by(id=racer_id).first()
        if racer:
            racer.total_points += bonus_objective.bonus_points

        # Commit changes
        db.session.commit()

        return jsonify({"message": "Bonus points assigned successfully."}), 201

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"error": "Failed to assign bonus points."}), 500



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

# ------------------------------------
# RACERTRAILMAP ROUTES
# ------------------------------------

@routes.route("/active-trail/<int:racer_id>", methods=["GET"])
def get_active_trail(racer_id):
    entry = RacerTrailMap.query.filter_by(racer_id=racer_id).first()
    if not entry:
        return jsonify({"message": "Racer is not currently on any trail"}), 404

    trail = Trail.query.get(entry.trail_id)
    if not trail:
        return jsonify({"error": "Trail not found"}), 404

    return jsonify({
        "id": entry.id,
        "racer_id": entry.racer_id,
        "trail_id": entry.trail_id,
        "trail_name": trail.name,  # ✅ Add this
        "start_time": entry.start_time
    })

@routes.route("/racertrailmap", methods=["POST"])
def add_racer_trail_map():
    data = request.json
    
    existing_entry = RacerTrailMap.query.filter_by(racer_id=data["racer_id"]).first()
    if existing_entry:
        return jsonify({"error": "Racer is already on a trail"}), 400
    
    new_entry = RacerTrailMap(**data)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Racer checked out successfully!"}), 201

@routes.route("/racertrailmap/<int:racer_id>", methods=["DELETE"])
def remove_racer_trail_map(racer_id):
    entry = RacerTrailMap.query.filter_by(racer_id=racer_id).first()
    if not entry:
        return jsonify({"error": "Racer is not currently on a trail"}), 404
    
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Racer checked in successfully!"}), 200

# ------------------------------------
# ACTIVE RUNNERS/LEADERBOARD Routes
# ------------------------------------

@routes.route("/active-runners", methods=["GET"])
def get_active_runners():
    try:
        # Query for all active runners from the racertrailmap table
        active_runners = db.session.execute(
            """
            SELECT r.RacerID, r.FirstName, r.LastName, m.StartTime
            FROM racers r
            JOIN racertrailmap m ON r.RacerID = m.RacerID
            ORDER BY m.StartTime ASC
            """
        ).fetchall()

        # Format the response
        runners_list = [
            {
                "racer_id": runner.RacerID,
                "first_name": runner.FirstName,
                "last_name": runner.LastName,
                "start_time": runner.StartTime.strftime("%Y-%m-%d %H:%M:%S")
            }
            for runner in active_runners
        ]

        return jsonify(runners_list), 200

    except Exception as e:
        print(f"Error fetching active runners: {e}")
        return jsonify({"error": "Failed to fetch active runners"}), 500

@routes.route("/leaderboard/category/<category>", methods=["GET"])
def get_leaderboard_by_category(category):
    try:
        query = Racer.query

        if category == "male_24hr":
            query = query.filter_by(gender="Male", division="24HR")
            query = query.order_by(Racer.total_points.desc())
        elif category == "female_24hr":
            query = query.filter_by(gender="Female", division="24HR")
            query = query.order_by(Racer.total_points.desc())
        elif category == "teams_24hr":
            query = query.filter(Racer.division == "24HR", Racer.team_id.isnot(None))
            query = query.order_by(Racer.total_points.desc())
        elif category == "100miler":
            query = query.filter_by(division="100Miler")
            # Not sorting unless needed
        else:
            return jsonify({"error": "Invalid category"}), 400

        racers = query.all()

        return jsonify([
            {
                "id": r.id,
                "first_name": r.first_name,
                "last_name": r.last_name,
                "total_points": r.total_points,
                "total_miles": r.total_miles,
                "team_id": r.team_id
            }
            for r in racers
        ]), 200

    except Exception as e:
        print(f"Error in leaderboard query: {e}")
        return jsonify({"error": "Failed to fetch leaderboard data"}), 500

@routes.route("/leaderboard/trails", methods=["GET"])
def get_trail_leaderboard_data():
    try:
        # Get all trails
        trails = Trail.query.all()
        results = []

        for trail in trails:
            # Get all racers currently on this trail (from RacerTrailMap)
            active_entries = (
                db.session.query(RacerTrailMap, Racer)
                .join(Racer, RacerTrailMap.racer_id == Racer.id)
                .filter(RacerTrailMap.trail_id == trail.id)
                .order_by(RacerTrailMap.start_time.asc())
                .all()
            )

            # Format active racers
            active_runners = [
                {
                    "racer_id": racer.id,
                    "first_name": racer.first_name,
                    "last_name": racer.last_name,
                    "start_time": entry.start_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                for entry, racer in active_entries
            ]

            results.append({
                "trail_id": trail.id,
                "first_ten_points": trail.first_ten_points,
                "second_ten_points": trail.second_ten_points,
                "active_runners": active_runners
            })

        return jsonify(results), 200

    except Exception as e:
        print("Error fetching trail leaderboard data:", e)
        return jsonify({"error": "Failed to load trail leaderboard data"}), 500
