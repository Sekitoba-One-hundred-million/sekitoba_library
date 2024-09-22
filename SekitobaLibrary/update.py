RACE_ID = "race_id"
HORCE_ID = "horce_id"
JOCKEY_ID = "jockey_id"
TRAINER_ID = "trainer_id"

def update_id_list_create():
    id_data = { RACE_ID: {}, HORCE_ID: {}, JOCKEY_ID: {}, TRAINER_ID: {} }
    f = open( "/Volumes/Gilgamesh/sekitoba-log/update_id_data.txt", "r" )
    all_data = f.readlines()
    f.close()

    for str_data in all_data:
        split_data = str_data.replace( "\n", "" ).split( " " )
        kind = split_data[0]
        str_id = split_data[1]
        id_data[kind][str_id] = True

    return id_data

def link_method_length( prod_data, dev_data ):
    if len( prod_data ) < len( dev_data ):
        return dev_data
    
    return prod_data

def link_method_value_length( prod_data, dev_data ):
    result = {}
    for k in prod_data.keys():
        if k in dev_data and len( prod_data[k] ) < len( dev_data[k] ):
            result[k] = dev_data[k]
        else:
            result[k] = prod_data[k]
            
    for k in dev_data.keys():
        if not k in result:
            result[k] = dev_data[k]

    return result

def link_prod_dev_data( prod_data, dev_data, method = "length" ):
    result = {}

    if not prod_data == None and not dev_data == None:
        if method == "length":
            result = link_method_length( prod_data, dev_data )
        elif method == "value_length":
            result = link_method_value_length( prod_data, dev_data )
    elif prod_data == None:
        race_money_data = dev_data
    elif dev_data == None:
        race_money_data = prod_data

    return result
