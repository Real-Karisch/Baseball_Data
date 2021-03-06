This project pulls data from the MLB stats API to build a local PostgreSQL database with team-level, game-level, at bat-level and pitch-level data.

The project makes use of the MLB-StatsAPI python library (https://pypi.org/project/MLB-StatsAPI/) to handle API requests, and the psycopg2 library (https://pypi.org/project/psycopg2/) for database management.

There are four main folders:

  1. info: basically a misc folder with API guides, notes, etc.
  
  2. JSON: a folder to hold any JSON files returned by the API that I want to save locally

  3. psql: a folder for sql files; contains code to create the database, delete the database, and delete the data

  4. python: a folder with any python files used in the project. The main two are api2psqlPopulateFns.py and api2psqlSupporting.py, which contain functions and items used to populate and update the database

The schema are:
  major, containing tables with MLB data
  <br>
  minor, containing tables with Minor League data

The output tables in the major schema are:
<ul>
  <li>
  actions, containing data on non-pitch events during games
  </li>
  <li>
  atbats, containing data on each at bat
  </li>
  <li>
  divisions, containing data on every Major League division
  </li>
  <li>
  games, containing data on every game
  </li>
  <li>
  leagues, containing data on the two MLB leagues
  </li>
  <li>
  pitches, containing data on every pitch
  </li>
  <li>
  players, containing data on all MLB players
  </li>
  <li>
  runners, containing data on runner movement during each at bat
  </li>
  <li>
  teams, containing data on every team
  </li>
  <li>
  venues, containing data on every venue used for MLB games
  </li>
  <li>
  seasons, containing data on key dates in the schedule
  </li>
</ul>
The output tables in the minor schema are:
<ul>
  <li>
  actions, containing data on non-pitch events during games
  </li>
  <li>
  atbats, containing data on each at bat
  </li>
  <li>
  games, containing data on every game
  </li>
  <li>
  pitches, containing data on every pitch
  </li>
  <li>
  runners, containing data on runner movement during each at bat
  </li>
  <li>
  venues, containing data on every venue used for MLB games
  </li>
  <li>
  seasons, containing data on key dates in the schedule
  </li>
  <li>
  sports, containing data on different minor leagues
  </li>
</ul>


