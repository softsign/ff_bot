import requests

from .utils import (two_step_dominance,
                    power_points, )
from .team import Team
from .settings import Settings
from .matchup import Matchup
from .exception import (PrivateLeagueException,
                        InvalidLeagueException,
                        UnknownLeagueException, )

import collections
import os
import webbrowser
import operator
from operator import itemgetter

from yql3 import *
from yql3.storage import FileTokenStore

class League(object):
    '''Creates a League instance for Yahoo league'''
    def __init__(self, league_id, year):

        self.league_id = league_id

        # yahoo oauth api (consumer) key and secret
        with open("./authentication/private.txt", "r") as auth_file:
            auth_data = auth_file.read().split("\n")
        consumer_key = auth_data[0]
        consumer_secret = auth_data[1]

        # yahoo oauth process
        self.y3 = ThreeLegged(consumer_key, consumer_secret)
        _cache_dir = "./authentication/oauth_token"
        if not os.access(_cache_dir, os.R_OK):
            os.mkdir(_cache_dir)

        token_store = FileTokenStore(_cache_dir, secret="sasfasdfdasfdaf")
        stored_token = token_store.get("foo")

        if not stored_token:
            raise Exception("Yahoo oauth_token missing. Run 'python first_time_token.py' one time to authenticate first time with Yahoo.")
        else:
            print("Verifying token...")
            self.token = self.y3.check_token(stored_token)
            if self.token != stored_token:
                print("Setting stored token!")
                token_store.set("foo", self.token)

        '''
                run base yql queries
                '''
        # get fantasy football game info
        #TODO: map game_key to year (i.e., current year='nfl', 2017='37', etc.)
        if year == '2018':
            gkey = 'nfl'
        elif year == '2017':
            gkey = '371'
        else:
            gkey = 'nfl'


        game_data = self.yql_query("select * from fantasysports.games where game_key='" + gkey + "'")
        # unique league key composed of this year's yahoo fantasy football game id and the unique league id
        self.league_key = game_data[0].get("game_key") + ".l." + self.league_id

        # get individual league roster
        roster_data = self.yql_query(
            "select * from fantasysports.leagues.settings where league_key='" + self.league_key + "'")

        roster_slots = collections.defaultdict(int)
        self.league_roster_active_slots = []
        flex_positions = []

        for position in roster_data[0].get("settings").get("roster_positions").get("roster_position"):

            position_name = position.get("position")
            position_count = int(position.get("count"))

            count = position_count
            while count > 0:
                if position_name != "BN":
                    self.league_roster_active_slots.append(position_name)
                count -= 1

            if position_name == "W/R":
                flex_positions = ["WR", "RB"]
            if position_name == "W/R/T":
                flex_positions = ["WR", "RB", "TE"]

            if "/" in position_name:
                position_name = "FLEX"

            roster_slots[position_name] += position_count

        self.roster = {
            "slots": roster_slots,
            "flex_positions": flex_positions
        }

        # get data for all teams in league
        self.teams_data = self.yql_query("select * from fantasysports.teams where league_key='" + self.league_key + "'")


        # get data for all league standings
        self.league_standings_data = self.yql_query(
            "select * from fantasysports.leagues.standings where league_key='" + self.league_key + "'")

        self.league_name = self.league_standings_data[0].get("name")

        #get matchups data for the current year
        self.scoreboard_data = self.yql_query("select * from fantasysports.leagues.scoreboard where league_key='" + self.league_key + "' and week in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)")

        self.year = year
        self.teams = []
        self._fetch_league()
        self.current_week = 1
        self._latest_week()


    def __repr__(self):
        return 'League(%s, %s)' % (self.league_id, self.year, )

    def _fetch_settings(self, data):
        self.settings = Settings(data)

    def power_rankings(self):
        '''Return power rankings for current week'''

        '''original approach
        # calculate win for every week
        win_matrix = []
        teams_sorted = sorted(self.teams, key=lambda x: x.team_id,
                              reverse=False)

        for team in teams_sorted:
            wins = [0]*32
            for mov, opponent in zip(team.mov[:week], team.schedule[:week]):
                opp = int(opponent.team_id)-1
                if mov > 0:
                    wins[opp] += 1
            win_matrix.append(wins)
        dominance_matrix = two_step_dominance(win_matrix)
        power_rank = power_points(dominance_matrix, teams_sorted, week)
        '''

        '''Replacing with Oberon Mt. Power Rating Formula <http://www.justlacrosse.com/omffl/powerrating.htm>
        
        ( (avg score x 6) + [(high score + low score) x 2] +[ (winning % x 200) x 2] ) / 10

        '''

        oberon = None
        for team in self.teams:
            # this will break if a team ever ties
            if team.points_for > 0:
                avg = team.points_for / float(team.gamesplayed)
            else:
                avg = team.high_score
            high = team.high_score
            low = team.low_score

            if team.gamesplayed > 0:
                winpct = float(team.wins) / float(team.gamesplayed)
            else:
                winpct = 0.0
            oberon = (avg*6 + (high+low)*2 + (winpct*200)*2) / 10
            team.set_power_rating(oberon)

        pranks_raw = { team.team_name: team.power_rating for team in self.teams }
        pranks_sorted = sorted(pranks_raw.items(), key=operator.itemgetter(1), reverse=True)
        return pranks_sorted

    def luck_rankings(self,fweek=None):
        '''Return luck rankings for current week'''


        if fweek is None:
            week = self._latest_week()
        elif fweek <= 13:
            week = fweek
        else:
            week = 13

        #TODO fix playoff bounds handling

        weekly_scores = []
        for team in self.teams:
            # this will break if a team ever ties
            weekly_scores += [ team.scores[week-1] ]

        luck_scores = []
        for team in self.teams:
            ew = 0

            for score in weekly_scores:
                if team.scores[week-1] > score:
                    ew += 1.0

            if team.mov[week-1] >= 0.0:
                lscore = (1.0 - ew/float(len(self.teams)-1))*100
            else:
                lscore = (0.0 - ew/float(len(self.teams)-1))*100

            luck_scores += [ (team.team_name, lscore) ]

        #TODO nice and clean (think about using this for power ranks)
        lscores_sorted = sorted(luck_scores, key=itemgetter(1), reverse=True)
        return lscores_sorted


