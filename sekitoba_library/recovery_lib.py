import os

import sekitoba_library.lib as lib
import sekitoba_data_manage as dm

def recovery_score_check( data: dict ):
    max_score = 5
    base = 0.75
    result = {}
    year_list = list( data.keys() )
    k_list = list( data[year_list[0]].keys() )
    
    for k in k_list:
        r = 0
        c = 0
        lib.dic_append( result, k, 0 )
        score = 0
        
        for year in year_list:
            try:
                r += data[year][k]["recovery"] * data[year][k]["count"]
                c += data[year][k]["count"]

                score += ( data[year][k]["recovery"] - 0.75 ) * 10
            except:
                continue

        result[k] = int( score )
        """
        if 0.79 <= r:
            result[k] = 3
        elif 0.76 <= r:
            result[k] = 1
        elif 0.73 <= r:
            result[k] = 0
        elif 0.7 <= r:
            result[k] = -1
        else:
            result[k] = -3
        """
    for k in result.keys():
        result[k] = max( result[k], -10 )
        result[k] = min( result[k], 10 )

    return result                


def write_recovery_csv( data :dict , file_name :str ):
    data_dir = os.environ["HOME"] + "/Desktop/recovery_data/"
    f = open( data_dir + file_name, "w" )
    key = list( data.keys() )[0]
    key_list = list( data[key].keys() )

    for i in range( 0, len( key_list ) ):
        key_list[i] = int( key_list[i] )

    key_list = sorted( key_list )
    first_write = "year/data,"

    for k in key_list:
        k = str( k )
        first_write += k + ","

    recovery = {}
    f.write( first_write + "\n" )
    
    for year in data.keys():
        write_str = year + ","
        
        for k in key_list:
            k = str( k )
            lib.dic_append( recovery, k, { "count": 0, "recovery": 0 } )
            
            try:
                write_str += str( data[year][k]["recovery"] ) + ","
                recovery[k]["count"] += data[year][k]["count"]
                recovery[k]["recovery"] += data[year][k]["recovery"] * data[year][k]["count"]
            except:
                write_str += "0,"

        write_str += "\n"
        f.write( write_str )

    write_str = "all,"
    count_str = "count,"
    for k in recovery.keys():
        if not recovery[k]["count"] == 0:
            recovery[k]["recovery"] /= recovery[k]["count"]
            
        recovery[k]["recovery"] = round( recovery[k]["recovery"], 2 )
        write_str += str( recovery[k]["recovery"] ) + ","
        count_str += str( recovery[k]["count"] ) + ","

    write_str += "\n"
    count_str += "\n"

    f.write( write_str )
    f.write( count_str )
    
    f.close()

def recovery_data_split( data_storage: list ):
    max_count = 10
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
