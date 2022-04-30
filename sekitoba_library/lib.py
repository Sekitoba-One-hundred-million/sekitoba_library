import os
import math

split_key = "race_id="
home_dir = os.getcwd()
test_years = [ "2019", "2020", "2021" ]

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

def recovery_score_check( data: dict ):
    max_score = 5
    result = {}
    year_list = list( data.keys() )
    k_list = list( data[year_list[0]].keys() )
    
    for k in k_list:
        dic_append( result, k, 0 )
        for year in year_list:
            score = 0

            try:
                if data[year][k]["recovery"] <= 0.75:
                    score = -1
                elif 0.85 < data[year][k]["recovery"]:
                    score = 2
                elif 0.75 < data[year][k]["recovery"]:
                    score = 1
                else:
                    continue
            except:
                continue

            result[k] += score

    for k in result.keys():
        result[k] = max( result[k], 0 )
        result[k] = min( result[k], max_score )

    return result                

def softmax( data ):
    result = []
    sum_data = 0
    value_max = max( data )

    for i in range( 0, len( data ) ):
        sum_data += math.exp( data[i] - value_max )

    for i in range( 0, len( data ) ):
        result.append( math.exp( data[i] - value_max ) / sum_data )

    return result

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

def speed_standardization( data ):
    result = []
    ave = 0
    conv = 0
    count = 0

    for d in data:
        if d < 0:
            continue
        
        ave += d
        count += 1

    if count == 0:
        return [0] * len( data )

    ave /= count

    for d in data:
        if d < 0:
            continue

        conv += math.pow( d - ave, 2 )

    conv /= count
    conv = math.sqrt( conv )

    if conv == 0:
        return [0] * len( data )
    
    for d in data:
        if d < 0:
            result.append( 0 )
        else:
            result.append( ( d - ave ) / conv )

    return result

def max_check( data ):
    try:
        return max( data )
    except:
        return -1

