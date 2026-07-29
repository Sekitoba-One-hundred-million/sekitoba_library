import SekitobaDataManage as dm
import SekitobaLibrary as lib
from SekitobaPsql.horce_data import HorceData

dm.dl.file_set( "run_add_dist.pickle" )

class TimeIndexGet:
    def __init__( self, horce_data: HorceData ):
        self.horce_data: HorceData = horce_data
        self.run_add_dist_data = dm.dl.data_get( "run_add_dist.pickle" )
    
    def main( self, horce_id, day_list ):
        result = {}
        result["max"] = lib.escapeValue
        result["min"] = lib.escapeValue
        result["average"] = lib.escapeValue
        result["before"] = lib.escapeValue

        try:
            time_index = self.horce_data.data[horce_id]["time_index"]
        except:
            return result

        count = 0
        
        for i in range( 0, len( day_list ) ):
            d = day_list[i]

            if not d in time_index:
                continue
            
            if not time_index[d] == 0:
                count += 1

                if result["average"] == lib.escapeValue:
                    result["max"] = -1
                    result["min"] = 10000
                    result["average"] = 0
                    result["before"] = time_index[d]
                    
                result["max"] = max( result["max"], time_index[d] )
                result["min"] = min( result["min"], time_index[d] )
                result["average"] += time_index[d]

        if not count == 0:
            result["average"] /= count

        return result

    def run_main( self, horce_id, pd: lib.PastData ):
        result = {}
        result["max"] = lib.escapeValue
        result["average"] = lib.escapeValue
        result["before"] = lib.escapeValue

        try:
            time_index = self.horce_data.data[horce_id]["time_index"]
        except:
            return result

        count = 0

        for past_cd in pd.past_cd_list():
            past_race_id = past_cd.race_id()

            if not past_race_id in self.run_add_dist_data:
                continue

            key_horce_num = str( int( past_cd.horce_number() ) )
            
            if not key_horce_num in self.run_add_dist_data[past_race_id]:
                continue
                
            m_dist = past_cd.dist() * 1000
            run_dist = m_dist + self.run_add_dist_data[past_race_id][key_horce_num]
            dist_rate = run_dist / m_dist
            d = past_cd.birthday()
        
            if not d in time_index:
                continue
            
            if not time_index[d] == 0:
                count += 1

                if result["average"] == lib.escapeValue:
                    result["max"] = -1
                    result["min"] = 10000
                    result["average"] = 0
                    result["before"] = time_index[d]
                    
                check_time_index = time_index[d] * dist_rate
                result["max"] = max( result["max"], time_index[d] )
                result["min"] = min( result["min"], time_index[d] )
                result["average"] += time_index[d]

        if not count == 0:
            result["average"] /= count

        return result

    def get_current( self, horce_id, day ):
        try:
            return self.horce_data.data[horce_id]["time_index"][day]
        except:
            return lib.escapeValue
