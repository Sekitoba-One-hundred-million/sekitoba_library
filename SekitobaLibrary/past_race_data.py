import SekitobaLibrary.feature_value as fv
import SekitobaLibrary.current_race_data as crd
import SekitobaLibrary.lib as lib
import SekitobaLibrary.current_race_data as crd
import SekitobaDataManage as dm
import SekitobaPsql.psql_race_data as ps

race_money_data = ps.RaceData().get_select_data( "money" )
race_ave_true_skill_data = ps.RaceData().get_select_data( "race_ave_true_skill" )
corner_horce_body_data = ps.RaceData().get_select_data( "corner_horce_body" )
wrap_data = ps.RaceData().get_select_data( "wrap" )

class PastData():
    def __init__( self, past_data,\
                 current_data,\
                 race_data: ps.RaceData ):
        self.past_data = past_data
        self.cd = crd.CurrentData( current_data )
        self.race_data: ps.RaceData = race_data        
        self.base_loaf_weight = 55

    def set_up3_analyze_data( self, up3_analyze ):
        self.race_data.data["up3_analyze"] = up3_analyze
        
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

    def past_cd_list( self ) -> list[ crd.CurrentData ]:
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            result.append( past_cd )

        return result        

    def before_cd( self ) -> crd.CurrentData:
        result = None

        if len( self.past_data ) == 0:
            return result

        for i in range( 0, len( self.past_data ) ):
            cd = crd.CurrentData( self.past_data[i] )

            if cd.race_check():
                result = cd
                break

        return result     

    def rank_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            result.append( past_cd.rank() )

        return result

    def all_horce_numList( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )
            
            if not past_cd.race_check():
                continue
            
            result.append( past_cd.all_horce_num() )

        return result
        
    def past_day_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            result.append( past_cd.birthday() )

        return result
    
    #過去3レースの平均順位(3レース以下の場合あり)
    def three_average( self ):
        rank = 0.0
        count = min( len( self.past_data ), 3 )

        for i in range( 0, count ):
            past_cd = crd.CurrentData( self.past_data[i] )
            rank += fv.data_check( past_cd.rank() )

        if not count == 0:
            rank /= count
            
        return rank

    def three_difference( self ):
        diff = 0.0
        count = min( len( self.past_data ), 3 )

        for i in range( 0, count ):
            past_cd = crd.CurrentData( self.past_data[i] )
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
                past_cd = crd.CurrentData( self.past_data[i] )
                d = past_cd.dist_kind()

                if d_kind == d:
                    rank += past_cd.rank()
                    count += 1

            if not count == 0:
                rank = rank / count

        return rank

    def race_kind_rank_average( self, r_kind = None  ):
        rank = 0.0
        count = 0.0

        if r_kind == None:
            r_kind = self.cd.race_kind()

        if not r_kind == 0:
            for i in range( 0, len( self.past_data ) ):
                past_cd = crd.CurrentData( self.past_data[i] )
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
                past_cd = crd.CurrentData( self.past_data[i] )
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
            past_cd = crd.CurrentData( self.past_data[i] )
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
                past_cd = crd.CurrentData( self.past_data[i] )
                w = past_cd.weather()

                if weather == w:
                    rank += fv.data_check( self.past_data[i][10] )
                    count += 1

            if not count == 0:
                rank = rank / count

        return rank

    #過去同じ競馬場での平均順位(1つもなかったら0)
    def place_rank_average( self ):
        rank = 0.0
        count = 0.0
        place = self.cd.place()

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )
            
            if past_cd.place() == place:
                rank += past_cd.rank()
                count += 1
                
        if not count == 0:
            rank = rank / count

        return rank

    def match_rank( self ):
        baba = self.cd.baba_status()
        dist_kind = fv.dist_check( self.cd.dist() * 1000 )
        place = self.cd.place()
        rank = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            c = 0

            if baba == past_cd.baba_status():
                c += 1

            if dist_kind == fv.dist_check( past_cd.dist() * 1000 ):
                c += 1

            if place == past_cd.place():
                c += 1

            rank += past_cd.rank() * c
            count += c

        if not count == 0:
            rank /= count

        return rank

    def match_up3( self ):
        baba = self.cd.baba_status()
        dist_kind = fv.dist_check( self.cd.dist() * 1000 )
        place = self.cd.place()
        up3 = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            c = 0

            if baba == past_cd.baba_status():
                c += 1

            if dist_kind == fv.dist_check( past_cd.dist() * 1000 ):
                c += 1

            if place == past_cd.place():
                c += 1

            up3 += past_cd.up_time() * c
            count += c

        if not count == 0:
            up3 /= count

        return up3

    def max_up3( self ):
        up3 = -1

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            up3 = max( past_cd.up_time(), up3 )

        return up3

    def min_up3( self ):
        up3 = 1000

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            up3 = min( past_cd.up_time(), up3 )

        return up3

    def dist_kind_count( self, dist_kind = None ):
        count = 0
        
        if dist_kind == None:
            dist_kind = fv.dist_check( self.cd.dist() * 1000 )
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if dist_kind == fv.dist_check( past_cd.dist() * 1000 ):
                count += 1

        return count

    def three_rate( self ):
        count = 0.0
        rank = 0.0
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )
            
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
            past_cd = crd.CurrentData( self.past_data[i] )
            
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
            past_cd = crd.CurrentData( self.past_data[i] )
            
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
            past_cd = crd.CurrentData( self.past_data[i] )
            
            try:
                money_data += past_cd.money()
            except:
                money_data += 0

        return money_data

    def race_id_get( self ):
        result = []
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.race_id() )

        return result

    def up_list( self ):
        result = []
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            up_time = past_cd.up_time()            
            result.append( up_time )

        return result            

    def max_time_point( self, race_time_analyze_data ):
        max_time_point = -1000

        for i in range( 0, min( len( self.past_data ), 5 ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if past_cd.race_check():
                key_place_num = str( past_cd.place() )
                race_time = past_cd.race_time()
                key_dist = str( int( past_cd.dist() * 1000 ) )

                if key_place_num in race_time_analyze_data and \
                  key_dist in race_time_analyze_data[key_place_num] and \
                   not race_time == 0:
                    time_point = ( race_time_analyze_data[key_place_num][key_dist]["ave"] - race_time ) / race_time_analyze_data[key_place_num][key_dist]["conv"]
                    time_point = max( time_point * 10 + 50, 0 )
                    max_time_point = max( max_time_point, time_point )

        return max_time_point

    def max_up3TimePoint( self, key_limb ):
        max_time_point = -1000
        race_id = self.cd.race_id()

        for i in range( 0, min( len( self.past_data ), 5 ) ):
            past_cd = crd.CurrentData( self.past_data[i] )
            
            if past_cd.race_check():
                key_place_num = str( int( past_cd.place() ) )
                key_kind = str( int( past_cd.race_kind() ) )
                key_dist_kind = str( int( past_cd.dist_kind() ) )
                up_time = past_cd.up_time()

                if key_place_num in self.race_data.data["up3_analyze"] and \
                  key_kind in self.race_data.data["up3_analyze"][key_place_num] and \
                  key_dist_kind in self.race_data.data["up3_analyze"][key_place_num][key_kind] and \
                  key_limb in self.race_data.data["up3_analyze"][key_place_num][key_kind][key_dist_kind]:
                    time_point = 0
                    
                    try:
                        time_point = \
                        ( self.race_data.data["up3_analyze"][key_place_num][key_kind][key_dist_kind][key_limb]["ave"] - up_time ) \
                        / self.race_data.data["up3_analyze"][key_place_num][key_kind][key_dist_kind][key_limb]["conv"]
                    except:
                        pass
                    
                    time_point = max( time_point * 10 + 50, 0 )
                    max_time_point = max( max_time_point, time_point )

        return max_time_point

    #過去のスペード指数をlistで返す
    def speed_index( self, baba_index_data ):
        speed_index_data = []
        up_speed_index_data = []
        pace_speed_index_data = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )
            
            if past_cd.race_check():
                kind_num = str( past_cd.race_kind() )
                place_num = str( past_cd.place() )
                race_time = past_cd.race_time()
                up_time = past_cd.up_time()
                dist = str( int( past_cd.dist() * 1000 ) )
                loaf_weight = past_cd.burden_weight()
                key_baba = str( int( past_cd.baba_status() ) )
                speed_index = -100
                up_speed_index = -100
                pace_speed_index = -100

                try:
                    speed_index = ( self.race_data.data["standard_time"][place_num][dist][kind_num][key_baba] - \
                                   race_time ) * self.race_data.data["dist_index"][dist]
                    speed_index += ( loaf_weight - self.base_loaf_weight ) + 80
                except:
                    pass

                try:
                    up_speed_index = ( self.race_data.data["up3_standard_time"][place_num][dist][kind_num][key_baba] - \
                                      up_time ) * self.race_data.data["dist_index"][dist]
                    up_speed_index += ( ( loaf_weight - self.base_loaf_weight ) * 2 ) / \
                      self.race_data.data["dist_index"][dist] + 80
                except:
                    pass

                try:
                    pace_speed_index = ( ( self.race_data.data["standard_time"][place_num][dist][kind_num][key_baba] - \
                                          self.race_data.data["up3_standard_time"][place_num][dist][kind_num][key_baba] ) - \
                                        ( race_time - up_time ) ) * self.race_data.data["dist_index"][dist]
                    pace_speed_index += ( ( loaf_weight - self.base_loaf_weight ) * 2 ) / \
                      self.race_data.data["dist_index"][dist] + 80
                except:
                    pass
                    

                try:
                    speed_index += baba_index_data[past_cd.birthday()]
                    up_speed_index += baba_index_data[past_cd.birthday()] / ( self.race_data.data["dist_index"][dist] + 1 )
                    pace_speed_index += baba_index_data[past_cd.birthday()] / ( self.race_data.data["dist_index"][dist] + 1 )
                except:
                    speed_index += fv.baba_index( key_baba )
                    up_speed_index += fv.baba_index( key_baba ) / ( self.race_data.data["dist_index"][dist] + 1 )
                    pace_speed_index += fv.baba_index( key_baba ) / ( self.race_data.data["dist_index"][dist] + 1 )

                speed_index_data.append( speed_index )
                up_speed_index_data.append( up_speed_index )
                pace_speed_index_data.append( pace_speed_index )

        return speed_index_data, up_speed_index_data, pace_speed_index_data
    
    def best_weight( self, current_weight = None ):
        all_w = 0
        count = 0
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )
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
            past_cd = crd.CurrentData( self.past_data[0] )
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
            past_cd = crd.CurrentData( self.past_data[0] )
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
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.passing_rank() )

        return result

    def passing_regression( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

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
            past_cd = crd.CurrentData( self.past_data[i] )

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

    def last_passing_rank( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            try:
                passing_rank = past_cd.passing_rank()
                last_rank = float( passing_rank.split( "-" )[-1] )
            except:
                continue

            result += last_rank
            count += 1

        if not count == 0:
            result /= count

        return result        

    def average_speed( self ):
        ave = 0
        count = 0
        
        for i in range( 0, min( len( self.past_data ), 5 ) ):
            past_cd = crd.CurrentData( self.past_data[0] )
            
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

    def best_first_passing_rank( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

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

    def best_second_passing_rank( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue
            
            rank = past_cd.rank()
            
            try:
                passing_rank = past_cd.passing_rank()
                second_rank = float( passing_rank.split( "-" )[1] )
            except:
                continue

            n = max( 1, 6 - rank )
            count += n
            result += second_rank * n

        if count == 0:
            return -1

        return result / count

    def diff_pace_time( self ):
        result = -10000
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

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
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.dist() )

        return result

    def time_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.race_time() )

        return result

    def pace_list( self ):
        result = []

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue

            result.append( past_cd.pace() )

        return result

    def diff_pace_first_passing( self ):
        result = -10000
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

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

    def pace_up_check( self, regressin_data ):
        result = -100
        
        for i in range( 0, len( self.past_data ) ):
            if len( self.past_data[i] ) == 22:                
                past_cd = crd.CurrentData( self.past_data[i] )
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
                        a = regressin_data[key_race_kind][key_dist]["a"]
                        b = regressin_data[key_race_kind][key_dist]["b"]
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
                past_cd = crd.CurrentData( self.past_data[i] )
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

    def before_continue_not_three_rank( self ):
        result = -1000
        
        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue

            if result == -1000:
                result = 0

            if 3 < past_cd.rank():
                result += 1
            else:
                 break

        return result

    def corner_diff_rank( self ):
        result = 0
        count = 0

        for i in range( 0, len( self.past_data ) ):
            past_cd = crd.CurrentData( self.past_data[i] )

            if not past_cd.race_check():
                continue

            passing_rank = past_cd.passing_rank()
            split_passing_rank = passing_rank.split( "-" )

            if len( split_passing_rank ) < 2:
                continue

            three_corner = int( split_passing_rank[-2] )
            four_corner = int( split_passing_rank[-1] )

            count += 1
            result += three_corner - four_corner

        if count == 0:
            result = 1000
        else:
            result /= count

        return result

    def first_result_rank_diff( self ):
        count = 0
        result = 0
        
        for past_cd in self.past_cd_list():
            if not past_cd.race_check():
                continue

            diff_rank = past_cd.first_result_diff()

            if diff_rank == -1000:
                continue

            result += diff_rank
            count += 1

        if not count == 0:
            result /= count

        return result

    def last_result_rank_diff( self ):
        count = 0
        result = 0
        
        for past_cd in self.past_cd_list():
            if not past_cd.race_check():
                continue

            diff_rank = past_cd.last_result_diff()

            if diff_rank == -1000:
                continue

            result += diff_rank
            count += 1

        if not count == 0:
            result /= count

        return result
    
    def pace_up_rate( self ):
        pace_up_rate_list = []
        
        for past_cd in self.past_cd_list():
            if not past_cd.race_check():
                continue

            past_race_id = past_cd.race_id()

            if not past_race_id in wrap_data or len( wrap_data[past_race_id]["wrap"] ) == 0:
                continue

            one_hudred_wrap = lib.one_hundred_pace( wrap_data[past_race_id]["wrap"] )
            last_up3 = sum( one_hudred_wrap[int(len(one_hudred_wrap)-6):len(one_hudred_wrap)] )
            
            if last_up3 <= 0:
                continue

            pace_up_rate_list.append( past_cd.up_time() / last_up3 )

        result = {}
        result["ave"] = lib.average( pace_up_rate_list )
        result["conv"] = lib.conv( pace_up_rate_list )
        result["max"] = lib.max_check( pace_up_rate_list )
        result["min"] = lib.minCheck( pace_up_rate_list )

        return result

    def up_rate( self, race_money_rank, up_kind_ave_data ):
        PLACE_DIST = "place_dist"
        BABA = "baba"
        MONEY = "money"
        race_id = self.cd.race_id()

        if not MONEY in up_kind_ave_data or \
          not race_money_rank in up_kind_ave_data[MONEY]:
            return -1000

        race_money_up = up_kind_ave_data[MONEY][race_money_rank]
        result = 0
        count = 0
        
        for past_cd in self.past_cd_list():
            if not past_cd.race_check():
                continue
                
            baba = str( int( past_cd.baba_status() ) )
            dist = str( int( past_cd.dist() * 1000 ) )
            place = str( int( past_cd.place() ) )

            if not baba in up_kind_ave_data[BABA]:
                continue

            if not place in up_kind_ave_data[PLACE_DIST] or not dist in up_kind_ave_data[PLACE_DIST][place]:
                continue

            up_time = past_cd.up_time()

            if up_time == 0:
                continue
                
            baba_up = up_kind_ave_data[BABA][baba]
            place_dist_up = up_kind_ave_data[PLACE_DIST][place][dist]
            up_score = ( race_money_up / up_time )
            up_score += ( baba_up / up_time )
            up_score += ( place_dist_up / up_time )
            up_score /= len( up_kind_ave_data.keys() )
            result += up_score
            count += 1

        if count == 0:
            result = -1000
        else:
            result /= count

        return result

    def level_score( self, money_class_true_skill_data ):
        c = 0
        score = 0
        
        for past_cd in self.past_cd_list():
            past_race_id = past_cd.race_id()

            if not past_race_id in race_ave_true_skill_data:
                continue
            
            if not past_race_id in race_money_data:
                continue
            
            past_rank = past_cd.rank()
            
            if past_rank == 0:
                continue

            key_past_money_class = str( int( fv.money_class_get( race_money_data[past_race_id]["money"] ) ) )
            past_race_true_skill = race_ave_true_skill_data[past_race_id]["race_ave_true_skill"]
            score_rate = past_race_true_skill / money_class_true_skill_data[key_past_money_class]
            rank_score = ( 1 / past_rank )
            rank_score *= score_rate
            score += rank_score
            c += 1
            
        if c == 0:
            score = -1
        else:
            score /= c

        return score

    def level_up3( self, money_class_true_skill_data ):
        c = 0
        score = 0
        
        for past_cd in self.past_cd_list():
            past_race_id = past_cd.race_id()

            if not past_race_id in race_ave_true_skill_data:
                continue
            
            if not past_race_id in race_money_data:
                continue
            
            past_up3 = past_cd.up_time()
            
            if past_up3 == 0:
                continue

            key_past_money_class = str( int( fv.money_class_get( race_money_data[past_race_id]["money"] ) ) )
            past_race_true_skill = race_ave_true_skill_data[past_race_id]["race_ave_true_skill"]
            score_rate = past_race_true_skill / money_class_true_skill_data[key_past_money_class]
            up3_score = ( 1 / past_up3 ) * score_rate
            score += up3_score
            c += 1
            
        if c == 0:
            score = -1
        else:
            score /= c

        return score

    def ave_odds( self ):
        ave_odds = 0
        count = 0
        
        for past_cd in self.past_cd_list():
            ave_odds += past_cd.odds()
            count += 1

        if count == 0:
            return -1
        
        return ave_odds / count

    def ave_three_odds( self ):
        ave_odds = 0
        count = 0
        
        for past_cd in self.past_cd_list():
            ave_odds += past_cd.odds()
            count += 1

            if count == 3:
                break

        if count == 0:
            return -1
        
        return ave_odds / count

    def ave_first_last_diff( self ):
        ave_diff = 0
        count = 0
        
        for past_cd in self.past_cd_list():
            ave_diff += past_cd.first_last_diff()
            count += 1

        if not count == 0:
            ave_diff /= count

        return ave_diff

    def past_first_horce_body_list( self ):
        result = []

        for past_cd in  self.past_cd_list():
            past_race_id = past_cd.race_id()
            past_key_horce_num = str( int( past_cd.horce_number() ) )

            if past_race_id in corner_horce_body_data and \
              not len( corner_horce_body_data[past_race_id]["corner_horce_body"] ) == 0:
                past_min_corner_key = min( corner_horce_body_data[past_race_id]["corner_horce_body"] )

                if past_key_horce_num in corner_horce_body_data[past_race_id]["corner_horce_body"][past_min_corner_key]:
                    result.append( corner_horce_body_data[past_race_id]["corner_horce_body"][past_min_corner_key][past_key_horce_num] )

        return result

    def past_last_horce_body_list( self ):
        result = []

        for past_cd in  self.past_cd_list():
            past_race_id = past_cd.race_id()
            past_key_horce_num = str( int( past_cd.horce_number() ) )

            if past_race_id in corner_horce_body_data and \
              not len( corner_horce_body_data[past_race_id]["corner_horce_body"] ) == 0:
                past_max_corner_key = max( corner_horce_body_data[past_race_id]["corner_horce_body"] )

                if past_key_horce_num in corner_horce_body_data[past_race_id]["corner_horce_body"][past_max_corner_key]:
                    result.append( corner_horce_body_data[past_race_id]["corner_horce_body"][past_max_corner_key][past_key_horce_num] )

        return result

    def stamina_create( self, key_limb ):
        count = 0
        ave_stamina = 0

        for past_cd in self.past_cd_list():
            past_race_id = past_cd.race_id()

            if not past_race_id in wrap_data:
                continue

            if not type( wrap_data[past_race_id]["wrap"] ) == dict \
              or len( wrap_data[past_race_id]["wrap"] ) == 0 \
              or past_cd.up_time() == 0:
                continue
            
            if not past_race_id in corner_horce_body_data or len( corner_horce_body_data[past_race_id]["corner_horce_body"] ) == 0:
                continue

            ave_horce_body = 0
            horce_body_count = 0
            ave_up3 = -1
            past_corner_horce_body = corner_horce_body_data[past_race_id]["corner_horce_body"]
            key_past_horce_num = str( int( past_cd.horce_number() ) )
            past_key_place = str( int( past_cd.place() ) )
            past_key_kind = str( int( past_cd.race_kind() ) )
            past_key_dist_kind = str( int( past_cd.dist_kind() ) )
            past_key_dist = str( int( past_cd.dist() * 1000 ) )
            past_passing = []
            ave_before_pace = -1

            try:
                ave_before_pace = self.race_data.data["before_pace"][past_key_dist]
            except:
                continue

            try:
                past_passing = past_cd.passing_rank().split( "-" )
            except:
                continue
                
            try:
                ave_up3 = self.race_data.data["up3_analyze"][past_key_place][past_key_kind][past_key_dist_kind][key_limb]["ave"]
            except:
                continue

            for conrner_key in past_corner_horce_body.keys():
                try:
                    ave_horce_body += past_corner_horce_body[conrner_key][key_past_horce_num]
                    horce_body_count += 1
                except:
                    continue

            if horce_body_count == 0:
                continue

            ave_horce_body /= horce_body_count
            diff_time = ave_horce_body * 0.17

            before_pace, _ = lib.before_after_pace( wrap_data[past_race_id]["wrap"] )
            pace_rate = ave_before_pace / ( before_pace + diff_time )
            up3_rate = ave_up3 / past_cd.up_time()
            stamina = up3_rate + pace_rate
            ave_stamina += stamina
            count += 1

        if count == 0:
            return -1000

        ave_stamina /= count

        return ave_stamina

    def best_dist( self ):
        score = 0
        data = 0
        count = 0
        cd_dist = self.cd.dist() * 1000

        for past_cd in self.past_cd_list():
            if not past_cd.race_check():
                continue

            past_rank = past_cd.rank()
            c = 1

            if past_rank == 1:
                c = 5
            elif past_rank == 2:
                c = 4
            elif past_rank == 3:
                c = 3
            elif past_rank <= 5:
                c = 2
                
            data += past_cd.dist() * 1000 * c
            count += c

        if count == 0:
            return -1000

        score = abs( data - cd_dist ) / count

        return score
