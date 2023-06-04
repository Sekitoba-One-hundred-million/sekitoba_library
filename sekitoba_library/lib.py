import os
import math

import sekitoba_library.current_race_data as crd
import sekitoba_library.past_race_data as prd

split_key = "race_id="
home_dir = os.getcwd()
test_years = [ "2022", "2023" ]

def id_get( url ):
    s_data = url.split( split_key )
    return s_data[len(s_data)-1]

def race_data_key_get( race_id ):
    return "https://race.netkeiba.com/race/shutuba.html?race_id=" + race_id

def current_check( current_data ):
    if len( current_data ) == 22:
        return True

    return False
    
def dic_append( dic, word, data ):
    if not word in dic:
        dic[word] = data

def text_replace( text: str ):
    return text.replace( " ", "" ).replace( "\n", "" )

def str_math_pull( text: str ):
    result = ""
    
    for t in text:
        if str.isdecimal( t ):
            result += t

    return result

def math_check( text: str ):
    try:
        return float( text )
    except:
        return 0

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

def normalization( data ):
    result = []

    if len( data ) == 0:
        return result
    
    ave_data = sum( data ) / len( data )
    std_data = 0

    for d in data:
        std_data += math.pow( ave_data - d, 2 )

    std_data /= len( data )

    if std_data == 0:
        return data
    
    std_data = math.sqrt( std_data )

    for d in data:
        result.append( ( d - ave_data ) / std_data )

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

    a = 0
    
    if not a2 == 0:
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

def next_race( all_data, ymd ) -> crd.current_data:
    next_cd = None
    
    for str_data in all_data:
        cd = crd.current_data( str_data )

        if not cd.race_check():
            continue

        birthday = cd.birthday()
        birthday = birthday.split( "/" )

        if len( birthday ) < 3:
            continue
        
        y = int( birthday[0] )
        m = int( birthday[1] )
        d = int( birthday[2] )

        if y == ymd["y"] and m == ymd["m"] and d == ymd["d"]:
            break

        next_cd = cd

    return next_cd

def place_check( place_num ):
    if int( place_num ) == 1:
        return "札幌"
    elif int( place_num ) == 2:
        return "函館"
    elif int( place_num ) == 3:
        return "福島"
    elif int( place_num ) == 4:
        return "新潟"
    elif int( place_num ) == 5:
        return "東京"    
    elif int( place_num ) == 6:
        return "中山"
    elif int( place_num ) == 7:
        return "中京"
    elif int( place_num ) == 8:
        return "京都"    
    elif int( place_num ) == 9:
        return "阪神"
    elif int( place_num ) == 10:
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

def conv( data_list, ave = None ):
    result = 0

    if ave == None:
        ave = sum( data_list ) / len( data_list )

    for d in data_list:
        result += math.pow( d - ave, 2 )

    result /= len( data_list )
    result = math.sqrt( result )

    return result

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

def match_rank_score( target_pd: prd.past_data, \
                     cd: crd.current_data, \
                     place = None, \
                     baba_status = None, \
                     dist_kind = None ):
    count = 0
    score = 0

    if not cd == None:
        place = cd.place()
        baba_status = cd.baba_status()
        dist_kind = cd.dist_kind()
            
    for target_cd in target_pd.past_cd_list():
        c = 0
                
        if target_cd.place() == place:
            c += 1
                
        if target_cd.baba_status() == baba_status:
            c += 1

        if target_cd.dist_kind() == dist_kind:
            c += 1

        count += c
        score += target_cd.rank() * c

    if not count == 0:
        score /= count
                
    return int( score )

def foot_used_create( current_wrap ):
    score = 0
    
    if len( current_wrap ) == 0:
        return score
    
    key_list = list( current_wrap.keys() )
    wrap_key_list = []

    for wrap_key in key_list:
        wrap_key_list.append( int( wrap_key ) )

    s1 = len( wrap_key_list ) - 4
    s2 = len( wrap_key_list )
    wrap_key_list = sorted( wrap_key_list )
    use_wrap_key_list = wrap_key_list[s1:s2]

    if not len( use_wrap_key_list ) == 4:
        return score

    check_wrap_list = []
    for wrap_key in use_wrap_key_list:
        key = str( wrap_key )
        check_wrap_list.append( current_wrap[key] )

    score = min( check_wrap_list )
    foot_score = 1 #long

    if score < 11.6:
        foot_score = 2 #change

    return foot_score

def pace_data( current_wrap ):
    wrap_key_list = list( current_wrap.keys() )
    n = len( wrap_key_list )

    if n == 0:
        return None
        
    s1 = int( n / 2 )
    before_wrap_key_list = wrap_key_list[0:s1]
    after_wrap_key_list = wrap_key_list[s1:n]
        
    if not len( before_wrap_key_list ) == len( after_wrap_key_list ):
        after_wrap_key_list.pop( 0 )

    before_time = 0
    after_time = 0

    for key in before_wrap_key_list:
        before_time += current_wrap[key]
        
    for key in after_wrap_key_list:
        after_time += current_wrap[key]

    if before_wrap_key_list[0] == "100":
        after_time -= round( current_wrap[after_wrap_key_list[0]] / 2 )

    return before_time - after_time

def kind_score_get( data, key_list, key_data, base_key ):
    score = 0
    count = 0
    
    for i in range( 0, len( key_list ) ):
        k1 = key_list[i]
        for r in range( i + 1, len( key_list ) ):
            k2 = key_list[r]
            key_name = k1 + "_" + k2
            try:
                score += data[key_name][key_data[k1]][key_data[k2]][base_key]
                count += 1
            except:
                continue

    if not count == 0:
        score /= count
        
    return score
