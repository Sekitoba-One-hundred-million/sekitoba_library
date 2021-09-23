import os
import math

split_key = "race_id="
home_dir = os.getcwd()
current_year = 2020

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

def id_get( url ):
    s_data = url.split( split_key )
    return s_data[len(s_data)-1]

def current_check( current_data ):
    if len( current_data ) == 22:
        return True

    return False
    
def dic_append( dic, word, data ):
    try:
        a = dic[word]
    except:
        dic[word] = data

def deviation_value( data, remove_data ):
    result = [ 50 ] * len( data )
    average = 0
    stde = 0
    count = 0
    
    for i in range( 0, len( data ) ):
        ok =  True
        
        for r in range( 0, len( remove_data ) ):
            if data[i] == remove_data[r]:
                ok = False
                break

        if ok:
            average += data[i]
            count += 1

    if count == 0:
        return result
            
    average /= count
    
    for i in range( 0, len( data ) ):
        ok =  True
        
        for r in range( 0, len( remove_data ) ):
            if data[i] == remove_data[r]:
                ok = False
                break

        if ok:
            stde += math.pow( average - data[i], 2 )

    stde = math.sqrt( stde / count )

    if stde == 0:
        return result

    for i in range( 0, len( data ) ):
        ok =  True
        
        for r in range( 0, len( remove_data ) ):
            if data[i] == remove_data[r]:
                ok = False
                break

        if ok:
            result[i] = ( data[i] - average ) / stde * 10 + 50

    return result

def regression_line( data ):
    a = 0
    #b = 0
    y_ave = 0
    x_ave = 0

    for i in range( 0, len( data ) ):
        y_ave += data[i]
        x_ave += i + 1

    y_ave /= len( data )
    x_ave /= len( data )

    a1 = 0
    a2 = 0

    for i in range( 0, len( data ) ):
        a1 += ( i + 1 - x_ave ) * ( data[i] - y_ave )
        a2 += math.pow( i + 1 - x_ave, 2 )

    a = a1 / a2
    b = y_ave - a * x_ave

    return a, b

def xy_regression_line( x_data, y_data ):
    a = 0
    #b = 0
    y_ave = 0
    x_ave = 0

    for i in range( 0, len( x_data ) ):
        y_ave += y_data[i]
        x_ave += x_data[i]

    y_ave /= len( y_data )
    x_ave /= len( x_data )

    a1 = 0
    a2 = 0

    for i in range( 0, len( x_data ) ):
        a1 += ( x_data[i] - x_ave ) * ( y_data[i] - y_ave )
        a2 += math.pow( x_data[i] - x_ave, 2 )

    if not a2 == 0:
        a = a1 / a2
    else:
        a = a1
        
    b = y_ave - a * x_ave

    return a, b

def limb_passing( passing_data, all_horce_num ):
    result = "None"
    
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

    return limb, result

def race_check( all_data, year, day, num, race_place_num ):
    current_data = []
    past_data = []
    check = False

    for i in range( 0, len( all_data ) ):        
        str_data = all_data[i]
        y = str_data[0].split( "/" )
        place = ""
        
        for r in range( 0, len( str_data[1] ) ):
            if not str.isdecimal( str_data[1][r] ):
                place += str_data[1][r]

        #対象のレースを選択
        if not len( str_data[1] ) == 0 \
           and y[0] == year \
           and str_data[1][0] == num \
           and str_data[1][ len( str_data[1] ) - 1 ] == day \
           and place_check( race_place_num ) == place:
            current_data = str_data
            check = True 
        elif check:
            past_data.append( str_data )
    
    return current_data, past_data

def place_check( place_num ):
    if place_num == "01":
        return "札幌"
    elif place_num == "02":
        return "函館"
    elif place_num == "03":
        return "福島"
    elif place_num == "04":
        return "新潟"
    elif place_num == "05":
        return "東京"    
    elif place_num == "06":
        return "中山"
    elif place_num == "07":
        return "中京"
    elif place_num == "08":
        return "京都"    
    elif place_num == "09":
        return "阪神"
    elif place_num == "10":
        return "小倉"

    return "None"

def horce_name_replace( horce_name ):
    horce_name = horce_name.replace( "○外", "" )
    horce_name = horce_name.replace( "○地", "" )
    horce_name = horce_name.replace( "□地", "" )
    horce_name = horce_name.replace( "□外", "" )
    horce_name = horce_name.replace( "○父", "" )

    return horce_name

def key_siniar( data, key ):
    result = ""
    max_count = -1

    for k in data.keys():
        count = 0
        
        for i in range( 0, min( len( k ), len( key ) ) ):
            if k[i] == key[i]:
                count += 1

        if max_count < count:
            max_count = count
            result = k

    return result

def key_zero( dic, data, key ):
    try:
        data.append( dic[key] )
    except:
        data.append( 0 )

    return data

