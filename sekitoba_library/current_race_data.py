import numpy as np

import sekitoba_library.feature_value as fv

class current_data():

    def __init__( self, data ):
        self.race_data = data

    def place( self ):#場所
        return fv.place_num( self.race_data[1] )

    def all_horce_num( self ):
        return fv.data_check( self.race_data[5] )

    def flame_number( self ):#枠番
        return fv.data_check( self.race_data[6] )

    def horce_number( self ):#馬番
        return fv.data_check( self.race_data[7] )

    def weight( self ):
        split_w = self.race_data[19].split( "(" )
        
        try:
            return float( split_w[0] )
        except:
            return 0
        
        
    def id_weight( self ):#馬体重の増減
        return fv.weight( self.race_data[19] )

    def weather( self ):#天気
        return fv.weather( self.race_data[2] )

    def rank( self ):
        return fv.data_check( self.race_data[10] )
    
    def popular( self ):
        return fv.data_check( self.race_data[9] )

    def race_num( self ):
        return fv.data_check( self.race_data[3] )

    def diff( self ):
        return fv.data_check( self.race_data[16] )

    def odds( self ):
        return fv.data_check( self.race_data[8] )

    def up_time( self ):
        return fv.data_check( self.race_data[18].split( "-" )[0] )

    def money( self ):
        return fv.data_check( self.race_data[20] )

    def pace( self ):
        data = self.race_data[17].split( "-" )

        try:
            return float( data[0] ), float( data[1] )
        except:
            return 0, 0

    def birthday( self ):
        return self.race_data[0]

    def ymd( self ):
        return self.race_data[0].split( "/" )
        
    def year( self ):
        y = self.race_data[0].split( "/" )

        try:
            return int( y[0] )
        except:
            return 0

    def dist( self ):#距離(kmで表す)
        str_d = ""
        d = 0.0

        for i in range( 0, len( self.race_data[13] ) ):
            if str.isdecimal( self.race_data[13][i] ):
                str_d += self.race_data[13][i]

        if not len( str_d ) == 0:
            d = float( str_d ) / 1000
            
        return d

    def key_dist( self ):
        return self.race_data[13]
        
    def baba_status( self ):#馬場状態
        return fv.baba( self.race_data[14] )

    def burden_weight( self ):#斤量
        return fv.data_check( self.race_data[12] )

    def race_kind( self ):
        _, t = fv.dist( self.race_data[13] )
        return t

    def dist_kind( self ):
        d, _ = fv.dist( self.race_data[13] )
        return d

    def answer( self ):
        a = []
        a.append( fv.data_check( self.race_data[10] ) )

        try:
            a.append( float( self.race_data[8] ) )
        except:
            a.append( 0.0 )

        a.append( fv.data_check( self.race_data[9] ) )
        
        return a

    def jockey_name_get( self ):
        return self.race_data[11].replace( " ", "" )
    
    def jockey_data( self, jockey_data_stprage ):
        jockey_name = self.race_data[11]
        y = self.race_data[0].split( "/" )
        year = ""
        before_year = ""

        if not len( y ) == 0:
            year = y[0]

        if str.isdecimal( year ):
            before_year = str( int( year ) - 1 )

        current_jockey = {}

        try:
            current_jockey = jockey_data_stprage[jockey_name]
        except:
            return [ -1, -1, -1, -1, -1 ]

        result = np.zeros( 5 )
        
        try:
            result = np.array( current_jockey[before_year] )
        except:
            return [ 0, 0, 0, 0, 0 ]    

        return result

    def race_time( self ):
        return fv.time( self.race_data[15] ) * 60

    def race_check( self ):
        if not len( self.race_data ) == 22:
            return False
        elif self.place() == 0:
            return False
        elif not self.race_kind() == 1 \
             and not self.race_kind() == 2:
            return False
        elif self.answer()[1] == 0 \
             or self.answer()[0] == 0:
            return False                

        return True
        
    def new_check( self ):
        word = "新馬"
        count = 0
        check = False
        
        for i in range( 0, len( self.race_data[4] ) ):
            if count != 2 \
               and word[count] == self.race_data[4][i]:
                count += 1

        if count == 2:
            check = True
            
        return check
