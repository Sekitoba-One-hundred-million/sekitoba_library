import os
import math
from statistics import stdev

import SekitobaLibrary.current_race_data as crd

escapeValue = -1000
split_key = "race_id="
home_dir = os.getcwd()
test_years = [ "2022", "2023", "2024", "2025" ]
valid_years = [ test_years[0] ]
score_years = [ test_years[1] ]
simu_years = [ test_years[2], test_years[3] ]
predict_pace_key_list = [ "pace", "pace_regression", "before_pace_regression", "after_pace_regression", "pace_conv", "first_up3", "last_up3" ]
prod_check = False
PREDICT_SERVER_URL = "http://100.102.168.34:2244"

def testYearCheck( year, state ):
    if ( state == "optuna" and year in valid_years ) \
       or ( state == "test" and ( year in valid_years or year in score_years ) ) \
       or ( state == "prod" and year in simu_years ):
        return "test"

    if ( state == "optuna" and year in score_years ) or year in simu_years:
        return "None"

    return "teacher"

def idGet( url ):
    s_data = url.split( split_key )
    return s_data[len(s_data)-1]

def currentCheck( current_data ):
    if len( current_data ) == 22:
        return True

    return False
    
def dicAppend( dic, word, data ):
    if not word in dic:
        dic[word] = data

def textReplace( text: str ):
    return text.replace( " ", "" ).replace( "\n", "" )

def strMathPull( text: str ):
    result = ""

    for t in text:
        if str.isdecimal( t ):
            result += t

    return result

def mathCheck( text: str ):
    try:
        return float( text )
    except:
        return 0

def paddingStrMath( text: str ):
    if len( text ) == 1:
        return "0" + text

    return text

def recoveryScoreCheck( data: dict ):
    max_score = 5
    result = {}
    year_list = list( data.keys() )
    k_list = list( data[year_list[0]].keys() )
    
    for k in k_list:
        dicAppend( result, k, 0 )
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

def deviationValue( data, remove_data ):
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

def regressionLine( data ):
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

def xyRegressionLine( x_data, y_data ):
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

def raceCheck( all_data, race_day ):
    current_data = []
    past_data = []
    current_time = int( race_day["year"] * 365 + race_day["month"] * 30 + race_day["day"] )
    check = False

    def dayCheck( str_day ):
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
        dc = dayCheck( str_day )

        if dc == "C":
            current_data = str_data
        elif dc == "P":
            past_data.append( str_data )
    
    return current_data, past_data

def minus( data1, data2, abort = [ escapeValue ] ):
    if data1 in abort or data2 in abort:
        return -1000

    return data1 - data2

def average( data, abort = [ escapeValue ] ):
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

def stdev( data, abort = [ escapeValue ] ):
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

def minimum( data, abort = [ escapeValue ] ):
    min_data = maxCheck( data )

    for d in data:
        if d in abort:
            continue

        min_data = min( min_data, d )

    return min_data

def standardization( data, abort = [ escapeValue ] ):
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

def deviationValue( data, abort = [ -1000 ] ):
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

def nextRace( all_data, ymd ) -> crd.CurrentData:
    next_cd = None
    
    for str_data in all_data:
        cd = crd.CurrentData( str_data )

        if not cd.raceCheck():
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

def placeCheck( place_num ):
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

def maxCheck( data ):
    try:
        return max( data )
    except:
        return -1000

def minCheck( data ):
    try:
        return min( data )
    except:
        return 1000

def oneHundredPace( wrap_data ):
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

def paceRegression( wrap_data ):
    N = len( wrap_data )
    a, b = regressionLine( wrap_data )
    berfore_a, _ = regressionLine( wrap_data[0:int(N/2)] )
    after_a, _ = regressionLine( wrap_data[int(N/2):N] )
    return a, berfore_a, after_a

def paceData( current_wrap ):
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

def beforeAfterPace( current_wrap ):
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

def paceTeacherAnalyze( current_race_data, t_instance = {} ):
    result = {}
    
    for data_key in current_race_data.keys():
        if not type( current_race_data[data_key] ) is list or \
          len( current_race_data[data_key] ) == 0:
            continue

        if data_key in t_instance:
            continue
        
        instanceData = [v for v in current_race_data[data_key] if not v == escapeValue ]
        sort_data = sorted( instanceData )
        reverse_sort_data = sorted( instanceData, reverse = True )

        if not "ave_"+data_key in t_instance:
            result["ave_"+data_key] = average( instanceData )

        if not "max_"+data_key in t_instance:
            result["max_"+data_key] = maxCheck( instanceData )

        if not "min_"+data_key in t_instance:
            result["min_"+data_key] = minimum( instanceData )

        if not "std_"+data_key in t_instance:
            result["std_"+data_key] = stdev( instanceData )

        for i in range( 0, 3 ):
            try:
                result[data_key+"_{}".format(i+1)] = sort_data[i]
            except:
                result[data_key+"_{}".format(i+1)] = escapeValue
                
        for i in range( 0, 3 ):
            try:
                result[data_key+"_reverse_{}".format(i+1)] = reverse_sort_data[i]
            except:
                result[data_key+"_reverse_{}".format(i+1)] = escapeValue

    return result

def horceTeacherAnalyze( current_race_data, t_instance, count ):
    result = {}
    str_index = "_index"

    for data_key in current_race_data.keys():
        if not type( current_race_data[data_key] ) == list:
            continue

        if len( current_race_data[data_key] ) == 0 or \
          data_key in t_instance:
            continue

        name = data_key

        if str_index in data_key:
            name = data_key.replace( str_index, "" )

            if name in current_race_data:
                result[data_key] = current_race_data[data_key].index( current_race_data[name][count] )
        else:
            result[data_key] = current_race_data[data_key][count]

    return result
