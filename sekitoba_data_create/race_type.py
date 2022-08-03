import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "foot_used.pickle" )
dm.dl.file_set( "race_rank_data.pickle" )

class RaceType:
    def __init__( self ):
        self.race_rank_data = dm.dl.data_get( "race_rank_data.pickle" )
        self.foot_used_data = dm.dl.data_get( "foot_used.pickle" )

    def stright_slope( self, cd: lib.current_data, pd: lib.past_data, prod_race_id = None, prod_current_slope = None ):
        if dm.dl.prod:
            race_id = prod_race_id
            current_slope = prod_current_slope
        else:
            race_id = cd.race_id()
            current_slope = lib.stright_slope( cd.place() )
            
        current_race_rank = self.race_rank_data[race_id]
        past_cd_list = pd.past_cd_list()
        before_cd = pd.before_cd()
        
        score = 0
        same_slope = 100
        diff_slope = 100

        if before_cd == None:
            return 0

        for past_cd in past_cd_list:
            try:
                past_race_rank = self.race_rank_data[past_cd.race_id()]
            except:
                continue

            if past_race_rank < current_race_rank:
                continue

            if lib.stright_slope( past_cd.place() ) == current_slope:
                same_slope = min( same_slope, past_cd.rank() )
            else:
                diff_slope = min( diff_slope, past_cd.rank() )
            
        if not lib.stright_slope( before_cd.place() ) == current_slope and same_slope < diff_slope:
            score = before_cd.rank()

        score = int( ( score - 1 ) / 3 )

        return score

    def foot_used( self, cd: lib.current_data, pd: lib.past_data, prod_race_id = None, prod_baba_status = None ):
        if dm.dl.prod:
            race_id = prod_race_id
            baba_status = prod_baba_status
        else:
            race_id = cd.race_id()
            baba_status = cd.baba_status()

        score = 0
        before_cd = pd.before_cd()
        
        if before_cd == None:
            return 0
            
        current_race_rank = self.race_rank_data[race_id]
        past_cd_list = pd.past_cd_list()
        foot_score = { "1": 100, "2": 100 }
        
        for past_cd in past_cd_list:
            past_race_id = past_cd.race_id()
                
            try:
                past_race_rank = self.race_rank_data[past_race_id]
                foot_used = self.foot_used_data[past_race_id]
            except:
                continue
            
            if past_race_rank < current_race_rank:
                continue
            
            key_foot_used = str( foot_used )
            foot_score[key_foot_used] = min( foot_score[key_foot_used], past_cd.rank() )

        try:
            before_foot_used = self.foot_used_data[before_cd.race_id()]
        except:
            return score
            
        if not foot_score["1"] == 100 and \
          not foot_score["2"] == 100 and \
          not foot_score["1"] == foot_score["2"]:
            good_foot_used = 0
            
            if foot_score["1"] < foot_score["2"]:
                good_foot_used = 1
            else:
                good_foot_used = 2

            score = baba_status * 10 + good_foot_used

        return score
