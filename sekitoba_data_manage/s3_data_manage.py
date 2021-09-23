import os
import boto3
import pickle

bucket_name = "sekitoba-data"

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

def pickle_save( file_name, data ):
    f = open( file_name, "wb" )
    pickle.dump( data, f )
    f.close()
    
def pickle_load( file_name ):
    bucket = s3.Bucket( bucket_name )
    
    try:
        obj = bucket.Object( "pickle_data/" + file_name ).get()
    except:
        print( file_name + " not found" )
        return None

    byte_data = obj['Body'].read()
    data = pickle.loads( byte_data )
    print( file_name + " download finish" )
    return data
    
def pickle_upload( file_name, data ):
    pickle_save( file_name, data )
    bucket = s3.Bucket( bucket_name )
    bucket.upload_file( file_name, "pickle_data/" + file_name )
    os.remove( file_name )    

def model_load( file_name ):
    bucket = s3.Bucket( bucket_name )
    
    try:
        obj = bucket.Object( "model_data/" + file_name ).get()
    except:
        print( file_name + " not found" )
        return None

    byte_data = obj['Body'].read()
    data = pickle.loads( byte_data )
    print( file_name + " model download finish" )
    return data

def model_upload( file_name, data ):
    pickle_save( file_name, data )
    bucket = s3.Bucket( bucket_name )
    bucket.upload_file( file_name, "model_data/" + file_name )
    os.remove( file_name )    
    
def other_upload( file_name ):
    bucket = s3.Bucket( 'sekitoba' )
    bucket.upload_file( file_name, "other_data/" + file_name )

