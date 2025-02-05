import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps
from SekitobaDataCreate.get_horce_data import GetHorceData

wrap_data = ps.RaceData().get_select_data( "wrap" )

class BeforeRaceScore:
    def __init__( self, race_data: ps.RaceData ):
        self.race_data : ps.RaceData = race_data

    def score_get( self, horce_id, getHorceData: GetHorceData ):
        score = lib.escapeValue

        if getHorceData.before_cd is None:
            return score

        if not getHorceData.before_cd.race_check():
            return score

        before_race_id = getHorceData.before_cd.race_id()

        if not before_race_id in wrap_data:
            return score

        pace = lib.pace_data( wrap_data[before_race_id]["wrap"] )

        if pace == None:
            return score

        waku_key = ""

        if getHorceData.before_cd.horce_number() < getHorceData.before_cd.all_horce_num() / 2:
            waku_key = "1"
        else:
            waku_key = "2"

        before_kind_key_data = {}
        before_kind_key_data["place"] = str( int( getHorceData.before_cd.place() ) )
        before_kind_key_data["dist"] = str( int( getHorceData.before_cd.dist() ) )
        before_kind_key_data["baba"] = str( int( getHorceData.before_cd.baba_status() ) )
        before_kind_key_data["kind"] = str( int( getHorceData.before_cd.race_kind() ) )
        before_kind_key_data["limb"] = getHorceData.key_limb
        before_waku_three_rate = getHorceData.getKindScore( self.race_data.data["waku_three_rate"], kind_key_data = before_kind_key_data )

        if getHorceData.limb_math >= 3:
            pace *= -1

        score = getHorceData.before_cd.rank() + pace - ( before_waku_three_rate * 50 )
        return score
