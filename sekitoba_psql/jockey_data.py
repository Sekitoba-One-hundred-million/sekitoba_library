import json
import itertools

import sekitoba_library as lib
from sekitoba_psql.psql_control import PsqlControl

class JockeyData:
    def __init__( self ):
        self.pc = PsqlControl()
        self.table_name = "jockey_data"
        self.colums = { "jockey_id": "text" }
        self.additional_colums = { "true_skill": "float(32)",\
                                  "first_passing_true_skill": "float(32)", \
                                  "last_passing_true_skill": "float(32)", \
                                  "up3_true_skill": "float(32)", \
                                  "corner_true_skill": "float(32)", \
                                  "jockey_judgment": "text", \
                                  "jockey_judgment_up3": "text", \
                                  "jockey_judgment_rate": "text", \
                                  "jockey_judgment_up3_rate": "text", \
                                  "jockey_analyze": "text", \
                                  "jockey_year_rank": "text" }
        self.json_data = [ "jockey_judgment", \
                          "jockey_judgment_rate", \
                          "jockey_analyze", \
                          "jockey_year_rank", \
                          "jockey_judgment_up3", \
                          "jockey_judgment_up3_rate" ]
        self.data = {}

    def get_multi_data( self, jockey_id_list ):
        self.data.clear()
        sql = "SELECT * from {} where ".format( self.table_name )

        for i, jockey_id in enumerate( jockey_id_list ):
            sql += "jockey_id = '{}'".format( jockey_id )

            if not i == len( jockey_id_list ) - 1:
                sql += " OR "

        sql += ";"
        get_data = self.pc.select_data( sql )

        for past_data in get_data:
            for key in past_data.keys():
                if key in self.json_data:
                    past_data[key] = json.loads( past_data[key] )
                    
            self.data[past_data["jockey_id"]] = past_data

    def get_select_all_data( self, data_name ):
        result = {}
        sql = "SELECT jockey_id, {} from {};".format( data_name, self.table_name )
        data_list = self.pc.select_data( sql )

        for data in data_list:
            result[data[0]] = data[1]

        return result

    def create_table( self ):
        if not self.pc.exist_table( self.table_name ):
            self.pc.create_table( self.table_name, self.colums )
            self.pc.update_data( "create index on jockey_data(jockey_id);" )

    def add_colum( self, colum_name, init_value ):
        if not self.pc.exist_colum( self.table_name, colum_name ):
            self.pc.add_colum( self.table_name, { "name": colum_name, "type": self.additional_colums[colum_name] }, init_value )

    def update_data( self, colum_name, value, jockey_id ):
        if self.additional_colums[colum_name] == "text":
            sql = "UPDATE {} SET {}='{}' WHERE jockey_id='{}';"\
              .format( self.table_name, colum_name, value, jockey_id )
        else:
            sql = "UPDATE {} SET {}={} WHERE jockey_id='{}';"\
              .format( self.table_name, colum_name, value, jockey_id )
            
        self.pc.update_data( sql )

    def insert_data( self, jockey_id_list ):
        insert_data = []

        for jockey_id in jockey_id_list:
            if not self.pc.exist_data( self.table_name, "jockey_id", jockey_id ):
                insert_data.append( { "jockey_id": jockey_id } )

        if len( insert_data ) == 0:
            return
            
        self.pc.insert_data( self.table_name, insert_data, self.colums )
