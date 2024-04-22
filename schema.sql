"creates the table for the user"
CREATE TABLE user(
Userid INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
major TEXT NOT NULL
);

"Based off the csv file"
"A table for the location for the class"
CREATE TABLE CLASSLOCATION
(
  BuildingName TEXT NOT NULL,
  CampusLocation TEXT NOT NULL,
  FOREIGN KEY (SectionName) REFERENCES CLASSLOCATION(SectionName)
);

"A table for any details regarding the class"
CREATE TABLE COURSEDETAILS(
  RoomNumber TEXT NOT NULL,
  MeetingDays TEXT NOT NULL,
  StartTime INT,
  EndTime INT,
  SectionName TEXT PRIMARY KEY NOT NULL,
  ShortTitle TEXT,
  MinCredits INT NOT NULL,
  MaxCredits INT NOT NULL,
  Prerequisites TEXT NOT NULL,
  SeatCapacity INT NOT NULL,
  SeatsAvailable INT NOT NULL,
  FacultyName TEXT NOT NULL,
  Coreq TEXT NOT NULL,
  AvailStatus TEXT NOT NULL
);