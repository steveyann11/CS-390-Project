"creates the table for the user"
CREATE TABLE user(
Userid INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
major TEXT NOT NULL,
);

"Based off the csv file"
"A table for the location for the class"
CREATE TABLE CLASSLOCATION
(
  BuildingName INT NOT NULL,
  CampusLocation INT NOT NULL
);

"A table for any details regarding the class"
CREATE TABLE COURSEDETAILS(
  RoomNumber INT NOT NULL,
  MeetingDays INT NOT NULL,
  StartTime INT NOT NULL,
  SectionName INT PRIMARY KEY NOT NULL,
  ShortTitle INT,
  MinCredits INT NOT NULL,
  MaxCredits INT NOT NULL,
  Prerequisites INT NOT NULL,
  SeatCapatcity INT NOT NULL,
  SeatsAvailable INT NOT NULL,
  FacultyName INT NOT NULL,
  Coreq INT NOT NULL,
  AvailStatus INT NOT NULL,
);