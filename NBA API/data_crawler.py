import csv
from pandas.io.json import json_normalize
import requests


def get_data(Counter = 3000, Direction = "DESC", LeagueID = "00", PlayerOrTeam = "P",
              Season = "2015-16", SeasonType = "Regular Season", Sorter = "PTS"):
    """
    Crawls NBA Player Data with default parameters above.
    :param Counter: Not sure
    :param Direction: DESC or ASC
    :param LeagueID: 00
    :param PlayerOrTeam: P for player, T for team
    :param Season: Only one year span allowed
    :param SeasonType: Regular Season or Playoffs
    :param Sorter: Sorts by PTS, REB, etc
    :return: List of lists of player data
    """

    params = {
                'Counter': str(Counter),
                'Direction': Direction,
                'LeagueID': LeagueID,
                'PlayerOrTeam': PlayerOrTeam,
                'Season': Season,
                'SeasonType': SeasonType,
                'Sorter': Sorter
            }

    # user_agent prevents NBA from blocking our access to the data
    user_agent = {'User-Agent': 'Mozilla/5.0'}

    # access site with parameters in param & user_agent
    r = requests.get('http://stats.nba.com/stats/leaguegamelog?', params=params, headers = user_agent)

    # header for either player or team data
    header = json_normalize(r.json()['resultSets'])['headers'][0]

    # corresponding data for parameters
    data = json_normalize(r.json()['resultSets'])["rowSet"][0]

    # data = get_data[0], header = get_data[1]
    return data, header





if __name__ == "__main__":

    # regular season / playoffs
    season_types = ['Regular Season', 'Playoffs']

    # player data or team data
    PlayerOrTeam = ['P', 'T']

    # get seasons from 1950 to 2016
    seasons = []
    for year in xrange(1950, 2016):
        year_next = str(year+1)[-2:]
        season = str(year)+'-'+year_next
        seasons.append(season)


    # iterate over season types, seasons, then write to data
    for player_or_team in PlayerOrTeam:
        for season_type in season_types:
            for season in seasons:
                data = get_data(Season = season, SeasonType=season_type, PlayerOrTeam=player_or_team)[0]
                header = get_data(Season = season, SeasonType=season_type, PlayerOrTeam=player_or_team)[1]

                stats = []
                for stat in data:
                    stats.append(stat)

                # writes csv file with format player_or_teamplayer_data_season_season_type
                with open('{0}_data_{1}_{2}.csv'.format(player_or_team, season, season_type), 'wb') as a:
                    writer = csv.writer(a)
                    writer.writerow(header)
                    writer.writerows(stats)