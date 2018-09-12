class Matchup(object):
    '''Creates Matchup instance'''
    def __init__(self, data):
        self.data = data['teams']['team']
        self.isPlayoff = int(data['is_playoffs'])
        self.week = data['week']
        self._fetch_matchup_info()

    def __repr__(self):
        return 'Matchup(%s, %s)' % (self.home_team, self.away_team, )

    def _fetch_matchup_info(self):
        '''Fetch info for matchup'''

        if not self.isPlayoff:
            self.home_team = self.data[0]['team_id']
            self.away_team = self.data[1]['team_id']
            self.home_score = float(self.data[0]['team_points']['total'])
            self.away_score = float(self.data[1]['team_points']['total'])
            self.home_projected = float(self.data[0]['team_projected_points']['total'])
            self.away_projected = float(self.data[1]['team_projected_points']['total'])
        else:
            self.home_team = None
            self.home_score = None
            self.away_team = None
            self.away_score = None
            self.away_projected = None
            self.home_projected = None
