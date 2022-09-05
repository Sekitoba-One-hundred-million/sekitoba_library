import os
import sys
import boto3
import torch
import pickle

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

key_data = key_get()
s3 = boto3.resource('s3',
                  aws_access_key_id = key_data["accsess_key"],
                  aws_secret_access_key = key_data["secret_key"],
                  region_name='ap-northeast-1'
)

client_s3 = boto3.client('s3',
                  aws_access_key_id = key_data["accsess_key"],
                  aws_secret_access_key = key_data["secret_key"],
                  region_name='ap-northeast-1'
)

def file_check( file_name ):
    return os.path.isfile( file_name )

def dist_index_get():
    bucket = s3.Bucket( bucket_name )
    obj = bucket.Object( "other_data/dist_index.txt" ).get()
    byte_data = obj['Body'].read()
    all_data = str( byte_data.decode() ).split( "\n" )
    dist_data = {}

    for i in range( 0, len( all_data ) - 1 ):
        data = all_data[i].split( " " )
        dist_data[data[0]] = float( data[1] )

    return dist_data

def course_data_get():
    bucket = s3.Bucket( bucket_name )
    obj = bucket.Object( "other_data/straight_dist.txt" ).get()
    byte_data = obj['Body'].read()
    all_data = str( byte_data.decode() ).split( "\n" )
    
    result = {}

    for i in range( 0, len( all_data ) - 1 ):
        data = all_data[i].replace( "\n", "" ).split( " " )
        result[data[0]] = [ float( data[1] ), float( data[2] ) ]

    return result

def local_pickle_save( file_name, data ):
    f = open( file_name, "wb" )
    pickle.dump( data, f )
    f.close()

def local_pickle_load( file_name ):

    for i in range( 0, 5 ):
        try:
            f = open( file_name, "rb" )
            result = pickle.load( f )
            f.close()
            return result
        except:
            continue

    return None
    
def pickle_delete( file_name ):
    file_path = "pickle_data/" + file_name
    bucket = s3.Bucket( bucket_name )
    bucket.Object( file_path ).delete()

# load rank
# 1 local 
# 2 Gilgamesh
# 3 AWS S3

def pickle_load( file_name, prod = False ):
    if prod:
        data = None
        
        if file_check( prod_dir_name + "/" + file_name ):
            data = local_pickle_load( prod_dir_name + "/" + file_name )

        if not data == None:
            print( file_name + " download finish Prod" )
        else:
            print( file_name + " download fail Prod" )

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
        
    bucket = s3.Bucket( bucket_name )

    try:
        obj = bucket.Object( "pickle_data/" + file_name ).get()
    except:
        print( file_name + " not found" )
        return None

    byte_data = obj['Body'].read()
    data = pickle.loads( byte_data )
    local_pickle_save( dir_name + "/" + file_name, data )
    print( file_name + " download finish" )
    
    return data
    
def pickle_upload( file_name, data, prod = False ):
    if prod:
        local_pickle_save( prod_dir_name + "/" + file_name, data )
    else:
        local_pickle_save( file_name, data )
        local_pickle_save( dir_name + "/" + file_name, data )
        bucket = s3.Bucket( bucket_name )
        bucket.upload_file( file_name, "pickle_data/" + file_name )
        os.remove( file_name )    

def model_load( file_name, model ):
    if file_check( dir_name + "/" + file_name ):
        model.load_state_dict( torch.load( file_name ) )
        return model
    
    bucket = s3.Bucket( bucket_name )

    try:
        obj = bucket.Object( "model_data/" + file_name ).get()
    except:
        print( file_name + " not found" )
        return None

    byte_data = obj['Body'].read()
    f = open( file_name, "wb" )
    f.write( byte_data )
    f.close()
    
    model.load_state_dict( torch.load( file_name ) )
    os.remove( file_name )
    print( file_name + " model download finish" )
    return model

def model_upload( file_name, model ):
    torch.save( model.to('cpu').state_dict(), file_name )
    bucket = s3.Bucket( bucket_name )    
    bucket.upload_file( file_name, "model_data/" + file_name )
    os.remove( file_name )
    
def other_upload( file_name ):
    bucket = s3.Bucket( 'sekitoba' )
    bucket.upload_file( file_name, "other_data/" + file_name )
