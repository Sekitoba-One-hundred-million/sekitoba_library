import os
import copy
import statistics

import SekitobaLibrary.lib as lib
import SekitobaDataManage as dm

def recovery_analyze( data: dict ):
    result = {}
    analyze_data = {}
    
    for year in data.keys():
        for k in data[year].keys():
            lib.dic_append( result, k, { "count": 0, "ave": 0, "conv": 0, "median": 0, "list": [] } )
            
            try:
                result[k]["list"].append( data[year][k]["recovery"] )
                result[k]["count"] += data[year][k]["count"]
                result[k]["ave"] += data[year][k]["recovery"] * data[year][k]["count"]
            except:
                continue

    for k in result.keys():
        if not result[k]["count"] == 0:
            result[k]["ave"] = result[k]["ave"] / result[k]["count"]
            result[k]["conv"] = lib.conv( result[k]["list"], ave = result[k]["ave"] )
            result[k]["ave"] = round( result[k]["ave"], 2 )
            result[k]["conv"] = round( result[k]["conv"], 2 )
            result[k]["median"] = statistics.median( result[k]["list"] )

    return result

def rank_analyze( data: dict ):
    result = {}
    analyze_data = {}
    
    for year in data.keys():
        for k in data[year].keys():
            lib.dic_append( result, k, { "count": 0, "ave": 0, "conv": 0, "median": 0, "list": [] } )
            
            try:
                result[k]["list"].append( data[year][k]["rank"] )
                result[k]["count"] += data[year][k]["count"]
                result[k]["ave"] += data[year][k]["rank"] * data[year][k]["count"]
            except:
                continue

    for k in result.keys():
        if not result[k]["count"] == 0:
            result[k]["ave"] = result[k]["ave"] / result[k]["count"]
            result[k]["conv"] = lib.conv( result[k]["list"], ave = result[k]["ave"] )
            result[k]["ave"] = round( result[k]["ave"], 2 )
            result[k]["conv"] = round( result[k]["conv"], 2 )
            result[k]["median"] = statistics.median( result[k]["list"] )

    return result

def write_recovery_csv( data :dict , file_name :str, add_dir = "" ):
    data_dir = "/Volumes/Gilgamesh/sekitoba-recovery/" + add_dir
    f = open( data_dir + file_name, "w" )
    key = list( data.keys() )[0]
    key_list = list( data[key].keys() )

    for i in range( 0, len( key_list ) ):
        key_list[i] = int( key_list[i] )

    key_list = sorted( key_list )
    first_write = "year/data,\t"

    for i in range( 0, len( key_list ) ):
        key_list[i] = str( key_list[i] )
        first_write += key_list[i] + ",\t"

    f.write( first_write + "\n" )
    year_list = list( data.keys() )

    for i in range( 0, len( year_list ) ):
        year_list[i] = int( year_list[i] )

    year_list = sorted( year_list )
    
    for math_year in year_list:
        year = str( math_year )
        write_str = year + ","
        
        for k in key_list:
            try:
                write_str += str( data[year][k]["recovery"] ) + ",\t"
            except:
                write_str += "0,\t"

        write_str += "\n"
        f.write( write_str )

    recovery_data = recovery_analyze( data )
    ave_str = "all,\t"
    count_str = "count,\t"
    conv_str = "conv,\t"
    median_str = "median,\t"
    
    for k in key_list:
        ave_str += str( recovery_data[k]["ave"] ) + ",\t"
        count_str += str( recovery_data[k]["count"] ) + ",\t"
        conv_str += str( recovery_data[k]["conv"] ) + ",\t"
        median_str += str( recovery_data[k]["median"] ) + ",\t"

    ave_str += "\n"
    count_str += "\n"
    conv_str += "\n"
    median_str += "\n"
    
    f.write( ave_str )
    f.write( median_str )
    f.write( conv_str )
    f.write( count_str )
    
    f.close()


def write_rank_csv( data :dict , file_name :str, add_dir = "" ):
    data_dir = "/Volumes/Gilgamesh/sekitoba-rank/" + add_dir
    f = open( data_dir + file_name, "w" )
    key = list( data.keys() )[0]
    key_list = list( data[key].keys() )

    for i in range( 0, len( key_list ) ):
        key_list[i] = int( key_list[i] )

    key_list = sorted( key_list )
    first_write = "year/data,\t"

    for i in range( 0, len( key_list ) ):
        key_list[i] = str( key_list[i] )
        first_write += key_list[i] + ",\t"

    f.write( first_write + "\n" )
    
    for year in data.keys():
        write_str = year + ","
        
        for k in key_list:
            try:
                write_str += str( data[year][k]["rank"] ) + ",\t"
            except:
                write_str += "0,\t"

        write_str += "\n"
        f.write( write_str )

    recovery_data = rank_analyze( data )
    ave_str = "all,\t"
    count_str = "count,\t"
    conv_str = "conv,\t"
    median_str = "median,\t"
    
    for k in key_list:
        ave_str += str( recovery_data[k]["ave"] ) + ",\t"
        count_str += str( recovery_data[k]["count"] ) + ",\t"
        conv_str += str( recovery_data[k]["conv"] ) + ",\t"
        median_str += str( recovery_data[k]["median"] ) + ",\t"

    ave_str += "\n"
    count_str += "\n"
    conv_str += "\n"
    median_str += "\n"
    
    f.write( ave_str )
    f.write( median_str )
    f.write( conv_str )
    f.write( count_str )
    
    f.close()

