import os
import sys
import time
import glob
import boto3
import torch
import pickle

BACKUP = 10
bucket_name = "sekitoba-data"
dir_name = "/Volumes/Gilgamesh/sekitoba-data"
prod_dir_name = "/Volumes/Gilgamesh/sekitoba-prod"
local_name = "./storage"

def key_get():
    result = {}
    f = open( os.environ["HOME"] + "/.aws_key/S3key.txt" )
    lines = f.readlines()
    result["accsess_key"] = lines[0].split( ":" )[1].replace( "\n", "" )
    result["secret_key"] = lines[1].split( ":" )[1].replace( "\n", "" )

    return result

#key_data = key_get()
#s3 = boto3.resource('s3',
#                  aws_access_key_id = key_data["accsess_key"],
#                  aws_secret_access_key = key_data["secret_key"],
#                  region_name='ap-northeast-1'
#)

#client_s3 = boto3.client('s3',
#                  aws_access_key_id = key_data["accsess_key"],
#                  aws_secret_access_key = key_data["secret_key"],
#                  region_name='ap-northeast-1'
#)

def file_check( file_name ):
    return os.path.isfile( file_name )

def dist_index_get():
    return pickle_load( "dist_index.pickle" )

def course_data_get():
    return pickle_load( "race_cource_info.pickle" )

def local_pickle_save( dir_name, file_name, data ):
    back_up_list = []
    file_list = glob.glob( dir_name + "*" )

    for name in file_list:
        split_name = name.split( ".backup-" )

        if len( split_name ) == 2 and split_name[0] == file_name:
            timestamp = int( split_name[1] )
            back_up_list.append( { "name": split_name[0], "time": timestamp } )

    if BACKUP <= len( back_up_list ):
        back_up_list = sorted( back_up_list, key = lambda x: x["time"] )
        os.remove( back_up_list[0]["name"] )

    if file_check( dir_name + file_name ):
        current_timestamp = int( time.time() )
        os.rename( dir_name + file_name, dir_name + file_name + ".backup-" + str( current_timestamp ) )
        
    f = open( dir_name + file_name, "wb" )
    pickle.dump( data, f )
    f.close()

def local_pickle_load( file_name ):
    
    for i in range( 0, 5 ):
        try:
            f = open( file_name, "rb" )
            result = pickle.load( f )
            f.close()
            return result
        except Exception as e:
            print( e )
            continue

    return None

# load rank
# 1 local 
# 2 Gilgamesh
# 3 AWS S3

def pickle_load( file_name, prod = False ):
    data = None

    if prod:
        if file_check( prod_dir_name + "/" + file_name ):
            data = local_pickle_load( prod_dir_name + "/" + file_name )

        if not data == None:
            print( file_name + " download finish Prod" )
            return data
    
    if file_check( local_name + "/" + file_name ):
        data = local_pickle_load( local_name + "/" + file_name )

        if not data == None:
            print( file_name + " download finish Local" )
            return data
    
    if file_check( dir_name + "/" + file_name ):
        try:
            data = local_pickle_load( dir_name + "/" + file_name )
        except:
            data = None
            
        if not data == None:
            print( file_name + " download finish Gilgamesh" )
            return data
            
    return data
    
def pickle_upload( file_name, data, prod = False ):
    if prod:
        local_pickle_save( prod_dir_name + "/", file_name, data )
    else:
        local_pickle_save( dir_name + "/", file_name, data )

def model_load( file_name, model ):
    model = None

    if file_check( dir_name + "/" + file_name ):
        model.load_state_dict( torch.load( file_name ) )
        return model
    
    return model
