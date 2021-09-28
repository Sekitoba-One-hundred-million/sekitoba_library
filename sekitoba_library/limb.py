limb_postion = {}
limb_postion["10"] = [ "A", "B", "B", "C", "C", "D", "E", "E", "E", "E" ]
limb_postion["11"] = [ "A", "B", "B", "C", "C", "D", "D", "E", "E", "E", "E" ]
limb_postion["12"] = [ "A", "B", "B", "B", "C", "C", "D", "D", "E", "E", "E", "E" ]
limb_postion["13"] = [ "A", "B", "B", "B", "C", "C", "D", "D", "E", "E", "E", "E", "E" ]
limb_postion["14"] = [ "A", "B", "B", "B", "C", "C", "C", "D", "D", "E", "E", "E", "E", "E" ]
limb_postion["15"] = [ "A", "B", "B", "B", "B", "C", "C", "D", "D", "D", "E", "E", "E", "E", "E" ]
limb_postion["16"] = [ "A", "B", "B", "B", "B", "C", "C", "C", "D", "D", "E", "E", "E", "E", "E", "E" ]
limb_postion["17"] = [ "A", "B", "B", "B", "B", "C", "C", "C", "D", "D", "D", "E", "E", "E", "E", "E", "E" ]
limb_postion["18"] = [ "A", "B", "B", "B", "B", "C", "C", "C", "C", "D", "D", "D", "E", "E", "E", "E", "E", "E" ]

limb_kind = { "逃げa": 1, "逃げb": 2, "先行a": 3, "先行b": 4, "差しa": 5, "差しb": 6, "追い": 7, "後方": 8 }

def limb_passing( passing_data, all_horce_num ):
    result = ""
    
    try:
        three_corner = int( passing_data[-1] )
        four_corner = int( passing_data[-2] )
    except:
        return result        
    
    if all_horce_num < 10:
        key_horce_num = "10"
    else:
        key_horce_num = str( int( all_horce_num ) )
    
    try:
        three_pos = limb_postion[key_horce_num][three_corner-1]
        four_pos = limb_postion[key_horce_num][four_corner-1]
    except:
        return result

    if three_pos == "A":
        result = "逃げ"
    elif three_pos == "B":
        result= "先行"
    elif three_pos == "C" or three_pos == "E":
        if four_pos == "A" or four_pos == "B":
            result = "差しa"
        else:
            result = "差しb"
    else:
        if four_pos == "A" or four_pos == "B" or four_pos == "C" or four_pos == "D":
            result = "追い"
        else:
            result = "後方" 

    return result

def limb_search( past_passing_data, pd ):
    count = 0
    use_passing_data = []
    past_day = pd.past_day_list()
    past_rank = pd.rank_list()
    all_horce_num_list = pd.all_horce_num_list()

    result = {}
    result["逃げ"] = []
    result["先行"] = []
    result["差しa"] = []
    result["差しb"] = []
    result["追い"] = []
    result["後方"] = []

    for day in past_day:
        try:
            use_passing_data.append( past_passing_data[day] )
        except:
            continue

    for i in range( 0, len( use_passing_data ) ):
        try:
            passing_data = use_passing_data[i].split( "-" )
        except:
            continue

        all_horce_num = all_horce_num_list[i]
        limb = limb_passing( passing_data, all_horce_num )

        if not len( limb ) == 0:
            result[limb].append( i )
            count += 1

        if count == 5:
            break

    max_size = -1
    limb = ""

    for k in result.keys():
        if max_size < len( result[k] ):
            limb = k
            max_size = len( result[k] )

    if limb == "逃げ":
        all_rank = 0
        all_count = 0
        
        for i in range( 0, len( result[limb] ) ):
            c = result[limb][i]
            all_count += all_horce_num_list[c]
            all_rank += past_rank[c]

        if all_rank < all_count / 2:
            limb = "逃げa"
        else:
            limb = "逃げb"        
        
    elif limb == "先行":
        if len( result["逃げ"] ) < 1:
            limb = "先行b"
        else:
            limb = "先行a"

    return limb_kind[limb]

