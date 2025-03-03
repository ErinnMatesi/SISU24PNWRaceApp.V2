from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Trails Model with Time Limit
class Trail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    elevation_gain = db.Column(db.Integer, nullable=False)
    base_points = db.Column(db.Integer, nullable=False)
    first_ten_points = db.Column(db.Integer, nullable=True)
    second_ten_points = db.Column(db.Integer, nullable=True)
    ping_pong_balls_remaining = db.Column(db.Integer, default=10)
    crystals_remaining = db.Column(db.Integer, default=10)
    time_limit_minutes = db.Column(db.Integer, nullable=False)

# Racer-Trail Mapping Model
class RacerTrailMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    racer_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)

# Race Entries Model (Tracks all check-ins and check-outs)
class RaceEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    racer_id = db.Column(db.Integer, db.ForeignKey('racer.id'), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'), nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    points_earned = db.Column(db.Integer, default=0)
    bonus_points_earned = db.Column(db.Integer, default=0)
    bonus_objective_id = db.Column(db.Integer, db.ForeignKey('bonus_objective.id'), nullable=True)

# Teams Model
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(255), nullable=False, unique=True)
    total_points = db.Column(db.Integer, default=0)

# Bonus Objectives Model
class BonusObjective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    associated_trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'), nullable=True)
    bonus_points = db.Column(db.Integer, default=0)
