import json
import itertools
from SekitobaPsql.psql_control import PsqlControl

class HorceData:
    def __init__( self ):
        self.pc = PsqlControl()
        self.table_name = "horce_data"
        self.colums = { "horce_id": "text", "past_data": "text[][]" }
        self.additional_colums = { "past_data": "text[][]",
                                  "true_skill": "float(32)", \
                                  "first_passing_true_skill": "float(32)", \
                                  "last_passing_true_skill": "float(32)", \
                                  "up3_true_skill": "float(32)", \
                                  "corner_true_skill": "float(32)", \
                                  "baba_index": "text", \
                                  "sex": "int", \
                                  "time_index": "text", \
                                  "parent_id": "text", \
                                  "flame_evaluation": "text" }
        self.json_data = [ "baba_index", \
                          "time_index", \
                          "parent_id", \
                          "flame_evaluation" ]
        self.data = {}

    def get_past_data( self, horce_id ):
        sql = "SELECT past_data from {} where horce_id = '{}';".format( self.table_name, horce_id )
        past_data = list( itertools.chain.from_iterable( self.pc.select_data( sql ) ) )

        if len( past_data ) == 0:
            return []
        
        return past_data[0]

    def get_select_all_data( self, data_name ):
        result = {}
        sql = "SELECT horce_id, {} from {};".format( data_name, self.table_name )
        data_list = self.pc.select_data( sql )

        for data in data_list:
            result[data[0]] = data[1]

        return result

    def get_multi_data( self, horce_id_list ):
        self.data.clear()
        sql = "SELECT * from {} where ".format( self.table_name )
        
        for i, horce_id in enumerate( horce_id_list ):
            sql += "horce_id = '{}'".format( horce_id )

            if not i == len( horce_id_list ) - 1:
                sql += " OR "

        sql += ";"
        get_data = self.pc.select_data( sql )

        for past_data in get_data:
            for key in past_data.keys():
                if key in self.json_data:
                    past_data[key] = json.loads( past_data[key] )
                    
            self.data[past_data["horce_id"]] = past_data
            
    def create_table( self ):
        if not self.pc.exist_table( self.table_name ):
            self.pc.create_table( self.table_name, self.colums )
            self.pc.update_data( "create index on horce_data(horce_id);" )

    def add_colum( self, colum_name, init_value ):
        if not self.pc.exist_colum( self.table_name, colum_name ):
            self.pc.add_colum( self.table_name, { "name": colum_name, "type": self.additional_colums[colum_name] }, init_value )

    def update_data( self, colum_name, value, horce_id ):
        if "[]" in self.additional_colums[colum_name]:
            value = "'" + "{}".format( str( value ).replace( "[", "{" ).replace( "]", "}" ) ).replace( "'", "\"" ) + "'"
            sql = "UPDATE {} SET {}={} WHERE horce_id='{}';"\
            .format( self.table_name, colum_name, value, horce_id )
        if self.additional_colums[colum_name] == "text":
            sql = "UPDATE {} SET {}='{}' WHERE horce_id='{}';"\
            .format( self.table_name, colum_name, value, horce_id )
        else:
            sql = "UPDATE {} SET {}={} WHERE horce_id='{}';"\
            .format( self.table_name, colum_name, value, horce_id )
            
        self.pc.update_data( sql )

    def insert_data( self, horce_data ):
        insert_data = []

        for horce_id in horce_data.keys():
            if not self.pc.exist_data( self.table_name, "horce_id", horce_id ):
                insert_data.append( { "horce_id": horce_id, "past_data": horce_data[horce_id] } )

        if len( insert_data ) == 0:
            return

        self.pc.insert_data( self.table_name, insert_data, self.colums )
