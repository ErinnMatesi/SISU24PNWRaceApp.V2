-- Create the new database
DROP DATABASE IF EXISTS raceeventapp_v2;
CREATE DATABASE raceeventapp_v2;
USE raceeventapp_v2;

-- Create the teams table
CREATE TABLE teams (
    TeamID INT AUTO_INCREMENT PRIMARY KEY,
    TeamName VARCHAR(255) NOT NULL,
    TotalPoints INT DEFAULT 0
);

-- Create the racers table
CREATE TABLE racers (
    RacerID INT AUTO_INCREMENT PRIMARY KEY,
    Gender ENUM('Male','Female','Nonbinary') NOT NULL,
    Age INT DEFAULT NULL,
    BibNumber INT NOT NULL,
    Division ENUM('100 milers','24hr individual','24hr team') NOT NULL,
    TeamID INT DEFAULT NULL,
    FirstName VARCHAR(255) DEFAULT NULL,
    LastName VARCHAR(255) DEFAULT NULL,
    TotalMiles DECIMAL(5,2) DEFAULT 0.00,
    TotalElevationGain INT DEFAULT 0,
    TotalPoints INT DEFAULT 0,
    FOREIGN KEY (TeamID) REFERENCES teams(TeamID) ON DELETE SET NULL
);

-- Create the trails table
CREATE TABLE trails (
    TrailID INT AUTO_INCREMENT PRIMARY KEY,
    TrailName VARCHAR(255) NOT NULL,
    Distance DECIMAL(5,2) NOT NULL,
    ElevationGain INT NOT NULL,
    BasePoints INT NOT NULL,
    FirstTenPoints INT DEFAULT NULL,
    SecondTenPoints INT DEFAULT NULL,
    ping_pong_balls_remaining INT DEFAULT 10,
    crystals_remaining INT DEFAULT 10,
    time_limit_minutes INT NOT NULL  -- store max expected time per trail, for safety flag
);

-- Create the bonus objectives table
CREATE TABLE bonusobjectives (
    ObjectiveID INT AUTO_INCREMENT PRIMARY KEY,
    Description TEXT,
    AssociatedTrailID INT DEFAULT NULL,
    BonusPoints INT DEFAULT NULL,
    FOREIGN KEY (AssociatedTrailID) REFERENCES trails(TrailID)
);

-- Create the race entries table (logs check-ins and check-outs)
CREATE TABLE raceentries (
    EntryID INT AUTO_INCREMENT PRIMARY KEY,
    RacerID INT NOT NULL,
    TrailID INT DEFAULT NULL,
    StartTime DATETIME DEFAULT NULL,
    EndTime DATETIME DEFAULT NULL,
    PointsEarned INT DEFAULT NULL,
    BonusPointsEarned INT DEFAULT NULL,
    BonusObjectiveID INT DEFAULT NULL,
    BonusObjectiveDescription VARCHAR(255) DEFAULT NULL,
    distress_flag BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (RacerID) REFERENCES racers(RacerID),
    FOREIGN KEY (TrailID) REFERENCES trails(TrailID),
    FOREIGN KEY (BonusObjectiveID) REFERENCES bonusobjectives(ObjectiveID)
);

-- Create the racer-trail mapping table
CREATE TABLE racertrailmap (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    RacerID INT NOT NULL UNIQUE,  -- Ensures a racer can only have ONE active trail at a time
    TrailID INT NOT NULL,
    StartTime DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Tracks when they checked out (started)
    FOREIGN KEY (RacerID) REFERENCES racers(RacerID),
    FOREIGN KEY (TrailID) REFERENCES trails(TrailID)
);

