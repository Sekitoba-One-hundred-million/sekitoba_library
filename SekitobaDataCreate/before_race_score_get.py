import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

wrap_data = ps.RaceData().get_select_data( "wrap" )

class BeforeRaceScore:
    def __init__( self, race_data: ps.RaceData ):
        self.race_data : ps.RaceData = race_data

    def score_get( self, before_cd: lib.current_data, limb, horce_id ):
        score = 1000

        if before_cd == None:
            return score

        if not before_cd.race_check():
            return score

        before_race_id = before_cd.race_id()

        if not before_race_id in wrap_data:
            return score

        pace = lib.pace_data( wrap_data[before_race_id]["wrap"] )

        if pace == None:
            return score

        waku_key = ""

        if before_cd.horce_number() < before_cd.all_horce_num() / 2:
            waku_key = "1"
        else:
            waku_key = "2"

        before_kind_key_data = {}
        before_kind_key_data["place"] = str( int( before_cd.place() ) )
        before_kind_key_data["dist"] = str( int( before_cd.dist() ) )
        before_kind_key_data["baba"] = str( int( before_cd.baba_status() ) )
        before_kind_key_data["kind"] = str( int( before_cd.race_kind() ) )
        before_kind_key_data["limb"] = str( int( limb ) )
        before_waku_three_rate = lib.kind_score_get( self.race_data.data["waku_three_rate"], \
                                                    list( before_kind_key_data.keys() ), \
                                                    before_kind_key_data, \
                                                    waku_key )

        if limb >= 3:
            pace *= -1

        score = before_cd.rank() + pace - ( before_waku_three_rate * 50 )
        return score
