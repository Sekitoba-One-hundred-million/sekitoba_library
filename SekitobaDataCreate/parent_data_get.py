import SekitobaLibrary as lib

def main( horce_data, parent_id, baba_index ):
    result = {}
    result["rank"] = 0
    result["two_rate"] = 0
    result["three_rate"] = 0
    result["average_speed"] = 0
    result["limb"] = 0
    result["speed_index"] = -100
    result["up_speed_index"] = -100
    result["pace_speed_index"] = -100

    try:
        parent_data = horce_data[parent_id]
    except:
        return result

    parent_pd = lib.PastData( parent_data, [] )
    
    try:
        speed, up_speed, pace_speed = parent_pd.speedIndex( baba_index[parent_id] )
    except:
        speed = []
        up_speed = []
        pace_speed = []
        
    result["rank"] = parent_pd.rank()
    result["two_rate"] = parent_pd.twoRate()
    result["three_rate"] = parent_pd.threeRate()
    result["average_speed"] = parent_pd.average_speed()
    result["speed_index"] = lib.maxCheck( speed )
    result["up_speed_index"] = lib.maxCheck( up_speed )
    result["pace_speed_index"] = lib.maxCheck( pace_speed )

    try:
        result["limb"] = lib.limbSearch( parent_pd )
    except:
        return result

    return result

        
