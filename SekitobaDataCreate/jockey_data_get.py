import copy

import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

class JockeyAnalyze:
    def __init__( self, race_data: ps.RaceData, race_horce_data: ps.RaceHorceData, jockey_data: ps.JockeyData ):
        self.race_data: ps.RaceData = race_data
        self.race_horce_data: ps.RaceHorceData = race_horce_data
        self.jockey_data: ps.JockeyData = jockey_data

    def distCheck( self, di ):
        if di < 1400:#短距離
            return 1
        elif di < 1800:#マイル
            return 2
        elif di < 2200:#中距離
            return 3
        elif di < 2800:#中長距離
            return 4
        else:#長距離
            return 5

    def rank( self, race_id, horce_id ):
        jockey_id = self.race_horce_data.data[horce_id]["jockey_id"]
        dist = self.distCheck( self.race_data.data["dist"] )
        kind = self.race_data.data["kind"]
        baba = self.race_data.data["baba"]
        key_dict = { "baba": str( baba ), "dist": str( dist ), "kind": str( kind ) }

        year = race_id[0:4]
        before_year = str( int( year ) - 1 )
        jockey_analyze = {}
        
        if jockey_id in self.jockey_data.data and \
          before_year in self.jockey_data.data[jockey_id]["jockey_analyze"]:
            jockey_analyze = self.jockey_data.data[jockey_id]["jockey_analyze"][before_year]
        else:
            return -1000

        rank = 0
        count = 0

        for check_key in key_dict.keys():
            try:
                rank += jockey_analyze[check_key][key_dict[check_key]]["rank"]
                count += 1
            except:
                continue

        if not count == 0:
            rank /= count

        return int( rank )

    def year_rank( self, horce_id, key_year ):
        result = -1000
        jockey_id = self.race_horce_data.data[horce_id]["jockey_id"]

        try:
            result = self.jockey_data.data[jockey_id]["jockey_year_rank"][key_year]
        except:
            return result

        return result
