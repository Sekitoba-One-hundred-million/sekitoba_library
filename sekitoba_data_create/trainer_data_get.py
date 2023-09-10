import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "trainer_analyze_data.pickle" )
dm.dl.file_set( "race_trainer_id_data.pickle" )

class TrainerData:
    def __init__( self ):
        self.race_info_data = dm.dl.data_get( "race_info_data.pickle" )
        self.race_trainer_id_data = dm.dl.data_get( "race_trainer_id_data.pickle" )
        self.trainer_analyze_data = dm.dl.data_get( "trainer_analyze_data.pickle" )

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

    def rank( self, race_id, horce_id, race_info = None, trainer_id = None ):

        if race_info == None or trainer_id == None:
            try:
                race_info = self.race_info_data[race_id]
                trainer_id = self.race_trainer_id_data[race_id][horce_id]
            except:
                return 0

        dist = self.dist_check( race_info["dist"] )
        kind = race_info["kind"]
        baba = race_info["baba"]
        key_dict = { "baba": str( baba ), "dist": str( dist ), "kind": str( kind ) }

        year = race_id[0:4]
        before_year = str( int( year ) - 1 )

        try:
            trainer_data = self.trainer_analyze_data[trainer_id][before_year]
        except:
            return 0

        rank = 0
        count = 0

        for check_key in key_dict.keys():
            try:
                rank += trainer_data[check_key][key_dict[check_key]]["rank"]
                count += 1
            except:
                continue

        if not count == 0:
            rank /= count

        return int( rank )
