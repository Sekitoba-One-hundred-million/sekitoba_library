import sekitoba_data_manage as dm
from sekitoba_psql.horce_data import HorceData

class TimeIndexGet:
    def __init__( self, horce_data: HorceData ):
        self.horce_data: HorceData = horce_data
    
    def main( self, horce_id, day_list ):
        result = {}
        result["max"] = 0
        result["min"] = 10000
        result["average"] = 0

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
                result["max"] = max( result["max"], time_index[d] )
                result["min"] = min( result["min"], time_index[d] )
                result["average"] += time_index[d]

        if not count == 0:
            result["average"] /= count

        return result
        
        
