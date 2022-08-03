import os
import statistics

import sekitoba_library.lib as lib
import sekitoba_data_manage as dm

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

def recovery_score_check( data: dict ):
    result = {}
    recovery_data = recovery_analyze( data )

    for k in recovery_data.keys():
        lib.dic_append( result, k, 0 )
        score = ( recovery_data[k]["ave"] + recovery_data[k]["median"] ) / 2
        #score -= 0.7
        score *= 10

        if 0.7 < recovery_data[k]["conv"]:
            score *= 0.5
            
        result[k] = score
        
    return result

def write_recovery_csv( data :dict , file_name :str ):
    data_dir = os.environ["HOME"] + "/Desktop/recovery_data/"
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
