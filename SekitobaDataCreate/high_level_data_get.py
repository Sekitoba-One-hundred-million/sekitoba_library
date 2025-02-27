import SekitobaDataManage as dm
import SekitobaLibrary as lib

dm.dl.file_set( "race_money_data.pickle" )
dm.dl.file_set( "next_race_data.pickle" )

class RaceHighLevel:
    def __init__( self ):
        self.race_money_data = dm.dl.data_get( "race_money_data.pickle" )
        self.next_racd_data: dict[ str, dict[ str, lib.CurrentData ] ] = dm.dl.data_get( "next_race_data.pickle" )

    def day_check( self, ymd, past_ymd ):
        if past_ymd["year"] < ymd["year"]:
            return True
        elif ymd["year"] < past_ymd["year"]:
            return False

        if past_ymd["month"] < ymd["month"]:
            return True
        elif ymd["month"] < past_ymd["month"]:
            return False

        if past_ymd["day"] < ymd["day"]:
            return True
        elif ymd["day"] < past_ymd["day"]:
            return False

        return False

    def current_high_level( self, race_id ):
        try:
            next_cd_data = self.next_racd_data[race_id]
        except:
            return 0

        count = 0

        for horce_id in next_cd_data.keys():
            if next_cd_data[horce_id].rank() == 1:
                count += 1

        return count
        
    def data_get( self, cd: lib.CurrentData, pd: lib.PastData, ymd: dict ):
        result = 1000
        race_id = cd.race_id()
        past_id_list = pd.race_id_get()
        past_day_list = pd.past_day_list()
        past_rank_list = pd.rank_list()
        current_race_rank = 1#self.race_rank_data[race_id]

        if race_id in self.race_money_data:
            current_race_rank = lib.money_class_get( self.race_money_data[race_id] )

        for i in range( 0, min( len( past_id_list ), 3 ) ):
            past_id = past_id_list[i]
            past_day = past_day_list[i]
            past_rank = past_rank_list[i]
            
            try:
                next_cd_data = self.next_racd_data[past_id]
                past_race_rank = lib.money_class_get( self.race_money_data[past_id] )
            except:
                continue

            if past_race_rank < current_race_rank:
                continue

            high_level = False
            # race level check
            for horce_id in next_cd_data.keys():
                next_cd = next_cd_data[horce_id]
                birthday = next_cd.ymd()
                past_ymd = { "year": int( birthday[0] ), "month": int( birthday[1] ), "day": int( birthday[2] ) }

                if not self.day_check( ymd, past_ymd ):
                    continue

                if not next_cd.race_check():
                    continue

                if next_cd.rank() == 1:
                    high_level = True
                    break

            if not high_level:
                continue

            result = min( result, past_rank )

        return result
