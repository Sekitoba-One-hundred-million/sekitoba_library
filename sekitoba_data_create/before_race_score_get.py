import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "wrap_data.pickle" )
dm.dl.file_set( "slow_start_data.pickle" )
dm.dl.file_set( "waku_three_rate_data.pickle" )

class BeforeRaceScore:
    def __init__( self ):
        self.wrap_data = dm.dl.data_get( "wrap_data.pickle" )
        self.slow_start_data = dm.dl.data_get( "slow_start_data.pickle" )
        self.waku_three_rate_data = dm.dl.data_get( "waku_three_rate_data.pickle" )

    def score_get( self, before_cd: lib.current_data, limb, horce_id ):
        score = 1000

        if before_cd == None:
            return score

        if not before_cd.race_check():
            return score

        before_race_id = before_cd.race_id()

        if not before_race_id in self.wrap_data:
            return score

        pace = lib.pace_data( self.wrap_data[before_race_id] )

        if pace == None:
            return score

        waku_key = ""

        if before_cd.horce_number() < before_cd.all_horce_num() / 2:
            waku = "1"
        else:
            waku = "2"

        before_kind_key_data = {}
        before_kind_key_data["place"] = str( int( before_cd.place() ) )
        before_kind_key_data["dist"] = str( int( before_cd.dist() ) )
        before_kind_key_data["baba"] = str( int( before_cd.baba_status() ) )
        before_kind_key_data["kind"] = str( int( before_cd.race_kind() ) )
        before_kind_key_data["limb"] = str( int( limb ) )
        before_waku_three_rate = lib.kind_score_get( self.waku_three_rate_data, \
                                                    list( before_kind_key_data.keys() ), \
                                                    before_kind_key_data, \
                                                    waku_key )

        if limb >= 3:
            pace *= -1

        score = before_cd.rank() + pace - ( before_waku_three_rate * 50 )
        return score
