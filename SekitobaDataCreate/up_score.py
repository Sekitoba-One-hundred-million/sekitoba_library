import SekitobaDataManage as dm

dm.dl.file_set( "upscore_regression.pickle" )

class UpScore:
    def __init__( self ):
        regression = dm.dl.data_get( "upscore_regression.pickle" )
        self.a = regression["a"]
        self.b = regression["b"]

    def score_get( self, pd ):
        up_list = pd.up_list()
        pace_list = pd.pace_list()
        day_list = pd.past_day_list()
        score = 0
        count = 0
        
        for i in range( 0, len( up_list ) ):
            p = pace_list[i][0] - pace_list[i][1]
            up = up_list[i]
            s = self.a * p + self.b
            score += up - s
            count += 1

        if count == 0:
            return -1

        score /= count

        return score
        
