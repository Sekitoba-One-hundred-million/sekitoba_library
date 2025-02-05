import SekitobaLibrary as lib
import SekitobaDataManage as dm
from SekitobaPsql.psql_race_data import RaceData

dm.dl.file_set( "wrap_data.pickle" )

AVE = "ave"
MAX = "max"
MIN = "min"
LEADING="leading_power"
LEADING_RATE="leading_power_rate"
PURSUING="pursuing_power"
ENDURANCE="endurance_power"
SUSTAIN="sustain_power"
EXPLOSIVE="explosive_power"

class StrideAblity:
    def __init__( self, race_data: RaceData ):
        self.race_data: RaceData = race_data
        self.wrap_data = dm.dl.data_get( "wrap_data.pickle" )

    def data_check( self, horce_num ):
        if not horce_num in self.race_data.data["first_up3_halon"]:
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

    def ablity_create( self, cd: lib.CurrentData, pd: lib.PastData ):
        result = {}
        analyze_data = {}
        analyze_data[LEADING] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[LEADING_RATE] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[PURSUING] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[ENDURANCE] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[SUSTAIN] = { AVE: -1000, MAX: -1000, MIN: -1000 }
        analyze_data[EXPLOSIVE] = { AVE: -1000, MAX: -1000, MIN: -1000 }

        for data_key in analyze_data.keys():
            for math_key in analyze_data[data_key].keys():
                result[data_key+"_"+math_key] = lib.escapeValue

        race_id = cd.race_id()
        horce_num = str( int( cd.horce_number() ) )

        if not self.data_check( horce_num ):
            return result

        count = 0
        match_count = 0

        for data_key in analyze_data.keys():
            self.data_init( analyze_data[data_key] )

        for past_cd in pd.past_cd_list():
            past_race_id = past_cd.race_id()

            if not past_race_id in self.race_data.data["first_up3_halon"][horce_num]:
                continue

            if not past_race_id in self.wrap_data:
                continue

            try:
                first_three_wrap = sum( lib.one_hundred_pace( self.wrap_data[past_race_id] )[0:6] )
            except:
                continue
                
            race_kind = str( int( past_cd.race_kind() ) )
            dist_kind = str( int( past_cd.dist_kind() ) )
            baba = str( int( past_cd.baba_status() ) )
            
            if not race_kind in self.race_data.data["stride_ablity_analyze"] or \
              not dist_kind in self.race_data.data["stride_ablity_analyze"][race_kind] or \
              not baba in self.race_data.data["stride_ablity_analyze"][race_kind][dist_kind]:
                continue

            instance_data = {}
            first_up3 = self.race_data.data["first_up3_halon"][horce_num][past_race_id]
            race_time = past_cd.race_time()
            final_up3 = past_cd.up_time()
            instance_data[LEADING] = first_up3
            instance_data[LEADING_RATE] = first_up3 / first_three_wrap
            instance_data[PURSUING] = race_time - final_up3
            instance_data[ENDURANCE] = race_time - final_up3 - first_up3
            instance_data[SUSTAIN] = race_time - first_up3
            instance_data[EXPLOSIVE] = first_up3

            for data_key in instance_data.keys():
                self.data_add( analyze_data[data_key], instance_data[data_key] )
            
            count += 1

        if not count == 0:
            for data_key in analyze_data.keys():
                analyze_data[data_key][AVE] /= count

        for data_key in analyze_data.keys():
            for math_key in analyze_data[data_key].keys():
                result[data_key+"_"+math_key] = analyze_data[data_key][math_key]

        return result
