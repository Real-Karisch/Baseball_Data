import statsapi
import psycopg2
import psycopg2.extras
import re

from api2psqlSupporting import *

import time

def populateDivisionTable(dbConnection):
    divisions = statsapi.get('divisions', {})['divisions']

    args = []

    for division in divisions[:6]:
        args.append(
            (
                division['id'],
                division['name'],
                division['nameShort'],
                division['abbreviation'],
                division['league']['id'],
                division['hasWildcard']
            )
        )

    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")

        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO major.divisions(
                id, 
                name,
                "nameShort",
                abbrev,
                "leagueId",
                "hasWildcard"
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
            args
        )
        cur.execute("SET session_replication_role='origin';")

def populateLeagueTable(dbConnection):
    leagues = statsapi.get('league', {'sportId': 1})['leagues']

    args = []

    for league in leagues[:2]:
        args.append(
            (
                league['id'],
                league['season'],
                league['name'],
                league['abbreviation'],
                league['nameShort']
            )
        )

    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")

        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO major.leagues(
                id, 
                season,
                name,
                abbrev,
                "nameShort"
                )
                VALUES (%s, %s, %s, %s, %s)
            """,
            args
        )
        cur.execute("SET session_replication_role='origin';")

def populatePlayerTable(dbConnection, startDate, endDate):
    startYear = int(re.search('\d\d.\d\d.(\d\d\d\d)', startDate).group(1))
    endYear = int(re.search('\d\d.\d\d.(\d\d\d\d)', endDate).group(1))

    sports = statsapi.get('sports', {})['sports']

    seasons = list(range(startYear, endYear + 1))

    args = []
    playerIds = []

    for sport in sports:
        for season in seasons:
            players = statsapi.get('sports_players', {'sportId': sport['id'], 'season': season})['people']
            for player in players:
                if player['id'] not in playerIds:
                    playerIds.append(player['id'])
                    args.append(
                        (
                            dictTry(player, ['id']),
                            dictTry(player, ['fullName']),
                            dictTry(player, ['firstName']),
                            dictTry(player, ['lastName']),
                            dictTry(player, ['primaryNumber']),
                            dictTry(player, ['birthDate']),
                            dictTry(player, ['birthCity']),
                            dictTry(player, ['birthCountry']),
                            dictTry(player, ['height']),
                            dictTry(player, ['weight']),
                            dictTry(player, ['primaryPosition','code']),
                            dictTry(player, ['primaryPosition','name']),
                            dictTry(player, ['primaryPosition','type']),
                            dictTry(player, ['primaryPosition','abbreviation']),
                            dictTry(player, ['useName']),
                            dictTry(player, ['middleName']),
                            dictTry(player, ['boxscoreName']),
                            dictTry(player, ['isPlayer']),
                            dictTry(player, ['mlbDebutDate']),
                            dictTry(player, ['batSide','code']),
                            dictTry(player, ['batSide','description']),
                            dictTry(player, ['pitchHand','code']),
                            dictTry(player, ['pitchHand','description']),
                            dictTry(player, ['strikeZoneTop']),
                            dictTry(player, ['strikeZoneBottom'])
                        )
                    )
    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")
        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO major.players(
                id,
                "fullName",
                "firstName",
                "lastName",
                "primaryNumber",
                "birthDate",
                "birthCity",
                "birthCountry",
                height,
                weight,
                "positionCode",
                "positionName",
                "positionType",
                "positionAbbrev",
                "useName",
                "middleName",
                "boxscoreName",
                "isPlayer",
                "mlbDebutDate",
                "batSideCode",
                "batSideDesc",
                "pitchHandCode",
                "pitchHandDesc",
                "szTop",
                "szBottom"

                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            args
        )
        cur.execute("SET session_replication_role='origin';")

def populateSeasonTable(dbConnection, startDate, endDate):
    startYear = int(re.search('\d\d.\d\d.(\d\d\d\d)', startDate).group(1))
    endYear = int(re.search('\d\d.\d\d.(\d\d\d\d)', endDate).group(1))

    args = []

    for year in range(startYear, endYear + 1):
        seasons = statsapi.get('season', {'seasonId': year, 'sportId': 1})['seasons']

        for season in seasons:
            args.append(
                (
                    season['seasonId'],
                    season['regularSeasonStartDate'],
                    season['regularSeasonEndDate'],
                    dictTry(season, ['preSeasonStartDate']),
                    dictTry(season, ['preSeasonEndDate']),
                    season['postSeasonStartDate'],
                    season['postSeasonEndDate'],
                    dictTry(season, ['lastDate1stHalf']),
                    dictTry(season, ['firstDate2ndHalf']),
                    season['allStarDate']
                )
            )

    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")

        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO major.seasons(
                "seasonId", 
                "regSeasStartDate",
                "regSeasEndDate",
                "preSeasStartDate",
                "preSeasEndDate",
                "postSeasStartDate",
                "postSeasEndDate",
                "lastDate1stHalf",
                "firstDate2ndHalf",
                "allStarDate"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            args
        )
        cur.execute("SET session_replication_role='origin';")

def populateTeamTable(dbConnection):
    teams = statsapi.get('teams', {})['teams']

    teams = [x for x in teams if 'division' in x.keys() and 'league' in x.keys()]
    teams = [x for x in teams if 'id' in x['league'].keys()]

    args = []
    for team in teams:
        args.append(
            (
                team['id'],
                team['name'],
                team['season'],
                team['venue']['id'],
                team['teamCode'],
                team['fileCode'],
                team['abbreviation'],
                team['teamName'],
                team['locationName'],
                team['firstYearOfPlay'],
                team['league']['id'],
                team['division']['id'],
                team['shortName']
            )
        )
    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")
        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO major.teams(
                id, 
                name,
                season,
                "venueID",
                "teamCode",
                "fileCode",
                abbrev,
                "teamName",
                "locationName",
                "firstYearOfPlay",
                "leagueID",
                "divisionID",
                "shortName"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            args
        )
        cur.execute("SET session_replication_role='origin';")

def populateVenueTable(dbConnection, venueArgs):
    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")
        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO major.venues(
                id, 
                name,
                city,
                state,
                latitude,
                longitude,
                "tzOffset",
                "tzName",
                capacity,
                "turfType",
                "roofType",
                "leftLine",
                "leftCenter",
                center,
                "rightCenter",
                "rightLine"
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            venueArgs
        )
        cur.execute("SET session_replication_role='origin';")

def populateGamesTablesMaster(dbConnection, schema, startDate, endDate, pathListListDict, commandDict):
    for key, value in commandDict.items():
        commandDict[key] = value.format(schema = schema)

    gamePks = generateGamePksFromDates(startDate=startDate, endDate=endDate)

    argsDict = {
        'games': [],
        'atBats': [],
        'actions': [],
        'pitches': [],
        'runners': []
    }

    for gamePk in gamePks:
        game = statsapi.get('game', {'gamePk': gamePk})

        argsDict['games'].append(generateGameArgs(game, pathListListDict['games']))
        argsDict['atBats'] += generateAtBatArgs(game, pathListListDict['atBats'])
        argsDict['actions'] += generateActionArgs(game, pathListListDict['actions'])
        argsDict['pitches'] += generatePitchArgs(game, pathListListDict['pitches'])
        argsDict['runners'] += generateRunnerArgs(game, pathListListDict['runners'])

    with dbConnection.cursor() as cur:
        cur.execute("SET session_replication_role='replica';")
        for key in argsDict.keys():
            psycopg2.extras.execute_batch(
                cur,
                commandDict[key],
                argsDict[key]
            )

        cur.execute("SET session_replication_role='origin';")

def populateMajorTablesMaster(dbConnection):
    startDate = '01/01/2019'
    endDate = '12/31/2019'
    schema = 'major'

    populateDivisionTable(dbConnection)
    populateLeagueTable(dbConnection)
    populatePlayerTable(dbConnection, startDate, endDate)
    populateSeasonTable(dbConnection, startDate, endDate)
    populateTeamTable(dbConnection)
    populateVenueTable(dbConnection, venueArgs)
    populateGamesTablesMaster(dbConnection, schema, startDate, endDate, pathListListDict, commandDict)

    dbConnection.commit()
    dbConnection.close()