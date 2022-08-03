import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "train_time_data.pickle" )
dm.dl.file_set( "train_ave_data.pickle" )

class TrainIndexGet:
    def __init__( self ):
        self.train_time_data = dm.dl.data_get( "train_time_data.pickle" )
        self.train_ave_data = dm.dl.data_get( "train_ave_data.pickle" )

    def main( self, race_id, key_horce_num ):
        result = {}
        result["score"] = 0
        result["a"] = 0
        result["b"] = 0        

        try:
            load = self.train_time_data[race_id][key_horce_num]["load"]
            cource = self.train_time_data[race_id][key_horce_num]["cource"] 
            t_time = self.train_time_data[race_id][key_horce_num]["time"][0]
            wrap = self.train_time_data[race_id][key_horce_num]["wrap"]
        except:
            return result

        n = len( self.train_time_data[race_id][key_horce_num]["time"] )
        t = 1
        try:
            a, b = lib.regression_line( wrap )
        except:
            a = 0
            b = 0

        result["a"] = a
        result["b"] = b        

        if not n == 1:
            t = n + 1

        t_time /= t

        try:
            ave_load = self.train_ave_data["load"][load]["time"]
        except:
            ave_load = t_time

        try:
            ave_cource = self.train_ave_data["cource"][cource]["time"]
        except:
            ave_cource = t_time

        result["score"] = ( ave_load - t_time ) + ( ave_cource - t_time )

        return result