def recovery_data_split( data_storage: list ):
    max_count = 20
    data_storage = sorted( data_storage, key = lambda x:x["key"] )
    base = int( len( data_storage ) / max_count )
    count = 1
    b = int( base * count )
    split_key = data_storage[b]["key"]
    split_list = [ split_key ]
    result = {}
    key = str( count )
    
    for i in range( 0, len( data_storage ) ):
        current_key = data_storage[i]["key"]

        if split_key < current_key:
            count += 1
            b = min( int( base * count ), len( data_storage ) - 1 )
            split_key = data_storage[b]["key"]
            key = str( int( len( split_list ) + 1 ) )
            
            if not split_key == split_list[-1]:
                split_list.append( split_key )

        if max_count < int( key ):
            key = str( int( max_count ) )
            
        year = data_storage[i]["year"]
        lib.dic_append( result, year, {} )
        lib.dic_append( result[year], key, { "recovery": 0, "count": 0 } )
        result[year][key]["recovery"] += data_storage[i]["odds"]
        result[year][key]["count"] += 1
        
    return result, split_list

def recovery_data_upload( name: str, score: dict, split_list: list ):    
    recovery_score_data = dm.pickle_load( "recovery_score_data.pickle" )
    split_data = dm.pickle_load( "split_data.pickle" )
    
    if recovery_score_data == None:
        recovery_score_data = {}

    if split_data == None:
        split_data = {}    
    
    recovery_score_data[name] = score
    split_data[name] = split_list    
    dm.pickle_upload( "split_data.pickle", split_data )
    dm.pickle_upload( "recovery_score_data.pickle", recovery_score_data )

def recovery_best_select( data, show = True ):    
    one_recovery = copy.deepcopy( data )
    plus_best_select = plus_recovery_select( one_recovery, show = show )
    for mk in plus_best_select:
        k = str( mk )
        for year in one_recovery.keys():
            if not k in one_recovery[year]:
                continue
            
            del one_recovery[year][k]

    middle_best_select = plus_recovery_select( one_recovery, show = show )

    for mk in middle_best_select:
        k = str( mk )
        for year in one_recovery.keys():
            if not k in one_recovery[year]:
                continue

            del one_recovery[year][k]

    minus_best_select = list( one_recovery[year].keys() )

    for i in range( 0, len( minus_best_select ) ):
        minus_best_select[i] = int( minus_best_select[i] )
    
    return plus_best_select, minus_best_select

def plus_recovery_select( data, show = True ):
    import math
    
    DATA = "recovery"
    COUNT = "count"
    
    def base10int(value, base):
        if (int(value / base)):
            return base10int(int(value / base), base) + str(value % base)
        return str(value % base)

    def str_hexadecimal( value, base, l ):
        str_data = base10int( value, base )

        if l < len( str_data ):
            return None
    
        str_data = int( l - len( str_data ) ) * '0' + str_data
        return str_data

    best_select = []
    best_score = 0
    best_recovery = 0
    year_list = list( data.keys() )
    key_list = {}#list( data[year_list[0]].keys() )
    key_data = {}

    for year in year_list:
        for score_key in data[year].keys():
            lib.dic_append( key_data, score_key, 0 )
            key_data[score_key] += data[year][score_key][COUNT]

    score_key_list = []
    key_data = sorted( key_data.items(), key = lambda x:x[1] ,reverse = True )
    
    for i in range( 0, len( key_data ) ):
        if key_data[i][1] < 3000 or len( score_key_list ) == 20:
            break
        
        score_key_list.append( key_data[i][0] )

    c = 2
    l = len( score_key_list )

    for i in range( 0, pow( c, l ) ):
        use_score_key_list = []
        str_check = str_hexadecimal( i, c, l )

        if str_check == None:
            print( i )
            continue

        for r, s in enumerate( str_check ):
            if not s == "1":
                continue

            use_score_key_list.append( score_key_list[r] )

        if len( use_score_key_list ) == 0:
            continue

        recovery = 0
        count = 0
        ave = {}
        conv = 0

        for year in year_list:
            lib.dic_append( ave, year, 0 )
            for score_key in use_score_key_list:

                if not score_key in data[year]:
                    continue
                
                recovery += data[year][score_key][DATA] * data[year][score_key][COUNT]
                count += data[year][score_key][COUNT]
                ave[year] += data[year][score_key][DATA]

        conv_count = 0
        recovery /= count
        min_recovery = 1
        max_recovery = -1

        for year in year_list:
            if ave[year] == 0:
                continue
            
            ave[year] /= len( use_score_key_list )
            conv += pow( recovery - ave[year], 2 )
            conv_count += 1
            min_recovery = min( min_recovery, ave[year] )
            max_recovery = max( max_recovery, ave[year] )

        conv = math.sqrt( conv / conv_count )
        score = recovery - conv# - ( recovery - min_recovery )
        #print( str_check, recovery, conv )
        
        if best_score < score:
            best_score = score
            best_recovery = recovery
            best_select = copy.deepcopy( use_score_key_list )

    for i in range( 0, len( best_select ) ):
        best_select[i] = int( best_select[i] )

    best_select = sorted( best_select )

    if show:
        print( "score: {}".format( best_score ) )
        print( "recovery: {}".format( best_recovery ) )
        print( best_select )

    return best_select
