import SekitobaDataManage as dm

dm.dl.file_set( "pace_time_score_regression.pickle" )

class PaceTimeScore:
    def __init__( self ):
        regression = dm.dl.data_get( "pace_time_score_regression.pickle" )
        self.a = regression["a"]
        self.b = regression["b"]
        self.aa = regression["aa"]
        self.bb = regression["bb"]
        self.cc = regression["cc"]


    def score_get( self, pd ):
        pace_list = pd.pace_list()
        time_list = pd.time_list()
        dist_list = pd.dist_list()        
        score = 0
        count = 0
            
        for i in range( 0, len( pace_list ) ):
            p = pace_list[i][0] - pace_list[i][1]

            if p <= 0:
                s = self.a * p + self.b
            else:
                s = self.aa * pow( p, 2 ) + self.bb * p + self.cc

            t = time_list[i] / ( dist_list[i] * 10 )            
            score += t - s
            count += 1

        if count == 0:
            return -1

        score /= count

        return score
        
