from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

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
    color = db.Column("color", db.String(20), nullable=True)

# Racer-Trail Mapping Model (Active Racers)
class RacerTrailMap(db.Model):
    __tablename__ = "racertrailmap"
    
    id = db.Column("ID", db.Integer, primary_key=True, autoincrement=True)
    racer_id = db.Column("RacerID", db.Integer, db.ForeignKey("racers.RacerID"), unique=True, nullable=False)
    trail_id = db.Column("TrailID", db.Integer, db.ForeignKey("trails.TrailID"), nullable=False)
    start_time = db.Column(
        "StartTime", db.DateTime, default=lambda: datetime.now(timezone.utc)
    )

# Race Entries Model (Tracks Check-ins/Check-outs)
class RaceEntry(db.Model):
    __tablename__ = "raceentries"
    
    id = db.Column("EntryID", db.Integer, primary_key=True, autoincrement=True)
    racer_id = db.Column("RacerID", db.Integer, db.ForeignKey("racers.RacerID"), nullable=False)
    trail_id = db.Column("TrailID", db.Integer, db.ForeignKey("trails.TrailID"), nullable=True)
    start_time = db.Column(
        "StartTime", db.DateTime, default=lambda: datetime.now(timezone.utc)
    )
    end_time = db.Column("EndTime", db.DateTime, nullable=True)
    points_earned = db.Column("PointsEarned", db.Integer, default=0)
    bonus_objective_id = db.Column("BonusObjectiveID", db.Integer, db.ForeignKey("bonusobjectives.ObjectiveID"), nullable=True)
    bonus_objective_description = db.Column("BonusObjectiveDescription", db.Text, nullable=True)
    distress_flag = db.Column("distress_flag", db.Boolean, default=False)

# Teams Model
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column("TeamID", db.Integer, primary_key=True)
    team_name = db.Column("TeamName", db.String(255), nullable=False, unique=True)
    total_points = db.Column("TotalPoints", db.Integer, default=0)


# Bonus Objectives Model
class BonusObjective(db.Model):
    __tablename__ = "bonusobjectives"
    
    id = db.Column("ObjectiveID", db.Integer, primary_key=True, autoincrement=True)
    description = db.Column("Description", db.Text, nullable=False)
    associated_trail_id = db.Column("AssociatedTrailID", db.Integer, db.ForeignKey("trails.TrailID"), nullable=True)
    bonus_points = db.Column("BonusPoints", db.Integer, default=0)

