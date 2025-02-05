import math

import SekitobaLibrary as lib
from SekitobaPsql.psql_race_data import RaceData

class KineticEnergy:
    def __init__( self, race_data: RaceData ):
        self.race_data: RaceData = race_data

    def create( self, cd: lib.CurrentData, pd: lib.PastData ):
        before_cd = pd.before_cd()

        if before_cd == None:
            return lib.escapeValue

        if before_cd.up_time() == 0:
            return lib.escapeValue

        key_limb = str( int( lib.limb_search( pd ) ) )
        before_key_place = str( int( before_cd.place() ) )
        before_key_kind = str( int( before_cd.race_kind() ) )
        before_key_dist = str( int( before_cd.dist() * 1000 ) )
        before_key_dist_kind = str( int( before_cd.dist_kind() ) )
        
        try:
            beforeAveRaceTime = self.race_data.data["race_time_analyze"][before_key_place][before_key_dist]["ave"]
            beforeAveUp3 = self.race_data.data["up3_analyze"][before_key_place][before_key_kind][before_key_dist_kind][key_limb]["ave"]
        except:
            return lib.escapeValue

        before_up3_speed = 600 / before_cd.up_time()
        before_up3_speed *= beforeAveUp3 / before_cd.up_time()
        before_weight = before_cd.burden_weight() + before_cd.weight()
        before_speed = ( before_cd.dist() * 1000 ) / before_cd.race_time()
        before_speed *= ( beforeAveRaceTime / before_cd.race_time()  )
        beforeUp3KineticEnergy = ( before_weight * math.pow( before_up3_speed, 2 ) ) / 2
        beforeKineticEnergy = ( before_weight * math.pow( before_speed, 2 ) ) / 2
        beforeKineticEnergy += beforeUp3KineticEnergy * 1.5
        
        weight = cd.burden_weight() + cd.weight()
        weightRate = weight / before_weight
        return math.sqrt( ( beforeKineticEnergy * 2 * weightRate ) / weight )
