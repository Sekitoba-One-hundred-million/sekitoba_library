import sekitoba_library as lib
import sekitoba_data_manage as dm

file_name = "slow_start_data.pickle"
dm.dl.file_set( file_name )

class SlowStart:
    def __init__( self ):
        self.slow_start_data = dm.dl.data_get( file_name )

    def main( self, horce_id: str, pd: lib.past_data ):
        result = 0
        count = 0
        past_day_list = pd.past_day_list()

        for day in past_day_list:
            try:
                slow_check = self.slow_start_data[horce_id][day]
            except:
                continue

            count += 1

            if slow_check:
                result += 1

        if not count == 0:
            result /= count

        return result