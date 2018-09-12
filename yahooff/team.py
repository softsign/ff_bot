class Team(object):
    '''Teams are part of the league'''
    '''feed in league_standings_data[0]['standings']['teams']['team'][XXXX]'''
    def __init__(self, teamdata, scoreboarddata):
        self.team_id = teamdata['team_id']
#        self.team_abbrev = data['teamAbbrev']
        self.team_name = teamdata['name']
        self.division_id = teamdata['division_id']
#        self.division_name = data['division']['divisionName']
        self.wins = int(teamdata['team_standings']['outcome_totals']['wins'])
        self.losses = int(teamdata['team_standings']['outcome_totals']['losses'])
        self.gamesplayed = self.wins + self.losses
        self.points_for = float(teamdata['team_standings']['points_for'])
        self.points_against = float(teamdata['team_standings']['points_against'])
        self.owner = teamdata['managers']['manager']['nickname']
        self.schedule = []
        self.scores = []
        self.projected = []
        self.mov = []
        self.pmov = []
        self.high_score = 0.0
        self.low_score = 9999.0
        self.power_rating = None
        self._fetch_schedule(scoreboarddata)

    def __repr__(self):
        return 'Team(%s)' % (self.team_name, )

    def _fetch_schedule(self, data):
        '''Fetch schedule and scores for team'''
        '''
        feed in scoreboard data from 
            "select * from fantasysports.leagues.scoreboard where league_key='" + self.league_key + "' and week='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16'")
        '''
        matchups_by_week = data

        # this is a horribly inefficient hack to make up for the fact that Yahoo stores schedule info differently
        count = 0
        for matchup_week in matchups_by_week:

            # TODO fix playoff handling during regular season

            count += 1
            if count >= 15:
                continue
            else:
                matchups_of_week = matchup_week['scoreboard']['matchups']['matchup']
                for matchup in matchups_of_week:
                    if (matchup['teams']['team'][0]['team_id'] == self.team_id) or (matchup['teams']['team'][1]['team_id'] == self.team_id):
                        if not int(matchup['is_playoffs']): #no easy way to determine bye for Yahoo, so just skip playoffs for now
                            if matchup['teams']['team'][1]['team_id'] == self.team_id:
                                score = float(matchup['teams']['team'][1]['team_points']['total'])
                                projected = float(matchup['teams']['team'][1]['team_projected_points']['total'])
                                opponentId = matchup['teams']['team'][0]['team_id']
                            else:
                                score = float(matchup['teams']['team'][0]['team_points']['total'])
                                projected = float(matchup['teams']['team'][0]['team_projected_points']['total'])
                                opponentId = matchup['teams']['team'][1]['team_id']

                            self.scores.append(score)
                            self.projected.append(projected)

                            if score >= max(float(h) for h in self.scores):
                                self.high_score = score

                            if score <= min(float(l) for l in self.scores):
                                self.low_score = score

                            self.schedule.append(opponentId)


    def get_roster(self, week):
        '''Get roster for a given week'''
        roster = None
        return roster

    def set_power_rating(self, rating):
        self.power_rating = rating
