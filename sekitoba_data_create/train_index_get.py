import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "train_time_data.pickle" )
dm.dl.file_set( "train_ave_data.pickle" )
dm.dl.file_set( "train_ave_key_data.pickle" )

class TrainIndexGet:
    def __init__( self ):
        self.train_time_data = dm.dl.data_get( "train_time_data.pickle" )
        self.train_ave_data = dm.dl.data_get( "train_ave_data.pickle" )
        self.train_ave_key_data = dm.dl.data_get( "train_ave_key_data.pickle" )
        self.base_time = self.train_ave_data["美"]["坂"]["馬也"]["time"]
        self.base_wrap = self.train_ave_data["美"]["坂"]["馬也"]["wrap"]

    def score_get( self, race_id, horce_num, prod_train_data = None ):
        result = 100
        key_horce_num = str( int( horce_num ) )

        if dm.dl.prod:
            if not key_horce_num in prod_train_data.keys():
                return result
            
            load = prod_train_data[key_horce_num]["load"]
            cource = prod_train_data[key_horce_num]["cource"] 
            t_time = prod_train_data[key_horce_num]["time"]
            wrap = prod_train_data[key_horce_num]["wrap"]
        else:
            try:
                load = self.train_time_data[race_id][key_horce_num]["load"]
                cource = self.train_time_data[race_id][key_horce_num]["cource"] 
                t_time = self.train_time_data[race_id][key_horce_num]["time"]
                wrap = self.train_time_data[race_id][key_horce_num]["wrap"]
            except:
                return result

        if len( t_time ) == 0 or len( wrap ) == 0:
            return result

        if not len( cource ) == 2:
            return result
        
        place_key = ""
        cource_key = ""
        load_key = ""

        for key in self.train_ave_key_data["place"]:
            if cource[0] in key:
                place_key = key
                break
            
        for key in self.train_ave_key_data["cource"]:
            if cource[1] in key:
                cource_key = key
                break

        for key in self.train_ave_key_data["load"]:
            if load in key:
                load_key = key
                break

        if len( place_key ) == 0 or len( cource_key ) == 0 or len( load_key ) == 0:
            return result

        try:
            ave_time = self.train_ave_data[place_key][cource_key][load_key]["time"]
            ave_wrap = self.train_ave_data[place_key][cource_key][load_key]["wrap"]
        except:
            return result
        
        time_score = ( self.base_time / ave_time )
        wrap_score = ( self.base_wrap / ave_wrap )
        result = wrap_score + time_score

        return result
