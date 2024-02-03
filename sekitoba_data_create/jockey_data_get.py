import copy

import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "jockey_analyze_data.pickle" )
dm.dl.file_set( "jockey_id_data.pickle" )
dm.dl.file_set( "jockey_year_rank_data.pickle" )

class JockeyData:
    def __init__( self ):
        self.race_info_data = dm.dl.data_get( "race_info_data.pickle" )
        self.race_jockey_id_data = dm.dl.data_get( "race_jockey_id_data.pickle" )
        self.jockey_analyze_data = dm.dl.data_get( "jockey_analyze_data.pickle" )
        self.jockey_year_rank_data = dm.dl.data_get( "jockey_year_rank_data.pickle" )

    def dist_check( self, di ):
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

    def rank( self, race_id, horce_id, jockey_id = None,  race_info = None ):
        if race_info == None and race_id in self.race_info_data:
            race_info = self.race_info_data[race_id]
        else:
            return 0

        if jockey_id == None and ( race_id in self.race_jockey_id_data and \
                                  horce_id in self.race_jockey_id_data[race_id] ):
            jockey_id = self.race_jockey_id_data[race_id][horce_id]
        else:
            return 0

        dist = self.dist_check( race_info["dist"] )
        kind = race_info["kind"]
        baba = race_info["baba"]
        key_dict = { "baba": str( baba ), "dist": str( dist ), "kind": str( kind ) }

        year = race_id[0:4]
        before_year = str( int( year ) - 1 )

        try:
            jockey_data = self.jockey_analyze_data[jockey_id][before_year]
        except:
            return 0

        rank = 0
        count = 0

        for check_key in key_dict.keys():
            try:
                rank += jockey_data[check_key][key_dict[check_key]]["rank"]
                count += 1
            except:
                continue

        if not count == 0:
            rank /= count

        return int( rank )

    def year_rank( self, race_id, horce_id, key_year, jockey_id = None ):
        result = -1000

        if jockey_id == None and ( race_id in self.race_jockey_id_data and \
                                  horce_id in self.race_jockey_id_data[race_id] ):
            jockey_id = self.race_jockey_id_data[race_id][horce_id]
        else:
            return result

        try:
            result = self.jockey_year_rank_data[jockey_id][key_year]
        except:
            return result

        return result
