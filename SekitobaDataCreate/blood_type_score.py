import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

from SekitobaDataCreate.get_horce_data import GetHorceData

class BloodTypeScore:
    def __init__( self, race_data: ps.RaceData, horce_data: ps.HorceData ):
        self.COLUM_NAME = "blood_type_score"
        self.race_data = race_data
        self.horce_data = horce_data

    def score_get( self, horce_id, cd: lib.CurrentData, pd: lib.PastData, getHorceData: GetHorceData, sex = lib.escapeValue ):
        result = lib.escapeValue
        blood_type_score_data: dict = self.race_data.data[self.COLUM_NAME]

        if len( blood_type_score_data ) == 0:
            return result
        
        horce_birth_day = int( horce_id[0:4] )
        key_sex = ""
        
        if sex == lib.escapeValue:
            key_sex = str( int( self.horce_data.data[horce_id]["sex"] ) )
        else:
            key_sex = str( int( sex ) )
            
        key_age = str( int( int( self.race_data.data["year"] ) - horce_birth_day ) )
        key_interval = str( int( min( pd.race_interval(), 10 ) ) )
        key_limb = str( int( getHorceData.limb_math ) )
        key_dist = str( self.race_data.data["dist"] )
        key_horce_num = str( int( cd.horce_number() ) )

        try:
            parent_blood_type: dict = self.race_data.data["blood_type"][key_horce_num]
        except:
            return result
            
        result = 0            
        key_data = { "dist": key_dist,
                     "age": key_age,
                     "interval": key_interval,
                     "limb": key_limb,
                     "sex": key_sex }

        for name in blood_type_score_data.keys():
            key_value = key_data[name]

            for blood_type in parent_blood_type.values():
                try:
                    result += blood_type_score_data[name][key_value][str(blood_type)]
                except:
                    continue

        return result
