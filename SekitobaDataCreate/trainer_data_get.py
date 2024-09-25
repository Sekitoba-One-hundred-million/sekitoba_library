import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

class TrainerAnalyze:
    def __init__( self, race_data: ps.RaceData, race_horce_data: ps.RaceHorceData, trainer_data: ps.TrainerData ):
        self.race_data: ps.RaceData  = race_data
        self.race_horce_data: ps.RaceHorceData  = race_horce_data
        self.trainer_data: ps.TrainerData = trainer_data

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
        trainer_id = self.race_horce_data.data[horce_id]["trainer_id"]
        dist = self.distCheck( self.race_data.data["dist"] )
        kind = self.race_data.data["kind"]
        baba = self.race_data.data["baba"]
        key_dict = { "baba": str( baba ), "dist": str( dist ), "kind": str( kind ) }

        year = race_id[0:4]
        before_year = str( int( year ) - 1 )
        trainer_analyze = {}
        
        if trainer_id in self.trainer_data.data and \
          before_year in self.trainer_data.data[trainer_id]["trainer_analyze"]:
            trainer_analyze = self.trainer_data.data[trainer_id]["trainer_analyze"][before_year]
        else:
            return -1000        

        rank = 0
        count = 0

        for check_key in key_dict.keys():
            try:
                rank += trainer_analyze[check_key][key_dict[check_key]]["rank"]
                count += 1
            except:
                continue

        if not count == 0:
            rank /= count

        return int( rank )
