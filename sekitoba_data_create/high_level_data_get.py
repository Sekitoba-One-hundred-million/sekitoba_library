import sekitoba_data_manage as dm
import sekitoba_library as lib

dm.dl.file_set( "race_rank_data.pickle" )
dm.dl.file_set( "race_level_data.pickle" )
dm.dl.file_set( "next_race_data.pickle" )

class RaceHighLevel:
    def __init__( self ):
        self.race_rank_data = dm.dl.data_get( "race_rank_data.pickle" )
        self.next_racd_data: dict[ str, dict[ str, lib.current_data ] ] = dm.pickle_load( "next_race_data.pickle" )
        #self.race_level_data = dm.dl.data_get( "race_level_data.pickle" )
        #self.race_level_split_data = dm.dl.data_get( "race_level_split_data.pickle" )

    def day_check( self, ymd, past_ymd ):
        if past_ymd["y"] < ymd["y"]:
            return True
        elif ymd["y"] < past_ymd["y"]:
            return False

        if past_ymd["m"] < ymd["m"]:
            return True
        elif ymd["m"] < past_ymd["m"]:
            return False

        if past_ymd["d"] < ymd["d"]:
            return True
        elif ymd["d"] < past_ymd["d"]:
            return False

        return False
        
    def data_get( self, cd: lib.current_data, pd: lib.past_data, ymd: dict ):
        result = 1000
        race_id = cd.race_id()
        past_id_list = pd.race_id_get()
        past_day_list = pd.past_day_list()
        past_rank_list = pd.rank_list()
        current_race_rank = self.race_rank_data[race_id]

        for i in range( 0, min( len( past_id_list ), 3 ) ):
            past_id = past_id_list[i]
            past_day = past_day_list[i]
            past_rank = past_rank_list[i]
            
            try:
                next_cd_data = self.next_racd_data[past_id]
                past_race_rank = self.race_rank_data[past_id]
            except:
                continue

            if past_race_rank < current_race_rank:
                continue

            high_level = False
            # race level check
            for horce_id in next_cd_data.keys():
                next_cd = next_cd_data[horce_id]
                birthday = next_cd.ymd()
                past_ymd = { "y": int( birthday[0] ), "m": int( birthday[1] ), "d": int( birthday[2] ) }

                if not self.day_check( ymd, past_ymd ):
                    continue

                if next_cd.rank() == 1:
                    high_level = True
                    break

            if not high_level:
                continue

            result = min( result, past_rank )

        return result
