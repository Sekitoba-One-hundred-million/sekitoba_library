import sekitoba_library.feature_value as fv
import sekitoba_library.current_race_data as crd
import sekitoba_library.lib as lib
import sekitoba_library.current_race_data as crd
import sekitoba_data_manage as dm

dm.dl.file_set( "dist_index.txt" )
dm.dl.file_set( "standard_time.pickle" )
dm.dl.file_set( "up_average.pickle" )
dm.dl.file_set( "up_pace_regressin.pickle" )

class past_data():

    def __init__( self, past_data, current_data ):
        self.past_data = past_data
        self.cd = crd.current_data( current_data )
        self.base_loaf_weight = 55
        self.dist_index = dm.dl.data_get( "dist_index.txt" )
        self.standard_time = dm.dl.data_get( "standard_time.pickle" )
        self.up_standard_time = dm.dl.data_get( "up_average.pickle" )
        self.regressin_data = dm.dl.data_get( "up_pace_regressin.pickle" )

    def diff_get( self ):
        try:
            return fv.data_check( self.past_data[0][16] )
        except:
            return 0

    def rank( self ):
        try:
            return fv.data_check( self.past_data[0][10] )
        except:
            return 0

    def rank_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            result.append( past_cd.rank() )

        return result

    def all_horce_num_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            
            if not past_cd.race_check():
                continue
            
            result.append( past_cd.all_horce_num() )

        return result
        
    def past_day_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            result.append( past_cd.birthday() )

        return result
    
    #過去3レースの平均順位(3レース以下の場合あり)
    def three_average( self ):
        rank = 0.0
        count = min( len( self.past_data ), 3 )

        for i in range( 0, count ):
            past_cd = crd.current_data( self.past_data[i] )
            rank += fv.data_check( past_cd.rank() )

        if not count == 0:
            rank /= count
            
        return rank

    def three_difference( self ):
        diff = 0.0
        count = min( len( self.past_data ), 3 )

        for i in range( 0, count ):
            past_cd = crd.current_data( self.past_data[i] )
            diff = past_cd.rank() * past_cd.diff()
            
        if not count == 0:
            diff /= count

        return diff
            
    #過去同じ距離の種類での平均順位(1つもなかったら0)
    def dist_rank_average( self, d_kind = None ):
        rank = 0.0
        count = 0.0

        if d_kind == None:
            d_kind = self.cd.dist_kind()

        if not d_kind == 0:
            for i in range( 0, len( self.past_data ) ):
                past_cd = crd.current_data( self.past_data[i] )
                d = past_cd.dist_kind()

                if d_kind == d:
                    rank += past_cd.rank()
                    count += 1

            if not count == 0:
                rank = rank / count

        return rank

    def racekind_rank_average( self, r_kind = None  ):
        rank = 0.0
        count = 0.0

        if r_kind == None:
            r_kind = self.cd.race_kind()

        if not r_kind == 0:
            for i in range( 0, len( self.past_data ) ):
                past_cd = crd.current_data( self.past_data[i] )
                r = past_cd.race_kind()

                if r_kind == r:
                    rank += past_cd.rank()
                    count += 1

            if not count == 0:
                rank = rank / count

        return rank

    #過去同じ馬場状態での平均順位(1つもなかったら0)
    def baba_rank_average( self, baba = None ):
        rank = 0.0
        count = 0.0

        if baba == None:
            baba = self.cd.baba_status()

        if not baba == 0:
            for i in range( 0, len( self.past_data ) ):
                past_cd = crd.current_data( self.past_data[i] )
                b = past_cd.baba_status()

                if baba == b:
                    rank += past_cd.rank()
                    count += 1

            if not count == 0:
                rank = rank / count

        return rank

    #過去同じ騎手での平均順位(1つもなかったら0)
    def jockey_rank_average( self, jockey = None ):
        rank = 0.0
        count = 0.0

        if jockey == None:
            jockey = self.cd.jockey_name_get()

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            j = past_cd.jockey_name_get()
            
            if jockey == j:
                rank += past_cd.rank()
                count += 1
                
        if not count == 0:
            rank = rank / count

        return rank

    #過去同じ天気での平均順位(1つもなかったら0)
    def weather_rank_average( self ):
        rank = 0.0
        count = 0.0
        weather = self.cd.weather()

        if not weather == 0:
            for i in range( 0, len( self.past_data ) ):
                past_cd = crd.current_data( self.past_data[i] )
                w = past_cd.weather()

                if weather == w:
                    rank += fv.data_check( self.past_data[i][10] )
                    count += 1

            if not count == 0:
                rank = rank / count

        return rank

    def three_rate( self ):
        count = 0.0
        rank = 0.0
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            
            if not past_cd.rank() == 0:
                count += 1

                if past_cd.rank() < 4:
                    rank += 1

        if not count == 0:
            rank = rank / count

        return rank

    def two_rate( self ):
        count = 0.0
        rank = 0.0
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            
            if not past_cd.rank() == 0:
                count += 1

                if past_cd.rank() < 3:
                    rank += 1

        if not count == 0:
            rank = rank / count

        return rank

    def one_rate( self ):
        count = 0.0
        rank = 0.0
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            
            if not past_cd.rank() == 0:
                count += 1

                if past_cd.rank() == 1:
                    rank += 1

        if not count == 0:
            rank = rank / count

        return rank

    def get_money( self ):
        money_data = 0
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            
            try:
                money_data += past_cd.money()
            except:
                money_data += 0

        return money_data

    def race_id_get( self ):
        result = []
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.race_id() )

        return result

    def up_list( self ):
        result = []
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            up_time = past_cd.up_time()            
            result.append( up_time )

        return result            
        
    #過去のスペード指数をlistで返す
    def speed_index( self, baba_index_data ):
        speed_index_data = []
        up_speed_index_data = []
        pace_speed_index_data = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            
            if past_cd.race_check():
                kind_num = str( past_cd.race_kind() )
                place_num = str( past_cd.place() )
                race_time = past_cd.race_time()
                up_time = past_cd.up_time()
                dist = str( int( past_cd.dist() * 1000 ) )
                loaf_weight = past_cd.burden_weight()
                key_baba = str( int( past_cd.baba_status() ) )

                if self.standard_time[place_num].get( past_cd.key_dist() ) and \
                   self.dist_index.get( dist ) and \
                   not loaf_weight == 0 and \
                   not race_time == 0:
                    speed_index = ( self.standard_time[place_num][past_cd.key_dist()] - race_time ) * self.dist_index[dist]
                    speed_index += ( loaf_weight - self.base_loaf_weight ) + 80

                    up_speed_index = ( self.up_standard_time[place_num][kind_num][dist]["data"] - up_time ) * self.dist_index[dist]
                    up_speed_index += ( ( loaf_weight - self.base_loaf_weight ) * 2 ) / self.dist_index[dist] + 80

                    pace_speed_index = ( ( self.standard_time[place_num][self.past_data[i][13]] - self.up_standard_time[place_num][kind_num][dist]["data"] ) - ( race_time - up_time ) ) * self.dist_index[dist]
                    pace_speed_index += ( ( loaf_weight - self.base_loaf_weight ) * 2 ) / self.dist_index[dist] + 80
                    
                    try:
                        speed_index += baba_index_data[past_cd.birthday()]
                        up_speed_index += baba_index_data[past_cd.birthday()] / ( self.dist_index[dist] + 1 )
                        pace_speed_index += baba_index_data[past_cd.birthday()] / ( self.dist_index[dist] + 1 )
                    except:
                        speed_index += fv.baba_index( key_baba )
                        up_speed_index += fv.baba_index( key_baba ) / ( self.dist_index[dist] + 1 )
                        pace_speed_index += fv.baba_index( key_baba ) / ( self.dist_index[dist] + 1 )

                    speed_index_data.append( speed_index )
                    up_speed_index_data.append( up_speed_index )
                    pace_speed_index_data.append( pace_speed_index )
                else:
                    speed_index_data.append( -100 )
                    up_speed_index_data.append( -100 )
                    pace_speed_index_data.append( -100 )
            else:
                speed_index_data.append( -100 )
                up_speed_index_data.append( -100 )
                pace_speed_index_data.append( -100 )                

        return speed_index_data, up_speed_index_data, pace_speed_index_data
    
    def best_weight( self, current_weight = None ):
        all_w = 0
        count = 0
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )
            weight = past_cd.weight()

            if weight == 0:
                continue
            
            rank = past_cd.rank()

            if rank == 0:
                continue
            elif rank == 1:
                all_w += weight * 4
                count += 4
            elif rank == 2:
                all_w += weight * 3
                count += 3
            elif rank == 3:
                all_w += weight * 2
                count += 2
            else:
                all_w += weight
                count += 1

        try:
            result = all_w / count
        except:
            result = -1

        if current_weight == None:
            current_weight = self.cd.weight()
            
        return abs( result - current_weight )

    def race_interval( self, ymd = None ):
        if not len( self.past_data ) == 0:
            past_cd = crd.current_data( self.past_data[0] )
            p_ymd = past_cd.ymd()
            interval = 0

            if ymd == None:
                ymd = self.cd.ymd()

            if len( p_ymd ) == 3 \
               and len( ymd ) == 3:
                interval += ( float( ymd[0] ) - float( p_ymd[0] ) ) * 365
                interval += ( float( ymd[1] ) - float( p_ymd[1] ) ) * 30
                interval += ( float( ymd[2] ) - float( p_ymd[2] ) )
                interval = int( interval / 7 )

                return interval
            else:
                return 0
        else:
            return 0

    def pace_change( self, pace_change_data ):
        up_change = 50

        if not len( self.past_data ) == 0:
            past_cd = crd.current_data( self.past_data[0] )
            race_time = past_cd.race_time()
            dist = past_cd.dist()
            race_kind = past_cd.race_kind()
            key_place_num = str( int( past_cd.place() ) )
            key_race_kind = str( int ( race_kind ) )
            key_dist = str( int( dist * 1000 ) )
            up_time = past_cd.up_time()

            if up_time == 0:
                return up_change

            try:
                current_pace_change_data = pace_change_data[key_place_num][key_dist][key_race_kind]
            except:
                return up_change

            up_change = ( ( ( race_time - up_time ) * 0.6 ) / ( dist - 0.6 ) ) / up_time * 100 - 50
            up_change = ( up_change - current_pace_change_data["average"] ) / current_pace_change_data["stde"] * 10 + 50 
        
        return up_change

    def passing_get( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.passing_rank() )

        return result

    def passing_regression( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            passing_rank = past_cd.passing_rank().split( "-" )
            ok = True

            for r in range( 0, len( passing_rank ) ):
                try:
                    passing_rank[r] = float( passing_rank[r] )
                except:
                    ok = False
                    break

            if len( passing_rank ) < 2 or not ok:
                continue
            
            a, _ = lib.regression_line( passing_rank )
            result += a
            count += 1

        if count == 0:
            return 1

        result /= count
        return result

    def first_passing_rank( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            try:
                passing_rank = past_cd.passing_rank()
                first_rank = float( passing_rank.split( "-" )[0] )
            except:
                continue

            result += first_rank
            count += 1

        if not count == 0:
            result /= count

        return result        
    
    def average_speed( self ):
        ave = 0
        count = 0
        
        for i in range( 0, min( len( self.past_data ), 5 ) ):
            past_cd = crd.current_data( self.past_data[0] )
            
            if past_cd.race_check():
                race_time = past_cd.race_time()
                dist = past_cd.dist()

                if not race_time == 0 \
                and not dist == 0:
                    ave += race_time / dist
                    count += 1                    
                
        if not count == 0:
            ave /= count

        return ave

    def best_passing_rank( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            rank = past_cd.rank()
            
            try:
                passing_rank = past_cd.passing_rank()
                first_rank = float( passing_rank.split( "-" )[0] )
            except:
                continue

            n = max( 1, 6 - rank )
            count += n
            result += first_rank * n

        if count == 0:
            return -1

        return result / count
        
    def diff_pace_time( self ):
        result = -10000
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            pace1, pace2 = past_cd.pace()

            if result == -10000:
                result = 0
            
            result += pace1 - pace2
            count += 1

        if not count == 0:
            result /= count

        return result

    def dist_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.dist() )

        return result

    def time_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.race_time() )

        return result

    def pace_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.pace() )

        return result

    def diff_pace_passing( self ):
        result = -10000
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.current_data( self.past_data[i] )

            if not past_cd.race_check():
                continue

            pace1, pace2 = past_cd.pace()
            diff_pace = pace1 - pace2
            str_passing = past_cd.passing_rank()

            try:
                first_passing_rank = float( str_passing.split( "-" )[0] )
            except:
                continue

            all_horce_num = past_cd.all_horce_num()

            if all_horce_num == 0:
                continue

            if result == -10000:
                result = 0

            result += diff_pace * ( first_passing_rank / all_horce_num )            
            count += 1

        if not count == 0:
            result /= count

        return result

    def pace_up_check( self ):
        result = -100
        
        for i in range( 0, len( self.past_data ) ):
            if len( self.past_data[i] ) == 22:                
                past_cd = crd.current_data( self.past_data[i] )
                dist = past_cd.dist()
                race_kind = past_cd.race_kind()

                if past_cd.race_check() \
                  and not dist == 0 \
                  and not race_kind == 0:
                    pace1, pace2 = past_cd.pace()
                    up_time = past_cd.up_time()
                    key_race_kind = str( int ( race_kind ) )
                    key_dist = str( int( dist * 1000 ) )
                    try:
                        a = self.regressin_data[key_race_kind][key_dist]["a"]
                        b = self.regressin_data[key_race_kind][key_dist]["b"]
                        result = max( ( pace1 - pace2 ) * a + b - up_time, result )
                    except:
                        continue

        return result

    def weather_rank( self, weather_data ):
        result = {}
        result["temperature"] = []
        result["rank"] = []

        for i in range( len( self.past_data ) ):
            if lib.current_check( self.past_data[i] ):
                past_cd = crd.current_data( self.past_data[i] )
                ymd = past_cd.ymd()

                if 2008 < int( ymd[0] ):
                    rank = 0
                    temp = -100
                    
                    try:
                        weather_key = ymd[0] + "/" + str( int( ymd[1] ) ) + "/" + str( int( ymd[2] ) )
                        rank = float( past_cd.rank() / past_cd.all_horce_num() )
                        temp = weather_data[weather_key]["temperature"]
                    except:
                        continue

                    result["rank"].append( rank )
                    result["temperature"].append( temp )

        return result
