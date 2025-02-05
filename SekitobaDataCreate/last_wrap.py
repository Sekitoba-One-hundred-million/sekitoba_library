import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

dm.dl.file_set( "wrap_data.pickle" )
dm.dl.file_set( "race_cource_info.pickle" )

MIN_LAST_WRAP = "min_last_wrap"
MAX_LAST_WRAP = "max_last_wrap"
AVE_LAST_WRAP = "ave_last_wrap"
STD_LAST_WRAP = "std_last_wrap"

class LastWrap:
    def __init__( self, race_data: ps.RaceData, horce_data: ps.HorceData, race_horce_data: ps.RaceHorceData ):
        self.race_data: ps.RaceData = race_data
        self.horce_data: ps.HorceData = horce_data
        self.race_horce_data: ps.RaceHorceData = race_horce_data
        self.key_list = [ MIN_LAST_WRAP, MAX_LAST_WRAP, AVE_LAST_WRAP, STD_LAST_WRAP ]
        self.horce_wrap_score = {}
        self.race_cource_info = dm.dl.data_get( "race_cource_info.pickle" )
        self.wrap_data = dm.dl.data_get( "wrap_data.pickle" )

    def one_hundred_wrap( self, wrap_data ):
        wrap_list = []
        
        if len( wrap_data ) == 0:
            return wrap_list
            
        ave_wrap = 0
        all_wrap = 0

        for key in wrap_data.keys():
            wrap = wrap_data[key]
    
            if key == '100':
                wrap *= 2

            ave_wrap += wrap
            all_wrap += wrap
            
        ave_wrap /= len( wrap_data )
        before_wrap = ave_wrap
        w = 0

        for key in wrap_data.keys():
            if key == '100':
                wrap_list.append( wrap_data[key] )
                before_wrap = wrap_data[key] * 2
                continue

            current_wrap = wrap_data[key]
            a = ( before_wrap - current_wrap ) / -200
            b = before_wrap
            middle_wrap = a * 100 + b
            wrap_list.append( middle_wrap / 2 )
            wrap_list.append( current_wrap / 2 )
            before_wrap = current_wrap

        return wrap_list

    def create_score( self):
        ymd = { "year": self.race_data.data["year"], \
               "month": self.race_data.data["month"], \
               "day": self.race_data.data["day"] }

        key_place = str( self.race_data.data["place"] )
        key_kind = str( self.race_data.data["kind"] )
        key_dist = str( self.race_data.data["dist"] )

        if self.race_data.data["out_side"]:
            key_dist += "外"

        #try:
        #    four_corner_dist = self.race_cource_info[key_place][key_kind][key_dist]["dist"][-1] + self.race_cource_info[key_place][key_kind][key_dist]["dist"][-2]
        #except:
        #    return
            
        #dist_one_index = int( ( self.race_data.data["dist"] - four_corner_dist ) / 100 )
        #dist_two_index = int( ( self.race_data.data["dist"] - four_corner_dist + 100 ) / 100 )

        #a = ( sum( wrap_list[0:dist_one_index] ) - sum( wrap_list[0:dist_two_index] ) ) / ( dist_one_index * 100 - dist_two_index * 100 )
        #b = sum( wrap_list[0:dist_one_index] ) - a * ( dist_one_index * 100 )
        #four_corner_to_goal_time = a * four_corner_dist + b
        #race_time = 100000

        for horce_id in self.race_horce_data.horce_id_list:
            current_data = []
            past_data = []

            if horce_id in self.horce_data.data:
                current_data, past_data = lib.race_check( self.horce_data.data[horce_id]["past_data"], ymd )
                
            cd = lib.CurrentData( current_data )
            pd = lib.PastData( past_data, current_data, self.race_data )
            self.horce_wrap_score[horce_id] = {}

            for key in self.key_list:
                self.horce_wrap_score[horce_id][key] = -1000

            if not cd.race_check():
                continue

            past_horce_last_wrap = []

            for past_cd in pd.past_cd_list():
                past_race_id = past_cd.race_id()
                #race_time = min( race_time, past_cd.race_time() )

                if not past_race_id in self.wrap_data:
                    continue

                wrap_list = self.one_hundred_wrap( self.wrap_data[past_race_id] )
                last_three_wrap = wrap_list[int(len(wrap_list)-6):len(wrap_list)]
                race_up3 = sum( last_three_wrap )
                horce_wrap = []

                for i in range( 0, len( last_three_wrap ) ):
                    horce_wrap.append( last_three_wrap[i] * ( past_cd.up_time() / race_up3 ) )

                if len( horce_wrap ) == 0:
                    continue
                
                past_horce_last_wrap.append( sum( horce_wrap[len(horce_wrap)-2:len(horce_wrap)] ) )

            self.horce_wrap_score[horce_id][MIN_LAST_WRAP] = lib.minCheck( past_horce_last_wrap )
            self.horce_wrap_score[horce_id][MAX_LAST_WRAP] = lib.max_check( past_horce_last_wrap )
            self.horce_wrap_score[horce_id][AVE_LAST_WRAP] = lib.average( past_horce_last_wrap )
            self.horce_wrap_score[horce_id][STD_LAST_WRAP] = lib.stdev( past_horce_last_wrap )

        #for horce_id in self.race_horce_data.horce_id_list:
        #    current_data, past_data = lib.race_check( self.horce_data.data[horce_id]["past_data"], ymd )
        #    cd = lib.CurrentData( current_data )

        #    if not cd.race_check():
        #        continue
            
        #    key_horce_num = str( int( cd.horce_number() ) )
        #    self.horce_four_corner_to_goal_time[horce_id] = four_corner_to_goal_time + ( cd.race_time() - race_time )
