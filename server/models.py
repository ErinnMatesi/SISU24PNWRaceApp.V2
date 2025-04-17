from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# User Model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     is_admin = db.Column(db.Boolean, default=False)

# Racer Model
class Racer(db.Model):
    __tablename__ = "racers" 

    id = db.Column("RacerID", db.Integer, primary_key=True)
    bib_number = db.Column("BibNumber", db.Integer, unique=True, nullable=False)
    first_name = db.Column("FirstName", db.String(100), nullable=False)
    last_name = db.Column("LastName", db.String(100), nullable=False)
    gender = db.Column("Gender", db.Enum('Male', 'Female', 'Nonbinary'), nullable=False)
    age = db.Column("Age", db.Integer, nullable=True)
    division = db.Column("Division", db.Enum('100 milers', '24hr individual', '24hr team'), nullable=False)
    team_id = db.Column("TeamID", db.Integer, db.ForeignKey('teams.TeamID'), nullable=True)
    total_miles = db.Column("TotalMiles", db.Float, default=0.0)
    total_elevation_gain = db.Column("TotalElevationGain", db.Integer, default=0)
    total_points = db.Column("TotalPoints", db.Integer, default=0)

# Trails Model 
class Trail(db.Model):
    __tablename__ = "trails" 

    id = db.Column("TrailID", db.Integer, primary_key=True)
    name = db.Column("TrailName", db.String(255), nullable=False)
    distance = db.Column("Distance", db.Float, nullable=False)
    elevation_gain = db.Column("ElevationGain", db.Integer, nullable=False)
    base_points = db.Column("BasePoints", db.Integer, nullable=False)
    first_ten_points = db.Column("FirstTenPoints", db.Integer, nullable=True)
    second_ten_points = db.Column("SecondTenPoints", db.Integer, nullable=True)
    ping_pong_balls_remaining = db.Column("ping_pong_balls_remaining", db.Integer, default=10)
    crystals_remaining = db.Column("crystals_remaining", db.Integer, default=10)
    time_limit_minutes = db.Column("time_limit_minutes", db.Integer, nullable=False)

# Racer-Trail Mapping Model (Active Racers)
class RacerTrailMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    racer_id = db.Column(db.Integer, db.ForeignKey('racer.id'), unique=True, nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)

# Race Entries Model (Tracks Check-ins/Check-outs)
class RaceEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    racer_id = db.Column(db.Integer, db.ForeignKey('racer.id'), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey('trail.id'), nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    points_earned = db.Column(db.Integer, default=0)
    bonus_points_earned = db.Column(db.Integer, default=0)
    bonus_objective_id = db.Column(db.Integer, db.ForeignKey('bonus_objective.id'), nullable=True)
    distress_flag = db.Column(db.Boolean, default=False)

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
