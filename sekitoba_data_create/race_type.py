import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "foot_used.pickle" )
dm.dl.file_set( "race_rank_data.pickle" )
dm.dl.file_set( "wrap_data.pickle" )

class RaceType:
    def __init__( self ):
        self.race_rank_data = dm.dl.data_get( "race_rank_data.pickle" )
        self.foot_used_data = dm.dl.data_get( "foot_used.pickle" )
        self.wrap_data = dm.dl.data_get( "wrap_data.pickle" )

    def set_race_rank_data( self, race_rank_data ):
        self.race_rank_data = race_rank_data

    def set_foot_used_data( self, foot_used_data ):
        self.foot_used_data = foot_used_data

    def set_wrap_data( self, wrap_data ):
        self.wrap_data = wrap_data

    def stright_slope( self, cd: lib.current_data, pd: lib.past_data, prod_race_rank = None, prod_current_slope = None ):
        if dm.dl.prod:
            current_slope = prod_current_slope
            current_race_rank = prod_race_rank
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

    def best_foot_used( self, cd: lib.current_data, pd: lib.past_data, prod_race_rank = None ):
        if dm.dl.prod:
            current_race_rank = prod_race_rank
        else:
            race_id = cd.race_id()
            current_race_rank = self.race_rank_data[race_id]

        good_foot_used = "0"
        past_cd_list = pd.past_cd_list()
        foot_score = { "1": { "count": 0, "rank": 0 }, "2": { "count": 0, "rank": 0 } }
        
        for past_cd in past_cd_list:
            past_race_id = past_cd.race_id()
            
            try:
                past_race_rank = self.race_rank_data[past_race_id]
                foot_used = self.foot_used_data[past_race_id]
            except:
                continue
            
            if past_race_rank < current_race_rank:
                continue

            if foot_used == 0:
                continue
            
            key_foot_used = str( foot_used )
            foot_score[key_foot_used]["rank"] += past_cd.rank()
            foot_score[key_foot_used]["count"] += 1

        for k in foot_score.keys():
            if not foot_score[k]["count"] == 0:
                foot_score[k]["rank"] /= foot_score[k]["count"]

        if foot_score["1"]["rank"] < foot_score["2"]["rank"]:
            good_foot_used = "1"
        else:
            good_foot_used = "2"

        return good_foot_used

    def foot_used_score_get( self, cd: lib.current_data, pd: lib.past_data, prod_race_rank = None ):
        if dm.dl.prod:
            current_race_rank = prod_race_rank
        else:
            race_id = cd.race_id()
            current_race_rank = self.race_rank_data[race_id]

        score = 100            
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

            if foot_used == 0:
                continue
            
            key_foot_used = str( foot_used )
            foot_score[key_foot_used] = min( foot_score[key_foot_used], past_cd.rank() )

        if not foot_score["1"] == 100 and \
          not foot_score["2"] == 100 and \
          not foot_score["1"] == foot_score["2"]:
            good_foot_used = 0
            
            if foot_score["1"] < foot_score["2"]:
                good_foot_used = 1
            else:
                good_foot_used = 2

            for i in range( 0, min( len( past_cd_list ), 3 ) ):
                try:
                    past_foot_used = self.foot_used_data[past_cd_list[i].race_id()]
                except:
                    continue

                if not past_foot_used == good_foot_used:
                    score = min( past_cd_list[i].rank(), score )

        return score

    def best_deployment( self, pd: lib.past_race_data ):
        best_dep = "-1"
        past_cd_list = pd.past_cd_list()
        check_deployment = { "1": 100, "2": 100, "3": 100, "4": 100, "5": 100, "6": 100 }

        for past_cd in past_cd_list:
            if past_cd == None:
                continue
                
            past_race_id = past_cd.race_id()

            try:
                past_wrap_data = self.wrap_data[past_race_id]
            except:
                continue

            past_deployment = lib.pace_create( past_wrap_data )

            if past_deployment == -1:
                continue
                
            key_past_deployment = str( int( past_deployment ) )
            check_deployment[key_past_deployment] = min( past_cd.rank(), check_deployment[key_past_deployment] )

        best_dep_score = 100
            
        for dk in check_deployment.keys():
            if check_deployment[dk] < best_dep_score:
                best_dep_score = check_deployment[dk]
                best_dep = dk

        return best_dep

    def deploypent( self, pd: lib.past_race_data ):
        score = 0
        before_cd = pd.before_cd()

        if before_cd == None:
            return score
            
        past_cd_list = pd.past_cd_list()
        before_race_id = before_cd.race_id()

        try:
            before_wrap = self.wrap_data[before_race_id]
        except:
            return score

        before_dep = lib.pace_create( before_wrap )
        check_deployment = { "1": 100, "2": 100, "3": 100, "4": 100, "5": 100, "6": 100 }

        for past_cd in past_cd_list:
            if past_cd == None:
                continue
                
            past_race_id = past_cd.race_id()

            if past_race_id == before_race_id:
                continue
                
            try:
                past_wrap_data = self.wrap_data[past_race_id]
            except:
                continue

            past_deployment = lib.pace_create( past_wrap_data )

            if past_deployment == -1:
                continue
                
            key_past_deployment = str( int( past_deployment ) )
            check_deployment[key_past_deployment] = min( past_cd.rank(), check_deployment[key_past_deployment] )

        best_dep_score = 100
        best_dep = ""
            
        for dk in check_deployment.keys():
            if check_deployment[dk] < best_dep_score:
                best_dep_score = check_deployment[dk]
                best_dep = dk

        if not best_dep == before_dep and not len( best_dep ) == 0:
            score = before_cd.rank()

        return score