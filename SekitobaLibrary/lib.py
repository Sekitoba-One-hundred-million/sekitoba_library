import os
import math
from statistics import stdev

import SekitobaLibrary.current_race_data as crd
import SekitobaLibrary.past_race_data as prd

base_abort = -1000
split_key = "race_id="
home_dir = os.getcwd()
test_years = [ "2021", "2022", "2023", "2024" ]
valid_years = [ test_years[0] ]
score_years = [ test_years[1] ]
simu_years = [ test_years[2], test_years[3] ]
predict_pace_key_list = [ "pace", "pace_regression", "before_pace_regression", "after_pace_regression", "pace_conv", "first_up3", "last_up3" ]
prod_check = False

def test_year_check( year, state ):
    if ( state == "optuna" and year in valid_years ) \
       or ( state == "test" and ( year in valid_years or year in score_years ) ) \
       or ( state == "prod" and year in simu_years ):
        return "test"

    if ( state == "optuna" and year in score_years ) or year in simu_years:
        return "None"

    return "teacher"

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

def padding_str_math( text: str ):
    if len( text ) == 1:
        return "0" + text

    return text

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

def softmax_test( data ):
    result = []
    sum_data = 0
    value_max = max( data )
    value_min = min( data )

    for i in range( 0, len( data ) ):
        result.append( ( data[i] - value_min ) / ( value_max - value_min ) )

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

def race_check( all_data, race_day ):
    current_data = []
    past_data = []
    current_time = int( race_day["year"] * 365 + race_day["month"] * 30 + race_day["day"] )
    check = False

    def day_check( str_day ):
        day_result = ""
        split_day = str_day.split( "/" )

        try:
            race_time = int( int( split_day[0] ) * 365 + int( split_day[1] ) * 30 + int( split_day[2] ) )
        except:
            return day_result

        if race_time == current_time:
            day_result = "C"
        elif race_time < current_time:
            day_result = "P"
        else:
            day_result = "F"

        return day_result

    for i in range( 0, len( all_data ) ):        
        str_data = all_data[i]
        str_day = str_data[0]
        dc = day_check( str_day )

        if dc == "C":
            current_data = str_data
        elif dc == "P":
            past_data.append( str_data )
    
    return current_data, past_data

def minus( data1, data2, abort = [ base_abort ] ):
    if data1 in abort or data2 in abort:
        return -1000

    return data1 - data2

def average( data, abort = [ base_abort ] ):
    ave = 0
    count = 0

    for d in data:
        if d in abort:
            continue

        ave += d
        count += 1

    if count == 0:
        return -1000

    return ave / count

def stdev( data, abort = [ base_abort ] ):
    std_data = 0
    count = 0
    ave_data = average( data )

    for d in data:
        if d in abort:
            continue

        std_data += math.pow( ave_data - d, 2 )
        count += 1

    if count == 0:
        return -1000

    return math.sqrt( std_data / count )

def minimum( data, abort = [ base_abort ] ):
    min_data = max_check( data )

    for d in data:
        if d in abort:
            continue

        min_data = min( min_data, d )

    return min_data

def standardization( data, abort = [ base_abort ] ):
    result = []
    abort_index = []

    ave = 0
    count = 0

    if len( data ) == 0:
        return []

    for d in data:
        if not d in abort:
            ave += d
            count += 1

    if count <= 1:
        return [0] * len( data )

    ave /= count
    std = stdev( data )

    if std == 0:
        return [0] * len( data )

    for i in range( 0, len( data ) ):
        if data[i] in abort:
            result.append( data[i] )
        else:
            result.append( ( data[i] - ave ) / std )

    return result

def deviation_value( data, abort = [ -1000 ] ):
    result = []
    abort_index = []

    ave = 0
    count = 0

    if len( data ) == 0:
        return []

    for d in data:
        if d in abort:
            continue
        
        ave += d
        count += 1

    if count <= 1:
        return [50] * len( data )

    ave /= count
    conv = 0

    for d in data:
        if d in abort:
            continue

        conv += math.pow( ave - d, 2 )

    conv = math.sqrt( conv / count )

    if conv == 0:
        return [50] * len( data )

    for i in range( 0, len( data ) ):
        if data[i] in abort:
            result.append( data[i] )
        else:
            result.append( ( ( data[i] - ave ) / conv ) * 10 + 50 )

    return result

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

        if y == ymd["year"] and m == ymd["month"] and d == ymd["day"]:
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
    if len( data_list ) == 0:
        return -1000
    
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
        return -1000

def min_check( data ):
    try:
        return min( data )
    except:
        return 1000

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

def one_hundred_pace( wrap_data ):
    wrap_list = []
        
    if len( wrap_data ) == 0:
        return 0
            
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

def pace_regression( wrap_data ):
    N = len( wrap_data )
    a, b = regression_line( wrap_data )
    berfore_a, _ = regression_line( wrap_data[0:int(N/2)] )
    after_a, _ = regression_line( wrap_data[int(N/2):N] )
    return a, berfore_a, after_a

def pace_data( current_wrap ):
    wrap_key_list = list( current_wrap.keys() )
    n = len( wrap_key_list )

    if n == 0:
        return 0

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

def before_after_pace( current_wrap ):
    wrap_key_list = list( current_wrap.keys() )
    n = len( wrap_key_list )

    if n == 0:
        return 0

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

    return before_time, after_time

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