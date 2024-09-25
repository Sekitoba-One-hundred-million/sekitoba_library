import math

import SekitobaLibrary as lib
import SekitobaDataManage as dm

dm.dl.file_set( "train_time_data.pickle" )
dm.dl.file_set( "train_ave_data.pickle" )
dm.dl.file_set( "train_ave_key_data.pickle" )

class TrainIndexGet:
    def __init__( self ):
        self.train_time_data = dm.dl.data_get( "train_time_data.pickle" )
        self.train_ave_data = dm.dl.data_get( "train_ave_data.pickle" )
        self.train_ave_key_data = dm.dl.data_get( "train_ave_key_data.pickle" )

    def data_check( self, race_id, horce_num ):
        key_horce_num = str( int( horce_num ) )

        try:
            load = self.train_time_data[race_id][key_horce_num]["load"]
            cource = self.train_time_data[race_id][key_horce_num]["cource"] 
            t_time = self.train_time_data[race_id][key_horce_num]["time"]
            wrap = self.train_time_data[race_id][key_horce_num]["wrap"]
        except:
            return None

        if len( t_time ) == 0 or len( wrap ) == 0:
            return None

        if not len( cource ) == 2:
            return None

        return { "load": load, "cource": cource, "t_time": t_time, "wrap": wrap }

    def train_time_rate( self, race_id, horce_num ):
        score = 100

        train_data = self.data_check( race_id, horce_num )

        if train_data == None:
            return score
        
        load = train_data["load"]
        cource = train_data["cource"]
        t_time = train_data["t_time"]
        wrap = train_data["wrap"]

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
            return score

        try:
            base_ave_time = self.train_ave_data[place_key][cource_key][load_key]["time"]
            #ave_wrap = self.train_ave_data[place_key][cource_key][load_key]["wrap"]
        except:
            return score

        train_time = max( t_time )
        score = ( base_ave_time / train_time )

        return score

    def wrap_rate( self, race_id, horce_num ):
        score = 100

        train_data = self.data_check( race_id, horce_num )

        if train_data == None:
            return score
        
        load = train_data["load"]
        cource = train_data["cource"]
        t_time = train_data["t_time"]
        wrap = train_data["wrap"]

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
            return score

        try:
            ave_wrap = self.train_ave_data[place_key][cource_key][load_key]["wrap"]
        except:
            return score

        train_wrap = min( wrap )
        score = ( ave_wrap / train_wrap )

        return score

    def train_time_slope_slice( self, race_id, horce_num ):
        train_data = self.data_check( race_id, horce_num )

        if train_data == None:
            return 100, 100
        
        a, b = lib.regressionLine( train_data["t_time"] )

        return a, b

    def wrap_slope_slice( self, race_id, horce_num ):
        train_data = self.data_check( race_id, horce_num )

        if train_data == None:
            return 100, 100

        a, b = lib.regressionLine( train_data["wrap"] )

        return a, b

    def first_wrap( self, race_id, horce_num ):
        train_data = self.data_check( race_id, horce_num )

        if train_data == None:
            return -1

        return train_data["wrap"][0]

    def final_wrap( self, race_id, horce_num ):
        train_data = self.data_check( race_id, horce_num )

        if train_data == None:
            return -1

        return train_data["wrap"][-1]

    def wrap_std( self, race_id, horce_num ):
        train_data = self.data_check( race_id, horce_num )

        if train_data == None:
            return -1

        score = 0
        wrap = train_data["wrap"]
        ave_wrap = sum( wrap ) / len( wrap )

        for w in wrap:
            score += math.pow( ave_wrap - w , 2 )

        score /= len( wrap )
        return score

    def score_get( self, race_id, horce_num ):
        score = 0
        first_wrap = self.first_wrap( race_id, horce_num )
        final_wrap = self.final_wrap( race_id, horce_num )
        wrap_a, b = self.wrap_slope_slice( race_id, horce_num )
        train_a, b = self.train_time_slope_slice( race_id, horce_num )
        score = ( first_wrap - final_wrap ) * wrap_a
        return score