#from ffmetrics

    def yql_query(self, query):
        # print("Executing query: %s\n" % query)
        q = self.y3.execute(query, token=self.token)
        result = q.rows
        return result

    # is this being used?
    def retrieve_data(self, chosen_week):

        teams_dict = {}
        for team in self.teams_data:

            team_id = team.get("team_id")
            team_name = team.get("name")
            team_managers = team.get("managers").get("manager")

            team_manager = ""
            if type(team_managers) is dict:
                team_manager = team_managers.get("nickname")
            else:
                for manager in team_managers:
                    if manager.get("is_comanager") is None:
                        team_manager = manager.get("nickname")

            team_info_dict = {"name": team_name, "manager": team_manager}
            teams_dict[team_id] = team_info_dict

        team_results_dict = {}

        # iterate through all teams and build team_results_dict containing all relevant team stat information
        for team in teams_dict:

            team_id = team
            team_name = teams_dict.get(team).get("name").encode("utf-8")

            # get data for this individual team
            roster_stats_data = self.yql_query(
                "select * from fantasysports.teams.roster.stats where team_key='" + self.league_key + ".t." +
                team + "' and week='" + chosen_week + "'")

            players = []
            positions_filled_active = []
            for player in roster_stats_data[0].get("roster").get("players").get("player"):
                pname = player.get("name")['full']
                pteam = player.get('editorial_team_abbr').upper()
                player_selected_position = player.get("selected_position").get("position")
                bad_boy_points = 0
                crime = ''
                if player_selected_position != "BN":
                    bad_boy_points, crime = self.BadBoy.check_bad_boy_status(pname, pteam, player_selected_position)
                    positions_filled_active.append(player_selected_position)

                player_info_dict = {"name": player.get("name")["full"],
                                    "status": player.get("status"),
                                    "bye_week": int(player.get("bye_weeks")["week"]),
                                    "selected_position": player.get("selected_position").get("position"),
                                    "eligible_positions": player.get("eligible_positions").get("position"),
                                    "fantasy_points": float(player.get("player_points").get("total", 0.0)),
                                    "bad_boy_points": bad_boy_points,
                                    "bad_boy_crime": crime
                                    }

                players.append(player_info_dict)

            team_name = team_name.decode('utf-8')
            bad_boy_total = 0
            worst_offense = ''
            worst_offense_score = 0
            num_offenders = 0
            for p in players:
                if p['selected_position'] != "BN":
                    bad_boy_total = bad_boy_total + p['bad_boy_points']
                    if p['bad_boy_points'] > 0:
                        num_offenders = num_offenders + 1
                        if p['bad_boy_points'] > worst_offense_score:
                            worst_offense = p['bad_boy_crime']
                            worst_offense_score = p['bad_boy_points']

            team_results_dict[team_name] = {
                "name": team_name,
                "manager": teams_dict.get(team).get("manager"),
                "players": players,
                "score": sum([p["fantasy_points"] for p in players if p["selected_position"] != "BN"]),
                "bench_score": sum([p["fantasy_points"] for p in players if p["selected_position"] == "BN"]),
                "team_id": team_id,
                "bad_boy_points": bad_boy_total,
                "worst_offense": worst_offense,
                "num_offenders": num_offenders,
                "positions_filled_active": positions_filled_active
            }

        return team_results_dict


    def _fetch_league(self):
        self._fetch_teams()
        #self._fetch_settings()

    def _fetch_teams(self):
        #Fetch teams in league

        teams = self.league_standings_data[0]['standings']['teams']['team']
        sbrd = self.scoreboard_data

        for team in teams:
            self.teams.append(Team(team,sbrd))

        # replace opponentIds in schedule with team instances
        for team in self.teams:
            for week, matchup in enumerate(team.schedule):
                for opponent in self.teams:
                    if matchup == opponent.team_id:
                        team.schedule[week] = opponent

        # calculate margin of victory and projected margin of victory
        for team in self.teams:
            for week, opponent in enumerate(team.schedule):
                mov = team.scores[week] - opponent.scores[week]
                pmov = team.projected[week] - opponent.projected[week]
                team.mov.append(mov)
                team.pmov.append(pmov)

        # sort by team ID
        self.teams = sorted(self.teams, key=lambda x: x.team_id, reverse=False)


    def scoreboard(self, fweek=None):
        #Returns list of matchups for a given week

        #todo map current date to week of season to use as default

        if fweek is None:
            week = self._latest_week()
        elif fweek <= 13:
            week = fweek
        else:
            week = 13

        matchups = self.scoreboard_data[week-1]['scoreboard']['matchups']['matchup']

        result = [Matchup(matchup) for matchup in matchups if self._checkmatchupweek(matchup,week)]

        #result = None
        '''
        for matchup in matchups:
            if (self._checkmatchupweek(matchup,week)):
                if result is None:
                    result = [Matchup(matchup)]
                    print(result)
                else:
                    result = result.append(Matchup(matchup))
                    print('.')
        '''
        for team in self.teams:
            for matchup in result:
                if matchup.home_team == team.team_id:
                    matchup.home_team = team
                if matchup.away_team == team.team_id:
                    matchup.away_team = team

        return result

    def standings(self):
        #returns list of current point totals

        standings_raw = { team.team_name: team.points_for for team in self.teams }
        standings_sorted = sorted(standings_raw.items(), key=operator.itemgetter(1), reverse=True)
        return standings_sorted




    def _latest_week(self):
        count = 1
        first_team = next(iter(self.teams or []), None)
        # Iterate through the first team's scores until you reach a week with 0 points scored
        for o in first_team.scores:
            if o == 0:
                '''
                if count != 1:
                    count = count - 1
                '''
                break
            else:
                count = count + 1

        self.current_week = count
        return count

    def _checkmatchupweek(self, matchup, week):
        # checks week of given matchup
        if int(matchup['week']) == week:
            return True
        else:
            return False
