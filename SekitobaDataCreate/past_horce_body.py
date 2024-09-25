import SekitobaDataManage as dm
import SekitobaLibrary as lib

dm.dl.file_set( "corner_horce_body.pickle" )

class PastHorceBody:
    def __init__( self ):
        self.corner_horce_body = dm.dl.data_get( "corner_horce_body.pickle" )

    def ave_first( self, pd: lib.PastData, key_horce_num: str  ):
        race_id_list = pd.raceIdGet()
        count = 0
        result = 0
        
        for race_id in race_id_list:
            try:
                key = min( self.corner_horce_body[race_id].keys() )
                result += self.corner_horce_body[race_id][key][key_horce_num]
                count += 1
            except:
                continue

        if count == 0:
            return -1
        else:
            result /= count

        return result

    def before_first( self, pd: lib.PastData, key_horce_num: str  ):
        race_id_list = pd.raceIdGet()
        
        if len( race_id_list ) == 0:
            return -1
        
        race_id = race_id_list[0]
        
        try:
            key = min( self.corner_horce_body[race_id].keys() )
            return self.corner_horce_body[race_id][key][key_horce_num]
        except:
            return -1

    def ave_last( self, pd: lib.PastData, key_horce_num: str ):
        race_id_list = pd.raceIdGet()
        count = 0
        result = 0
        
        for race_id in race_id_list:
            try:
                key = max( self.corner_horce_body[race_id].keys() )
                result += self.corner_horce_body[race_id][key][key_horce_num]
                count += 1
            except:
                continue

        if count == 0:
            return -1
        else:
            result /= count

        return result

    def before_last( self, pd: lib.PastData, key_horce_num: str ):
        race_id_list = pd.raceIdGet()
        
        if len( race_id_list ) == 0:
            return -1
        
        race_id = race_id_list[0]
        
        try:
            key = min( self.corner_horce_body[race_id].keys() )
            return self.corner_horce_body[race_id][key][key_horce_num]
        except:
            return -1    

    def best_first( self, pd: lib.PastData, key_horce_num: str ):
        race_id_list = pd.raceIdGet()
        rank_list = pd.rankList()

        if len( race_id_list ) == 0 or \
          len( rank_list ) == 0 or \
          not len( race_id_list ) == len( rank_list ):
            return -1

        count = 0
        result = 0

        for i in range( 0, len( race_id_list ) ):
            race_id = race_id_list[i]
            rank = rank_list[i]

            try:
                key = min( self.corner_horce_body[race_id].keys() )
                first_horce_body = self.corner_horce_body[race_id][key][key_horce_num]
            except:
                continue

            n = max( 1, 6 - rank )
            count += n
            result += first_horce_body * n

        if count == 0:
            return -1

        result /= count

        return result

    def best_last( self, pd: lib.PastData, key_horce_num: str ):
        race_id_list = pd.raceIdGet()
        rank_list = pd.rankList()

        if len( race_id_list ) == 0 or \
          len( rank_list ) == 0 or \
          not len( race_id_list ) == len( rank_list ):
            return -1

        count = 0
        result = 0

        for i in range( 0, len( race_id_list ) ):
            race_id = race_id_list[i]
            rank = rank_list[i]

            try:
                key = max( self.corner_horce_body[race_id].keys() )
                last_horce_body = self.corner_horce_body[race_id][key][key_horce_num]
            except:
                continue

            n = max( 1, 6 - rank )
            count += n
            result += last_horce_body * n

        if count == 0:
            return -1

        result /= count

        return result
    
