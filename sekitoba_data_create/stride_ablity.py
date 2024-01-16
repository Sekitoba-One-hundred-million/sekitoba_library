import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "first_up3_halon.pickle" )
dm.dl.file_set( "stride_ablity_analyze_data.pickle" )

AVE = "ave"
MAX = "max"
MIN = "min"
LEADING="leading_power"
PURSUING="pursuing_power"
ENDURANCE="endurance_power"
SUSTAIN="sustain_power"
EXPLOSIVE="explosive_power"

class StrideAblity:
    def __init__( self ):
        self.first_up3_halon = dm.dl.data_get( "first_up3_halon.pickle" )
        self.stride_ablity_analyze_data = dm.dl.data_get( "stride_ablity_analyze_data.pickle" )

    def set_first_up3_halon( self, first_up3_halon ):
        self.first_up3_halon.update( first_up3_halon )

    def data_check( self, race_id, horce_num ):
        if not race_id in self.first_up3_halon or \
          not horce_num in self.first_up3_halon[race_id]:
            return False

        return True

    def data_init( self, dict_data ):
        dict_data[AVE] = 0
        dict_data[MAX] = -1000
        dict_data[MIN] = 1000

    def data_add( self, dict_data, add_data ):
        dict_data[AVE] += add_data
        dict_data[MAX] = max( dict_data[MAX], add_data )
        dict_data[MIN] = min( dict_data[MIN], add_data )

    def ablity_create( self, cd: lib.current_data, pd: lib.past_data ):
        analyze_data = {}
        analyze_data[LEADING] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[PURSUING] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[ENDURANCE] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[SUSTAIN] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[EXPLOSIVE] = { AVE: -1000, MAX: -1000, MIN: -1000 }

        race_id = cd.race_id()
        horce_num = int( cd.horce_number() )

        if not self.data_check( race_id, horce_num ):
            return analyze_data

        count = 0
        match_count = 0

        for data_key in analyze_data.keys():
            self.data_init( analyze_data[data_key] )

        for past_cd in pd.past_cd_list():
            past_race_id = past_cd.race_id()

            if not past_race_id in self.first_up3_halon[race_id][horce_num]:
                continue

            race_kind = int( past_cd.race_kind() )
            dist_kind = int( past_cd.dist_kind() )
            baba = int( past_cd.baba_status() )

            if not race_kind in self.stride_ablity_analyze_data or \
              not dist_kind in self.stride_ablity_analyze_data[race_kind] or \
              not baba in self.stride_ablity_analyze_data[race_kind][dist_kind]:
                continue

            instance_data = {}
            first_up3 = self.first_up3_halon[race_id][horce_num][past_race_id]
            race_time = past_cd.race_time()
            final_up3 = past_cd.up_time()
            instance_data[LEADING] = first_up3
            instance_data[PURSUING] = race_time - final_up3
            instance_data[ENDURANCE] = race_time - final_up3 - first_up3
            instance_data[SUSTAIN] = race_time - first_up3
            instance_data[EXPLOSIVE] = first_up3

            for data_key in instance_data.keys():
                instance_data[data_key] = \
                  ( ( ( instance_data[data_key] - self.stride_ablity_analyze_data[race_kind][dist_kind][baba][data_key]["ave"] ) * 10 ) \
                   / self.stride_ablity_analyze_data[race_kind][dist_kind][baba][data_key]["conv"] ) + 50
                self.data_add( analyze_data[data_key], instance_data[data_key] )
            
            count += 1

        if not count == 0:
            for data_key in analyze_data.keys():
                analyze_data[data_key][AVE] /= count

        return analyze_data
